from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class NonAnonChat(LineReceiver):
	def __init__(self, protocols):
		self.users = {'john':'john', 'adastra':'adastra'}
		self.userName = None
		self.userLogged = False
		self.protocols = protocols

	def connectionMade(self):
		self.sendLine('Your Username: ')

	def connectionLost(self, reason):
		for protocol in self.protocols:
			if protocol != self:
				protocol.sendLine('Connection Lost: %s '%(reason))

	def lineReceived(self, line):
		if self.userName == None:
			if self.users.has_key(line):
				self.userName = line
				self.sendLine('Password: ')
			else:
				self.sendLine('Wrong Username')
		elif self.userLogged == False:
			if self.users[self.userName] == line:
				self.userLogged = True
				self.protocols.append(self)
			else:
				self.sendLine('Wrong Password')
		elif self.userLogged == True:
			for protocol in self.protocols:
				if protocol != self:
					protocol.sendLine('%s Said: %s ' %(self.userName, line))

class NonAnonFactory(Factory):
	def __init__(self):
		self.protocols = []

	def buildProtocol(self, addr):
		return NonAnonChat(self.protocols)

reactor.listenTCP(8000, NonAnonFactory())
reactor.run()

