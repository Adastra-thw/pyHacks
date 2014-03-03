import socket
import socks
import urllib2
import mechanize

def connectTOR():
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
	socket.socket = socks.socksocket

if __name__ == "__main__":
	connectTOR()
	browser = mechanize.Browser()
	browser.open("http://www.google.com")
	try:
		for form in browser.forms():
			print "[*] Form Name %s " %(form.name)
			for control in form.controls:
				controlName = control.name
				controlValue = control.value
				controlType = control.type
				if controlValue == None:
					controlValue = ""
                                if controlName == None:
                                        controlName = ""
                                if controlType == None:
                                        controlType = ""
				print "[*][*] Control Name: %s " %(str(controlName))
                                print "[*][*] Control Type: %s " %(str(controlType))
                                print "[*][*] Control Value: %s " %(str(controlValue))


	except AttributeError:
		pass
