#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-05-03

import struct
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import connectionDone

from framework.context import Context
from autobahn.twisted.websocket import WebSocketClientFactory
from autobahn.twisted.websocket import WebSocketClientProtocol


class WSClientProtocol(WebSocketClientProtocol):
    def onConnect(self, response):
        Context.Log.debug("Server connected: {0}".format(response.peer))

    def onOpen(self):
        Context.Log.debug("WebSocket connection open.")
        self.player.run()

    def onMessage(self, payload, isBinary):
        cmd, msg_len, _ = struct.unpack('III', payload[:12])
        if msg_len > len(payload) - 12:
            return
        body_data = payload[12:12 + msg_len]
        param = Context.json_loads(body_data)
        #Context.Log.debug("====%06d recv: 0x08%X %s" % (self.player.uid, cmd, body_data))
        self.player.on_msg(cmd, param)

    def onClose(self, wasClean, code, reason):
        self.factory.done(reason)

    def sendMsg(self, cmd, param):
        if self.transport and self.connected:
            body = Context.json_dumps(param)
            header = struct.pack('III', cmd, len(body), 0)
            try:
                WebSocketClientProtocol.sendMessage(self, header + body, True)
                #Context.Log.debug("====%06d send：0x08%X %s" % (self.player.uid, cmd, body))
                return True
            except Exception, e:
                Context.Log.exception()
                return False
        else:
            Context.Log.info('not connect, cannot send msg 0x%06x|%s' % (cmd, param))
            return False

    def stop(self):
        Context.Log.info('active close connect')
        self.sendClose()


class WSClientFactory(WebSocketClientFactory):
    protocol = WSClientProtocol

    def __init__(self, deferred, player):
        addr = 'ws://%s:%d' % (player.http.host, player.http.port)
        super(WSClientFactory, self).__init__(addr)
        self.deferred = deferred
        self.player = player

    def done(self, reason):
        if self.deferred:
            d, self.deferred = self.deferred, None
            d.callback(reason)

    def clientConnectionFailed(self, connector, reason):
        if self.deferred:
            d, self.deferred = self.deferred, None
            d.errback(reason)

    def buildProtocol(self, addr):
        p = WebSocketClientFactory.buildProtocol(self, addr)
        p.player = self.player
        self.player.protocol = p
        return p


class TcpClientProtocol(Protocol):
    def __init__(self):
        self._data = ''

    def dataReceived(self, data):
        self._data += data
        while len(self._data) > 12:
            cmd, msg_len, _ = struct.unpack('III', self._data[:12])
            if msg_len > len(self._data) - 12:
                return
            body_data = self._data[12:12 + msg_len]
            self._data = self._data[12 + msg_len:]
            param = Context.json_loads(body_data)
            Context.Log.debug("====%06d recv: 0x08%X %s" % (self.player.uid, cmd, body_data))
            self.player.on_msg(cmd, param)

    def sendMsg(self, cmd, param):
        if self.transport and self.connected:
            body = Context.json_dumps(param)
            header = struct.pack('III', cmd, len(body), 0)
            try:
                self.transport.write(header + body)
                Context.Log.debug("====%06d send：0x08%X %s" % (self.player.uid, cmd, body))
                return True
            except Exception, e:
                Context.Log.exception()
                return False
        else:
            Context.Log.info('not connect, cannot send msg 0x%06x|%s' % (cmd, param))
            return False

    def stop(self):
        Context.Log.info('active close connect')
        self.transport.loseConnection()

    def connectionMade(self):
        self._data = ''
        self.player.run()

    def connectionLost(self, reason=connectionDone):
        self.factory.done(reason)


class TcpClientFactory(ClientFactory):
    protocol = TcpClientProtocol

    def __init__(self, deferred, player):
        self.deferred = deferred
        self.player = player

    def done(self, reason):
        if self.deferred:
            d, self.deferred = self.deferred, None
            d.callback(reason)

    def clientConnectionFailed(self, connector, reason):
        if self.deferred:
            d, self.deferred = self.deferred, None
            d.errback(reason)

    def buildProtocol(self, addr):
        p = ClientFactory.buildProtocol(self, addr)
        p.player = self.player
        self.player.protocol = p
        return p
