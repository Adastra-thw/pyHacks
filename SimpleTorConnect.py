import socks
import socket
import requests

def connectTor():
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
	socket.socket = socks.socksocket


if __name__ == "__main__":
	connectTor()
	r = requests.get("http://www.google.com")
	for header in r.headers.keys():
		print header + " : " + r.headers[header]
