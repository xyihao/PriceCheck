from django.shortcuts import render

# Create your views here.
import pickle
import sqlite3
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from django.http import HttpResponse
from priceQuery.models import DataQueries
from Site.DataQuery import DataQuery
from Modules.settings import TEST_DB,QUERY_TABLE
from Site.DrawChart import GetChartDataObject

def getList(request):
	try:
		views=DataQueries.objects.all()
		template=get_template('DataQueryView.html')
		data=[]
		for view in views:
			a=[]
			a.append(view.id)
			a.append(view.user)
			obj=pickle.loads(view.object)
			a.append(obj.key)
			a.append(obj.startdate)
			a.append(obj.enddate)
			a.append(obj.unit)
			data.append(a)

		context=Context({'queries':data})
		html=template.render(context)
		return HttpResponse(html)

	except Exception, e:
		raise e


def addNewQuery(request):
	try:
		if not 'key' in request.POST:
			return render(request,'NewQueryForm.html')
		user=request.POST['user']
		key=request.POST['key']
		date_period=request.POST['date_period']
		startdate=request.POST['startdate']
		enddate=request.POST['enddate']
		unit=request.POST['unit']
		obj=DataQuery(key,date_period,(startdate,enddate),unit)

		query=DataQueries()
		query.user=user
		query.key=key
		query.object=pickle.dumps(obj)
		query.save()

		return render(request,'NewQueryForm.html',{
				'user':user,'key':key,'startdate':startdate,\
				'enddate':enddate,'unit':unit,
				})
	except Exception, e:
		raise e

def delQuery(key):
	pass

def updateQuery(key,parameters):
	pass



def getData(request,key):
	try:
		key=int(key)
		query=DataQueries.objects.filter(id=key)
		if query:
			#filter will return a list even it contains only 1 item
			obj=pickle.loads(query[0].object)
			data=GetChartDataObject(obj)
			data=zip(*data)
			return render(request,'dataTable.html',{'obj':obj,'data':data,})
	except Exception, e:
		raise e
	pass



def hello(request):
	return HttpResponse("Hello world")


