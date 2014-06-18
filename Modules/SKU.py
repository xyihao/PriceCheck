#This is a common class to represent a SKU

class SKU(object):


	@property
	def name(self):
		return self._name
	@name.setter
	def name(self,value):
		self._name=value
		return self._name

	@property
	def pid(self):
		return self._pid
	@pid.setter
	def pid(self,value):
		self._pid=value
		return self._pid

	@property
	def price(self):
		return self._price
	@price.setter
	def price(self,value):
		self._price=value
		return self._price
	
	@property
	def promotion(self):
		return self._promotion
	@promotion.setter
	def promotion(self,value):
		self._promotion=value
		return self._promotion

	@property
	def rsp(self):
		return self._rsp
	@rsp.setter
	def rsp(self,value):
		self._rsp=value
		return self._rsp

	@property
	def retailer(self):
		return self._retailer
	@retailer.setter
	def retailer(self,value):
		self._retailer=value
		return self._retailer
	
	#represents the seller
	#to differentiate the flagship_store from other seller
	@property
	def store(self):
		return self._store
	@store.setter
	def store(self,value):
		self._store=value
		return self._store
	#@property
	#def sourceid(self):
	#	return self._sourceid
	#@sourceid.setter
	#def sourceid(self,value):
	#	self._sourceid=value
	#	return self._sourceid

	@property
	def datetime(self):
		return self._datetime
	@datetime.setter
	def datetime(self,value):
		self._datetime=value
		return self._datetime

	@property
	def year(self):
		return self._year
	@year.setter
	def year(self,value):
		self._year=value
		return self._year

	@property
	def quarter(self):
		return self._quarter
	@quarter.setter
	def quarter(self,value):
		self._quarter=value
		return self._quarter

	@property
	def month(self):
		return self._month
	@month.setter
	def month(self,value):
		self._month=value
		return self._month

	@property
	def week(self):
		return self._week
	@week.setter
	def week(self,value):
		self._week=value
		return self._week

	@property
	def day(self):
		return self._day
	@day.setter
	def day(self,value):
		self._day=value;
		return self._day

	@property
	def hour(self):
		return self._hour
	@hour.setter
	def hour(self,value):
		self._hour=value
		return self._hour

	@property
	def memo1(self):
		return self._memo1
	@memo1.setter
	def memo1(self,value):
		self._memo1=value
		return self._memo1

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return "{name} of {store} from {retailer}".format(name=self.name.encode('GBK'),store=self.store,retailer=self.retailer)

	def toList(self):
		return [self.pid,self.name,self.rsp,self.price,self.promotion,self.retailer,self.store,self.datetime,self.year,self.quarter,self.month,self.week,self.day,self.hour,self.memo1]

