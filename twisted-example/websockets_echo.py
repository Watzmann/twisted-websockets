import os

from twisted.internet.protocol import Factory
from twisted.internet import reactor

from twisted.protocols.wire import Echo

from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.web.websockets import WebSocketsResource


class EchoFactory(Factory):
    protocol = Echo


def main():
    resource = WebSocketsResource(EchoFactory())
    root = Resource()
    path = os.path.join(os.path.dirname(__file__), "websockets_echo.html")
    root.putChild("", File(path))
    root.putChild("ws", resource)

    reactor.listenTCP(8000, Site(root))
    reactor.run()

if __name__ == '__main__':
    main()
