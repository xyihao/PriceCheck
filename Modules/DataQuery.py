#Here stores the DataQuery class
#DataQuery class represents a query to the database

from datetime import date,timedelta
Date_Period=(
		('ALL','All'),
		('P1W','Past 1 week'),
		('P1M','Past 1 month'),
		('P3M','Past 3 months'),
		('P6M','Past 6 months'),
		('P1Y','Past 1 year'),
		('CTM','Custimzed'),
		)

class DataQuery(object):
	#date_period is a descriptive date selection
	#date_period ='all','past 1 week','past 1 month','past 3 month','past 6 months','past 1 year','customized'
	#date_selection is a lenght=2 tuple, with startdate as the first, enddate as the second
	def __init__(self,key,date_period='all',date_selection=None,unit='day'):
		self._key=key
		self._unit=unit
		self._startdate=''
		self._enddate=''
		if date_period==Date_Period[0][0]:
			self._startdate=None
			self._enddate=None
		elif date_period==Date_Period[1][0]: #Past 1 week
			self._enddate=date.today().isoformat()
			self._startdate=(date.today()-timedelta(days=7)).isoformat()
		elif date_period==Date_Period[2][0]: #Past 1 month
			self._enddate=date.today().isoformat()
			self._startdate=(date.today()-timedelta(days=30)).isoformat()
		elif date_period==Date_Period[3][0]: #Past 3 months
			self._enddate=date.today().isoformat()
			self._startdate=(date.today()-timedelta(days=90)).isoformat()
		elif date_period==Date_Period[4][0]: #Past 6 months
			self._enddate=date.today().isoformat()
			self._startdate=(date.today()-timedelta(days=180)).isoformat()
		elif date_period==Date_Period[5][0]: #Past 1 year
			self._enddate=date.today().isoformat()
			self._startdate=(date.today()-timedelta(days=365)).isoformat()
		elif date_period==Date_Period[6][0]: #Customized
			if date_selection is not None:
				self.validateDate(date_selection)
				self._startdate=date_selection[0]
				self._enddate=date_selection[1]

	
	def validateDate(self,dates):
		pass


	@property
	def key(self):
		return self._key

	@property
	def startdate(self):
		return self._startdate

	@property
	def enddate(self):
		return self._enddate

	@property
	def unit(self):
		return self._unit 


			



