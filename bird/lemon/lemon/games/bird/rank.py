#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-12-17

from props import BirdProps
from account import BirdAccount
from lemon.entity.rank import Rank
from framework.util.tool import Tool
from framework.util.tool import Time
from framework.context import Context
from framework.entity.const import Message
from framework.entity.msgpack import MsgPack


class BirdRank(Rank):
    def get_ranks(self, uid, gid, mi):
        rank_name = mi.get_param('rank')
        if not rank_name:
            rank_name = ['chip', 'exp', 'egg']
        elif isinstance(rank_name, (str, unicode)):
            rank_name = [rank_name]

        start = mi.get_param('start', 0)
        end = mi.get_param('end', 49)
        if start < 0 or end < start:
            return
        if end - start > 49:
            end = start + 49

        mo = MsgPack(Message.MSG_SYS_RANK_LIST | Message.ID_ACK)
        rank_list, mine = {}, {}
        if 'chip' in rank_name:
            _, rank_list['chip'] = self.get_chip_rank_list(uid, gid, start, end)
        if 'exp' in rank_name:
            _, rank_list['exp'] = self.get_exp_rank_list(uid, gid, start, end)
        if 'egg' in rank_name:
            _, rank_list['egg'] = self.get_egg_rank_list(uid, gid, start, end)
        if 'love' in rank_name:
            rank, rank_list['love'] = self.get_love_rank_list(uid, gid, start, end)
            if rank is None:
                rank = self.get_rank(uid, gid, 'love')
            if rank is not None:
                mine['rank'] = rank
        if 'day' in rank_name:
            rank_list['day'] = self.__get_three_day_match_rank_list(uid, gid)

        mo.update_param(rank_list)
        if 'chip' in rank_list or 'exp' in rank_list or 'egg' in rank_list:
            _info = self.__get_user_info(uid, gid)
            mine.update(_info)
            if 'egg' in rank_list:
                mine['egg'] = BirdProps.get_egg_count(uid, gid)
        if mine:
            mo.set_param('mine', mine)
        return mo

    def get_chip_rank_list(self, uid, gid, start, end):
        """
        头像, vip等级, 昵称, 游戏等级, 鸟蛋
        """
        rank = None
        _list = self.get_rank_list(gid, 'chip', start, end)
        for i, item in enumerate(_list):
            _list[i] = item[2]
            if uid == item[0]:
                rank = i
        return rank, _list

    def get_exp_rank_list(self, uid, gid, start, end):
        """
        头像, vip等级, 昵称, 游戏等级, 经验值
        """
        rank = None
        _list = self.get_rank_list(gid, 'exp', start, end)
        for i, item in enumerate(_list):
            _list[i] = item[2]
            if uid == item[0]:
                rank = i
        return rank, _list

    def get_love_rank_list(self, uid, gid, start, end):
        """
        昵称、等级、最近公益时间、累计公益次数
        """
        rank = None
        _list = self.get_rank_list(gid, 'love', start, end)
        for i, item in enumerate(_list):
            _list[i] = item[2]
            if uid == item[0]:
                rank = i
        return rank, _list

    def get_egg_rank_list(self, uid, gid, start, end):
        """
        头像, vip等级, 昵称, 游戏等级, egg
        """
        rank = None
        _list = self.get_rank_list(gid, 'egg', start, end)
        for i, item in enumerate(_list):
            _list[i] = item[2]
            if uid == item[0]:
                rank = i
        return rank, _list

    def __get_user_info(self, uid, gid):
        game_attr = ['chip', 'exp']
        chip, exp = Context.Data.get_game_attrs(uid, gid, game_attr)
        chip = Tool.to_int(chip, 0)
        exp = Tool.to_int(exp, 0)
        user_attr = ['nick', 'avatar', 'sex']
        nick, avatar, sex = Context.Data.get_attrs(uid, user_attr)
        sex = Tool.to_int(sex, 0)
        level = BirdAccount.get_vip_level(uid, gid)
        return {
            'uid': uid,
            'chip': chip,
            'exp': exp,
            'sex': sex,
            'nick': nick,
            'avatar': avatar,
            'vip': level
        }

    def get_match_rank(self, uid, gid, name, ts=None):
        if ts is None:
            if name == 'day':
                ts = Time.current_ts()
            elif name == 'week':
                ts = Time.current_week_start_ts()
            else:
                ts = Time.current_month_start_ts()

        day = Time.timestamp_to_str(ts, '%Y-%m-%d')
        return self.get_rank(uid, gid, 'match.%s.%s' % (name, day))

    def get_match_score(self, uid, gid, name, ts=None):
        if ts is None:
            if name == 'day':
                ts = Time.current_ts()
            elif name == 'week':
                ts = Time.current_week_start_ts()
            else:
                ts = Time.current_month_start_ts()

        day = Time.timestamp_to_str(ts, '%Y-%m-%d')
        score = self.get_score(uid, gid, 'match.%s.%s' % (name, day))
        if score is not None:
            score = int(score) / 10000000000
        return score

    def add_match_rank(self, uid, gid, name, score, cache_string, ts=None):
        if ts is None:
            if name == 'day':
                ts = Time.current_ts()
            elif name == 'week':
                ts = Time.current_week_start_ts()
            else:
                ts = Time.current_month_start_ts()
        day = Time.timestamp_to_str(ts, '%Y-%m-%d')
        score = score * 10000000000 + (10000000000 - Time.current_ts())
        self.add(uid, gid, 'match.%s.%s' % (name, day), score, cache_string, 1000)

    def set_match_cache_info(self, gid, name, ts=None, *args, **kwargs):
        if ts is None:
            if name == 'day':
                ts = Time.current_ts()
            elif name == 'week':
                ts = Time.current_week_start_ts()
            else:
                ts = Time.current_month_start_ts()
        day = Time.timestamp_to_str(ts, '%Y-%m-%d')
        self.set_cache_info(gid, 'match.%s.%s' % (name, day), *args, **kwargs)

    def get_match_cache_info(self, gid, name, ts=None, *args):
        if ts is None:
            if name == 'day':
                ts = Time.current_ts()
            elif name == 'week':
                ts = Time.current_week_start_ts()
            else:
                ts = Time.current_month_start_ts()
        day = Time.timestamp_to_str(ts, '%Y-%m-%d')
        return self.get_cache_info(gid, 'match.%s.%s' % (name, day), *args)

    def get_day_match_rank_list(self, gid, start, end, ts=None):
        if ts is None:
            ts = Time.current_ts()
        day = Time.timestamp_to_str(ts, '%Y-%m-%d')
        _list = self.get_rank_list(gid, 'match.day.' + day, start, end)
        for i, item in enumerate(_list):
            _list[i] = item[2]
        return _list

    def get_week_match_rank_list(self, gid, start, end, ts=None):
        if ts is None:
            ts = Time.current_week_start_ts()
        day = Time.timestamp_to_str(ts, '%Y-%m-%d')
        _list = self.get_rank_list(gid, 'match.week.' + day, start, end)
        for i, item in enumerate(_list):
            _list[i] = item[2]
        return _list

    def get_month_match_rank_list(self, gid, start, end, ts=None):
        if ts is None:
            ts = Time.current_month_start_ts()
        day = Time.timestamp_to_str(ts, '%Y-%m-%d')
        _list = self.get_rank_list(gid, 'match.month.' + day, start, end)
        for i, item in enumerate(_list):
            _list[i] = item[2]
        return _list

    def __get_three_day_match_rank_list(self, uid, gid):
        rank_list = []
        now_ts = Time.current_ts()
        for _ in (0, 1, 2):
            now_ts = Time.next_days_ts(now_ts, -1)
            info = self.__get_one_day_match_rank_list(uid, gid, now_ts)
            rank_list.append(info)
        return rank_list

    def __get_one_day_match_rank_list(self, uid, gid, ts):
        info = {}
        reward_conf = self.get_match_cache_info(gid, 'day', ts, 'reward')
        if not reward_conf:
            return info

        reward_conf = Context.json_loads(reward_conf)
        rank_list = self.get_day_match_rank_list(gid, 0, 9, ts)
        if not rank_list:
            return info

        score = BirdRank.get_match_score(uid, gid, 'day', ts)
        if score:
            nick, sex = Context.Data.get_attrs(uid, ['nick', 'sex'])
            sex = Tool.to_int(sex, 0)
            info['mine'] = {
                'uid': uid,
                'score': score,
                'vip': BirdAccount.get_vip_level(uid, gid),
                'nick': nick,
                'sex': sex
            }
            rank = BirdRank.get_match_rank(uid, gid, 'day', ts)
            if rank is not None:
                if ts >= 1473264000:  # 从2016-09-08开始， 前几天不处理
                    rank = self.trans_to_fake_match_rank(gid, rank)
                if rank is not None and rank < 1000:
                    info['mine']['rank'] = rank
                    reward = self.get_match_day_reward_by_rank(rank, reward_conf)
                    if reward:
                        info['mine']['reward'] = BirdProps.convert_pid_count(reward)

        info['list'] = rank_list
        if len(info['list']) >= 10:
            for rank in (20, 50, 100, 300, 500, 1000):
                if ts >= 1473264000:    # 从2016-09-08开始， 前几天不处理
                    rank = self.trans_to_real_match_rank(gid, rank - 1)
                else:
                    rank -= 1
                if rank is not None:
                    rank_list = self.get_day_match_rank_list(gid, rank, rank, ts)
                    if not rank_list:
                        break
                    info['list'].append(rank_list[0])

        return self.__convert_award_list(gid, info, reward_conf)

    def __convert_award_list(self, gid, info, conf):
        show_rank = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 50, 100, 300, 500, 1000)
        length = min(len(show_rank), len(info['list']))
        for i in range(length):
            rank = show_rank[i] - 1
            one = info['list'][i]
            reward = self.get_match_day_reward_by_rank(rank, conf)
            if reward:
                one = Context.json_loads(one)
                one['reward'] = BirdProps.convert_pid_count(reward)
                info['list'][i] = one

        return info

    def get_match_day_reward_by_rank(self, rank, reward_conf):
        for item in reward_conf:
            if item['rank'][0] <= rank <= item['rank'][1]:
                return item['reward']

    def trans_to_fake_match_rank(self, gid, rank):
        conf = Context.Configure.get_game_item_json(gid, 'day.fake.rank')
        if rank >= (1000 - conf['fake_total']):
            return

        for left, _, count in conf['fake']:
            if rank < left:
                break
            rank += count
        return rank

    def trans_to_real_match_rank(self, gid, rank):
        conf = Context.Configure.get_game_item_json(gid, 'day.fake.rank')
        if rank >= conf['total']:
            return

        for left, _, count in conf['fake']:
            if left <= rank < _:
                return

        add = 0
        for left, _, count in conf['fake']:
            if rank < left:
                break
            add += count
        return rank - add

    def village_lv_rank_add(self, gid, exp, vid):
        key = 'rank:%d:village_lv' % gid
        exp = exp * 10000000000 + (10000000000 - Time.current_ts())
        Context.RedisMix.zset_add(key, exp, vid)

    def village_lv_rank_list(self, gid):
        key = 'rank:%d:village_lv' % gid
        res = Context.RedisMix.zset_revrange(key, 0, -1, withscores=True)
        return res[::2]

    def village_lv_rank_rem(self, gid, vid):
        key = 'rank:%d:village_lv' % gid
        Context.RedisMix.zset_rem(key, vid)


BirdRank = BirdRank()
