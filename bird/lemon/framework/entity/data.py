#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2014-10-14

from framework.util.tool import Tool, Time
from framework.interface import IContext
from framework.interface import ICallable
from userattr import SdkeyEvent


class Data(IContext, ICallable):

    def __init__(self):
        pass

    # 通用的update和select（尽量少用）--------------------------------------
    def set_attr_common(self, uid, table, attr, value):
        return self.ctx.RedisCluster.hash_set(uid, table, attr, value)

    def get_attr_common(self, uid, table, attr, default = None):
        return self.ctx.RedisCluster.hash_get(uid, table, attr, default)
    # ------------------------------------------------------------------

    # user attr
    def exists_attr(self, uid, attr):
        return self.ctx.RedisCluster.hash_exists(uid, 'user:%d' % uid, attr)

    def get_attr(self, uid, attr, default=None):
        return self.ctx.RedisCluster.hash_get(uid, 'user:%d' % uid, attr, default)

    def get_attr_int(self, uid, attr, default=None):
        return self.ctx.RedisCluster.hash_get_int(uid, 'user:%d' % uid, attr, default)

    def get_attr_json(self, uid, attr, default=None):
        return self.ctx.RedisCluster.hash_get_json(uid, 'user:%d' % uid, attr, default)

    def set_attr(self, uid, attr, value):
        return self.ctx.RedisCluster.hash_set(uid, 'user:%d' % uid, attr, value)

    def setnx_attr(self, uid, attr, value):
        return self.ctx.RedisCluster.hash_setnx(uid, 'user:%d' % uid, attr, value)

    def get_attrs(self, uid, attrs):
        return self.ctx.RedisCluster.hash_mget(uid, 'user:%d' % uid, *attrs)

    def get_attrs_dict(self, uid, attrs):
        return self.ctx.RedisCluster.hash_mget_as_dict(uid, 'user:%d' % uid, *attrs)

    def get_all(self, uid):
        return self.ctx.RedisCluster.hash_getall(uid, 'user:%d' % uid)

    def set_attrs(self, uid, attrs, values):
        l = Tool.make_list(attrs, values)
        return self.ctx.RedisCluster.hash_mset(uid, 'user:%d' % uid, *l)

    def set_attrs_dict(self, uid, kvs):
        return self.ctx.RedisCluster.hash_mset(uid, 'user:%d' % uid, **kvs)

    def del_attrs(self, uid, *attrs):
        return self.ctx.RedisCluster.hash_del(uid, 'user:%d' % uid, *attrs)

    # game attr
    def get_game_attr(self, uid, gid, attr, default=None):
        return self.ctx.RedisCluster.hash_get(uid, 'game:%d:%d' % (gid, uid), attr, default)

    def get_game_attr_int(self, uid, gid, attr, default=None):
        return self.ctx.RedisCluster.hash_get_int(uid, 'game:%d:%d' % (gid, uid), attr, default)

    def get_game_attr_json(self, uid, gid, attr, default=None):
        return self.ctx.RedisCluster.hash_get_json(uid, 'game:%d:%d' % (gid, uid), attr, default)

    def set_game_attr(self, uid, gid, attr, value):
        return self.ctx.RedisCluster.hash_set(uid, 'game:%d:%d' % (gid, uid), attr, value)

    def setnx_game_attr(self, uid, gid, attr, value):
        return self.ctx.RedisCluster.hash_setnx(uid, 'game:%d:%d' % (gid, uid), attr, value)

    def get_game_attrs(self, uid, gid, attrs):
        return self.ctx.RedisCluster.hash_mget(uid, 'game:%d:%d' % (gid, uid), *attrs)

    def get_game_attrs_dict(self, uid, gid, attrs):
        return self.ctx.RedisCluster.hash_mget_as_dict(uid, 'game:%d:%d' % (gid, uid), *attrs)

    def get_game_all(self, uid, gid):
        return self.ctx.RedisCluster.hash_getall(uid, 'game:%d:%d' % (gid, uid))

    def set_game_attrs(self, uid, gid, attrs, values):
        l = Tool.make_list(attrs, values)
        return self.ctx.RedisCluster.hash_mset(uid, 'game:%d:%d' % (gid, uid), *l)

    def set_game_attrs_dict(self, uid, gid, kvs):
        return self.ctx.RedisCluster.hash_mset(uid, 'game:%d:%d' % (gid, uid), **kvs)

    def hincr_game(self, uid, gid, attr, delta):
        return self.ctx.RedisCluster.hash_incrby(uid, 'game:%d:%d' % (gid, uid), attr, delta)

    def hmincr_game(self, uid, gid, *args, **kwargs):
        return self.ctx.RedisCluster.hash_mincrby(uid, 'game:%d:%d' % (gid, uid), *args, **kwargs)

    def del_game_attrs(self, uid, gid, *attrs):
        return self.ctx.RedisCluster.hash_del(uid, 'game:%d:%d' % (gid, uid), *attrs)

    # shop attr
    # table = 'shop:exchange' 兑换记录
    # table = 'shop:time:10001' 限时商城个人兑换数量
    # table = 'shop:day:10001' 日限制的个人兑换数量
    # table = 'shop:week:10001' 周限制的个人兑换数量
    # table = 'shop:month:10001' 月限制的个人兑换数量
    # table = 'shop:time:10002' 限时商城服务器兑换数量
    # table = 'shop:day:10002' 日限制的服务器兑换数量
    # table = 'shop:week:10002' 周限制的服务器兑换数量
    # table = 'shop:month:10002' 月限制的服务器兑换数量
    def set_shop_attr(self, uid, table, attr, value):
        return self.ctx.RedisCluster.hash_set(uid, table+':'+str(uid), attr, value)

    def set_shop_attrs_dict(self, uid, table, kvs):
        return self.ctx.RedisCluster.hash_mset(uid, table+':'+str(uid), **kvs)

    def get_shop_attr(self, uid, table, attr, default = None):
        return self.ctx.RedisCluster.hash_get(uid, table+':'+str(uid), attr, default)

    def get_shop_all(self, uid, table):
        return self.ctx.RedisCluster.hash_getall(uid, table+':'+str(uid))

    def del_shop_attrs(self, uid, table, *attrs):
        return self.ctx.RedisCluster.hash_del(uid, table+':'+str(uid), *attrs)

    def get_shop_attr_json(self, uid, table, attr, default=None):
        return self.ctx.RedisCluster.hash_get_json(uid, table+':'+str(uid), attr, default)

    #rank
    def get_rank_all(self, uid, gid):
        return self.ctx.RedisCluster.hash_getall(uid, 'rank:%d:%d' % (gid, uid))

    def del_rank_attrs(self, uid, gid, *attrs):
        return self.ctx.RedisCluster.hash_del(uid, 'rank:%d:%d' % (gid, uid), *attrs)

    def get_rank_attr_int(self, uid, gid, attr, default=None):
        return self.ctx.RedisCluster.hash_get_int(uid, 'rank:%d:%d' % (gid, uid), attr, default)

    def get_rank_attr(self, uid, gid, attr, default=None):
        return self.ctx.RedisCluster.hash_get(uid, 'rank:%d:%d' % (gid, uid), attr, default)

    def set_rank_attr(self, uid, gid, attr, value):
        return self.ctx.RedisCluster.hash_set(uid, 'rank:%d:%d' % (gid, uid), attr, value)

    # 排行榜数据更新
    def hincr_rank(self, room, gid, attr, delta):
        if room == 100:
            uid = 1000
        elif room == 101:
            uid = 1001
        elif room == 201:
            uid = 1002
        elif room == 202:
            uid = 1003
        elif room == 203:
            uid = 1004
        else:
            return
        return self.ctx.RedisCluster.hash_incrby(uid, 'rank:%d:%d' % (gid, uid), attr, delta)

    def hincr_world_rank(self, uid, gid, attr, delta):
        return self.ctx.RedisCluster.hash_incrby(uid, 'rank:%d:%d' % (gid, uid), attr, delta)

    # cdkey
    def set_cdkey_attr(self, uid, attr, value):
        return self.ctx.RedisCluster.hash_set(uid, 'cdkey:exchange:%s' % (uid), attr, value)

    def get_cdkey_attr(self, uid, attr, default=None):
        return self.ctx.RedisCluster.hash_get(uid, 'cdkey:exchange:%s' % (uid), attr, default)

    def del_cdkey_attrs(self, uid, userid, event, *attrs):
        if event == 'exchange' and userid != -1:
            k,v = SdkeyEvent.get_sdkey_event_dict(attrs[0], event)
            SdkeyEvent.add_event(userid, k, v)
        return self.ctx.RedisCluster.hash_del(uid, 'cdkey:exchange:%s' % (uid), *attrs)

    def get_cdkey_all(self, uid):
        return self.ctx.RedisCluster.hash_getall(uid, 'cdkey:exchange:%d' % uid)

    def get_coupon_event_all(self, uid):
        return self.ctx.RedisCluster.hash_getall(uid, 'event:coupon:%d' % uid)

    def set_timer_attr(self, uid, gid, attr, value):
        return self.ctx.RedisCluster.hash_set(uid, 'timer:%d:%d' % (gid, uid), attr, value)

    def get_timer_attr(self, uid, gid, attr, default = None):
        return self.ctx.RedisCluster.hash_get(uid, 'timer:%d:%d' % (gid, uid), attr, default)

    def del_timer_attr(self, uid, gid, *attr):
        return self.ctx.RedisCluster.hash_del(uid, 'timer:%d:%d' % (gid, uid), *attr)

    def get_timer_all(self, uid, gid):
        return self.ctx.RedisCluster.hash_getall(uid, 'timer:%d:%d' % (gid, uid))

    def get_task_all(self, uid, gid):
        return self.ctx.RedisCluster.hash_getall(uid, 'task:%s:%d' % (gid, uid))

    def get_task_attr(self, uid, gid, attr, default=None):
        return self.ctx.RedisCluster.hash_get(uid, 'task:%s:%d' % (gid, uid), attr, default)

    def get_task_attr_json(self, uid, gid, attr, default=None):
        return self.ctx.RedisCluster.hash_get_json(uid, 'task:%s:%d' % (gid, uid), attr, default)

    def set_task_attr(self, uid, gid, attr, value):
        return self.ctx.RedisCluster.hash_set(uid, 'task:%s:%d' % (gid, uid), attr, value)

    def set_task_attr_dict(self, uid, gid, kvs):
        return self.ctx.RedisCluster.hash_mset(uid, 'task:%s:%d' % (gid, uid), **kvs)

    def del_task_attr(self, uid, gid, *attr):
        return self.ctx.RedisCluster.hash_del(uid, 'task:%s:%d' % (gid, uid), *attr)

    def hincr_task_attr(self, uid, gid, attr, delta):
        return self.ctx.RedisCluster.hash_incrby(uid, 'task:%s:%d' % (gid, uid), attr, delta)

    # red_packet
    def get_red_packet_all(self, uid, table, now):
        return self.ctx.RedisCluster.hash_getall(uid, table + ':' + str(now))

    def del_red_packet_attrs(self, uid, table, now, *attrs):
        return self.ctx.RedisCluster.hash_del(uid, table + ':' + str(now), *attrs)

    def set_red_packet_attr(self, uid, table, now, attr, value):
        return self.ctx.RedisCluster.hash_set(uid, table + ':' + str(now), attr, value)

    def set_red_packet_attrs(self, uid, table, now, attrs, values):
        l = Tool.make_list(attrs, values)
        return self.ctx.RedisCluster.hash_mset(uid, table + ':' + str(now), *l)

    def hincr_red_packet(self, uid,  table, now, attr, delta):
        return self.ctx.RedisCluster.hash_incrby(uid, table+':'+str(now), attr, delta)

    def get_red_packet_attr(self, uid, table, now, attr, default=None):
        return self.ctx.RedisCluster.hash_get(uid, table+':'+str(now), attr, default)

    def get_red_packet_attrs(self, uid, table, now, attrs):
        return self.ctx.RedisCluster.hash_mget(uid, table + ':' + str(now), *attrs)

    def set_red_packet_dict(self, uid, table, now, kvs):
        return self.ctx.RedisCluster.hash_mset(uid, table + ':' + str(now), **kvs)

    def get_red_packet_attr_json(self, uid, table, now, attr, default=None):
        return self.ctx.RedisCluster.hash_get_json(uid, table+':'+str(now), attr, default)

    #props
    def hincr_props(self, uid, gid, attr, delta):
        return self.ctx.RedisCluster.hash_incrby(uid, 'props:%d:%d' % (gid, uid), attr, delta)

    # 获取一个玩家是否是新手玩家（创建账号前7天属于新手玩家）
    def get_uid_is_new_player(self, uid):
        create_time = self.ctx.Data.get_attr(uid, 'createTime')
        create_time = Time.str_to_timestamp(create_time[:10], '%Y-%m-%d')
        create_time += (24*3600*3)
        if Time.current_ts() < create_time:
            return True
        return False

    def get_uid_create_day(self, uid):
        create_time = self.ctx.Data.get_attr(uid, 'createTime')
        create_time = Time.str_to_timestamp(create_time[:10], '%Y-%m-%d')
        current_ts = Time.current_ts()
        day = (current_ts-create_time)/(24*3600)
        return day + 1

    def get_uid_create(self, uid):
        create_time = self.ctx.Data.get_attr(uid, 'createTime')
        ct = Time.str_to_timestamp(create_time[:10], '%Y-%m-%d')
        cl = Time.current_localtime(ct)
        import datetime
        create = Time.up_days(datetime.date(cl.tm_year, cl.tm_mon, cl.tm_mday))
        return create

    def is_new_player(self, uid, gid):
        pay_total = self.get_game_attr_int(uid, gid, 'pay_total', 0)
        if pay_total >= 200:
            return False
        if not self.get_uid_is_new_player(uid):
            return False
        return True

    # 处理玩家的cycle水池时间
    def hincr_pool_cycle(self, uid, key, event, delta):
        final = self.ctx.RedisMix.hash_incrby('game.2.share', key, delta)
        d = {'uid': uid, 'key': key, 'event': event, 'delta': delta, 'final': final}
        self.set_attr_common(uid, 'event:%s:%d' % ('pool_cycle', uid), Time.current_ms(),
                                     self.ctx.json_dumps(d))
        return final
Data = Data()
