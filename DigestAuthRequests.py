import requests
from requests.auth import HTTPDigestAuth

users=['administrator', 'admin']
passwords=['administrator', 'admin123','admin']
protectedResource = 'http://localhost/digest-secured/'

foundPass = False
for user in users:
	if foundPass:
		break
	for passwd in passwords:
		res = requests.get(protectedResource)
		if res.status_code == 401:
			resDigest = requests.get(protectedResource, auth=HTTPDigestAuth(user, passwd))
			if resDigest.status_code == 200:
				print 'User Found...'
				print 'User: '+user+' Pass: '+passwd				
				foundPass = True

