import requesocks as requests

if __name__ == "__main__":
	session = requests.session()
	session.proxies = {'http': 'socks5://127.0.0.1:9150', 'https': 'socks5://127.0.0.1:9150'}
	r = session.get("http://www.google.com")
	print r.status_code
	for header in r.headers.keys():
		print header + " : " + r.headers[header]
