import multiprocessing
import sys
from bs4 import BeautifulSoup
import mechanize
import argparse
import urllib
import urllib2
import time
import MySQLdb

class WebSpider():

	def __init__(self, webSite, depth, proxyhost, proxyuser, proxypassword, proxyport,proxysecure="http"):
		try:
			self.webSite = webSite
			self.depth = int(depth)
			self.totalDeepCrawled = 0
			self.linksVisited = [self.webSite]
			self.totalProfundity = 0;
			self.proxyhost = proxyhost
			self.proxyuser = proxyuser
			self.proxypassword = proxypassword
			self.proxysecure = proxysecure
			self.proxyport = proxyport
			self.proxies = None
			if self.proxyhost != None and self.proxyport != None:
				if self.proxyuser != None and self.proxypassword != None: 
					self.proxies = urllib2.ProxyHandler({self.proxysecure: self.proxysecure+"://"+self.proxyuser+":"+self.proxypassword+"@"+self.proxyhost+":"+self.proxyport})
				else:
					self.proxies = urllib2.ProxyHandler({self.proxysecure: self.proxysecure+"://"+self.proxyhost+":"+self.proxyport})
			#Perform the connection with the database.
			print "[*] Performing Connection with Database..."
			print "[*] Reading the Mysql Setting from the file 'MySQLSettings.ini'"
			settingsFile = open("MySQLSettings.ini", "r");
			settingConnection = {}

			for setting in settingsFile:
				(key, value) = setting.split("=")
				settingConnection[key] = value.rstrip('\n').rstrip('\r')
				
			settingsFile.close()
			self.db = MySQLdb.connect(settingConnection["host"],settingConnection["user"],settingConnection["password"],settingConnection["databaseName"])
			self.cursorDB = self.db.cursor()
			print "[*] Connection Established!" 
		except:
			print "[-] Exception trying to connect with the database. Check the connection settings for the MySQL instance"
			print "[-] We can't continue... closing the program."
			print sys.exc_info()[0]
			print sys.exc_info()[1]
			print sys.exc_info()[2]
			sys.exit(0)

	def crawl(self):
		print "[*] Starting the web crawling ..."
		if self.proxies != None:
			urlRootSite = urllib.urlopen(self.webSite, proxies=self.proxies)
		else:
			urlRootSite = urllib.urlopen(self.webSite)
		contents = urlRootSite.read()
		rootSite = BeautifulSoup(contents)
		links = rootSite.find_all("a")
		print "[*] Getting the links for the URL: ", self.webSite
		self.idWebSiteRoot = self.storeWebSiteRoot(self.webSite, contents)
		self.storeWebSiteForms(self.webSite)
		self.storeWebSiteLinks(links)
		try:
			for link in links:
				#process = multiprocessing.Process(target=self.handleLink, args=[link])
				#process.daemon = True
				#process.start()	
				#process.join()
				self.handleLink(link)				
				self.totalProfundity = 0
		finally:
			self.db.close()
			self.cursorDB.close()
		
	def handleLink(self, link):
		self.totalProfundity = self.totalProfundity + 1	
		if ('href' in dict(link.attrs) and "http" in link['href']):
			try:
				href = link["href"]
				if href in self.linksVisited:
					return
				if self.proxies != None:
					urlLink = urllib.urlopen(href,proxies=self.proxies)
				else:
					urlLink = urllib.urlopen(href)
				self.linksVisited.append(link['href'])
				print "Handling Link %s. url: %s" %(link.text, link['href'])
				#Extract info about the link, before to get links in this page.
				if self.totalProfundity <= self.depth:
					linkSite = BeautifulSoup(urlLink, "lxml")
					depthLinks = linkSite.find_all("a")				
					self.storeWebSiteForms(link['href'])
				        self.storeWebSiteLinks(depthLinks)
					for sublink in depthLinks:
						#processLink = multiprocessing.Process(target=self.handleLink, args=[sublink])
	        	        		#processLink.daemon = True
						#processLink.start()
						self.handleLink(sublink)
				else:
					self.totalProfundity = self.totalProfundity - 1
					return
			except:
				print "[-] Error in Link..."	
				print link
				print sys.exc_info()[1]
				self.storeError("Error visiting Link: " + "[0] " + str(sys.exc_info()[0]) + " [1] " + str(sys.exc_info()[1]) + " [2] " + str(sys.exc_info()[2]))
	'''
		SQL Table: 
		create table WebSites(webSiteRoot VARCHAR(100) NOT NULL, contents VARCHAR(1000000) NOT NULL, id MEDIUMINT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id));
	'''
	def storeWebSiteRoot(self,url, contents):
		try:
			#insertSQL = "INSERT INTO WebSiteRoot (webSiteRoot,contents) values (%s, %s)", (str(url), str(contents))
			self.cursorDB.execute("""INSERT INTO WebSites (webSiteRoot,contents) values (%s, %s)""", (url, contents))
			self.db.commit()
			self.cursorDB.execute("SELECT Auto_increment FROM information_schema.tables WHERE table_name='WebSites';")
			return self.cursorDB.fetchall()[0][0]
		except:
			print "[-] Exception trying to insert the WebSite root in database."
			self.db.rollback()
			self.storeError("Exception trying to insert the WebSite root in database. " + "[0]" + sys.exc_info()[0] + "[1]" + sys.exc_info()[1] + "[2]" + sys.exc_info()[2])
			#print sys.exc_info()[0]
			#print sys.exc_info()[1]
			#print sys.exc_info()[2]

	'''
		SQL Table:
		CREATE TABLE WebSiteLinks(id MEDIUMINT NOT NULL AUTO_INCREMENT, idWebSiteRoot MEDIUMINT NOT NULL, link VARCHAR(500) NOT NULL, PRIMARY KEY (id));
	'''
	def storeWebSiteLinks(self, links):
		try:
			for link in links:
				if ('href' in dict(link.attrs) and "http" in link['href']):
					self.cursorDB.execute("INSERT INTO WebSiteLinks (idWebSiteRoot,link) values (%s, %s)", (str(self.idWebSiteRoot), link['href']))
	                        	self.db.commit()
		except:
			self.db.rollback()
			print "Exception trying to insert a web link."
			self.storeError("Exception trying to insert a web link " + "[0]" + sys.exc_info()[0] + "[1]" + sys.exc_info()[1] + "[2]" + sys.exc_info()[2])
            #print sys.exc_info()[0]
            #print sys.exc_info()[1]
            #print sys.exc_info()[2]


	'''
		SQL Table:
		CREATE TABLE WebSiteForms(id MEDIUMINT NOT NULL AUTO_INCREMENT, idWebSiteRoot MEDIUMINT NOT NULL, formAction VARCHAR(500), formName VARCHAR(500), formMethod VARCHAR(20), PRIMARY KEY (id));
		CREATE TABLE FormData(id MEDIUMINT NOT NULL AUTO_INCREMENT, idWebSiteForm MEDIUMINT NOT NULL, attributeName VARCHAR(200), attributeValue VARCHAR(200), attributeType MEDIUMINT, PRIMARY KEY(id) )
	'''		
	def storeWebSiteForms(self, url):
		browser = mechanize.Browser()		
		if self.proxies != None:
			browser.set_proxies(self.proxies)
		browser.open(url)
		try:
			for form in browser.forms():
				self.cursorDB.execute("INSERT INTO WebSiteForms (idWebSiteRoot,formAction, formName, formMethod) values (%s, %s, %s, %s)", (str(self.idWebSiteRoot), form.action,form.name,form.method))
				self.db.commit()
				self.cursorDB.execute("SELECT Auto_increment FROM information_schema.tables WHERE table_name='WebSiteForms';")
	                        idForm =  self.cursorDB.fetchall()[0][0]
				for control in form.controls:
					controlName = control.name
					controlType = control.type
					controlValue = control.value
					if controlName == None:
						controlName = ""
					if controlType == None:
						controlType = ""
					if controlValue == None:
						controlValue = ""
					#print str(controlName) +" - "+str(controlType)+" - "+ str(controlValue)
	        	                self.cursorDB.execute("INSERT INTO FormData (idWebSiteForm,attributeName,attributeValue,attributeType) values (%s, %s, %s, %s)", (str(idForm), str(controlName), str(controlValue), str(controlType)))
					self.db.commit()
		except AttributeError:
			pass
		except:
			self.db.rollback()
			print "Exception trying to insert a web form. Storing error..."
			self.storeError("Exception trying to insert a web form. " + "[0]" + sys.exc_info()[0] + "[1]" + sys.exc_info()[1] + "[2]" + sys.exc_info()[2])
			#print sys.exc_info()[0]
			#print sys.exc_info()[1]
            #print sys.exc_info()[2]


	def storeError(self, errorMessage):
		try:
			self.cursorDB.execute("INSERT INTO Errors (errorMessage) values (%s)", (errorMessage))
			self.db.commit()
		except:
			print "Error storing an error in database... Ironic, isn't?"


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Python WebSpider")
	parser.add_argument("-t", "--target", required=True,  help="Target website")
	parser.add_argument("-d", "--depth", required=False, help="Number of links to crawl")

	parser.add_argument("-l", "--host", required=False, help="Proxy Host")
	parser.add_argument("-u", "--user", required=False, help="Proxy user")
	parser.add_argument("-p", "--password", required=False, help="Proxy password")
	parser.add_argument("-s", "--secure", required=False, help="Proxy protocol (HTTP/HTTPS)")
	parser.add_argument("-m", "--port", required=False, help="Proxy port")	
	
	
	try:
		args = parser.parse_args()

		spider = WebSpider(args.target,args.depth,args.host,args.user,args.password,args.port,args.secure)
		spider.crawl()
	except KeyboardInterrupt:
		sys.exit(0)
	except SystemExit:
		pass
	except:
		print "[-] Fatal Error captured..."
		print sys.exc_info()[0]
		print sys.exc_info()[1]
		print sys.exc_info()[2]
