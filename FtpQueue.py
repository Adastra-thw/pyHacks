#!/usr/bin/env python

import threading
import Queue
import time
import ftplib
from shodan import WebAPI

#lock = threading.Lock()

class WorkerThread(threading.Thread) :


	def __init__(self, queue, tid) :
		threading.Thread.__init__(self)
		self.queue = queue
		self.tid = tid
		print "Worker %d Reporting "%self.tid



	def run(self) :
		lock = threading.Lock()

		while True :
			lock.acquire()
			host = None

			try:
				site = self.queue.get(timeout=1)

			except Queue.Empty :
				print "Worker %d exiting... "%self.tid


			try :	
			 ftp = ftplib.FTP(site)
			 ftp.login()
			 print "Connecting to site %s"%site			
			 print ftp.retrlines('LIST')
			 ftp.quit()

			 print "Exiting site %s"%site

			except :
			 print "Error in listing " +site	
			finally:
				lock.release() 


			#print "Finished logging into ftp site %s"%site
			self.queue.task_done()



queue = Queue.Queue()

#sites = ["rtfm.mit.edu", "ftp.ncsa.uiuc.edu", "prep.ai.mit.edu", "gatekeeper.dec.com"]
shodanKey = open('shodanKey').readline().rstrip('\n')
api = WebAPI(shodanKey)
results = api.search("port:21 anonymous")
sites=results['ip']

threads = []			
for i in range(4) :
	print "Creating WorkerThread : %d"%i
	worker = WorkerThread(queue, i)
	worker.setDaemon(True)
	worker.start()
	threads.append(worker)
	print "WorkerThread %d Created!"%i 	

for site in sites :
	queue.put(site)	

queue.join()

print "All Tasks over!"	
