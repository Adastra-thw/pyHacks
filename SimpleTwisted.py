from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

class SimpleProtocol(Protocol):
	def connectionMade(self):
		self.transport.write(self.factory.msg + '\r\n')
		self.transport.loseConnection()

class SimpleFactory(Factory):
	protocol = SimpleProtocol
	def recvMsg(self, msg):
		self.msg = msg

	def startFactory(self):
		print 'Start'

	def stopFactory(self):
		print 'Stop'
	
endpoint = TCP4ServerEndpoint(reactor, 2000)
factory = SimpleFactory()
factory.recvMsg('Hello')
endpoint.listen(factory)
reactor.run()
