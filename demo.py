import sys
import os
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.web.static import File
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.web.websockets import WebSocketsProtocol, WebSocketsResource

class Echohandler(WebSocketsProtocol):
    def frameReceived(self, opcode, frame, fin):
        log.msg("Received frame '%s (%s|%s)'" % (frame, opcode, fin))
        self.sendFrame(opcode, frame + "\n", True)

class EchoFactory(Factory):
    protocol = Echohandler

def main():
    log.startLogging(sys.stdout)
    resource = WebSocketsResource(EchoFactory())
    root = Resource()
    path = os.path.join(os.path.dirname(__file__), "index.html")
    root.putChild("", File(path))
    root.putChild("ws", resource)

    reactor.listenTCP(8000, Site(root))
    reactor.run()


if __name__ == "__main__":
    main()
