#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-29

from framework.interface import IContext
from framework.interface import ICallable
from framework.entity.const import Const
import time


class UserAttr(IContext, ICallable):
    def incr_attr(self, uid, gid, field, delta, event, low=-1, high=-1, mode=Const.chip_operate_noop, **kwargs):
        """
        对用户的%(attr)进行操作
        @param uid: userId
        @param gid: 游戏ID
        @param field: 属性字段
        @param delta: 变化的值可以是负数
        @param low: 用户最低%(attr)数，-1表示没有最低限制
        @param high: 用户最高%(attr)数，-1表示没有最高限制
        @param mode: 当INCR动作会变成负数时的处理模式, 0表示不进行操作; 1会给%(attr)清零
        @param event: 触发INCR的事件ID
        @param kwargs: 需要根据事件传入附加参数
        @return (real, final) real表示实际变化的值, final表示变化后的最终数量
        """
        assert isinstance(uid, int)
        assert isinstance(gid, int)
        assert isinstance(field, (str, unicode))
        assert isinstance(delta, int)
        assert isinstance(low, int)
        assert isinstance(high, int)
        assert mode in (Const.chip_operate_noop, Const.chip_operate_zero)
        assert isinstance(event, (str, unicode))
        alias = 'incr_attr'
        key = 'game:%d:%d' % (gid, uid)
        real, final, fixed = self.ctx.RedisCluster.execute_lua_alias(uid, alias, delta, low, high, mode, key, field)
        if fixed:
            self.ctx.Log.report('%s.fixed:' % field, [uid, gid, int(fixed), 0, event, kwargs])
            channel_id = self.ctx.Data.get_attr(uid, 'channelid', '1001_0')
            self.ctx.Stat.incr_daily_data(channel_id, 'in.%s.fixed' % field, fixed)
            self.ctx.Stat.incr_daily_user_data(channel_id, uid, 'in.%s.fixed' % field, fixed)
            self.ctx.RedisMix.hash_incrby('game.%d.info.hash' % gid, 'in.%s.fixed' % field, fixed)

        if real or delta == 0:
            self.ctx.Log.report('%s.update:' % field, [uid, gid, int(real), int(final), event, kwargs])
            if real != 0:
                if real > 0:
                    in_or_out = 'in'
                else:
                    in_or_out = 'out'

                if 'roomtype' in kwargs:
                    _field = '%s.%s.%s.%d' % (in_or_out, field, event, kwargs['roomtype'])
                else:
                    _field = '%s.%s.%s' % (in_or_out, field, event)

                channel_id = self.ctx.Data.get_attr(uid, 'channelid', '1001_0')
                if real > 0:
                    self.ctx.Stat.incr_daily_data(channel_id, _field, real)
                    self.ctx.Stat.incr_daily_user_data(channel_id, uid, _field, real)
                    self.ctx.Stat.incr_user_data(uid, gid, _field, real)
                    self.ctx.RedisMix.hash_incrby('game.%d.info.hash' % gid, '%s.%s' % (in_or_out, field), real)
                else:
                    self.ctx.Stat.incr_daily_data(channel_id, _field, -real)
                    self.ctx.Stat.incr_daily_user_data(channel_id, uid, _field, -real)
                    self.ctx.Stat.incr_user_data(uid, gid, _field, -real)
                    self.ctx.RedisMix.hash_incrby('game.%d.info.hash' % gid, '%s.%s' % (in_or_out, field), -real)

        return real, final

    def incr_chip(self, uid, gid, delta, event, low=-1, high=-1, mode=Const.chip_operate_noop, **kwargs):
        return self.incr_attr(uid, gid, 'chip', delta, event, low, high, mode, **kwargs)

    def incr_play_shot_gift_chip(self, uid, gid, delta, gift_chip_pool_id, event, low=-1, high=-1, mode=Const.chip_operate_noop, **kwargs):
        key = 'play_shot_gift_chip.%d' % gift_chip_pool_id
        return self.incr_attr(uid, gid, key, delta, event, low, high, mode, **kwargs)

    def get_play_shot_gift_chip(self, uid, gid, gift_chip_pool_id, default=0):
        key = 'play_shot_gift_chip.%d' % gift_chip_pool_id
        return self.ctx.Data.get_game_attr_int(uid, gid, key, default)

    # 鸟券掉落累积进度
    def get_fall_coupon_total_cost(self, uid, gid, default=None):
        return self.ctx.Data.get_game_attr(uid, gid, 'fall_coupon_total_cost', default)

    def set_fall_coupon_total_cost(self, uid, gid, delta, event):
        return self.ctx.Data.set_game_attr(uid, gid, 'fall_coupon_total_cost', delta)

    # 子弹触发赠分进度
    def get_play_shot_gift_progress(self, uid, gid, barrel_multiple, default=None):
        key = 'play_shot_gift_total.%d' % barrel_multiple
        return self.ctx.Data.get_game_attr(uid, gid, key, default)

    def incr_play_shot_gift_progress(self, uid, gid, barrel_multiple, delta, event):
        key = 'play_shot_gift_total.%d' % barrel_multiple
        return self.ctx.Data.hincr_game(uid, gid, key, delta)

    # 玩家限时商城特殊充值额度
    def get_limit_special_pay(self, uid, gid, default=None):
        key = 'limit_special_pay_total'
        return self.ctx.Data.get_game_attr(uid, gid, key, default)

    def incr_limit_special_pay(self, uid, gid, value):
        key = 'limit_special_pay_total'
        return self.ctx.Data.hincr_game(uid, gid, key, value)

    # 玩家炮倍池状态
    def get_barrel_pool_chip_state(self, uid, gid, pool_id):
        key_pool_chip = 'state_barrel_pool_chip' + str(pool_id)
        key_state_time = 'state_barrel_pool_time' + str(pool_id)
        key_state_end_time = 'state_barrel_pool_end_time' + str(pool_id)
        pool_chip = self.ctx.Data.get_game_attr_int(uid, gid, key_pool_chip, 0)     # 炮倍池时间
        state_time = self.ctx.Data.get_game_attr_int(uid, gid, key_state_time, 0)   # 该状态持续时间
        state_end_time = self.ctx.Data.get_game_attr_int(uid, gid, key_state_end_time, 0)  # 状态结束时间
        return pool_chip, state_time, state_end_time

    def set_barrel_pool_chip_state(self, uid, gid, pool_id, pool_chip, state_time, state_end_time):
        key_pool_chip = 'state_barrel_pool_chip' + str(pool_id)
        key_state_time = 'state_barrel_pool_time' + str(pool_id)
        key_state_end_time = 'state_barrel_pool_end_time' + str(pool_id)
        self.ctx.Data.set_game_attr(uid, gid, key_pool_chip, pool_chip)  # 炮倍池时间
        self.ctx.Data.set_game_attr(uid, gid, key_state_time, state_time)  # 该状态持续时间
        self.ctx.Data.set_game_attr(uid, gid, key_state_end_time, state_end_time)  # 状态结束时间

    # 获取用户是否支付用户标签
    def get_user_pay_flag(self, uid, gid):
        key = 'user_pay_flag'
        key_end_time = 'pay_flag_end_time'
        is_pay_user = self.ctx.Data.get_game_attr_int(uid, gid, key, 0)  # 是否支付用户
        state_end_time = self.ctx.Data.get_game_attr_int(uid, gid, key_end_time, 0)  # 状态结束时间
        return is_pay_user, state_end_time

    def set_user_pay_flag(self, uid, gid, is_pay_user, state_end_time):
        key = 'user_pay_flag'
        key_end_time = 'pay_flag_end_time'
        self.ctx.Data.set_game_attr(uid, gid, key, is_pay_user)  # 设置支付用户标签
        self.ctx.Data.set_game_attr(uid, gid, key_end_time, state_end_time)  # 状态结束时间

    # -------------Start min_cost_percent_flag--------------
    def get_user_min_cost_percent_flag(self, uid, gid):
        key = 'user_min_cost_percent'
        min_percnet = self.ctx.Data.get_game_attr(uid, gid, key, 0)  # 最小消耗百分比
        return float(min_percnet)

    def set_user_min_cost_percent_flag(self, uid, gid, min_percnet):
        key = 'user_min_cost_percent'
        fValue = float(min_percnet)
        self.ctx.Data.set_game_attr(uid, gid, key, fValue)  # 设置最小消耗百分比

    # -------------End--------------

    #def get_recharge_gift_times(self, uid, gid, default=None):
     #   return self.ctx.Data.get_game_attr_int(uid, gid, 'recharge_gift_times', default)

    #def incr_recharge_gift_times(self, uid, gid, delta, event, low=-1, high=-1, mode=Const.chip_operate_noop, **kwargs):
    #    return self.incr_attr(uid, gid, 'recharge_gift_times', delta, event, low, high, mode, **kwargs)

    def get_chip(self, uid, gid, default=None):
        return self.ctx.Data.get_game_attr_int(uid, gid, 'chip', default)

    def incr_diamond(self, uid, gid, delta, event, low=-1, high=-1, mode=Const.chip_operate_noop, **kwargs):
        return self.incr_attr(uid, gid, 'diamond', delta, event, low, high, mode, **kwargs)

    def get_diamond(self, uid, gid, default=None):
        return self.ctx.Data.get_game_attr_int(uid, gid, 'diamond', default)

    def incr_coupon(self, uid, gid, delta, event, low=-1, high=-1, mode=Const.chip_operate_noop, **kwargs):
        real, final = self.incr_attr(uid, gid, 'coupon', delta, event, low, high, mode, **kwargs)
        # 如果计数不计入总数且不加入事件中，不能调用此函数
        if real == delta:
            if delta > 0:
                self.ctx.Data.hincr_game(uid, gid, 'coupon_fall', delta)    # 用户记录掉落鸟券数
            # k, v = CouponEvent.get_coupon_event_dict(uid, gid, delta, event)        # 鸟券事件处理
            # CouponEvent.add_event(uid, k, v)
        return real, final

    def get_coupon(self, uid, gid, default=None):
        return self.ctx.Data.get_game_attr_int(uid, gid, 'coupon', default)

    def get_coupon_fall(self, uid, gid, default=0):
        return self.ctx.Data.get_game_attr_int(uid, gid, 'coupon_fall', default)

    # --------------- 支付击杀加成机制
    def incr_pool_pay_kill_add(self, uid, pool_id, value):
        return self.ctx.Data.hincr_game(uid, 2, 'pay_kill_add_value.%d' % pool_id, value)

    def get_pool_pay_kill_add(self, uid, pool_id, default):
        return self.ctx.Data.get_game_attr_int(uid, 2, 'pay_kill_add_value.%d' % pool_id, default)

    def set_pool_pay_kill_add(self, uid, pool_id, value):
        return self.ctx.Data.set_game_attr(uid, 2, 'pay_kill_add_value.%d' % pool_id, value)

    def incr_pool_pay_kill_add_cost(self, uid, pool_id, value):
        return self.ctx.Data.hincr_game(uid, 2, 'pay_kill_add_cost.%d' % pool_id, value)

    def get_pool_pay_kill_add_cost(self, uid, pool_id, default):
        return self.ctx.Data.get_game_attr_int(uid, 2, 'pay_kill_add_cost.%d' % pool_id, default)

    def set_pool_pay_kill_add_cost(self, uid, pool_id, value):
        return self.ctx.Data.set_game_attr(uid, 2, 'pay_kill_add_cost.%d' % pool_id, value)

    def set_pay_kill_add_percent(self, uid, value):
        return self.ctx.Data.set_game_attr(uid, 2, 'pay_kill_add_percent', value)

    def get_pay_kill_add_percent(self, uid, default):
        return self.ctx.Data.get_game_attr(uid, 2, 'pay_kill_add_percent', default)

    # --------------- 支付击杀加成机制 end

    # --针对送分 开始
    # 针对玩家当前送分额度
    def get_give_chip(self, uid, gid, default=None):
        return self.ctx.Data.get_game_attr_int(uid, gid, 'give_chip', default)

    # 送分额度增减
    def incr_give_chip(self, uid, gid, delta, event, low=-1, high=-1, mode=Const.chip_operate_noop, **kwargs):
        return self.incr_attr(uid, gid, 'give_chip', delta, event, low, high, mode, **kwargs)

    # 送分触发比例  rate_arr=[10, 1]  10触发1
    def set_give_chip_rate(self, uid, gid, rate_arr):
        self.ctx.Data.set_game_attr(uid, gid, 'give_chip_rate', self.ctx.json_dumps(rate_arr))

    def get_give_chip_rate(self, uid, gid, default=None):
        kill_chip = self.ctx.Data.get_game_attr(uid, gid, 'give_chip_rate', None)
        if kill_chip:
            return self.ctx.json_loads(kill_chip)
        else:
            return default

    # 送分触发炮倍区间   rate_arr=[10, 100]  炮倍>=10 且 <= 100
    def set_give_chip_effect_bm(self, uid, gid, rate_arr):
        self.ctx.Data.set_game_attr(uid, gid, 'give_chip_effect_bm', self.ctx.json_dumps(rate_arr))

    def get_give_chip_effect_bm(self, uid, gid, default=None):
        kill_chip = self.ctx.Data.get_game_attr(uid, gid, 'give_chip_effect_bm', None)
        if kill_chip:
            return self.ctx.json_loads(kill_chip)
        else:
            return default

    # 针对送分 结束--

    # 针对杀分 开始--
    # 针对玩家当前杀分额度
    def get_kill_chip(self, uid, gid, default=None):
        return self.ctx.Data.get_game_attr_int(uid, gid, 'kill_chip', default)

    # 杀分额度增减
    def incr_kill_chip(self, uid, gid, delta, event, low=-1, high=-1, mode=Const.chip_operate_noop, **kwargs):
        return self.incr_attr(uid, gid, 'kill_chip', delta, event, low, high, mode, **kwargs)

    # 杀分抽比例  rate_arr=[10, 1]  10抽1
    def set_kill_chip_rate(self, uid, gid, rate_arr):
        self.ctx.Data.set_game_attr(uid, gid, 'kill_chip_rate', self.ctx.json_dumps(rate_arr))

    def get_kill_chip_rate(self, uid, gid, default=None):
        kill_chip = self.ctx.Data.get_game_attr(uid, gid, 'kill_chip_rate', None)
        if kill_chip:
            return self.ctx.json_loads(kill_chip)
        else:
            return default
    # 针对杀分 结束--

    def get_target(self, uid, gid, default=None):
        return self.ctx.Data.get_game_attr_int(uid, gid, 'target_coupon', default)

    def incr_target(self, uid, gid, delta, event, low=-1, high=-1, mode=Const.chip_operate_noop, **kwargs):
        real, final = self.incr_attr(uid, gid, 'target_coupon', delta, event, low, high, mode, **kwargs)
        # 如果计数不计入总数且不加入事件中，不能调用此函数
        if real == delta:
            # channel_id = self.ctx.Data.get_attr(uid, 'channelid', '1001_0')
            if delta > 0:
                self.ctx.Data.hincr_game(uid, gid, 'target_fall', delta)
            #     self.ctx.Stat.incr_daily_data(channel_id, 'in_channel_target', delta)
            # else:
            #     self.ctx.Stat.incr_daily_data(channel_id, 'out_channel_target', delta)
            # k, v = TargetEvent.get_target_event_dict(uid, gid, delta, event)
            # TargetEvent.add_event(uid, k, v)
        return real, final

    def get_coupon_private_pool(self, uid, gid, default=None):
        return self.ctx.Data.get_game_attr_int(uid, gid, 'coupon_pool_private', default)

    #暂时只用于鸟券怪和抽奖
    def incr_coupon_private_pool(self, uid, gid, delta, event, low=-1, high=-1, mode=Const.chip_operate_noop, **kwargs):
        return self.incr_attr(uid, gid, 'coupon_pool_private', delta, event, low, high, mode, **kwargs)

    def get_exp(self, uid, gid, default=None):
        return self.ctx.Data.get_game_attr_int(uid, gid, 'exp', default)

    def check_exist(self, uid, gid):
        chip = self.ctx.Data.get_game_attr(uid, gid, 'chip')
        return chip is not None

class Event(IContext, ICallable):
    def __init__(self, event_name):
        self.event_name = None
        if isinstance(event_name, str):
            self.event_name = event_name

    def add_event(self, uid, key, value):
        if not self.event_name:
            return False
        UserAttr.ctx.Data.set_attr_common(uid, 'event:%s:%d'%(self.event_name, uid), key, value)
        return True

    def get_coupon_event_dict(self, uid, gid, count, event):
        times = time.time()
        timeArray = time.localtime(int(times))
        timeArray = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        coupon_pool = UserAttr.ctx.RedisMix.hash_get('game.2.share', 'coupon_pool', default=0)

        v = UserAttr.ctx.json_dumps([event, count, timeArray, coupon_pool])
        return times, v

    def get_sdkey_event_dict(self, sdkey, event):
        times = time.time()
        idx = UserAttr.ctx.Data.get_cdkey_attr(10003, sdkey)
        value = int(int(idx)/1000000)
        version = str(int(value / 100)) + '.' + str(int((value % 100) / 10)) + '.' + str(int(value % 10))
        timeArray = time.localtime(int(times))
        timeArray = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
        v = UserAttr.ctx.json_dumps([event, sdkey, version, timeArray])
        return times, v

    def get_target_event_dict(self, uid, gid, count, event):
        times = time.time()
        _chip = UserAttr.ctx.Data.get_game_attr_int(uid, gid, 'chip', 0)
        _coupon = UserAttr.ctx.Data.get_game_attr_int(uid, gid, 'coupon', 0)
        _target = UserAttr.ctx.Data.get_game_attr_int(uid, gid, 'target_coupon', 0)
        timeArray = time.localtime(int(times))
        timeArray = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)

        target_pool = UserAttr.ctx.RedisMix.hash_get('game.2.share', 'target_pool', default=0)

        v = UserAttr.ctx.json_dumps([event, count, _chip, timeArray, _coupon, _target, target_pool])
        return times, v

    def get_super_weapon_event_dict(self, gid, chip, event):
        times = time.time()
        timeArray = time.localtime(int(times))
        timeArray = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        key = 'game.%d.info.super_weapon_pool' % gid
        key2 = 'pool.barrel_level_chip'
        pool_chip = UserAttr.ctx.RedisMix.hash_get(key, key2, 0)
        strPoolLeft = 'pool_left_chip:' + str(pool_chip)
        v = UserAttr.ctx.json_dumps([event, chip, timeArray, strPoolLeft])
        return times, v

    # def get_fanfanle_event_dict(self, gid, chip, event):
    #     times = time.time()
    #     timeArray = time.localtime(int(times))
    #     timeArray = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    #
    #     key = 'game.%d.fanfanle_pool' % gid
    #     key2 = 'reward_chip'
    #     pool_chip = UserAttr.ctx.RedisMix.hash_get(key, key2, 0)
    #     strPoolLeft = 'pool_left_chip:' + str(pool_chip)
    #     v = UserAttr.ctx.json_dumps([event, chip, timeArray, strPoolLeft])
    #     return times, v

CouponEvent = Event('coupon')

TargetEvent = Event('target')

SdkeyEvent = Event('cdkey')

SuperWeaponEvent = Event('super_weapon')

FanfanleEvent = Event('fanfanle')

UserAttr = UserAttr()
