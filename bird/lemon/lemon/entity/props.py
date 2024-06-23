#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-12-21

from framework.context import Context
from lemon.games.bird.newtask import NewTask
from framework.entity.const import Message
from framework.entity.msgpack import MsgPack

class Props(object):
    PROP_CHIP = 1           # 鸟蛋
    PROP_DIAMOND = 2        # 钻石
    PROP_COUPON = 3         # 奖券
    PROP_RMB = 4            # 人民币

    PROP_VIP = 10           # 月卡
    AUTO_SHOT = 12          # 自动开炮
    GOLD_MONTH_CARD = 14    # 黄金月卡
    KILL_MONTH_CARD = 15    # 至尊月卡

    def get_month_info(self, uid, gid):
        today = Context.Time.up_days()
        month = Context.RedisCluster.hash_get_json(uid, "props:%d:%d" % (gid, uid), 10)
        if month == None:
            create = today
            life = -1
        else:
            create = int(month[0])
            life = int(month[1])
        state = Context.Daily.get_daily_data(uid, gid, 'month_state')
        if state == None:
            state = 0
        return today, create, life, state

    def incr_vip(self, uid, gid, delta, event, **kwargs):
        assert int(delta) != 0
        today, create, life, state = self.get_month_info(uid, gid)
        if life + create > today and life >= 0:
            days = life + delta
            month_data = [create, days]
        else:
            days = delta
            month_data = [today, days]
        Context.RedisCluster.hash_set(uid, "props:%d:%d" % (gid, uid), 10, month_data)
        month = Context.RedisCluster.hash_get_json(uid, "props:%d:%d" % (gid, uid), 12)
        if month == None:
            self.get_auto_shot_info(uid, gid)
        else:
            self.incr_auto_shot(uid, gid, delta, 'month_card')

        auto_shot_day = self.get_auto_shot(uid, gid)
        mo = MsgPack(Message.MSG_SYS_SEND_AUTO_SHOT_TIME | Message.ID_ACK)
        mo.set_param('auto_shot', {'left': auto_shot_day})
        Context.GData.send_to_connect(uid, mo)

        Context.Log.report('incr.vip:', [uid, gid, delta, days, event, kwargs])
        if state == None:
            state = 0
        return state, life - today + create - 1

    def get_vip(self, uid, gid):
        today, create, life, state = self.get_month_info(uid, gid)
        if state == None:
            state = 0
        return state, life - today + create - 1

    def use_vip(self, uid, gid):
        today, create, life, state = self.get_month_info(uid, gid)
        if life + create >= today and life >= 0 and state == 0:
            left_days = life + create - today
            Context.Log.report('use.vip:', [uid, gid, -1, left_days])
            Context.Daily.set_daily_data(uid, gid, 'month_state', 1)
            return True, left_days
        else:
            return False, life - today + create - 1

    def incr_auto_shot(self, uid, gid, delta, event, **kwargs):
        assert int(delta) != 0
        today, create, life = self.get_auto_shot_info(uid, gid)
        if life + create > today and life >= 0:
            days = life + delta
            month_data = [create, days]
            ret = days
        else:
            days = delta
            month_data = [today, days]
            ret = delta
        Context.RedisCluster.hash_set(uid, "props:%d:%d" % (gid, uid), 12, Context.json_dumps(month_data))
        return ret


    def get_auto_shot_info(self, uid, gid):
        today = Context.Time.up_days()
        month = Context.RedisCluster.hash_get_json(uid, "props:%d:%d" % (gid, uid), 12)
        if month == None:
            month_card = Context.RedisCluster.hash_get_json(uid, "props:%d:%d" % (gid, uid), 10)
            if month_card != None:
                create = int(month_card[0])
                life = int(month_card[1])
                Context.RedisCluster.hash_set(uid, "props:%d:%d" % (gid, uid), 12, Context.json_dumps(month_card))
            else:
                create = today
                life = -1
        else:
            create = int(month[0])
            life = int(month[1])
        return today, create, life

    def get_auto_shot(self, uid, gid):
        today, create, life = self.get_auto_shot_info(uid, gid)
        return life - today + create

    def get_new_month_card_info(self, uid, gid, month_card_id):
        today = Context.Time.up_days()

        month = Context.RedisCluster.hash_get_json(uid, "props:%d:%d" % (gid, uid), month_card_id)
        if month == None:
            create = today
            life = -1
        else:
            create = int(month[0])
            life = int(month[1])
        state = Context.Daily.get_daily_data(uid, gid, 'new_month_state_%d'%month_card_id)
        if state == None:
            state = 0
        return today, create, life, state

    def get_new_month_card(self, uid, gid, month_card_id):
        today, create, life, state = self.get_new_month_card_info(uid, gid, month_card_id)
        if state == None:
            state = 0
        return state, life - today + create

    def incr_new_month_card(self, uid, gid, delta, month_card_id):
        assert int(delta) != 0
        today, create, life, state = self.get_new_month_card_info(uid, gid, month_card_id)
        if life + create > today and life >= 0:
            days = life + delta
            month_data = [create, days]
        else:
            days = delta
            month_data = [today, days]
        Context.RedisCluster.hash_set(uid, "props:%d:%d" % (gid, uid), month_card_id, month_data)
        if state == None:
            state = 0
        return state, life - today + create

    def use_new_month_card(self, uid, gid, month_card_id):
        today, create, life, state = self.get_new_month_card_info(uid, gid, month_card_id)
        Context.Log.info('-----------', today, create, life, state)
        if life + create >= today and life >= 0 and state == 0:
            left_days = life + create - today
            Context.Daily.set_daily_data(uid, gid, 'new_month_state_%d'%month_card_id, 1)
            return True, left_days
        else:
            return False, life - today + create

    # cdkey 值 处理
    def incr_cdkey_pay(self, uid, gid, delta, event, **kwargs):
        assert int(delta) != 0
        from lemon.games.bird.account import BirdAccount
        from framework.entity.msgpack import MsgPack
        from lemon.games.bird.const import Message
        from framework.util.tool import Time
        vip_level_form = BirdAccount.get_vip_level(uid, gid)
        final = Context.Data.hincr_game(uid, gid, 'cdkey_pay_total', delta)
        final = Context.Data.hincr_game(uid, gid, 'pay_total', delta)
        vip_level = BirdAccount.get_vip_level(uid, gid)
        if vip_level >= 4 and vip_level > vip_level_form:
            bulletin = 3
            nick = Context.Data.get_attr(uid, 'nick')
            nick = Context.hide_name(nick)
            led = u'玩家<color=#00FF00FF>%s</color>VIP等级晋升到<color=#FFFF00FF>%d</color>，羡煞众人！' % (nick, vip_level)
            mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
            mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
            Context.GData.broadcast_to_system(mo)
        Context.Log.report('cdkey_pay.update:', [uid, gid, delta, final, event, kwargs])
        return final

    def incr_pay(self, uid, gid, delta, event, **kwargs):
        assert int(delta) != 0
        from lemon.games.bird.account import BirdAccount
        from framework.entity.msgpack import MsgPack
        from lemon.games.bird.const import Message
        from framework.util.tool import Time
        vip_level_form = BirdAccount.get_vip_level(uid, gid)
        final = Context.Data.hincr_game(uid, gid, 'pay_total', delta)
        vip_level = BirdAccount.get_vip_level(uid, gid)
        if vip_level >= 4 and vip_level > vip_level_form:
            bulletin = 3
            nick = Context.Data.get_attr(uid, 'nick')
            nick = Context.hide_name(nick)
            led = u'玩家<color=#00FF00FF>%s</color>VIP等级晋升到<color=#FFFF00FF>%d</color>，羡煞众人！' % (nick, vip_level)
            mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
            mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
            Context.GData.broadcast_to_system(mo)
        Context.Log.report('pay.update:', [uid, gid, delta, final, event, kwargs])
        return final

    def incr_props(self, uid, gid, pid, count, event, **kwargs):
        assert self.check_props(pid)
        assert int(count) != 0

        real, final, fixed = Context.RedisCluster.execute_lua_alias(uid, 'props_op', 'incr', uid, gid, pid, count)
        if fixed:
            Context.Log.report('props.%s.fixed:' % pid, [uid, gid, int(fixed), 0, event, kwargs])
            channel_id = Context.Data.get_attr(uid, 'channelid', '1001_0')
            Context.Stat.incr_daily_data(channel_id, 'in.props.%d.fixed' % pid, fixed)
            Context.Stat.incr_user_data(uid, gid, 'in.props.%d.fixed' % pid, fixed)
            Context.Stat.incr_daily_user_data(channel_id, uid, 'in.props.%d.fixed' % pid, fixed)
            Context.RedisMix.hash_incrby('game.%d.info.hash' % gid, 'in.props.%d.fixed' % pid, fixed)

        if real or count == 0:
            Context.Log.report('props.%s.update:' % pid, [uid, gid, int(real), int(final), event, kwargs])
            if real != 0:
                if real > 0:
                    in_or_out = 'in'
                else:
                    in_or_out = 'out'
                if 'roomtype' in kwargs:
                    _field = '%s.props.%d.%s.%d' % (in_or_out, pid, event, kwargs['roomtype'])
                else:
                    _field = '%s.props.%d.%s' % (in_or_out, pid, event)
                channel_id = Context.Data.get_attr(uid, 'channelid', '1001_0')
                Context.Stat.incr_daily_data(channel_id, _field, real)
                Context.Stat.incr_user_data(uid, gid, _field, real)
                Context.Stat.incr_daily_user_data(channel_id, uid, _field, real)
                Context.RedisMix.hash_incrby('game.%d.info.hash' % gid, '%s.props.%d' % (in_or_out, pid), real)
                self.stat_props(uid, gid, pid, count, event)

        return real, final

    def get_props(self, uid, gid, pid):
        return Context.RedisCluster.execute_lua_alias(uid, 'props_op', 'get', uid, gid, pid)

    def __check_incr_args(self, *args):
        l = list(args)
        if len(l) < 2 or len(l) % 2 != 0:
            raise Exception('error count')

        for i in xrange(0, len(l), 2):
            assert self.check_props(l[i])
            assert int(l[i + 1]) != 0
        return l

    def mincr_props(self, uid, gid, event, *args, **kwargs):
        self.__check_incr_args(*args)

        failed, finals = Context.RedisCluster.execute_lua_alias(uid, 'props_op', 'mincr', uid, gid, *args)
        if failed:
            return False

        for i, final in enumerate(finals):
            pid, real = args[2 * i], args[2 * i + 1]
            Context.Log.report('props.%s.update:' % pid, [uid, gid, int(real), int(final), event, kwargs])
            if real != 0:
                if real > 0:
                    in_or_out = 'in'
                else:
                    in_or_out = 'out'
                if 'roomtype' in kwargs:
                    _field = '%s.props.%d.%s.%d' % (in_or_out, pid, event, kwargs['roomtype'])
                else:
                    _field = '%s.props.%d.%s' % (in_or_out, pid, event)
                channel_id = Context.Data.get_attr(uid, 'channelid', '1001_0')
                Context.Stat.incr_daily_data(channel_id, _field, real)
                Context.Stat.incr_daily_user_data(channel_id, uid, _field, real)
                Context.RedisMix.hash_incrby('game.%d.info.hash' % gid, '%s.props.%d' % (in_or_out, pid), real)
        return finals

    def check_props(self, pid):
        raise NotImplementedError

    def stat_props(self, uid, gid, pid, count, event):
        raise NotImplementedError

    '''
    need_gift 是否是服务器赠送给玩家鸟蛋，如果是需要额外赠送额度
    '''
    BOX_PRICE_DICT = {
        211: 150000,
        212: 300000,
        213: 500000,
        214: 1000000,
    }

    def deal_none_reward(self, reward):
        result = {}
        if 'chip' in reward and reward['chip'] > 0:
            result['chip'] = reward['chip']
        if 'coupon' in reward and reward['coupon'] > 0:
            result['coupon'] = reward['coupon']
        if 'diamond' in reward and reward['diamond'] > 0:
            result['diamond'] = reward['diamond']
        if 'props' in reward:
            props = []
            for one in reward['props']:
                if one['count'] > 0:
                    props.append(one)
            if len(props) > 0:
                result['props'] = props
        return result

    def issue_rewards(self, uid, gid, reward, event, need_gift=False, **kwargs):
        rewards_info = {}
        if reward:
            rewards = self.deal_spacial_reward(uid, gid, reward)
            vip_exp = rewards.get('vip_exp', 0)
            if vip_exp > 0:
                final = Context.Data.hincr_game(uid, gid, 'vip_exp', vip_exp)
                Context.Log.report('vip_exp.update:', [uid, gid, int(final), event])
            chip = rewards.get('chip', 0)
            if chip > 0:
                _, final = Context.UserAttr.incr_chip(uid, gid, chip, event, **kwargs)
                #if need_gift:   # 如果需要赠送

                room = None
                if 'roomtype' in kwargs:
                    room = kwargs['roomtype']
                NewTask.get_chip_task(uid, chip, event, room)
                rewards_info['chip'] = final
            # shit = rewards.get('shit', 0)
            # if shit > 0:
            #     _, final = Context.UserAttr.incr_shit(uid, gid, shit, event, **kwargs)
            #     chip = Context.UserAttr.get_chip(uid, gid, 0)
            #     rewards_info['chip'] = final+chip
            diamond = rewards.get('diamond', 0)
            if diamond:
                _, final = Context.UserAttr.incr_diamond(uid, gid, diamond, event, **kwargs)
                room = None
                if 'roomtype' in kwargs:
                    room = kwargs['roomtype']
                NewTask.get_diamond_task(uid, diamond, event, room)
                rewards_info['diamond'] = final

            coupon = rewards.get('coupon', 0)
            if coupon:
                _, final = Context.UserAttr.incr_coupon(uid, gid, coupon, event, **kwargs)
                rewards_info['coupon'] = final

            target = rewards.get('target', 0)
            if target:
                _, final = Context.UserAttr.incr_target(uid, gid, target, event, **kwargs)

                rewards_info['target'] = final

            props = rewards.get('props')
            if props:
                _props = []
                for prop in props:
                    if self.check_props(prop['id']):
                        _, final = self.incr_props(uid, gid, prop['id'], prop['count'], event, **kwargs)
                        _props.append({'id': prop['id'], 'count': final})
                if _props:
                    rewards_info['props'] = _props

            rewards_info['reward'] = rewards
        return rewards_info

    def deal_spacial_reward(self, uid, gid, gift_box):
        reward = Context.copy_json_obj(gift_box)
        if reward.has_key('auto_shot'):
            auto_shot_day = self.incr_auto_shot(uid, gid, int(reward['auto_shot']), 'gift.box.buy')
            mo = MsgPack(Message.MSG_SYS_SEND_AUTO_SHOT_TIME | Message.ID_ACK)
            mo.set_param('auto_shot', {'left': auto_shot_day})
            Context.GData.send_to_connect(uid, mo)
            del reward['auto_shot']
        if reward.has_key('weapon'):
            for i in reward['weapon']:
                info = {}
                mo = MsgPack(Message.MSG_SYS_BUY_WEAPON | Message.ID_ACK)
                weapon_buy_dict = Context.Data.get_game_attr_json(uid, gid, 'weapon_buy_dict')
                info['weapon'] = i
                info['success'] = 1
                mo.update_param(info)
                weapon_buy_dict[str(i)] = 1
                Context.Data.set_game_attr(uid, gid, 'weapon_buy_dict', Context.json_dumps(weapon_buy_dict))
                Context.GData.send_to_connect(uid, mo)
            del reward['weapon']
        return reward

    def merge_reward(self, *args):
        if not args:
            return {}
        if len(args) == 1:
            return args[0]
        rewards = {}
        for arg in args:
            rewards = self.__merge_reward(rewards, arg)
        return rewards

    def __merge_reward(self, prev, later):
        if not prev:
            return Context.copy_json_obj(later)
        if not later:
            return Context.copy_json_obj(prev)

        rewards = {}
        # merge鸟蛋
        if 'chip' in prev or 'chip' in later:
            rewards['chip'] = prev.get('chip', 0) + later.get('chip', 0)
        # merge钻石
        if 'diamond' in prev or 'diamond' in later:
            rewards['diamond'] = prev.get('diamond', 0) + later.get('diamond', 0)
        # merge兑换券
        if 'coupon' in prev or 'coupon' in later:
            rewards['coupon'] = prev.get('coupon', 0) + later.get('coupon', 0)
        if 'target' in prev or 'target' in later:
            rewards['target'] = prev.get('target', 0) + later.get('target', 0)
        # merge道具
        props = {}
        for tmp in [prev, later]:
            if 'props' in tmp:
                for prop in tmp['props']:
                    if prop['id'] not in props:
                        props[prop['id']] = prop
                    else:
                        props[prop['id']]['count'] += prop['count']

        if props:
            rewards['props'] = props.values()

        return rewards

    def merge_reward_result(self, detail, *args):
        if not args:
            return {}
        if len(args) == 1:
            return args[0]
        rewards = {}
        for arg in args:
            rewards = self.__merge_reward_result(detail, rewards, arg)
        return rewards

    def __merge_reward_result(self, detail, prev, later):
        if not prev:
            return Context.copy_json_obj(later)
        if not later:
            return Context.copy_json_obj(prev)

        ret = {}

        # 合并最终的字段
        if 'chip' in later:
            ret['chip'] = later['chip']
        elif 'chip' in prev:
            ret['chip'] = prev['chip']

        if 'diamond' in later:
            ret['diamond'] = later['diamond']
        elif 'diamond' in prev:
            ret['diamond'] = prev['diamond']

        if 'coupon' in later:
            ret['coupon'] = later['coupon']
        elif 'coupon' in prev:
            ret['coupon'] = prev['coupon']

        if 'target' in later:
            ret['target'] = later['target']
        elif 'target' in prev:
            ret['target'] = prev['target']

        _props = {}
        for tmp in [prev, later]:
            if 'props' in tmp:
                for prop in tmp['props']:
                    _props[prop['id']] = prop
        if _props:
            ret['props'] = _props.values()

        if detail:
            # 合并奖励字段
            prev_reward, later_reward = prev['reward'], later['reward']
            rewards = {}
            # merge鸟蛋
            if 'chip' in prev_reward or 'chip' in later_reward:
                rewards['chip'] = prev_reward.get('chip', 0) + later_reward.get('chip', 0)
            # merge fake 鸟蛋
            if 'fake_chip' in prev_reward or 'fake_chip' in later_reward:
                rewards['fake_chip'] = prev_reward.get('fake_chip', 0) + later_reward.get('fake_chip', 0)
            # merge钻石
            if 'diamond' in prev_reward or 'diamond' in later_reward:
                rewards['diamond'] = prev_reward.get('diamond', 0) + later_reward.get('diamond', 0)
            # merge兑换券
            if 'coupon' in prev_reward or 'coupon' in later_reward:
                rewards['coupon'] = prev_reward.get('coupon', 0) + later_reward.get('coupon', 0)
            if 'target' in prev_reward or 'target' in later_reward:
                rewards['target'] = prev_reward.get('target', 0) + later_reward.get('target', 0)
            # merge道具
            props = {}
            for tmp in [prev_reward, later_reward]:
                if 'props' in tmp:
                    for prop in tmp['props']:
                        if prop['id'] not in props:
                            props[prop['id']] = prop
                        else:
                            props[prop['id']]['count'] += prop['count']

            if props:
                rewards['props'] = props.values()

            if rewards:
                ret['reward'] = rewards

        return ret
