from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
import time, sys

class IRCProtocol(irc.IRCClient):

    nickname = 'aaanotherOne'
    '''
    nickname	Nickname the client will use.
    password	Password used to log on to the server. May be None.
    realname	Supplied to the server during login as the "Real name" or "ircname". May be None.
    username	Supplied to the server during login as the "User name". May be None
    userinfo	Sent in reply to a USERINFO CTCP query. If None, no USERINFO reply will be sent. "This is used to transmit a string which is settable by the user (and never should be set by the client)."
    fingerReply	Sent in reply to a FINGER CTCP query. If None, no FINGER reply will be sent. (type: Callable or String )
    versionName	CTCP VERSION reply, client name. If None, no VERSION reply will be sent.
    versionNum	CTCP VERSION reply, client version,
    versionEnv	CTCP VERSION reply, environment the client is running in.
    sourceURL	CTCP SOURCE reply, a URL where the source code of this client may be found. If None, no SOURCE reply will be sent.
    lineRate	Minimum delay between lines sent to the server. If None, no delay will be imposed. (type: Number of Seconds. )
    '''
    def __init__(self, factory):
	self.factory = factory

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
	print "disconnected at %s" % time.asctime(time.localtime(time.time()))

    # Funciones de callback para eventos producidos en el servidor (Twisted es orientado a eventos!)
    def signedOn(self): #Logado en el servidor
        self.join(self.factory.channel)

    def joined(self, channel): #Cuando el usuario (programa) se une al canal
	print 'Joined to %s ' %(channel)

    def privmsg(self, user, channel, msg): # Mensaje privado
	print "%s sends a private message: %s " %(user, msg)

    def action(self, user, channel, msg): # Cuando cualquier usuario ejecuta una accion en el canal
	print "%s action %s: " %(user, msg)

    def userJoined(self, user, channel): # Cuando un usuario se une al canal.
        print "%s Joined! " %(user)

    def userQuit(self, user, quitMessage): # Cuando un usuario sale del canal.
	print '%s Quit... %s' %(user, quitMessage)

    def userRenamed(self, oldname, newname): #Cuando un usuario cambia su nickname.
	print 'Oldnick: %s Newnick: %s ' %(oldname, newname)


class IRCFactory(protocol.ClientFactory):
    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        p = IRCProtocol(self)
	return p

    def clientConnectionLost(self, connector, reason):
        """Reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

reactor.connectTCP("irc.freenode.net", 6667, IRCFactory('offsec'))
reactor.run()
