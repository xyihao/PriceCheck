#Thi is the scrapy program for YHD
from Modules.Internet.GetHTML import GetHttpObject
from Modules.common import QUERY_SEARCH,QUERY_PRODUCT
from Modules.SKU import SKU
from scrapy.selector import Selector
from datetime import datetime
from math import ceil
import codecs
import re
import json


TEST_URL="http://www.yhd.com/ctg/s2/c5010-0/b904351-3335/#page=1&sort=1"
TEST_URL2="http://search.yhd.com/s2/c0-0/k%25E7%25BE%25BD%25E8%25A5%25BF/1/"


def ValidateResult(result):
	return result

#OBJECTIVE: clear the escaped controll characters in the txt
#INPUT: string
#OUTP: string
def CleanEscapeChars(txt):
	CharToClean=['\\\\t','\\\\r\\\\n','\\\\','\\r\\n','\\\\r','\\\\n','\\r','\\n','( ){4,}']
	for char in CharToClean:
		txt=re.sub(char,'',txt)
	return txt

#OBJECTIVE:Call different scraping function according qType
#NOTE:main entry of the module
#INPUT: url, qType is the page type, sourceId
#OUTPUT: List of scraped data
def YHD_Scraper(url,qType):
	try:
		result=[]
		#response=GetHttpObject(url)
		#To make it more common, the detail scraper shall get the response by themselves
		if qType==QUERY_SEARCH:
			result=YHD_SearchPage_Scraper(url)
		elif qType==QUERY_PRODUCT:
			result=YHD_ItemPage_Scraper(url)
		if result is not None and len(result)>0:
			#a validate function to check, format the result
			result=ValidateResult(result)
			# an output function to process the result
			#OutputResult(result)
			return result
		return None
	except Exception, e:
		print "error in YHD_Scraper"
		raise e

#OBJECTIVE: Get the promotion information of a specified product
#NOTES: It is replaced by the GetPromotionInfo function
#INPUT: pid, merchantid, mid, vid are string
#OUPUT: string
def GetPromotionInfoPage(pid,merchantid,mid,vid):
	try:
		if re.search('\+',vid) is not None:
			vid=re.sub('\+','%252B',vid)
		#TODO:change to the new promotion request string
		url='http://item-home.yhd.com/item/ajax/ajaxProductPromotion.do?callback=detailPromotion.reduceScrollbar&productID={pid}&merchantID={merchantid}&productMercantID={mid}&vId={vid}'\
			.format(pid=pid,merchantid=merchantid,mid=mid,vid=vid)
		response=GetHttpObject(url)
		value=re.search("\"value\":\"(.*)\"",response).group(1)#get the promotion html code from the format: "value":"promotion html code here"
		#the return value contains all the escaped control characters like \\\\t,\\\\r\\\\n
		#the following code will clean these
		#TODO:make it a common function
		CharToClean=['\\\\t','\\\\r\\\\n','\\\\','( ){4,}']
		for char in CharToClean:
			value=re.sub(char,'',value)
		value=value.decode('utf8','ignore')
	except Exception as e:
		print 'error in Get Promotion Info'
		value=''
		#raise e
	else:
		return value

#OBJECTIVE: Get the promotion information of a product
#INPUT:mid is string
#OUTPUT: sPtring
def GetPromotionInfo(mid):
	try:
		url='http://interface.yhd.com/promotion/search/getPromotionInfoWithSku.do?mcsiteId=1&provinceId=1&siteType=1&pmInfoIds={mid}&pointSearch=1&caller=search'.format(mid=mid)
		response=GetHttpObject(url)
		data=json.loads(response)
		#TODO:need to remove the sign like !
		return data[0]['promotionInfo'][0]['promDesc']
	except TypeError as e:
		#no promotion information for this product
		return ''
	except Exception, e:
		raise e

#OBJECTIVE: Process the scraping of product page
#INPUT: url is string, sourceId is string
#OUTPUT:a list
def YHD_ItemPage_Scraper(url):
	try:
		response=GetHttpObject(url)
		result=[]
		item=SKU()
		time=datetime.now()
		#initiate the html selector
		sel=Selector(text=response,type='html')
		pid=sel.xpath('//input[@id="productId"]/@value').extract()[0]
		mid=sel.xpath('//input[@id="productMercantId"]//@value').extract()[0]
		merchantid=sel.xpath('//input[@id="merchantId"]/@value').extract()[0]
		vid=re.search('paramSignature:\"(.*)\"',response).group(1)
		item.pid=pid
		item.name=sel.xpath('//head/title/text()').extract()[0]
		item.price=sel.xpath('//span[@id="current_price"]/text()').extract()[0]
		item.rsp=sel.xpath('//span[@class="oldprice"]/del/text()').extract()[0]
		item.promotion=GetPromotionInfo(mid)
		item.store=sel.xpath('//input[@id="companyName"]/@value').extract()[0]
		item.retailer='1' 
		#item.sourceid=sourceId
		item.datetime=time.isoformat()
		item.year=time.year
		item.month=time.month
		item.quarter=ceil(float(item.month)/3.0)
		item.week=time.isocalendar()[1]
		item.day=time.day
		item.hour=time.hour
		item.memo1=GetPromotionInfoPage(pid,merchantid,mid,vid) #used to store the promotion html get from html page, need to be further processed to store in the promotion
		result.append(item.toList())
	except IndexError as e:
		print 'Lose network connection or the page structure changed'
		raise e
	except Exception as e:
		print 'error in YHD_ItemPage_Scraper'
		raise e
	else:
		return result

#OBJECTIVE: Remove all the HTML control characters like &nsp in the string
#INPUT:source is string, encoding is string
#OUPUT: string
def ProcessHTMLString(source,encoding):
	if type(source)==unicode:
		source=source.encode(encoding,'ignore')
	source=source.decode(encoding,'ignore')
	return source

#OBJECTIVE:Turn the query url into a Yihaodian common query url
#INPUT: url is string
#OUTPUT: url is string
def NormalizeUrl(url):
	keyword=''
	#remove the query like #page=1&sort=1
	if re.search('#(page=\d{1,})*(&)*(sort=\d{1,})*',url) is not None:
		url=re.sub('#(page=\d)*(&)*(sort=\d)*','',url)
	#check if the url is already nomral
	if re.search('/(\w{1,}\d{0,}-){3,}\w*/',url) is None:
		#check if it's search.yhd.com or www.yhd.com
		if re.search('search.yhd.com',url) is not None:
			#replace search to www, and add /ctg
			url=re.sub('search.yhd.com','www.yhd.com/ctg',url)
			#get the seach keyword
			keyword=re.search('/k([^/]*)/',url).group(1)
			#replace the /keyword/1/ to /b/
			url=re.sub('/k.*','/b/',url)
		#Converappend the control section
		url=url+u'a-s1-v0-p1-price-d0-f0-m1-rt0-pid-mid0-k'
		#append the keyword
		url=url+keyword+u'/'
	#switch s2 into searchPage
	url=re.sub('/s2/','/searchPage/',url)
	return url

#OBJECTIVE:For query url have following pages, get the url of next page
#NOTE: it will just increase the page num, no checking performed
#INPUT: url is string
#OUTPU: string
def GetNextPageUrl(url):
	#this function is used in the re.sub
	#it is to replace the old page with the new page
	def increasePageNum(matchobj):
		oldline=matchobj.group(0)
		num=int(matchobj.group(2))
		oldpage='p'+unicode(num)
		newpage='p'+unicode(num+1)
		newline=oldline.replace(oldpage,newpage)
		return newline
	#add /(\w{1,}\d{0,}-){2,} is to make sure the p1 is in the query not in the keyword input by users
	#count=1, to make the replace of the first pattern met
	url=re.sub('/(\w{1,}\d{0,}-){2,}p(\d{1,})-',increasePageNum,url,count=1)
	return url

#OBJECTIVE:Get the next 32 products of a query page
#INPUT: url is string
#OUTPUT: the data of products
def GetMoreProduct(url):
	url=url+u'?isGetMoreProducts=1&moreProductsDefaultTemplate=0'
	response=GetHttpObject(url)
	return response


#OBJECTIVE: Perform scraping on a query source
#INPUT: url is string, sourceId is string
#OUTPUT: List
def YHD_SearchPage_Scraper(url):
	try:
		url=NormalizeUrl(url)
		#TODO:when GetHttpObject error in the middle of page, program will jump
		#out without saving the previous work. Need to work out
		response=GetHttpObject(url)
		response=CleanEscapeChars(response)
		result=[]
		item=SKU()
		time=datetime.now()
		sel=Selector(text=response,type='html')
		#get the page num
		#as the location of pageNo is unknow
		pageNo=sel.xpath('//div[@class="select_page_num"]/text()').extract()
		ttlpage=0
		for num in pageNo:
			num=re.search('(\d{1,})',num)
			if num is not None:
				ttlpage=int(num.group(0))
		print 'Totalpage:',ttlpage
		#get the product page for each page number
		for i in range(1,ttlpage+1):
			#fetch the hiden products
			#combine the hiden products with the existing products
			print 'pageno:',i
			response=CleanEscapeChars(GetHttpObject(url))
			moreResponse=CleanEscapeChars(GetMoreProduct(url))
			response=response+moreResponse
			sel=Selector(text=response,type='html')
			products=sel.xpath('//li[@class="search_item"]')
			print 'product num:',len(products)
			#Parse products
			for product in products:
				item.pid=product.xpath('.//div[@class="search_item_box"]/@comproid').extract()[0]
				mid=product.xpath('.//a[@class="title"]/@pmid').extract()[0]
				merchantid=product.xpath('.//a[@class="buy_btn"]/@merchantid').extract()[0]
				item.name=ProcessHTMLString(product.xpath('.//a[@class="title"]/text()').extract()[0],'gbk')
				print item.name
				item.price=float(product.xpath('.//span[@class="color_red price"]/@yhdprice').extract()[0])
				item.rsp=float(product.xpath('.//del/text()').extract()[0][1:]) #format is $100, this is to remove the $ sign 
				item.store=product.xpath('.//div[@class="owner"]//text()').extract()[0]
				print 'store name:',item.store
				item.promotion=GetPromotionInfo(mid)
				item.retailer='1' #TODO: need to turn it into a constant 
				#item.sourceid=sourceId
				item.datetime=time.isoformat()
				item.year=time.year
				item.month=time.month
				item.quarter=ceil(float(item.month)/3.0)
				item.week=time.isocalendar()[1]
				item.day=time.day
				item.hour=time.hour
				item.memo1=""
				result.append(item.toList())
				item=SKU()
			#switch to next page
			url=GetNextPageUrl(url)
			print url
	except Exception as e:
		print e
		raise e
	return result

#For test purpose
def GetResponse(url):
	return GetHttpObject(url)
