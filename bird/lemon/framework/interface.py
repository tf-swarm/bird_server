#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-03-01

from framework.util.exceptions import NotInitException


class IContext(object):
    def __getattr__(self, item):
        if item == 'ctx':
            raise NotInitException('not init, please call init_ctx first')

    @classmethod
    def init_ctx(cls):
        from framework.context import Context
        cls.ctx = Context
        setattr(cls, 'init_ctx', None)


class ICallable(object):
    def __call__(self, *args, **kwargs):
        return self


class ILogic(object):
    def on_init(self):
        pass

    def on_join(self, uid):
        pass

    def on_sit_down(self, uid, sid):
        pass

    def on_ready(self, uid):
        pass

    def on_cancel_ready(self, uid):
        pass

    def on_stand_up(self, uid):
        pass

    def on_robot_join(self, uid, sid, level):
        pass

    def on_robot_leave(self, uid):
        pass

    def on_leave(self, uid):
        pass

    def on_force_quit(self, uid):
        pass

    def on_viewer_join(self, uid, sid):
        pass

    def on_viewer_leave(self, uid):
        pass

    def on_offline(self, uid):
        pass

    def on_reconnect(self, uid):
        pass

    def on_broadcast(self, uid, msg):
        pass

    def on_flush(self, uid, msg):
        pass

    def on_trustee(self, uid):
        pass

    def on_cancel_trustee(self, uid):
        pass

    def on_timeout(self, uid):
        pass

    def on_game_start(self):
        pass

    def on_client_message(self, uid, cmd, mi):
        pass

    def get_all_user(self):
        pass

    def get_game_info(self, uid):
        pass

    def get_user_info(self, uid):
        pass

    def get_table_info(self):
        pass

    def get_user_state(self, uid):
        pass
