#Test
import threading
import thread
import signal
import sys
import time
IsReady=True
IsClosed=False
ReadyLock=threading.Lock()

class Listener(threading.Thread):
    def __init__(self,name):
	threading.Thread.__init__(self)
	self.name=name

    def run(self):
	print "starting " + self.name
	T2=Scraper('Scraper',5)
	T2.start()
	while not IsClosed:
           listen_fun()
	print "exiting " + self.name


def listen_fun():
    command=sys.stdin.readline()
    if command[:-1]=='exit':
	exit_fun()
	return
    elif command[:-1]=='cancel':
	print 'Are you sure to cancel scraping, y/n'
	command=sys.stdin.readline()
	if command[:-1]=='y':
	    cancel_fun()
	return
    elif command[:-1]=='restart':
	restart_fun()
	return
    print 'Hello, you have just typed :[%s]'%(command)
    return
def exit_fun():
    print 'Are you sure to exit, y/n'
    command=sys.stdin.readline()
    if command[:-1]=='y':
	global IsClosed
	IsClosed=True
	cancel_fun()
    return

def cancel_fun():
    ReadyLock.acquire()
    global IsReady
    IsReady=False
    ReadyLock.release()
    return

def restart_fun():
    thread=Scraper('scraper',5)
    ReadyLock.acquire()
    global IsReady
    IsReady=True
    ReadyLock.release()
    thread.start()
    return


class Scraper(threading.Thread):
    def __init__(self,name,interval):
	threading.Thread.__init__(self)
	self._name=name
	self._interval=interval

    def run(self):
	print "starting " + self._name
	count=0
	while IsReady:
	   print "%d run"%(count)
	   print "start scraping"
	   scrape_fun(self._interval)
	   print "finished scraping"
	   count=count+1
	print "exiting " + self._name

def scrape_fun(interval):
    print "scraping in process" 
    time.sleep(interval)

lc=threading.Condition()

def WaitTimeOut(timeout):
	lc.acquire()
	print 'I\'m going to sleep now...'
	result=lc.wait(timeout)
	print 'result=',result
	if result==False:
		print 'Nobody wakes me up...'
	else:
		print 'I\'m waken up now'
	


def main():
	thread.start_new_thread(WaitTimeOut,(5,))
	time.sleep(1)
	while True:
		print 'YOU INPUT'
		line=sys.stdin.readline()
		if line[:-1]=='wake':
			lc.acquire()
			print 'I will wake up the thread'
			lc.notify()
			lc.release()
		else:
			print 'You have input [%s]'%(line)
	return
