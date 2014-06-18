#Here is all the function related to the write the data to the storage
import codecs
import sqlite3
from Modules.settings import SOURCE_TABLE,PRODUCT_TABLE,DATA_DB,CONFIG_DB,TEST_DB

#write the result to the file
def OutputResult_text(result,filename):
	file=codecs.open(filename,encoding='GBK',mode='a')
	for item in result:
		file.write(item)
		file.write('\t\n')
	file.close()

#OBSOLETE
def UpdateProductSQL(items,sourceId):
	conn=sqlite3.connect(DATA_DB)
	sql='INSERT INTO {table}\
	(uid,name,rsp,price,promotion,site,store,sourceid,datetime,year,quarter,month,week,day,hour,memo1) values\
	(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'.format(table=PRODUCT_TABLE)
	#conn.execute('BEGIN')
		#sql=u'INSERT INTO {table} \
		#(name,rsp,price,site,store,datetime,year,quarter,month,week) \
		#values ("{name}",{rsp},{price},"{site}","{store}",date("{datetime}"),{year},{quarter},{month},{week})'\
		#.format(table=PRODUCT_TABLE,name=item.name,rsp=item.rsp,price=item.price,site=item.retailer,store=item.store,datetime=item.datetime,year=item.year,quarter=item.quarter,month=item.month,week=item.week)
	conn.executemany(sql,items)
	conn.commit()
	conn.close()


def UpdateSource(sourceId):
	pass

#OBJECTIVE: 1)put the result back to the database 2) update the source's last_update and next_update 
#INPUT: items is a list of result,
#		sourceId is the id of the source
#		period_type is the update period type, HH,DY,WK,MH
#		period_num is the update frequency within the specified period_type
#OUTPUT: none
def OutputResult(items,sourceId,period_type,period_num):
	try:
		conn=sqlite3.connect(TEST_DB)
		#Insert the result into the database
		sql='INSERT INTO {table}\
		(uid,name,rsp,price,promotion,site,store,datetime,year,quarter,month,week,day,hour,memo1,sourceid) values\
		(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'.format(table=PRODUCT_TABLE)
		conn.executemany(sql,items)
		#Update the source table with update time
		shift_time=''
		if period_type=='HH':
			shift_time='%.1f hours'%(1.0/float(period_num))
		elif period_type=='DY':
			shift_time='%.1f days'%(1.0/float(period_num))
		elif period_type=='WK':
			shift_time='%.1f days'%(7.0/float(period_num))
		elif period_type=='MH':
			shift_time='%.1f months'%(1.0/float(period_num))

		#TODO:need to insert the [next_update] column into the database
		sql='UPDATE {table} SET last_update=datetime("now","localtime"),\
		next_update=datetime("now","localtime","{shift_time}") WHERE\
		id={sourceId}'.format(table=SOURCE_TABLE,sourceId=sourceId,shift_time=shift_time)
		conn.execute(sql)
		conn.commit()
		conn.close()
	except Exception as e:
		print "error in OutputResult"
		print e
		raise e


