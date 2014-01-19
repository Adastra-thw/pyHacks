#!/usr/bin/env python

import urllib
from bs4 import BeautifulSoup
import urllib2
from mechanize import Browser

url = "http://www.google.com"
#URLLIB PROXY SUPPORT.

#proxies = {'http': 'http://localhost:8008'}
#urlhandle = urllib.urlopen(url, proxies=proxies)
#print urlhandle.read()

#URLLIB2 PROXY SUPPORT AND THEN USING BEAUTIFULSOUP
proxy = urllib2.ProxyHandler( {'http': 'localhost:8008'} )
opener = urllib2.build_opener( proxy )
urllib2.install_opener( opener )
request = urllib2.Request( url )
response = urllib2.urlopen( request )
html = response.read()
soup = BeautifulSoup(html, "lxml")
div = soup.find_all( 'div', id="gs_lc0" )

#print div

#MECHANIZE PROXY SUPPORT.
br = Browser()
br.set_proxies({"http": "localhost:8008"})
response = br.open(url)

print response
