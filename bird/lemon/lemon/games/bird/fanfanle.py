#!/usr/bin/env python
# -*- coding=utf-8 -*-

import random
from framework.context import Context
from framework.entity.msgpack import MsgPack
from framework.entity.const import Message
from framework.util.tool import Time, Tool
from props import BirdProps
from account import BirdAccount
from framework.entity.userattr import FanfanleEvent
from newtask import NewTask


class BirdFanFanLe(object):
    def send_config(self, uid, gid):
        mo = MsgPack(Message.MSG_SYS_FFL_CONFIG | Message.ID_ACK)
        info = {}

        chip_info = self.get_config(gid, 0)
        diamond_info = self.get_config(gid, 1)

        info['chip_room'] = chip_info
        info['diamond_room'] = diamond_info
        mo.set_param('conf', info)
        Context.GData.send_to_connect(uid, mo)
        return

    def get_config(self, gid, index):
        conf = Context.Configure.get_game_item_json(gid, 'fanfanle.config')
        _conf = Context.copy_json_obj(conf)
        return _conf.get(str(index))

    def open_game(self, uid, gid):
        mo = MsgPack(Message.MSG_SYS_FFL_OPEN | Message.ID_ACK)

        conf_dat = Context.RedisMix.hash_get_json('game.%d.background' % gid, 'fanfanle.config', {})
        if conf_dat.get('open', 1) == 0:
            mo.set_error(3, u'活动已被关闭')
            Context.GData.send_to_connect(uid, mo)
            return

        match_status = Context.MatchDB.get_match_player_status(uid)
        if match_status:
            mo.set_error(2, u'您正在竞技场中')
            Context.GData.send_to_connect(uid, mo)
            return

        status = Context.RedisCache.hash_get_int('smart_game:%d' % uid, 'status', 0)
        if status > 0:
            return mo.set_error(0, u"你正在进行第三方小游戏，无法开启翻翻乐")

        index, price, level, result, change = self.get_player_data(uid, gid)
        if index != None and price != None and level != None and result != None and \
                int(result) <= 5 and int(result) >= 3:
            mo.set_param('last', 1)
            mo.set_param('price', price)
            mo.set_param('index', index)
            mo.set_param('level', level)
            mo.set_param('result', result)
            mo.set_param('change', change)
            Context.GData.send_to_connect(uid, mo)
        else:
            mo.set_param('last', 0)
            Context.GData.send_to_connect(uid, mo)

    # 开始玩翻翻乐
    def start_game(self, uid, gid, mi):
        index = mi.get_param('index')       # 场次  钻石or鸟蛋场
        price = mi.get_param('price')       # 入场额度
        _conf = self.get_config(gid, int(index))
        self.get_result(uid, gid, _conf, index, price)

    def change_card(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_FFL_CHANGE | Message.ID_ACK)
        index, price, level, result, change = self.get_player_data(uid, gid)
        if index == None or price == None or level == None or result == None or \
                result >= 5 or result < 3 or change != None:
            mo.set_error(1, u'数据错误')
            Context.GData.send_to_connect(uid, mo)
            return
        p = mi.get_param('price')
        if price != p:
            mo.set_error(2, u'换牌的等级必须保持一致')
            Context.GData.send_to_connect(uid, mo)
            return
        _conf = self.get_config(gid, int(index))
        self.get_change_result(uid, gid, index, _conf, price, result, level)

    # 获取本次翻翻乐结果
    def get_result(self, uid, gid, conf, index, priceIdx):
        channel_id = Context.Data.get_attr(uid, 'channelid')
        entrance_cost = conf.get('entrance_cost')
        cost = entrance_cost[priceIdx - 1]
        if not self.check_enable_play_cost(index, cost, uid, gid, priceIdx, conf):     # 判断是否能够进行游戏
            return
        # 添加各渠道玩的次数
        if index == 0:
            Context.Stat.incr_daily_data(channel_id, 'v2_server_fanfanle_play_chip_times')
        else:
            Context.Stat.incr_daily_data(channel_id, 'v2_server_fanfanle_play_diamonds_times')
        self.get_game_relust(uid, gid, conf, index, priceIdx)


    def _get_calc_rate(self, gid, conf, index, price_idx):
        pool_value = self.get_pool_value(gid, index, price_idx)
        rate_data = conf.get('rate_calc').get(str(price_idx))

        base_line = rate_data.get('baseLine')
        add_line = rate_data.get('addLine')
        add_rate = rate_data.get('addRate')
        lowRate = conf.get('lowRate')
        highRate = conf.get('highRate')

        add_value = int((pool_value - base_line)/(add_line))*float(add_rate)
        low_rt = lowRate+add_value
        high_rt = highRate + add_value

        return low_rt, high_rt

    def get_game_relust(self, uid, gid, conf, index, price_idx):
        low_rt, high_rt = self._get_calc_rate(gid, conf, index, price_idx) # 根据池子获取区间
        level_rand = random.random()
        if level_rand < low_rt:
            level = 3
        elif level_rand < high_rt:
            level = 2
        else:
            level = 1
        little_rand = random.random()
        if little_rand < conf.get('little_reward') and low_rt > 0:
            result = 5
        else:
            result_rand = random.random()
            if result_rand < low_rt:
                result = 4
            elif result_rand < high_rt:
                result = 3
            else:
                level = 0
                result = 2

        mo = MsgPack(Message.MSG_SYS_FFL_START | Message.ID_ACK)
        mo.set_param('index', index)
        mo.set_param('level', level)
        mo.set_param('result', result)
        Context.GData.send_to_connect(uid, mo)
        if result < 3:
            pool_chip = self.get_pool_value(gid, index, price_idx)
            entrance_cost = conf.get('entrance_cost')
            cost = entrance_cost[price_idx - 1]
            inf = {'type': index, 'cost': cost, 'change': 0, 'reward': {}, 'pool_chip': pool_chip}
            tmp = Time.current_time('%Y-%m-%d')
            Context.RedisStat.hash_set('fanfanle:%s:%d' % (tmp, uid), Time.current_ms(), Context.json_dumps(inf))
            return

        # 池中扣除奖励内容
        reward = self.get_reard_data(index, level, conf, result, price_idx)
        reward_chip = BirdProps.get_props_price(reward)
        self.incr_pool_value(gid, index, price_idx, -reward_chip)
        l = ['index', index, 'price', price_idx, 'level', level, 'result', result]
        Context.RedisActivity.hash_mset('fanfanle:%d:%d' % (gid, uid), *l)

        return

    def get_change_result(self, uid, gid, index, conf, price_idx, result, level):
        channel_id = Context.Data.get_attr(uid, 'channelid')
        switchCard_cost = conf.get('switchCard_cost')
        cost = switchCard_cost[price_idx - 1]
        if not self.check_enable_switch_cost(uid, gid, cost, index, price_idx):
            return
        if index != 0:
            Context.Stat.incr_daily_data(channel_id, 'server_fanfanle_exchange_diamond_times')
        else:
            Context.Stat.incr_daily_data(channel_id, 'server_fanfanle_exchange_chip_times')
        success = False
        if result == 4:
            little_rand = random.random()
            if little_rand < conf.get('little_reward'):
                success = True
        low_rt, high_rt = self._get_calc_rate(gid, conf, index, price_idx)  # 根据池子获取区间
        if result == 3:
            result_rand = random.random()
            if result_rand < high_rt:
                success = True
        mo = MsgPack(Message.MSG_SYS_FFL_CHANGE | Message.ID_ACK)
        if success:  # 换牌成功
            # 旧奖励退还
            reward = self.get_reard_data(index, level, conf, result, price_idx)
            reward_chip = BirdProps.get_props_price(reward)
            result = result + 1  # 替换为新奖励
            # 池中扣除奖励内容
            current_reward = self.get_reard_data(index, level, conf, result, price_idx)
            current_reward_chip = BirdProps.get_props_price(current_reward)
            self.incr_pool_value(gid, index, price_idx, reward_chip-current_reward_chip)
            Context.RedisActivity.hash_set('fanfanle:%d:%d' % (gid, uid), 'result', result)
        mo.set_param('index', index)
        mo.set_param('level', level)
        mo.set_param('result', result)
        Context.GData.send_to_connect(uid, mo)
        Context.RedisActivity.hash_set('fanfanle:%d:%d' % (gid, uid), 'change', price_idx)

    #核对玩家是否能换牌
    def check_enable_switch_cost(self, uid, gid, cost, index, priceIdx):
        if index != 0:
            real, final = Context.UserAttr.incr_diamond(uid, gid, -cost, 'game.fanfanle.change')
            if real != -cost:
                mo = MsgPack(Message.MSG_SYS_FFL_CHANGE | Message.ID_ACK)
                mo.set_error(3, '钻石不足')
                Context.GData.send_to_connect(uid, mo)
                return False
            NewTask.get_diamond_consume_task(uid, cost)
            self.incr_pool_value(gid, index, priceIdx, cost * 500)
        else:
            real, final = Context.UserAttr.incr_chip(uid, gid, -cost, 'game.fanfanle.change')
            if real != -cost:
                mo = MsgPack(Message.MSG_SYS_FFL_CHANGE | Message.ID_ACK)
                mo.set_error(3, '鸟蛋不足')
                Context.GData.send_to_connect(uid, mo)
                return False
            self.incr_pool_value(gid, index, priceIdx, cost)
        return True

    #核对玩家是否能玩
    def check_enable_play_cost(self, index, cost, uid, gid, priceIdx, conf):
        mo = MsgPack(Message.MSG_SYS_FFL_START | Message.ID_ACK)
        conf_dat = Context.RedisMix.hash_get_json('game.%d.background' % gid, 'fanfanle.config', {})
        if conf_dat.get('open', 1) == 0:
            mo.set_error(4, u'活动已被关闭')
            Context.GData.send_to_connect(uid, mo)
            return False
        user_vip = BirdAccount.get_vip_level(uid, gid)
        if index != 0:
            vip_limit = conf_dat.get('vip_limit', 0)
            if vip_limit <= 0:
                vip_limit = conf.get('vip_limit', 0)
            if user_vip < vip_limit:
                mo.set_error(5, u'vip等级不足')
                Context.GData.send_to_connect(uid, mo)
                return False

            real, final = Context.UserAttr.incr_diamond(uid, gid, -cost, 'game.fanfanle.play')
            if real != -cost:
                mo.set_error(3, u'钻石不足')
                Context.GData.send_to_connect(uid, mo)
                return False
            self.incr_pool_value(gid, index, priceIdx, cost * 500)
            NewTask.get_diamond_consume_task(uid, cost)
        else:
            if user_vip < conf.get('vip_limit', 0):
                mo.set_error(5, u'vip等级不足')
                Context.GData.send_to_connect(uid, mo)
                return False

            real, final = Context.UserAttr.incr_chip(uid, gid, -cost, 'game.fanfanle.play')
            if real != -cost:
                mo.set_error(3, u'鸟蛋不足')
                Context.GData.send_to_connect(uid, mo)
                return False
            self.incr_pool_value(gid, index, priceIdx, cost)
        return True

    # 根据玩家翻牌状态数据获取玩家的奖励
    def get_reard_data(self, index, level, conf, result, price_idx):
        price_cost = conf.get('entrance_cost')[price_idx - 1]

        reward_model = conf.get('reward_model')[price_idx-1][level-1]
        if level == 3:
            reward_list = conf.get('reward_scale').get('reward_C')
        elif level == 2:
            reward_list = conf.get('reward_scale').get('reward_B')
        else:
            reward_list = conf.get('reward_scale').get('reward_A')

        if reward_model == 'diamond':
            count = int(reward_list[5 - result] * price_cost)
            reward = {'diamond': count}
        elif reward_model == 'chip':
            count = int(reward_list[5 - result] * price_cost)
            reward = {'chip': count}
        else:
            if index == 1:
                diamond_chip = conf.get('diamond_chip')
            else:
                diamond_chip = 1
            chip_ex_coupon = conf.get('reward_scale').get('reward_C_chip_ex_coupon')
            count = int(reward_list[5 - result] * price_cost * diamond_chip / chip_ex_coupon)
            reward = {'coupon': count}
        return reward

    #获取池子数据
    def get_pool_value(self, gid, index, level):
        sub_key = 'game.%d.share'%gid
        primary_key = 'ffl_pool_%d_level_%d'%(index, level)
        return Context.RedisMix.hash_get_int(sub_key, primary_key, 0)

    # 增减池
    def incr_pool_value(self, gid, index, level, delta):
        assert isinstance(delta, int)
        sub_key = 'game.%d.share'%gid
        primary_key = 'ffl_pool_%d_level_%d'%(index, level)
        return Context.RedisMix.hash_incrby(sub_key, primary_key, delta)

    # 获取玩家翻牌状态数据
    def get_player_data(self, uid, gid):    #获取玩家玩过的数据值
        filed = ['index', 'price', 'level', 'result', 'change']
        i, p, l, r, c = Context.RedisActivity.hash_mget('fanfanle:%d:%d' % (gid, uid), *filed)
        index = Tool.to_int(i)
        price = Tool.to_int(p)
        level = Tool.to_int(l)
        result = Tool.to_int(r)
        change = Tool.to_int(c)
        return index, price, level, result, change

    # 玩家获取奖励数据
    def send_reward(self, uid, gid):
        mo = MsgPack(Message.MSG_SYS_FFL_REWARD | Message.ID_ACK)
        index, price, level, result, change = self.get_player_data(uid, gid)
        if index == None or level == None or result == None or price == None or \
                int(result) > 5 or int(result) < 3:
            mo.set_error(1, '数据错误')
            Context.GData.send_to_connect(uid, mo)
            return

        _conf = self.get_config(gid, index)
        reward_g = self.get_reard_data(index, level, _conf, result, price)

        entrance_cost = _conf.get('entrance_cost')
        switchCard_cost = _conf.get('switchCard_cost')
        cost = entrance_cost[price - 1]
        change_cost = 0
        if change > 0:
            change_cost = switchCard_cost[change - 1]

        pool_chip = self.get_pool_value(gid, index, price)
        inf = {'type': index, 'cost': cost, 'change': change_cost, 'reward': reward_g, 'pool_chip' : pool_chip}
        tmp = Time.current_time('%Y-%m-%d')
        Context.RedisStat.hash_set('fanfanle:%s:%d'%(tmp, uid), Time.current_ms(), Context.json_dumps(inf))

        BirdProps.issue_rewards(uid, gid, reward_g, 'game.fanfanle.get')
        rw = BirdProps.convert_reward(reward_g)
        mo.set_param('rw', rw)
        Context.GData.send_to_connect(uid, mo)
        all = Context.RedisActivity.hash_getall('fanfanle:%d:%d' % (gid, uid))
        for i in all:
            Context.RedisActivity.hash_del('fanfanle:%d:%d' % (gid, uid), i)

        if result == 5 and rw != None:
            bulletin = 3
            nick = Context.Data.get_attr(uid, 'nick')
            nick = Context.hide_name(nick)
            rw_str = u''
            if rw.has_key('c'):
                rw_str += u'%d鸟蛋'%rw['c']
            if rw.has_key('d'):
                rw_str += u'%d钻石'%rw['d']
            if rw.has_key('o'):
                rw_str += u'%d鸟券'%rw['o']

            led = u'运气爆棚！玩家<color=#00FF00FF>%s</color>在<color=#FF0000FF>小游戏-翻翻乐</color>中获得<color=#FFFF00FF>%s</color>' % (
            nick, rw_str)
            mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
            mou.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
            Context.GData.broadcast_to_system(mou)

BirdFanFanLe = BirdFanFanLe()