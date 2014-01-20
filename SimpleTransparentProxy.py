from twisted.internet import reactor
from twisted.web import proxy, http

class ProxyRequest(proxy.ProxyRequest):
	def process(self):
		print 'Request from: %s ' %(self.getClientIP()) 
		print 'Headers : '
		for header in self.getAllHeaders().keys():
			print self.getAllHeaders()[header]

		try:
			proxy.ProxyRequest.process(self)
		except KeyError:
			print 'HTTPS is not supported.'

class SimpleProxy(proxy.Proxy):
	requestFactory = ProxyRequest

class ProxyFactory(http.HTTPFactory):
	def buildProtocol(self, addr):
		return SimpleProxy()

reactor.listenTCP(8080, ProxyFactory())
reactor.run()
