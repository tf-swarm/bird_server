#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-30

from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Tool
from framework.entity.const import Enum
from framework.entity.globals import Global


class Account(object):
    game_attrs = {
        'exp': 0
    }
    auto_issue_benefit = True

    @classmethod
    def get_user_info(cls, uid, gid):
        attrs = ['nick', 'sex', 'avatar']
        values = Context.Data.get_attrs(uid, attrs)
        for i in range(len(attrs)):
            if values[i] is None:
                return None
            elif attrs[i] == 'sex':
                values[i] = int(values[i])
            elif attrs[i] == 'avatar':
                values[i] = values[i]
        return dict(zip(attrs, values))

    @classmethod
    def get_game_info(cls, uid, gid):
        return cls.get_common_game_info(uid, gid)

    @classmethod
    def get_common_game_info(cls, uid, gid):
        chip = Context.UserAttr.get_chip(uid, gid)
        if chip is None:
            kvs = Context.copy_json_obj(cls.game_attrs)
            Context.Data.set_game_attrs_dict(uid, gid, kvs)
            startup_conf = Context.Configure.get_game_item_json(gid, 'game.startup')
            Context.UserAttr.incr_chip(uid, gid, startup_conf[0], 'game.startup')           # 角色初始鸟蛋
            Context.UserAttr.incr_limit_special_pay(uid, gid, 1)  # 设置一个默认值，避免后面的遍历查询
            Context.UserAttr.incr_coupon_private_pool(uid, gid, startup_conf[2], 'game.startup')  # 角色池中初始鸟券

            kvs['chip'] = startup_conf[0]
            is_new = True
        else:
            attrs = cls.game_attrs.keys()
            kvs = Context.copy_json_obj(cls.game_attrs)
            kvs.update(Context.Data.get_game_attrs_dict(uid, gid, attrs))
            for k, v in kvs.iteritems():
                kvs[k] = int(kvs[k])
            kvs['chip'] = chip
            is_new = False

            channel_id = Context.Data.get_attr(uid, 'channelid', '1001_0')
            pay_total = Context.Data.get_game_attr_int(uid, gid, 'pay_total', 0)
            key = 'user_daily:%s:%s:%s' % (channel_id, Time.current_time('%Y-%m-%d'), str(uid))
            cdkey_pay_total = Context.Data.get_game_attr_int(uid, gid, 'cdkey_pay_total', 0)
            Context.RedisStat.hash_set(key, 'his_pay_total', pay_total - cdkey_pay_total)  # 本日历史充值数据写入

        diamond = Context.UserAttr.get_diamond(uid, gid, 0)
        kvs['diamond'] = diamond
        coupon = Context.UserAttr.get_coupon(uid, gid, 0)
        kvs['coupon'] = coupon
        weapon_use_dict = Context.Data.get_game_attr_int(uid, gid, 'weapon_use_dict', 0)
        if weapon_use_dict != 0:
            kvs['weapon'] = weapon_use_dict
        else:
            kvs['weapon'] = 20000
            Context.Data.set_game_attr(uid, gid, 'weapon_use_dict', 20000)
        return is_new, kvs

    @classmethod
    def on_create_user(cls, uid, gid):
        Context.Daily.set_daily_data(uid, gid, 'new_user', 1)

    @classmethod
    def on_user_login(cls, uid, gid):
        channel = Context.Data.get_attr(uid, 'channelid', '1001_0')
        Context.Data.set_game_attr(uid, gid, 'session_login', Time.datetime_now())
        login = Context.Daily.incr_daily_data(uid, gid, 'login.times', 1)
        Context.Stat.incr_daily_user_data(channel, uid, 'login.times', 1)
        if login == 1:
            login_user_count = Context.Stat.incr_daily_data(channel, '%s.login.user.count' % channel, 1)
            if login_user_count <= 10:   # 多次测试
                in_chip, out_chip = Context.RedisMix.hash_mget('game.%d.info.hash' % gid, 'in.chip', 'out.chip')
                in_chip = Tool.to_int(in_chip, 0)
                out_chip = Tool.to_int(out_chip, 0)
                Context.Stat.setnx_daily_data(channel, 'carrying.volume.chip', in_chip - out_chip)

        Context.Log.report('user.login:', [uid, gid, login])
        return login

    @classmethod
    def check_forbidden(cls, uid, gid, token):
        Context.Log.info('gameId =', gid, 'userId =', uid, 'session =', token)
        if gid not in Context.GData.game_list:
            return 2, 'error gameId'
        if not token:
            return 1, 'error session'
        redis_session = Context.RedisCache.hash_get('token:%d' % uid, 'session')
        if redis_session != token:
            Context.Log.error('verify session failed', token, redis_session)
            return 1, 'error session'

        forbidden = Context.RedisMix.set_ismember('forbidden.user', uid)
        if forbidden:
            Context.Log.info('user is forbidden login', uid)
            return Enum.login_failed_forbidden, 'forbidden'

        disable = Context.RedisMix.set_ismember('game.%d.disable.user' % gid, uid)
        if disable:
            Context.Log.info('user is disable login', uid)
            return Enum.login_failed_forbidden, u'您的账号已被封停，如有疑问请联系客服'

        end_ts = Context.RedisMix.hash_get_int('game.%d.freeze.user' % gid, uid, 0)
        if end_ts:
            if end_ts > Time.current_ts():
                Context.Log.info('user is freeze login', uid)
                when = Time.timestamp_to_str(end_ts, '%Y-%m-%d %H:%M')
                return Enum.login_failed_freeze, u'您的账号已被冻结，%s解封，如有疑问请联系客服' % when
            else:
                Context.RedisMix.hash_del('game.%d.freeze.user' % gid, uid)
        return Enum.login_success, ''

    @classmethod
    def get_login_info(cls, uid, gid):
        now_day = Time.up_days()
        last_login, ns_login, np_login = Context.Data.get_game_attrs(uid, gid, ['lastlogin', 'nslogin', 'nplogin'])
        last_login = Tool.to_int(last_login, 0)
        ns_login = Tool.to_int(ns_login, 0)
        np_login = Tool.to_int(np_login, 0)
        return now_day, last_login, ns_login, np_login

    @classmethod
    def set_login_info(cls, uid, gid, last_login, ns_login, create_day = 8):
        Context.Data.set_game_attrs(uid, gid, ['lastlogin', 'nslogin'], [last_login, ns_login])
        if create_day <= 7:
            Context.Data.hincr_game(uid, gid, 'nplogin', 1)
        Context.Daily.set_daily_data(uid, gid, 'sign_in', 1)

    @classmethod
    def check_global_lock(cls, uid, gid):
        lock = Context.RedisCache.hash_get_json('global.playing.lock', uid)
        if lock and lock['gid'] != gid:
            now_ts = Time.current_ts()
            if now_ts < lock['ts']:
                game = Context.GData.game_desc.get(lock['gid'])
                if game:
                    lock['name'] = game['name']
                else:
                    lock['name'] = u'其他'
                return lock
            Context.RedisCache.hash_del('global.playing.lock', uid)
        return False

    @classmethod
    def global_lock(cls, uid, gid, expire_at):
        data = Context.json_dumps({'gid': gid, 'ts': expire_at})
        Context.RedisCache.hash_set('global.playing.lock', uid, data)

    @classmethod
    def global_unlock(cls, uid, gid):
        lock = Context.RedisCache.hash_get_json('global.playing.lock', uid)
        if lock and lock['gid'] != gid:
            now_ts = Time.current_ts()
            if now_ts < lock['ts']:
                return False

        Context.RedisCache.hash_del('global.playing.lock', uid)
        return True
