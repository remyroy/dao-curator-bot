import asyncio
import json

from autobahn.websocket.protocol import WebSocketProtocol
from autobahn.asyncio.websocket import WebSocketClientProtocol


class EtherscanClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        def ping():
            if self.state != WebSocketProtocol.STATE_OPEN:
                return
            msg = json.dumps({
                "event": "ping"
                }).encode('utf8')
            self.sendMessage(msg)
            self.factory.loop.call_later(20, ping)

        ping()

        msg = json.dumps({
            "event": "txlist",
            "address": self.factory.appconfig.CURATOR_ADDRESS
            }).encode('utf8')
        self.sendMessage(msg)

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
