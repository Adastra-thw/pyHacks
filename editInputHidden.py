#!/usr/bin/env python

import mechanize

br = mechanize.Browser()
br.set_handle_robots(False) # ignore robots. Avoid mechanize._response.httperror_seek_wrapper: HTTP Error 403: request disallowed by robots.txt
br.open("http://www.google.com")

for form in br.forms():
	form.find_control("hl").readonly = False
	br.select_form(nr=0)
	br.form["hl"] = "hhhhh"
	print form



