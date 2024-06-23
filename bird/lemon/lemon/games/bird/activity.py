#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-02-17

from task import BirdTask
import props
from framework.context import Context
from framework.util.tool import Tool
from framework.util.tool import Algorithm
from lemon.entity.activity import Activity
from framework.entity.msgpack import MsgPack
from framework.entity.const import Message


class BirdActivity(Activity):
    @classmethod
    def find_handler_by_type(cls, gid, atype):
        if atype == 100:
            return Activity100
        elif atype == 200:
            return Activity200
        elif atype == 300:
            return Activity300
        elif atype == 310:
            return Activity310
        elif atype == 320:
            return Activity320
        elif atype == 330:
            return Activity330
        elif atype == 340:
            return Activity340
        elif atype == 350:
            return Activity350
        elif atype == 360:
            return Activity360
        elif atype == 370:
            return Activity370
        elif atype == 380:
            return Activity380
        elif atype == 381:
            return Activity381
        elif atype == 382:
            return Activity382
        elif atype == 383:
            return Activity383

    def get_activity_title(self, gid):
        conf = Context.Configure.get_game_item_json(gid, 'activity.config')
        _list = []
        for act in conf['list']:
            state = self.check_time(act)
            if state == 1:
                _list.append(act['desc'])
        return {'ver': conf['version'], 'tip': conf['tip'], 'list': list(set(_list))}


BirdActivity = BirdActivity()


class Activity100(object):
    @classmethod
    def load_activity(cls, uid, gid, act, show=False):
        item = {'id': act['id'], 'type': act['type']}
        fields = ['cache_barrel_multi', 'win.chip', 'act.%d' % act['id']]
        cache_barrel_multi, win_chip, done = Context.Daily.get_daily_data(uid, gid, *fields)
        if cache_barrel_multi is None:
            return None
        win_chip = Tool.to_int(win_chip, 0)
        cache_barrel_multi = int(cache_barrel_multi)
        var = [cache_barrel_multi * act['var'][0], cache_barrel_multi * act['var'][1], win_chip]
        if done:
            state = 2
        elif win_chip >= var[0]:
            state = 1
        else:
            state = 0
        item['var'] = var
        item['state'] = state
        return item

    '''@classmethod
    def consume_activity(cls, uid, gid, act, mi):
        aid, atype = act['id'], act['type']
        key = 'act.%d' % aid
        fields = ['cache_barrel_multi', 'win.chip', key]
        cache_barrel_multi, win_chip, done = Context.Daily.get_daily_data(uid, gid, *fields)
        if cache_barrel_multi is None:
            return None
        cache_barrel_multi = int(cache_barrel_multi)
        mo = MsgPack(Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_ACK)
        if done:
            return mo.set_error(1, 'have consume')
        var = [cache_barrel_multi * act['var'][0], cache_barrel_multi * act['var'][1]]
        if not win_chip or int(win_chip) < var[0]:
            return mo.set_error(2, 'not done')
        Context.Daily.set_daily_data(uid, gid, key, var[1])
        real, final = Context.UserAttr.incr_chip(uid, gid, var[1], 'activity.reward', aid=aid, atype=atype)
        mo.set_param('id', aid)
        mo.set_param('reward', {'chip': real})
        mo.set_param('chip', final)
        return mo
        '''


class Activity200(object):
    @classmethod
    def load_activity(cls, uid, gid, act, show=False):
        times = Context.Data.get_game_attr_int(uid, gid, 'act_200_reward_times', 0)
        item = {'id': act['id'], 'type': act['type']}
        if times >= len(act['var']):
            state = 0
        else:
            count = Context.Daily.get_daily_data(uid, gid, 'act_200_reward')
            if count:
                state = 2
            else:
                state = 1
        item['var'] = times
        item['state'] = state
        return item

    @classmethod
    def consume_activity(cls, uid, gid, act, mi):
        mo = MsgPack(Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_ACK)
        times = Context.Data.get_game_attr_int(uid, gid, 'act_200_reward_times', 0)
        if times >= len(act['var']):
            return mo.set_error(1, 'already consume')

        aid, atype = act['id'], act['type']
        count = Context.Daily.get_daily_data(uid, gid, 'act_200_reward')
        if count:
            return mo.set_error(1, 'have reward')

        var = act['var']
        Context.Data.hincr_game(uid, gid, 'act_200_reward_times', 1)
        Context.Daily.set_daily_data(uid, gid, 'act_200_reward', var[times])
        real, final = Context.UserAttr.incr_diamond(uid, gid, var[times], 'activity.reward', aid=aid, atype=atype)
        mo.set_param('id', aid)
        mo.set_param('reward', {'diamond': real})
        mo.set_param('diamond', final)
        return mo


class Activity300(object):
    @classmethod
    def load_activity(cls, uid, gid, act, show=False):
        item = {'id': act['id'], 'type': act['type']}
        done, barrel_level = Context.Data.get_game_attrs(uid, gid, ['act.%d' % act['id'], 'barrel_level'])
        if done:
            state = 2
        else:
            barrel_level = Tool.to_int(barrel_level, 1)
            from account import BirdAccount
            multi = BirdAccount.trans_barrel_level(gid, barrel_level)
            if multi >= act['var'][0]:
                state = 1
            else:
                state = 0
        item['state'] = state
        return item
'''
    @classmethod
    def consume_activity(cls, uid, gid, act, mi):
        mo = MsgPack(Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_ACK)
        aid, atype, var = act['id'], act['type'], act['var']
        key = 'act.%d' % aid
        done, barrel_level = Context.Data.get_game_attrs(uid, gid, [key, 'barrel_level'])
        if done:
            return mo.set_error(1, 'have consume')

        barrel_level = Tool.to_int(barrel_level, 1)
        from account import BirdAccount
        multi = BirdAccount.trans_barrel_level(gid, barrel_level)
        if multi < var[0]:
            return mo.set_error(2, 'not done')

        Context.Data.set_game_attr(uid, gid, key, 1)
        props.BirdProps.issue_rewards(uid, gid, var[1], 'activity.reward', aid=aid, atype=atype)
        mo.set_param('id', aid)
        return mo
'''

class Activity310(object):
    @classmethod
    def load_activity(cls, uid, gid, act, show=False):
        item = {'id': act['id'], 'type': act['type']}
        done = Context.Daily.get_daily_data(uid, gid, 'act.%d' % act['id'])
        if done:
            state = 2
        else:
            from account import BirdAccount
            level = BirdAccount.get_vip_level(uid, gid)
            if level >= act['var']['vip']:
                state = 1
            else:
                state = 0
        item['state'] = state
        return item
'''
    @classmethod
    def consume_activity(cls, uid, gid, act, mi):
        mo = MsgPack(Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_ACK)
        aid, atype, var = act['id'], act['type'], act['var']
        key = 'act.%d' % aid
        done = Context.Daily.get_daily_data(uid, gid, key)
        if done:
            return mo.set_error(1, 'have consume')

        from account import BirdAccount
        level = BirdAccount.get_vip_level(uid, gid)
        if level < var['vip']:
            return mo.set_error(2, 'not done')

        Context.Daily.set_daily_data(uid, gid, key, 1)
        props.BirdProps.issue_rewards(uid, gid, var['reward'], 'activity.reward', aid=aid, atype=atype)
        mo.set_param('id', aid)
        return mo
'''

class Activity320(object):
    @classmethod
    def load_activity(cls, uid, gid, act, show=False):
        item = {'id': act['id'], 'type': act['type']}
        done, pay_total = Context.Daily.get_daily_data(uid, gid, 'act.%d' % act['id'], 'pay_total')
        if done:
            state = 2
        else:
            if pay_total:
                state = 1
            else:
                state = 0
        item['state'] = state
        return item
'''
    @classmethod
    def consume_activity(cls, uid, gid, act, mi):
        mo = MsgPack(Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_ACK)
        aid, atype, var = act['id'], act['type'], act['var']
        key = 'act.%d' % aid
        done, pay_total = Context.Daily.get_daily_data(uid, gid, key, 'pay_total')
        if done:
            return mo.set_error(1, 'have consume')

        if not pay_total:
            return mo.set_error(2, 'not done')

        Context.Daily.set_daily_data(uid, gid, key, 1)
        props.BirdProps.issue_rewards(uid, gid, var, 'activity.reward', aid=aid, atype=atype)
        mo.set_param('id', aid)
        return mo
'''

class Activity330(object):
    @classmethod
    def load_activity(cls, uid, gid, act, show=False):
        item = {'id': act['id'], 'type': act['type']}
        times, pay_total = Context.Daily.get_daily_data(uid, gid, 'act.%d' % act['id'], 'pay_total')
        pay_total = Tool.to_int(pay_total, 0)
        times = Tool.to_int(times, 0)
        total = pay_total / act['var']['unit'] + 1
        if times >= total or total == 0:
            state = 0
        else:
            state = 1
        item['state'] = state
        item['var'] = total - times
        return item
'''
    @classmethod
    def consume_activity(cls, uid, gid, act, mi):
        mo = MsgPack(Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_ACK)
        aid, atype, var = act['id'], act['type'], act['var']
        key = 'act.%d' % aid
        times, pay_total = Context.Daily.get_daily_data(uid, gid, key, 'pay_total')
        pay_total = Tool.to_int(pay_total, 0)
        times = Tool.to_int(times, 0)
        total = pay_total / var['unit'] + 1
        if times >= total:
            return mo.set_error(1, 'have consume')

        Context.Daily.incr_daily_data(uid, gid, key, 1)
        if times == 0:  # 第一次为free
            reward = var['free']
        else:
            reward = var['pay']
        _, which = Algorithm.choice_by_ratio(reward, 10000, func=lambda l: l[0])
        props.BirdProps.issue_rewards(uid, gid, which[1], 'activity.reward', aid=aid, atype=atype)
        mo.set_param('desc', which[2])
        mo.set_param('id', aid)
        mo.set_param('left', total - times - 1)
        return mo
'''

class Activity340(object):
    @classmethod
    def load_activity(cls, uid, gid, act, show=False):
        item = {'id': act['id'], 'type': act['type']}
        done, bird_301 = Context.Daily.get_daily_data(uid, gid, 'act.%d' % act['id'], 'bird.301')
        if done:
            state = 2
        elif bird_301:
            state = 1
        else:
            state = 0
        item['state'] = state
        return item
'''
    @classmethod
    def consume_activity(cls, uid, gid, act, mi):
        mo = MsgPack(Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_ACK)
        aid, atype, var = act['id'], act['type'], act['var']
        key = 'act.%d' % aid
        done, bird_301 = Context.Daily.get_daily_data(uid, gid, key, 'bird.301')

        if done:
            return mo.set_error(1, 'have consume')
        if not bird_301:
            return mo.set_error(2, 'not done')

        Context.Daily.set_daily_data(uid, gid, key, 1)
        props.BirdProps.issue_rewards(uid, gid, var, 'activity.reward', aid=aid, atype=atype)
        mo.set_param('id', aid)
        return mo
'''

class Activity350(object):
    @classmethod
    def load_activity(cls, uid, gid, act, show=False):
        item = {'id': act['id'], 'type': act['type']}
        done, cache_barrel_multi = Context.Daily.get_daily_data(uid, gid, 'act.%d' % act['id'], 'cache_barrel_multi')
        if done:
            state = 2
        else:
            degree = BirdTask.get_total_degree(uid, gid)
            if degree >= 100:
                state = 1
            else:
                state = 0
        if cache_barrel_multi:
            item['var'] = int(cache_barrel_multi) * 50
        else:
            item['var'] = 0
        item['state'] = state
        return item
'''
    @classmethod
    def consume_activity(cls, uid, gid, act, mi):
        mo = MsgPack(Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_ACK)
        aid, atype, var = act['id'], act['type'], act['var']
        key = 'act.%d' % aid
        done, cache_barrel_multi = Context.Daily.get_daily_data(uid, gid, key, 'cache_barrel_multi')

        if done:
            return mo.set_error(1, 'have consume')

        degree = BirdTask.get_total_degree(uid, gid)
        if degree < 100:
            return mo.set_error(2, 'not done')

        if cache_barrel_multi:
            var = Context.copy_json_obj(var)
            var['chip'] = int(cache_barrel_multi) * 50

        Context.Daily.set_daily_data(uid, gid, key, 1)
        props.BirdProps.issue_rewards(uid, gid, var, 'activity.reward', aid=aid, atype=atype)
        mo.set_param('id', aid)
        return mo
'''

class Activity360(object):
    @classmethod
    def load_activity(cls, uid, gid, act, show=False):
        from rank import BirdRank
        item = {'id': act['id'], 'type': act['type']}
        _vars = [one[0] for one in act['var']]
        score = BirdRank.get_score(uid, gid, act['key'])
        score = Tool.to_int(score, 0)
        if show:
            state_list = [0] * len(_vars)
        else:
            _fields = ['%d:%d' % (uid, _var) for _var in _vars]
            _states = BirdRank.get_cache_info(gid, act['key'], *_fields)
            state_list = []
            for _var, _state in zip(_vars, _states):
                if _state:
                    state_list.append(2)
                elif score and score >= _var:
                    state_list.append(1)
                else:
                    state_list.append(0)
        item['state'] = state_list
        if score:
            item['score'] = score
        else:
            item['score'] = 0
        rank_list = BirdRank.get_rank_list(gid, act['key'], 0, 9)
        if rank_list:
            for i, one in enumerate(rank_list):
                info = Context.json_loads(one[2])
                info['uid'] = int(one[0])
                info['score'] = int(one[1])
                rank_list[i] = info
            item['rank'] = rank_list
        return item

    @classmethod
    def handle_activity(cls, uid, gid, act, *props_list, **kwargs):
        info_map = {211: 1, 212: 2, 213: 4, 214: 8}
        total = 0
        for one in props_list:
            if one[0] in info_map:
                total += info_map[one[0]] * one[1]
        if total:
            nick, sex = Context.Data.get_attrs(uid, ['nick', 'sex'])
            sex = Tool.to_int(sex, 0)
            from rank import BirdRank
            BirdRank.incrby(uid, gid, act['key'], total, cache={'nick': nick, 'sex': sex})
'''
    @classmethod
    def consume_activity(cls, uid, gid, act, mi):
        from rank import BirdRank
        mo = MsgPack(Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_ACK)
        aid, atype = act['id'], act['type']
        score = BirdRank.get_score(uid, gid, act['key'])
        if score is None:
            return mo.set_error(1, u'未达到要求')

        score = int(score)
        _vars = [one[0] for one in act['var']]
        _fields = ['%d:%d' % (uid, _var) for _var in _vars]
        _states = BirdRank.get_cache_info(gid, act['key'], *_fields)
        for i, state in enumerate(_states):
            if state:
                continue
            if score >= _vars[i]:
                conf = act['var'][i]
                BirdRank.set_cache_info(gid, act['key'], '%d:%d' % (uid, conf[0]), 2)
                props.BirdProps.issue_rewards(uid, gid, conf[1], 'activity.reward', aid=aid, atype=atype, which=i)

        mo.set_param('id', aid)
        return mo
'''

class Activity370(object):
    @classmethod
    def load_activity(cls, uid, gid, act, show=False):
        item = {'id': act['id'], 'type': act['type']}
        key = 'game.%d.%s' % (gid, act['key'])
        _state = Context.RedisMix.hash_get_int(key, uid, 0)
        if _state:
            state = 2
        else:
            state = 1
        item['state'] = state
        return item

    @classmethod
    def consume_activity(cls, uid, gid, act, mi):
        mo = MsgPack(Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_ACK)
        aid = act['id']
        key = 'game.%d.%s' % (gid, act['key'])
        result = Context.RedisMix.hash_incrby(key, uid, 1)
        if result != 1:
            return mo.set_error(1, 'have consume')

        conf = Context.Configure.get_game_item_json(gid, 'shop.config')
        pids = [pid for pid in conf['chip']]
        pid_fields = ['product_' + str(pid) for pid in pids]
        pid_counts = Context.Data.get_game_attrs(uid, gid, pid_fields)
        rc_fields = []
        for pid, pid_count in zip(pids, pid_counts):
            if pid_count and int(pid_count) > 0:
                rc_fields.append('reset_' + str(pid))
        if rc_fields:
            kvs = dict.fromkeys(rc_fields, 1)
            Context.Data.set_game_attrs_dict(uid, gid, kvs)
        mo.set_param('id', aid)
        return mo


class Activity380(object):
    @classmethod
    def load_activity(cls, uid, gid, act, show=False):
        item = {'id': act['id'], 'type': act['type']}
        key = 'act.%d.%s' % (gid, act['key'])
        fileds = ['%d.%d' % (uid, i) for i in range(10)]
        values = Context.RedisMix.hash_mget(key, *fileds)
        from account import BirdAccount
        vip = BirdAccount.get_vip_level(uid, gid)
        # state_list = []
        # for i, value in enumerate(values):
        #     if value:
        #         state_list.append(2)
        #     elif vip >= i:
        #         state_list.append(1)
        #     else:
        #         state_list.append(0)
        # item['state'] = state_list
        state = 2
        for i, value in enumerate(values):
            if value:
                pass
            elif vip >= i:
                state = 1

        item['state'] = state
        item['vip'] = vip
        return item
'''
    @classmethod
    def consume_activity(cls, uid, gid, act, mi):
        mo = MsgPack(Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_ACK)
        aid, atype, var = act['id'], act['type'], act['var']
        from account import BirdAccount
        vip = BirdAccount.get_vip_level(uid, gid)
        key = 'act.%d.%s' % (gid, act['key'])
        fileds = ['%d.%d' % (uid, i) for i in range(10)]
        values = Context.RedisMix.hash_mget(key, *fileds)
        for i, value in enumerate(values):
            if value is None and vip >= i:
                Context.RedisMix.hash_set(key, '%d.%d' % (uid, i), 1)
                reward = var[str(i)]
                props.BirdProps.issue_rewards(uid, gid, reward, 'activity.reward', aid=aid, atype=atype, which=i)

        return mo
'''

class Activity381(object):
    @classmethod
    def load_activity(cls, uid, gid, act, show=False):
        item = {'id': act['id'], 'type': act['type']}
        shot_chip = Context.Daily.get_daily_data(uid, gid, 'shot.chip')
        shot_chip = Tool.to_int(shot_chip, 0)
        fields = []
        for one in act['var']:
            fields.append('act.%d.%d' % (act['id'], one[0]))
        values = Context.Daily.get_daily_data(uid, gid, *fields)
        # state_list = []
        # for i, value in enumerate(values):
        #     if value:
        #         state_list.append(2)
        #     elif shot_chip >= act['var'][i][0]:
        #         state_list.append(1)
        #     else:
        #         state_list.append(0)
        # item['state'] = state_list
        state = 2
        for i, value in enumerate(values):
            if value:
                pass
            elif shot_chip >= act['var'][i][0]:
                state = 1

        item['state'] = state
        item['chip'] = shot_chip
        return item

    @classmethod
    def handle_activity(cls, uid, gid, act, cost, **kwargs):
        Context.Daily.incr_daily_data(uid, gid, 'shot.chip', cost)

    '''@classmethod
    def consume_activity(cls, uid, gid, act, mi):
        mo = MsgPack(Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_ACK)
        aid, atype = act['id'], act['type']
        shot_chip = Context.Daily.get_daily_data(uid, gid, 'shot.chip')
        shot_chip = Tool.to_int(shot_chip, 0)
        fields = []
        for one in act['var']:
            fields.append('act.%d.%d' % (act['id'], one[0]))
        values = Context.Daily.get_daily_data(uid, gid, *fields)
        for one, field, value in zip(act['var'], fields, values):
            if value is None and shot_chip >= one[0]:
                Context.Daily.set_daily_data(uid, gid, field, 1)
                props.BirdProps.issue_rewards(uid, gid, one[1], 'activity.reward', aid=aid, atype=atype, which=one[0])

        return mo
    '''


class Activity382(object):
    @classmethod
    def load_activity(cls, uid, gid, act, show=False):
        item = {'id': act['id'], 'type': act['type']}
        chip = Context.UserAttr.get_chip(uid, gid, 0)
        item['state'] = 0 if chip < 20000 else 1
        item['chip'] = chip
        return item

    '''
    @classmethod
    def consume_activity(cls, uid, gid, act, mi):
        mo = MsgPack(Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_ACK)
        aid, atype, var = act['id'], act['type'], act['var']
        real, final = Context.UserAttr.incr_chip(uid, gid, -20000, 'activity.raffle', aid=aid, atype=atype)
        if real != -20000:
            return mo.set_error(1, u'鸟蛋不足')

        index, reward = Algorithm.choice_by_ratio(var, 10000, func=lambda l: l[0])
        rw = props.BirdProps.issue_rewards(uid, gid, reward[1], 'activity.reward', aid=aid, atype=atype, which=index)
        if 'chip' in rw:
            mo.set_param('chip', rw['chip'])
        else:
            mo.set_param('chip', final)
        mo.set_param('id', index)
        return mo
    '''

class Activity383(object):
    @classmethod
    def load_activity(cls, uid, gid, act, show=False):
        item = {'id': act['id'], 'type': act['type']}
        key = 'act.%d.%s' % (gid, act['key'])
        state = Context.Daily.get_daily_data(uid, gid, key)
        if not state:
            state = 1
        else:
            state = 2
        from account import BirdAccount
        vip = BirdAccount.get_vip_level(uid, gid)
        item['state'] = state
        item['vip'] = vip
        return item

    '''@classmethod
    def consume_activity(cls, uid, gid, act, mi):
        mo = MsgPack(Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_ACK)
        aid, atype, var = act['id'], act['type'], act['var']
        from account import BirdAccount
        vip = BirdAccount.get_vip_level(uid, gid)
        key = 'act.%d.%s' % (gid, act['key'])
        state = Context.Daily.get_daily_data(uid, gid, key)
        if not state:
            reward = var[str(vip)]
            props.BirdProps.issue_rewards(uid, gid, reward, 'activity.reward', aid=aid, atype=atype)
            Context.Daily.set_daily_data(uid, gid, key, 2)
        else:
            return mo.set_error(-1, 'already')
        return mo
        '''
