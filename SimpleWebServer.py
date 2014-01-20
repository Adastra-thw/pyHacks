from twisted.web import server, resource
from twisted.internet import reactor

class SimpleResource(resource.Resource):
	def render_GET(self, request):
		return "<html><center><h1>I'm a twisted server!!</h1></center></html>"

root = resource.Resource()
root.putChild("simple", SimpleResource())
site = server.Site(root)
reactor.listenTCP(8080, site)
reactor.run()

