#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-09-28

from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet import error
from proto import TcpClientFactory
from proto import WSClientFactory

from framework.context import Context
from framework.entity.const import Message
from framework.entity.const import Enum
from framework.entity.manager import TaskManager


class PlayerClient(object):
    gid = 0

    def __init__(self, http):
        self.http = http
        self.uid = http.userId
        self.roomType = None
        self.tableId = None
        self.seatId = None
        self.protocol = None

    def is_connected(self):
        return self.protocol.connected

    def close(self):
        self.protocol.stop()

    def run(self):
        if not self.req_user_info():
            self.close()

        if not self.req_game_info():
            self.close()

        if not self.req_room_list():
            self.close()

        if not self.req_server_info():
            self.close()

        if not self.req_bind_game():
            self.close()

    def on_msg(self, cmd, param):
        if 'error' in param:
            self.close()
            return
        if cmd == Message.MSG_SYS_USER_INFO | Message.ID_ACK:
            pass
        elif cmd == Message.MSG_SYS_GAME_INFO | Message.ID_ACK:
            pass
        elif cmd == Message.MSG_SYS_ROOM_LIST | Message.ID_ACK:
            pass
        elif cmd == Message.MSG_SYS_SERVER_INFO | Message.ID_ACK:
            self.req_quick_start()
        elif cmd == Message.MSG_SYS_QUICK_START | Message.ID_ACK:
            for k, v in param.iteritems():
                setattr(self, k, v)
            self.req_join_table()
        elif cmd == Message.MSG_SYS_JOIN_TABLE | Message.ID_ACK:
            self.req_sit_down()
        elif cmd == Message.MSG_SYS_SIT_DOWN | Message.ID_ACK:
            self.req_ready()
        elif cmd == Message.MSG_SYS_READY | Message.ID_ACK:
            pass
        elif cmd == Message.MSG_SYS_TABLE_EVENT | Message.ID_NTF:
            self.on_ntf_table_event(param)
        elif cmd == Message.MSG_SYS_FORCE_QUIT | Message.ID_ACK:
            self.close()

    def send_to_svrd(self, msg):
        return self.protocol.sendMsg(msg['cmd'], msg['param'])

    def req_hold(self, loop=False, gap=5):
        msg = {
            'cmd': Message.MSG_SYS_HOLD | Message.ID_REQ,
            'param': {}
        }
        if loop:
            TaskManager.add_delay_task(gap, self.req_hold, loop)
        return self.send_to_svrd(msg)

    def req_user_info(self):
        msg = {
            'cmd': Message.MSG_SYS_USER_INFO | Message.ID_REQ,
            'param': {
                'userId': int(self.http.userId),
                'gameId': self.gid,
                'session': self.http.session,
                'login': 1
            }
        }
        return self.send_to_svrd(msg)

    def req_game_info(self):
        msg = {
            'cmd': Message.MSG_SYS_GAME_INFO | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
            }
        }
        return self.send_to_svrd(msg)

    def req_room_list(self):
        msg = {
            'cmd': Message.MSG_SYS_ROOM_LIST | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
            }
        }
        return self.send_to_svrd(msg)

    def req_server_info(self):
        msg = {
            'cmd': Message.MSG_SYS_SERVER_INFO | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
            }
        }
        return self.send_to_svrd(msg)

    def req_led(self):
        msg = {
            'cmd': Message.MSG_SYS_LED | Message.ID_REQ,
            'param': {
                'userId': int(self.http.userId),
                'gameId': self.gid,
                'last_ts': 1443600377,
            }
        }
        return self.send_to_svrd(msg)

    def req_server_time(self):
        msg = {
            'cmd': Message.MSG_SYS_SERVER_TIME | Message.ID_REQ,
            'param': {
                'ts': 1448267793206
            }
        }
        return self.send_to_svrd(msg)

    def req_bind_game(self):
        msg = {
            'cmd': Message.MSG_SYS_BIND_GAME | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
            }
        }
        return self.send_to_svrd(msg)

    def req_quick_start(self):
        msg = {
            'cmd': Message.MSG_SYS_QUICK_START | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
            }
        }
        return self.send_to_svrd(msg)

    def req_join_table(self):
        msg = {
            'cmd': Message.MSG_SYS_JOIN_TABLE | Message.ID_REQ,
            'param': {
                'roomType': self.roomType,
                'tableId': self.tableId,
            }
        }
        return self.send_to_svrd(msg)

    def req_sit_down(self):
        msg = {
            'cmd': Message.MSG_SYS_SIT_DOWN | Message.ID_REQ,
            'param': {
                'seatId': self.seatId,
            }
        }
        return self.send_to_svrd(msg)

    def req_ready(self):
        msg = {
            'cmd': Message.MSG_SYS_READY | Message.ID_REQ,
            'param': {
            }
        }
        return self.send_to_svrd(msg)

    def req_trustee(self):
        msg = {
            'cmd': Message.MSG_SYS_TRUSTEE | Message.ID_REQ,
            'param': {
                'trustee': 1
            }
        }
        return self.send_to_svrd(msg)

    def req_force_quit(self):
        msg = {
            'cmd': Message.MSG_SYS_FORCE_QUIT | Message.ID_REQ,
            'param': {
            }
        }
        return self.send_to_svrd(msg)

    def req_leave_table(self):
        msg = {
            'cmd': Message.MSG_SYS_LEAVE_TABLE | Message.ID_REQ,
            'param': {
            }
        }
        return self.send_to_svrd(msg)

    def on_reconnect(self, param):
        self.close()

    def on_ntf_table_event(self, param):
        for event in param['event']:
            if event['type'] == Enum.table_event_login:
                pass
            elif event['type'] == Enum.table_event_join_table:
                pass
            elif event['type'] == Enum.table_event_sit_down:
                pass
            elif event['type'] == Enum.table_event_stand_up:
                pass
            elif event['type'] == Enum.table_event_ready:
                pass
            elif event['type'] == Enum.table_event_cancel_ready:
                pass
            elif event['type'] == Enum.table_event_leave_table:
                pass
            elif event['type'] == Enum.table_event_force_quit:
                pass
            elif event['type'] == Enum.table_event_viewer_join_table:
                pass
            elif event['type'] == Enum.table_event_viewer_leave_table:
                pass
            elif event['type'] == Enum.table_event_kick_off:
                pass
            elif event['type'] == Enum.table_event_offline:
                pass
            elif event['type'] == Enum.table_event_reconnect:
                pass
            elif event['type'] == Enum.table_event_game_start:
                Context.Log.info("game start")
            elif event['type'] == Enum.table_event_game_end:
                Context.Log.info("game end")
            elif event['type'] == Enum.table_event_game_info:
                pass
            elif event['type'] == Enum.table_event_user_info:
                pass
            elif event['type'] == Enum.table_event_table_info:
                pass
            elif event['type'] == Enum.table_event_broadcast:
                pass
            elif event['type'] == Enum.table_event_trustee:
                pass
            elif event['type'] == Enum.table_event_cancel_trustee:
                pass


def connect_lost(err):
    if not err or err.check(error.ConnectionDone):
        Context.Log.info('connect close gracefully')
    elif err.check(error.ConnectionLost):
        Context.Log.info('connect close unexpected')
    else:
        Context.Log.error(repr(err))


def run_as_tcp(http_args, player_client, tcp_args=None, sdk_client=None):
    return __run_as_client(http_args, player_client, tcp_args, sdk_client)


def run_as_websocket(sdk_args, player_client, player_args=None, sdk_client=None):
    return __run_as_client(sdk_args, player_client, player_args, sdk_client, websocket=True)


def __run_as_client(sdk_args, player_client, player_args=None, sdk_client=None, websocket=False):
    if sdk_client is None:
        from HttpSdk import HttpSdk
        sdk_client = HttpSdk
    if player_args is None:
        player_args = []
    print 12
    Context.init_with_redis_key(sdk_args[0])
    print 13
    Context.load_lua_script()
    print 14
    params = Context.Configure.get_global_item_json('params')
    print 15
    http_sdk = params['server']['http.sdk']
    print 16
    http = sdk_client(player_client.gid, http_sdk, *sdk_args[1:])
    print 17
    Context.Log.open_std_log()
    print 1
    http.run_as_player()
    print 2
    if not http.has_login:
        Context.Log.error('user login failed', sdk_args)
    else:
        player = player_client(http, *player_args)
        d = defer.Deferred()
        if websocket:
            factory = WSClientFactory(d, player)
        else:
            factory = TcpClientFactory(d, player)
        d.addBoth(connect_lost)
        reactor.connectTCP(http.host, int(http.port), factory)
        return d
