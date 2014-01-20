from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor

resource = File('/opt/WebServerApacheFull/httpd-2.2.22/htdocs/')
factory = Site(resource)
reactor.listenTCP(8080, factory)
reactor.run()
