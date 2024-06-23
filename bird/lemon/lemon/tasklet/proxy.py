#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-07-19

from framework.core.tasklet import server
from framework.entity.msgpack import MsgPack
from framework.entity.msgline import MsgLine
from framework.entity.const import Message
from framework.util.tool import Algorithm
from framework.context import Context


class ProxyTasklet(server.BasicServerTasklet):
    def onInnerMessage(self, cmd, mi, *args, **kwargs):
        gid = mi.get_gid()
        conn = Context.GData.map_three_server.get(gid)
        if conn:
            conn.sendMsg(cmd, self.raw)
        else:
            Context.Log.debug('no connect found')

    def onOuterMessage(self, cmd, raw, *args, **kwargs):
        if cmd == Message.MSG_INNER_SERVER_REGISTER | Message.ID_REQ:
            with self.connection.locker:
                self.on_server_register(cmd, raw)
                return True

        if self.connection.has_auth():
            return Context.GData.forward_to_system(cmd, self.raw)

        return False

    def on_server_heart_beat(self):
        pass

    def on_server_register(self, cmd, raw):
        mi = MsgLine.unpack(raw)
        req = mi.to_msgpack(cmd)
        ack = MsgPack(Message.MSG_INNER_SERVER_REGISTER | Message.ID_ACK)
        gid = req.get_param('gameId')
        if gid <= 10000:
            ack.set_error(1, 'error gameId')
            return Context.GData.send_to_three(ack, connection=self.connection)

        sign = req.get_param('sign')
        ts = req.get_param('ts')
        token = Context.Configure.get_game_item(gid, 'appKey')
        line = 'gameId=%d&token=%s&ts=%d' % (gid, token, ts)
        _sign = Algorithm.md5_encode(line)
        if sign != _sign:
            ack.set_error(2, 'error sign')
            return Context.GData.send_to_three(ack, connection=self.connection)

        self.connection.auth(gid)
        Context.GData.map_three_server[gid] = self.connection
        http_game = Context.Global.http_game()
        ack.set_param('http', http_game)
        return Context.GData.send_to_three(ack, connection=self.connection)
