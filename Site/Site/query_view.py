import pickle
import sqlite3
from django.http import HttpResponse

from Modules.settings import TEST_DB,QUERY_TABLE


def getlist():
	try:
		pass	
	except Exception, e:
		raise e


def newQuery():
	pass

def delQuery(key):
	pass

def updateQuery(key,parameters):
	pass




def hello(request):
	return HttpResponse("Hello world")


