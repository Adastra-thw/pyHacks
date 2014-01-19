from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory

class SimpleClient(Protocol):
	def connectionMade(self):
		self.transport.write('Conexion Establecida!!')

	def dataReceived(self, data):
		print 'Server Said: ', data
		self.transport.loseConnection()

	def connectionLost(self, reason):
		print 'Connection Lost %s ' %(reason)

class SimpleClientFactory(ClientFactory):
	protocol = SimpleClient 

	def clientConnectionFailed(self, connector, reason):
		print 'Connection Failed!!'
		reactor.stop()
	
	def clientConnectionLost(self, connector, reason):
		print 'Connection Lost'
		reactor.stop()

reactor.connectTCP('localhost', 8000, SimpleClientFactory())
reactor.run()
