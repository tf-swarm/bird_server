#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-02-17

from framework.util.tool import Time
from framework.context import Context
from framework.entity.msgpack import MsgPack
from framework.entity.const import Message
from framework.util.exceptions import NotFoundException


class Activity(object):
    @classmethod
    def check_time(cls, activity):
        # 判断是否在时间设置范围内, 可以设置某个日期区间和小时区间
        start_ts = Time.str_to_timestamp(activity['start'])
        end_ts = Time.str_to_timestamp(activity['end'])
        now_ts = Time.current_ts()
        if start_ts < now_ts < end_ts:
            return 1

        if 'show' in activity:
            show_ts = Time.str_to_timestamp(activity['show'])
            if start_ts < now_ts < show_ts:
                return 2
        return 0

    def get_activity_list(self, uid, gid, mi):
        conf = Context.Configure.get_game_item_json(gid, 'activity.config')
        _list = []
        for act in conf['list']:
            state = self.check_time(act)
            if state == 0:
                continue

            handler = self.find_handler_by_type(gid, act['type'])
            if handler:
                item = handler.load_activity(uid, gid, act, state == 2)
                if item:
                    _list.append(item)
        mo = MsgPack(Message.MSG_SYS_ACTIVITY_LIST | Message.ID_REQ)
        mo.set_param('list', _list)
        return mo

    def consume_activity(self, uid, gid, mi):
        aid = mi.get_param('id')
        act = self.find_activity_by_id(gid, aid)
        if act:
            handler = self.find_handler_by_type(gid, act['type'])
            if handler:
                return handler.consume_activity(uid, gid, act, mi)
        raise NotFoundException('Not Found')

    def handle_activity(self, uid, gid, atype, *args, **kwargs):
        conf = Context.Configure.get_game_item_json(gid, 'activity.config')
        handler = self.find_handler_by_type(gid, atype)
        if handler:
            for act in conf['list']:
                if act['type'] == atype:
                    state = self.check_time(act)
                    if state == 1:
                        handler.handle_activity(uid, gid, act, *args, **kwargs)

    def find_activity_by_id(self, gid, aid):
        conf = Context.Configure.get_game_item_json(gid, 'activity.config')
        for act in conf['list']:
            if act['id'] == aid:
                return act

    def find_handler_by_type(self, gid, atype):
        return None
