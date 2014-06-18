from Modules.settings import TEST_DB,PRODUCT_TABLE
import sqlite3

#startdate, enddate shall be datestring in the format of %Y-%m-%D
def GetChartData(key,key_value,agg_func='avg',startdate=None,enddate=None,unit='day'):
	select_clause=''
	group_clause=''
	date_condition=''
	pre_date_AND='AND ' 
	in_date_AND='' 
	#compose the date_cndition express
	if startdate:
		date_condition=pre_date_AND+date_condition+'datetime>=datetime("%s")'%(startdate)
		pre_date_AND=''
		in_date_AND=' AND '
	if enddate:
		date_condition=pre_date_AND+date_condition+in_date_AND+'datetime<=datetime("%s")'%(enddate)
	#compose the select clause
	select_clause='%s(price)'%agg_func
	group_clause=''
	select_clause=select_clause+',year'
	group_clause=group_clause+'year'
	if unit=='quarter':
		select_clause=select_clause+',quarter'
		group_clause=group_clause+',quarter'
	if unit=='month':
		select_clause=select_clause+',month'
		group_clause=group_clause+',month'
	if unit=='week':
		select_clause=select_clause+',week'
		group_clause=group_clause+',week'
	if unit=='day':
		select_clause=select_clause+',month,day'
		group_clause=group_clause+',month,day'

	sql='SELECT {0} From {1} WHERE {2}={3} {4} GROUP BY {5} ORDER BY datetime \
	ASC'.format(select_clause,PRODUCT_TABLE,key,key_value,date_condition,group_clause)
	
	print sql
	try:
		conn=sqlite3.connect(TEST_DB)
		cursor=conn.execute(sql)
		results=cursor.fetchall()
		conn.close()

		#get the query into to list
		prices=[]
		dates=[]
		for result in results:
			prices.append(result[0])
			date=''
			for x in result[1:-1]:
				date=date+'%s-'%(x)
			date=date+'%s'%(result[-1:])
			dates.append(date)
		return (prices,dates)
	except Exception, e:
		raise e


def GetChartDataObject(query):
	return GetChartData('uid',query.key,startdate=query.startdate,enddate=query.enddate,unit=query.unit)
