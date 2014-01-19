#!/usr/bin/env python

import mechanize

br = mechanize.Browser()
br.open("http://www.google.com")

for form in br.forms():
	form.find_control("hl").readonly = False
	br.select_form(nr=0)
	br.form["hl"] = "hhhhh"
	print form



