#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-02-23

from rank import BirdRank
from props import BirdProps
from match import BirdMatch
from account import BirdAccount
from activity import BirdActivity
from framework.util.tool import Tool
from framework.util.tool import Time
from framework.context import Context
from framework.entity.const import Message
from framework.entity.msgpack import MsgPack
from comm import BirdComm
from lemon.games.bird.newtask import NewTask


class BirdHttp(object):
    def __init__(self):
        self.json_path = {
            #'/v1/game/activity_list': self.get_activity_list,
            #'/v1/game/consume_activity': self.consume_activity,
            #'/v1/game/rank_list': self.get_rank_list,
            #'/v1/game/history': self.get_history,
            #'/v1/game/get_item_info': self.get_item_info,
            #'/v1/game/exchange': self.exchange,
            #'/v1/game/verify_session': self.verify_session,
        }
        self.three_json_path = {
            #'/v1/game/third/user/info': self.three_user_info,
            #'/v1/game/third/props/info': self.three_props_info,
            #'/v1/game/third/incr/chip': self.three_incr_chip,
            #'/v1/game/third/incr/props': self.three_incr_props,
            #'/v1/game/third/playing/lock': self.three_playing_lock,
            #'/v1/game/third/playing/unlock': self.three_playing_unlock,
            #'/v1/game/third/playing/query': self.three_playing_query,
        }

    def verify_session(self, uid, gid, mi, request):
        return MsgPack(0)

    def get_item_info(self, uid, gid, mi, request):
        chip = Context.UserAttr.get_chip(uid, gid, 0)
        diamond = Context.UserAttr.get_diamond(uid, gid, 0)
        coupon = Context.UserAttr.get_coupon(uid, gid, 0)
        return MsgPack(0, {'userId': uid, 'chip': chip, 'diamond': diamond, 'coupon': coupon})

    '''def exchange(self, uid, gid, mi, request):
        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')
        t = mi.get_param('type')
        num = mi.get_param('num')
        add_t = mi.get_param('add_type')
        add_num = mi.get_param('add_num')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')
        if type(num) is int:
            num *= -1
        else:
            return MsgPack.Error(0, 4, 'num error')

        if t == 1:
            real, final = Context.UserAttr.incr_chip(uid, gid, num, 'http.exchange')
            if num > 0:
                NewTask.get_chip_task(uid, num, 'http.exchange')
        elif t == 2:
            real, final = Context.UserAttr.incr_diamond(uid, gid, num, 'http.exchange')
            if num > 0:
                NewTask.get_diamond_task(uid, num, 'http.exchange')
        elif t == 3:
            real, final = Context.UserAttr.incr_coupon(uid, gid, num, 'http.exchange')
        else:
            return MsgPack.Error(0, 2, 'type error')
        if real != num:
            return MsgPack.Error(0, 3, 'not enough')

        if not add_t:
            return MsgPack(0, {'userId': uid})
        if BirdProps.check_props(add_t):
            BirdProps.incr_props(uid, gid, add_t, add_num, 'http.exchange')
        elif add_t == 1:
            real, final = Context.UserAttr.incr_chip(uid, gid, add_num, 'http.exchange')
            if add_num > 0:
                NewTask.get_chip_task(uid, add_num, 'http.exchange')
        elif add_t == 2:
            real, final = Context.UserAttr.incr_diamond(uid, gid, add_num, 'http.exchange')
            if add_num > 0:
                NewTask.get_diamond_task(uid, add_num, 'http.exchange')
        elif add_t == 3:
            real, final = Context.UserAttr.incr_coupon(uid, gid, add_num, 'http.exchange')
        else:
            return MsgPack.Error(0, 2, 'add type error')
        return MsgPack(0, {'userId': uid})
    '''
    def get_activity_list(self, uid, gid, mi, request):
        return BirdActivity.get_activity_list(uid, gid, mi)

    def consume_activity(self, uid, gid, mi, request):
        return BirdActivity.consume_activity(uid, gid, mi)

    def get_rank_list(self, uid, gid, mi, request):
        return BirdRank.get_ranks(uid, gid, mi)

    def get_history(self, uid, gid, mi, request):
        mo = MsgPack(Message.MSG_SYS_HISTORY | Message.ID_ACK)
        which = mi.get_param('which')
        if which == 'fame':
            _list = self.__get_history_fame_list(uid, gid)
            mo.set_param('fame', _list)
        elif which == 'honor':
            _list = self.__get_history_honor_list(uid, gid)
            mo.set_param('honor', _list)
        else:
            _list = self.__get_history_exchange_list(uid, gid)
            mo.set_param('exchange', _list)
        return mo

    def __get_history_fame_list(self, uid, gid):
        key = 'game.%d.fame.hall' % gid
        _list = Context.RedisMix.list_range(key, 0, -1)
        fame_hall = []
        for one in _list:
            one = Context.json_loads(one)
            fame_hall.append({
                'nick': one['nick'],
                'score': one['score'],
                'level': one['level'],
                'tm': BirdMatch.make_award_date_fmt(one['level'], one['ts'])
            })

        return fame_hall

    def __get_history_honor_list(self, uid, gid):
        key = 'history:%d:%d:award' % (gid, uid)
        kvs = Context.RedisCluster.hash_getall(uid, key)
        keys = sorted(kvs.keys())
        honor_list = []
        for aid in keys:
            one = Context.json_loads(kvs[aid])
            honor_list.append({
                'rank': one['rank'],
                'level': one['level'],
                'tm': BirdMatch.make_award_date_fmt(one['level'], one['ts']),
                'reward': BirdProps.convert_pid_count(one['reward'])
            })
        return honor_list

    def __get_history_exchange_list(self, uid, gid):
        _list = []
        all_history = Context.RedisCluster.hash_getall(uid, 'history:%d:%d' % (gid, uid))
        if all_history:
            keys = all_history.keys()
            values = Context.RedisMix.hash_mget('game.%d.exchange.record' % gid, *keys)
            for k, v in zip(keys, values):
                v = Context.json_loads(v)
                if v and v['type'] == 'exchange':
                    _r = {
                        'ts': v['ts'],
                        'desc': v['desc'],
                        'cost': v['cost'],
                        'state': int(all_history[k])
                    }
                    if 'phone' in v:
                        _r['phone'] = v['phone']
                    _list.append(_r)
        return _list

    def three_user_info(self, gid, mi, request):
        uid = mi.get_param('userId')
        nick = Context.Data.get_attr(uid, 'nick', '')
        chip, pay_total, vip_exp = Context.Data.get_game_attrs(uid, gid, ['chip', 'pay_total', 'vip_exp'])

        chip = Tool.to_int(chip, 0)
        pay_total = Tool.to_int(pay_total, 0)
        today_pay_total = Context.Daily.get_daily_data(uid, gid, 'pay_total')
        today_pay_total = Tool.to_int(today_pay_total, 0)
        param = {
            'nick': nick,
            'chip': chip,
            'pay_total': today_pay_total,
            'vip': BirdAccount.get_vip_level(uid, gid, pay_total+Tool.to_int(vip_exp, 0))
        }
        return MsgPack(0, param)

    def three_props_info(self, gid, mi, request):
        uid = mi.get_param('userId')
        pid = mi.get_param('pid')
        if isinstance(pid, int):
            pid = [pid]
        pid_list = BirdProps.get_props_list(uid, gid, pid)
        mo = MsgPack(0)
        if pid_list:
            mo.set_param('props', pid_list)
        return mo

    '''def three_incr_chip(self, gid, mi, request):
        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')

        delta = mi.get_param('delta')
        appId = mi.get_param('appId')
        real, final = Context.UserAttr.incr_chip(uid, gid, delta, 'game.' + str(appId))
        if delta > 0:
            NewTask.get_chip_task(uid, delta, 'game.' + str(appId))
        if real != delta:
            return MsgPack.Error(0, 2, 'no enough', chip=final)

        # 修改个人盈利
        if appId == 10004:
            barrel_level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level', 1)
            BirdComm.deal_chips(gid, uid, -delta, barrel_level)

        if final <= 0:
            mo = BirdAccount.check_bankrupt(uid, gid)
            Context.GData.send_to_connect(uid, mo)
        return MsgPack(0, {'chip': final})
        '''

    def three_incr_props(self, gid, mi, request):
        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')

        pid, delta = mi.get_param('delta')
        appId = mi.get_param('appId')

        real, final = BirdProps.incr_props(uid, gid, pid, delta, 'game.' + str(appId))
        if real != delta:
            return MsgPack.Error(0, 2, 'no enough', pid=pid, count=final)

        return MsgPack(0, {'props': [[pid, final]]})

    def three_playing_lock(self, gid, mi, request):
        uid = mi.get_param('userId')
        appId = mi.get_param('appId')
        time = mi.get_param('time')
        expire = Time.current_ts() + time
        lock = BirdAccount.check_global_lock(uid, appId)
        if lock:
            return MsgPack.Error(0, 1, 'in other game', gameId=lock['gid'])
        BirdAccount.global_lock(uid, appId, expire)
        return MsgPack(0)

    def three_playing_unlock(self, gid, mi, request):
        uid = mi.get_param('userId')
        appId = mi.get_param('appId')
        if BirdAccount.global_unlock(uid, appId):
            return MsgPack(0)
        return MsgPack.Error(1, 'in other game')

    def three_playing_query(self, gid, mi, request):
        uid = mi.get_param('userId')
        appId = mi.get_param('appId')
        lock = BirdAccount.check_global_lock(uid, appId)
        if lock:
            return MsgPack(0, {'gameId': lock['gid']})
        return MsgPack(0)


BirdHttp = BirdHttp()
