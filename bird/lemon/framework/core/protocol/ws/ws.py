#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-04-29

import struct
from framework.util.log import Logger
from framework.entity.manager import TaskManager
from framework.entity.msgpack import MsgPack
from framework.util.locker import Locker
from framework.util.tool import Time
from framework.context import Context
from framework.entity.const import Message
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol


class WSServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super(WSServerProtocol, self).__init__()
        self.heart_beat_count = 0
        self.access_ts = Time.current_ts()
        self.userId = 0
        self.gameId = 0
        self.session = None
        self.room = None
        self.locker = Locker()

    @property
    def peer_key(self):
        return 'CLIENT[%s]' % self.userId

    def onConnect(self, request):
        Logger.debug_network('Client connecting:', request.peer)

    def onOpen(self):
        Logger.debug_network('WebSocket connection open')

    def onMessage(self, payload, isBinary):
        if not isBinary:
            Logger.warn('only support binary msg')
            self.sendClose()
            return

        if len(payload) < 12:
            Logger.warn('msg len < 12')
            self.sendClose()
            return

        cmd, msg_len, _ = struct.unpack('III', payload[:12])
        if msg_len > len(payload) - 12:
            Logger.warn('msg_len error')
            self.sendClose()
            return

        body_data = payload[12:12 + msg_len]
        try:
            self.access_ts = Time.current_ts()
            tasklet = self.makeTasklet(cmd, body_data, self)
            TaskManager.add_task(tasklet.run, peer=self.peer_key, proto='WS')
        except Exception, e:
            Logger.exception(body_data)
            self.sendClose()

    def onClose(self, wasClean, code, reason):
        try:
            Logger.info('ConnectionLost', 'userId =', self.userId)
            if self.userId > 0:
                if self.userId in Context.GData.map_client_connect:
                    del Context.GData.map_client_connect[self.userId]
                msg = MsgPack(Message.MSG_INNER_BROKEN)
                msg.set_param('userId', self.userId)
                if self.gameId > 0:
                    msg.set_param('gameId', self.gameId)
                tasklet = self.makeTasklet(Message.MSG_INNER_BROKEN, msg, self)
                TaskManager.add_task(tasklet.run)
            else:
                Logger.debug_network('empty user connection lost ... ')
        except Exception, e:
            Logger.exception()

    def terminate_connection(self):
        if self.userId > 0:
            if self.userId in Context.GData.map_client_connect:
                del Context.GData.map_client_connect[self.userId]
            msg = MsgPack(Message.MSG_INNER_BROKEN)
            msg.set_param('userId', self.userId)
            if self.gameId > 0:
                msg.set_param('gameId', self.gameId)
            tasklet = self.makeTasklet(Message.MSG_INNER_BROKEN, msg, self)
            TaskManager.run_task(tasklet)
            self.logout()
        self.sendClose()

    def sendMsg(self, cmd, data):
        try:
            Logger.debug_network('==== SEND WS TO %s:' % self.peer_key, '%08X' % cmd, repr(data))
            if self.transport and self.connected:
                header = struct.pack('III', cmd, len(data), 0)
                WebSocketServerProtocol.sendMessage(self, header + data, True)
                return True
            else:
                Logger.error('==== ERROR: cannot connected !! protocol =', self, '%08X' % cmd, repr(data))
        except Exception, e:
            Logger.exception(data)

        return False

    def has_login(self):
        return self.userId > 0

    def login(self, uid, gid, session=None):
        self.userId = uid
        self.gameId = gid
        if session:
            self.session = session

    def logout(self):
        self.userId = 0
        self.gameId = 0
        self.room = None
        self.session = None

    def bind_game(self, gid, room):
        self.gameId = gid
        self.room = room

    def makeTasklet(self, cmd, raw, connection):
        raise NotImplementedError


class WSServerFactory(WebSocketServerFactory):
    protocol = WSServerProtocol
