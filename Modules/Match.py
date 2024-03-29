#_*_coding:GBK_*_
#This modules is about finding the common substring across strings
from Modules.settings import DATA_DB,PRODUCT_TABLE
import sqlite3

TEST_STR=[u'����ŷ���Ż��׾���15ml',u'ŷ���Ż�����˪15ml']

MIN_LENGTH=3


class HashTable(dict):
	pass

class stringLocation:
	def __init__(self,stringID,position):
		self._stringID=stringID
		self._positioin=position
	@property
	def stringID(self):
		return self._stringID
	@stringID.setter
	def stringID(self,value):
		self._stringID=value
		return self._stringID
	@property
	def position(self):
		return self._position
	@position.setter
	def position(self,value):
		self._position=value
		return self_position


def GetTestStr():
	strings=[]
	conn=sqlite3.connect(DATA_DB)
	conn.row_factory=sqlite3.Row
	cursor=conn.cursor()
	cursor.execute('select name from {0}'.format(PRODUCT_TABLE))
	for str in cursor:
		strings.append(str['name'])
	return strings


def HashScan(ID,string,hashtable,length):
	for i in range(0,len(string)-length+1):
		value=string[i:i+length]
		if hashtable.has_key(value):
			if hashtable[value].has_key(ID):
				hashtable[value][ID].append(i)
			else:
				hashtable[value][ID]=[i,]
		else:
			hashtable[value]=dict()
			hashtable[value][ID]=[i,]

	return hashtable

#removes all the characters who doesn't exist in stringNum of strings
#usually the stringNum is set the same as total string number
#this will ask the function to remain those characters only existing in all the strings
def ClearHashTable(hashtable,stringNum):
	for k,v in hashtable.items():
		if len(v)<stringNum:
			del hashtable[k]
	return hashtable

			
def BuildHashTable(strings):
	table=HashTable()
	n=0 
	#n serves as a simple representation of string ID, string ID is used t:w
	#identify different string, it will be used to fetch the substring in each
	#string
	for string in strings:
		table=HashScan(n,string,table,MIN_LENGTH)
		n=n+1
	table=ClearHashTable(table,len(strings))
	table2=dict(table) #test purpose	
	result=dict() #holds the common substring value, it's for display purpose
	result[MIN_LENGTH]=[]
	for k in table.iterkeys():
		result[MIN_LENGTH].append(k)
	level=MIN_LENGTH+1
	while True:
		print 'checking substring of {0} length'.format(level)
		items=table.items()
		table.clear()
		for item in items:
			for ID,locs in item[1].items():
				for loc in locs:
					endloc=(loc+level) if loc+level<=len(strings[ID]) else 0
					if endloc==0:
						continue
					substr=strings[ID][loc:loc+level]
					#print u'substring={0}'.format(substr)
					if table.has_key(substr):
						if table.has_key(ID):
							table[substr][ID].append(loc)
						else:
							table[substr][ID]=[loc,]
					else:
						table[substr]=dict()
						table[substr][ID]=[loc,]


		table=ClearHashTable(table,len(strings))
		if len(table)==0:
			break
		result[level]=[]
		for k in table.iterkeys():
			result[level].append(k)
		level=level+1

	return result

#return gap or 0
#0 means not equal
#test successful so far
def HashCompare(item1,item2):
	#the item1,item2 are tuples like (key,dict)
	#this conversion save the item1[1] to only item1
	#better for code reading
	item1=item1[1]
	item2=item2[1]
	gap=0
	#due the string may have more than one string location
	#to find the key with one location in both string
	#use that to calculate the gap
	for key, locs1 in item1.items():
		if len(locs1)==1:
			if item2.has_key(key):
				locs2=item2[key]
				if len(locs2)==1:
					gap=locs1[0]-locs2[0]
					break;

	for key,locs1 in item1.items():
		equal=False
		if item2.has_key(key):
			locs2=item2[key]
			for i in locs1:
				for j in locs2:
					if (i-j)==gap:
						equal=True
		if equal==False:
			gap=0
			break
	return gap

def Merge(item1,item2,gap):
	#merge the key value
	newKey=u''
	if gap>0:
		newKey=item2[0]+item1[0][-gap:]
		preItem=dict(item2[1])
		aftItem=dict(item1[1])
	else:
		newKey=item1[0]+item2[0][gap:]
		preItem=dict(item1[1])
		aftItem=dict(item2[1])
	#merge the location value
	for key,locs1 in preItem.items():
		if len(locs1)>1:
			equal=False
			locs2=aftItem[key]
			for i in locs1:
				for j in locs2:
					if (i-j)==-abs(gap):
						equal=True
						continue
				if equal==False:
					locs1.remove(i)
	newItem=(newKey,preItem)
	return newItem

def HashCompareMerge(item1,item2):
	key1=item1[0]
	key2=item2[0]
	#print u'compare {0} with {1}'.format(key1,key2)
	item1=item1[1]
	item2=item2[1]
	rowLength=len(item1) #the rows number of each item
	gaps=dict()
	for key,locs1 in item1.items():
		if item2.has_key(key):
			locs2=item2[key]
			for i in locs1:
				for j in locs2:
					gap=i-j
					if gap<0:
						m=i
					else:
						m=j
					if gaps.has_key(gap):
						if gaps[gap].has_key(key):
							gaps[gap][key].append(m)
						else:
							gaps[gap][key]=[m,]
					else:
						gaps[gap]=dict()
						gaps[gap][key]=[m,]
	#check the gaps dictionary
	result=[]
	for key,val in gaps.items():
		if abs(key)==1 and len(val)==rowLength:
			if key==1:
				newKey=key2+key1[-1:]
			else:
				newKey=key1+key2[-1:]
			result.append((newKey,val))
			#print newKey,val
	return result




def MergeList(itemList,level):
	if len(itemList)<2:
		return itemList
	tb=itemList

	status=range(0,len(tb))
	result=[] #hold the merged items
	for i in range(0,len(tb)):
		for j in range(i,len(tb)):
			#gap=HashCompare(tb[i],tb[j])
			#if abs(gap)==1:
			#	t=Merge(tb[i],tb[j],gap)
			#	result.append(t)
			mergeResult=HashCompareMerge(tb[i],tb[j])
			if len(mergeResult)>0:
				status[i]='y'
				status[j]='y'
				for o in mergeResult:
					result.append(o)
	#print '{0} merge has {1} result'.format(level,len(result))
	#for i in range(0,len(result)):
	#	print result[i][0]
	result=MergeList(result,level+1)
	for i in range(0,len(status)):
		if status[i]=='y':
			continue
		result.append(tb[i])
	return result




def MergeHashTable(hashtable):
	t0=hashtable
	tTemp=[]
	tEnd=HashTable()
	
	#sort hashtable by the number of rows for each item descending
	#the return value will be a list in the format of
	#{(key,{(rowID,(loc,)),(rowID2,(loc,))})}
	items=sorted(t0.iteritems(),key=lambda(k,v):len(v),reverse=True)
	rowNum=len(items[0][1]) #the number row contains in an substring
	tTemp.append(items[0])
	n=1
	level=MIN_LENGTH
	while n<len(items):
		if len(items[n][1])==rowNum:
			tTemp.append(items[n])
		else:
			#process the merge in tTmep
			if rowNum>1 and len(tTemp)>1:
				result=MergeList(tTemp,level)
				for i in range(0,len(result)):
					tEnd[result[i][0]]=result[i][1]
			rowNum=len(items[n][1])
			tTemp=[]
			tTemp.append(items[n])
		n=n+1
		if rowNum==1:
			break;
	#if rowNum>1 and len(tTemp)>1:
	#	result=MergeList(tTemp,level)
	#	for i in range(0,len(result)):
	#		tEnd[result[i][0]]=result[i][1]	
	return tEnd



#This function will scan the strings set to build an initial hashtable
#then use merge to find the largest common set
def BuildHashTable2(strings):
	table=HashTable()
	n=0
	for string in strings:
		table=HashScan(n,string,table,MIN_LENGTH)
		n=n+1
	table=MergeHashTable(table)
	return table



def DisplayResult(result):
	for k,v in result.items():
		print '{0} chars substring-----------------\n'.format(k)
		for s in v:
			print u'{0}'.format(s)


