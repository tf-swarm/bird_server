#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-12-28

from const import Message
import props
import copy
from activity import BirdActivity
from framework.util.tool import Time
from framework.util.tool import Tool
from framework.context import Context
from lemon.entity.account import Account
from lemon.entity.upgrade import Upgrade
from framework.entity.msgpack import MsgPack
import lemon.games.bird.newtask


class BirdAccount(Account):
    game_attrs = {
        'exp': 0,
        'play': 0,
        'broken': 0,
        'barrel_level': 1,
        'barrel_skin': 1
    }
    auto_issue_benefit = False

    login_level = {
        1:[1, 1],
        2:[2, 2],
        3:[3, 6],
        4:[7, 29],
    }

    @classmethod
    def get_game_info(cls, uid, gid):
        is_new, kvs = cls.get_common_game_info(uid, gid)

        conf = Context.Configure.get_game_item_json(gid, 'barrel.unlock.config')
        kvs['barrel_multiple'] = conf[kvs['barrel_level'] - 1]['multiple']

        vip = cls.get_vip_info(uid, gid)
        if vip:
            kvs['vip'] = vip
        now_day, last_login, ns_login, np_login = cls.get_login_info(uid, gid)

        # login
        login_conf = copy.deepcopy(Context.Configure.get_game_item_json(gid, 'login.reward'))
        create_day = Context.Data.get_uid_create_day(uid)
        channel_id = Context.Data.get_attr(uid, 'channelid', '1004_0')
        if channel_id not in ['1000_0', '1003_0', '1004_0','1005_0','1007_0','1008_0'] or create_day > 7:
            login = {'done': 0}
            if now_day == last_login:  # 已经签到
                if create_day == 8:
                    ns_login = 0
                login['done'] = 1
            elif now_day == last_login + 1 and create_day != 8:  # 连续登陆
                ns_login += 1
            else:
                ns_login = 0
            login_conf = login_conf['common']
            confSignReward = []
            vipConfig = Context.Configure.get_game_item_json(gid, 'vip.config')
            for k, tmp in enumerate(login_conf):
                reward = tmp[0]
                if vip['level'] > 0 and vipConfig[vip['level'] -1].has_key('day_sign_times') and reward.has_key('chip'):
                    reward['chip'] = vipConfig[vip['level'] - 1]['day_sign_times'][k]
                reward2 = tmp[1]
                if len(reward2) > 0:
                    reward = props.BirdProps.merge_reward_result(False, reward, reward2)
                reward = props.BirdProps.convert_reward(reward)
                confSignReward.append(reward)
            login['which'] = ns_login % len(login_conf)
            login['conf'] = confSignReward
            login['news'] = 0
            kvs['login'] = login
        else:
            login = {'done': 0}
            if now_day == last_login:  # 已经签到
                login['done'] = 1

            login_conf = login_conf['new']
            confSignReward = []

            for tmp in login_conf:
                reward = tmp[0]
                reward2 = tmp[1]
                if len(reward2) > 0:
                    reward = props.BirdProps.merge_reward_result(False, reward, reward2)
                reward = props.BirdProps.convert_reward(reward)
                confSignReward.append(reward)
            login['which'] = np_login
            login['conf'] = confSignReward
            login['news'] = 1
            kvs['login'] = login

        # exp
        level, diff = cls.get_exp_info(uid, gid, kvs['exp'])
        kvs['exp_level'] = level
        if diff:
            kvs['exp_diff'] = diff
        else:
            kvs['exp_diff'] = [0, 0]

        # month card
        state, left_days = props.BirdProps.get_vip(uid, gid)
        if left_days >= 0:
            kvs['card'] = {'state': state, 'left': left_days}

        auto_shot_day = props.BirdProps.get_auto_shot(uid, gid)
        if auto_shot_day > 0:
            kvs['auto_shot'] = {'left': auto_shot_day}

        state, gold_card = props.BirdProps.get_new_month_card(uid, gid, 14)
        if gold_card > 0:
            kvs['gold_card'] = {'state': state, 'left': gold_card}
        state, kill_card = props.BirdProps.get_new_month_card(uid, gid, 15)
        if kill_card > 0:
            kvs['kill_card'] = {'state': state, 'left': kill_card}
        # activity info
        act = BirdActivity.get_activity_title(gid)
        if act:
            kvs['activity'] = act

        # skill test
        # vt, sw = Context.Data.get_game_attrs(uid, gid, ['try_violent', 'try_super_weapon'])
        # can_try = []
        # if vt is None:
        #     can_try.append(203)
        # if sw is None:
        #     can_try.append(204)
        # if can_try:
        #     kvs['try'] = can_try

        info = Context.RedisCache.hash_getall('global.notice')
        end = info.get('end')
        if end and end > Time.current_ts():
            kvs['notice_start'] = info.get('start')
            kvs['notice_end'] = info.get('end')
            kvs['notice_led'] = info.get('led')

        # 今日已使用赠送次数
        present_times = Context.Daily.get_daily_data(uid, gid, 'present_times')
        present_times = Tool.to_int(present_times, 0)
        kvs['present_times'] = present_times

        return is_new, kvs

    @classmethod
    def get_vip_level(cls, uid, gid, pay_total=None):
        if pay_total is None:
            pay_total = Context.Data.get_game_attr_int(uid, gid, 'pay_total', 0)
            pay_total += Context.Data.get_game_attr_int(uid, gid, 'vip_exp', 0)
        conf = Context.Configure.get_game_item_json(gid, 'vip.level')
        if conf:
            start = 0
            for i, v in enumerate(conf):
                if start <= pay_total < v:
                    level = i
                    break
                start = v
            else:
                level = len(conf)
        else:
            level = 0
        return level

    @classmethod
    def get_vip_info(cls, uid, gid):
        pay_total = Context.Data.get_game_attr_int(uid, gid, 'pay_total', 0)
        pay_total += Context.Data.get_game_attr_int(uid, gid, 'vip_exp', 0)
        conf = Context.Configure.get_game_item_json(gid, 'vip.level')
        vip = {}
        if conf:
            start = 0
            for i, v in enumerate(conf):
                if start <= pay_total < v:
                    vip['level'] = i
                    vip['next'] = v
                    break
                start = v
            else:
                vip['level'] = len(conf)
        else:
            vip['level'] = 0
            vip['next'] = conf[0]

        # if vip['level'] > 7:
            # session_ver = Context.Data.get_game_attr(uid, gid, 'session_ver')
            # if Upgrade.cmp_version(session_ver, '1.1.0') < 0:
            #     vip['level'] = 7
            #     if 'next' in vip:
            #         del vip['next']

        vip['pay_total'] = pay_total
        return vip

    @classmethod
    def get_exp_info(cls, uid, gid, exp=None):
        if exp is None:
            exp = Context.Data.get_game_attr_int(uid, gid, 'exp', 0)
        conf = Context.Configure.get_game_item_json(gid, 'exp.level')
        if conf:
            start = 0
            for i, v in enumerate(conf):
                if start <= exp < v:
                    level, diff = i, [start, v]
                    break
                start = v
            else:
                level, diff = len(conf), None
        else:
            level, diff = 1, [0, conf[1]]
        return level, diff

    @classmethod
    def trans_barrel_level(cls, gid, level):
        conf = Context.Configure.get_game_item_json(gid, 'barrel.unlock.config')
        return conf[level - 1]['multiple']

    @classmethod
    def trans_barrel_multi(cls, gid, multi):
        conf = Context.Configure.get_game_item_json(gid, 'barrel.unlock.config')
        for i in conf:
            if i.get('multiple') == multi:
                return i.get('level')
        return None

    @classmethod
    def on_create_user(cls, uid, gid):
        super(BirdAccount, cls).on_create_user(uid, gid)
        # 发放一级礼包
        conf = Context.Configure.get_game_item_json(gid, 'exp.level.reward')
        rewards_info = props.BirdProps.issue_rewards(uid, gid, conf[0], 'exp.upgrade', True)
        rewards_info = props.BirdProps.convert_reward(rewards_info)
        mo = MsgPack(Message.BIRD_MSG_EXP_UPGRADE | Message.ID_NTF)
        mo.set_param('exp', 0)
        mo.set_param('lv', 1)
        mo.set_param('df', [1, [0, conf[1]]])
        mo.update_param(rewards_info)
        Context.GData.send_to_connect(uid, mo)

        from lemon.games.bird.newactivity import WxNewPlayerActivity
        WxNewPlayerActivity.send_activity_mail(uid, gid)

        # new user carrying
        pipe_args = []
        for k in ('chip', 'diamond', 'coupon'):
            if k in rewards_info:
                pipe_args.append('login.carrying.volume.%s' % k)
                pipe_args.append(rewards_info[k])
        if 'chip' in rewards_info:
            pipe_args.append('carrying.volume.chip')
            pipe_args.append(rewards_info['chip'])
        if pipe_args:
            channel_id = Context.Data.get_attr(uid, 'channelid')
            Context.Stat.mincr_daily_data(channel_id, *pipe_args)
            Context.Stat.mincr_daily_user_data(channel_id, uid, *pipe_args)

    @classmethod
    def on_user_login(cls, uid, gid):
        login = super(BirdAccount, cls).on_user_login(uid, gid)
        vip_level = cls.get_vip_level(uid, gid)
        from lemon.games.bird.newactivity import LoginActivity
        LoginActivity.add_login_account(uid)
        cls.deal_login_level(uid, gid)
        if login == 1:  # 今天第一次登陆
            max_barrel = Context.Data.get_game_attr_int(uid, gid, 'barrel_level', 1)
            cache_barrel_multi = cls.trans_barrel_level(gid, max_barrel)
            Context.Daily.set_daily_data(uid, gid, 'cache_barrel_multi', cache_barrel_multi)

            # 登陆用户携带量统计
            kvs = Context.Data.get_game_attrs_dict(uid, gid, ['chip', 'diamond', 'coupon'])
            pipe_args = []
            for k, v in kvs.iteritems():
                pipe_args.append('login.carrying.volume.%s' % k)
                pipe_args.append(v)
            if vip_level > 0:
                pipe_args.append('daily.pay.active.player')
                pipe_args.append(1)
            if pipe_args:
                channel_id = Context.Data.get_attr(uid, 'channelid')
                Context.Stat.mincr_daily_data(channel_id, *pipe_args)
                Context.Stat.mincr_daily_user_data(channel_id, uid, *pipe_args)

        if vip_level >= 6:
            bulletin = 1
            nick = Context.Data.get_attr(uid, 'nick')
            nick = Context.hide_name(nick)
            led = u'高手来袭！<color=#00FF00FF>VIP%d</color>玩家<color=#00FF00FF>%s</color>强势登录，空域争霸一触即发！' % (vip_level, nick)
            mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
            mou.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
            Context.GData.broadcast_to_system(mou)

        status = Context.RedisCache.hash_get_int('smart_game:%d' % uid, 'status', 0)
        if status > 0:
            game_info = Context.RedisCache.hash_get_json('smart_game:%d' % uid, 'game_info')
            if game_info:
                gameId = game_info.get('gid', 0)
                if gameId > 0:
                    token = Context.RedisCache.hash_get('smart_game:%d' % uid, 'token')
                    mon = MsgPack(Message.MSG_SYS_SMART_GAME_TOKEN | Message.ID_ACK)
                    url = Context.Configure.get_game_item(gid, 'smart_game_ddz.config')
                    mon.set_param('url', url)
                    mon.set_param('gid', gameId)
                    mon.set_param('token', token)
                    Context.GData.send_to_connect(uid, mon)

        for i in range(14, 15+1):
            mo = MsgPack(Message.MSG_SYS_MONTH_REWARD | Message.ID_ACK)
            success, left_days = props.BirdProps.use_new_month_card(uid, gid, i)
            if success:
                if i == 14:
                    product_id = '102001'
                else:
                    product_id = '102002'
                product_config = Context.Configure.get_game_item_json(gid, 'product.config')
                product_info = product_config.get(product_id)
                conf = product_info.get('content')
                reward = props.BirdProps.issue_rewards(uid, gid, conf, 'new.month.card' + str(product_id), True)
                mo.set_param('cid', i)
                mo.set_param('final', reward)
                Context.GData.send_to_connect(uid, mo)

    @classmethod
    def deal_login_level(cls, uid, gid):
        login_level = cls.login_level
        createTime = Context.Data.get_attr(uid, 'createTime')
        create_time = Time.str_to_timestamp(createTime[:10], '%Y-%m-%d')
        days = (Time.current_ts() - create_time)/(3600*24)
        if days <= 0:
            return
        for k,v in login_level.items():
            if days >= v[0] and days <= v[1]:
                login_level = Context.Stat.get_user_data(gid, uid, 'login_level_%d'%k)
                login_level = Tool.to_int(login_level, 0)
                if login_level <= 0:
                    Context.Stat.incr_user_data(uid, gid, 'login_level_%d' % k)
                    channel_id = Context.Data.get_attr(uid, 'channelid')
                    Context.Stat.incr_daily_time_data(channel_id, createTime[:10], 'login_level_%d' % k)
                break
        return

    @classmethod
    def check_bankrupt(cls, uid, gid):
        benefit_times, bankrupt_ts = Context.Daily.get_daily_data(uid, gid, 'benefit_times', 'bankrupt_ts')
        benefit_times = Tool.to_int(benefit_times, 0)
        wait, which = None, None
        if bankrupt_ts:  # 已经在破产状态, 未领取
            which = benefit_times + 1
            wait = int(bankrupt_ts) - Time.current_ts()
            if wait < 0:
                wait = 0
        else:
            conf = Context.Configure.get_game_item_json(gid, 'benefit.config')
            vip_level = BirdAccount.get_vip_level(uid, gid)
            total_times = conf['reward'][vip_level]['times']
            if benefit_times < total_times:
                wait = conf['wait'][benefit_times]
                bankrupt_ts = Time.current_ts() + wait
                Context.Daily.set_daily_data(uid, gid, 'bankrupt_ts', bankrupt_ts)
                which = benefit_times + 1

        mo = MsgPack(Message.BIRD_MSG_BANKRUPT | Message.ID_NTF)
        mo.set_param('userId', uid)
        if wait is not None:
            mo.set_param('wait', wait)
        if which is not None:
            mo.set_param('which', which)  # 可以领取哪一次

        return mo

    @classmethod
    def issue_benefit(cls, uid, gid, reward):
        rewards = reward
        keys = [uid, gid, Time.tomorrow_start_ts(), len(rewards)]
        keys.extend(rewards)
        result = Context.RedisCluster.execute_lua_alias(uid, 'issue_benefit', *keys)
        if result[0] <= 0:
            return False

        pipe_args = []
        pipe_args.append('in.chip.benefit.reward')
        pipe_args.append(result[1])
        channel_id = Context.Data.get_attr(uid, 'channelid', '1001_0')
        Context.Stat.mincr_daily_data(channel_id, *pipe_args)  # 本日充值数据写入
        Context.Stat.mincr_daily_user_data(channel_id, uid, *pipe_args)
        Context.Stat.mincr_user_data(uid, gid, *pipe_args)

        # 添加救济金
        #real, final = Context.UserAttr.incr_chip(uid, gid, result[1], 'benefit')
        #Context.Log.report('chip.update: [%s, %s, %s, issue.benefit, {}]' % (uid, gid, result[1]))
        #shit = Context.UserAttr.get_shit(uid, gid, 0)
        return {
            'which': result[0],         # 领取第几次
            'total': len(rewards),
            'reward': result[1],
            'chip': result[1],
        }


if __name__ == '__main__':
    Context.init_with_redis_key('127.0.0.1:6379:0')
    print BirdAccount.get_exp_info(20001, 2, 0)
    print BirdAccount.get_exp_info(20001, 2, 10)
    print BirdAccount.get_exp_info(20001, 2, 1111)
    print BirdAccount.get_exp_info(20001, 2, 1600000)
    print BirdAccount.get_exp_info(20001, 2, 1700000)
