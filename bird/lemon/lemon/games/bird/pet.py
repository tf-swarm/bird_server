#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: Cuick

import random
from rank import BirdRank
from props import BirdProps
from account import BirdAccount
from framework.util.tool import Time
from framework.context import Context
from framework.entity.msgpack import MsgPack
from framework.entity.const import Message
from framework.util.tool import Tool
from newtask import NewTask


class BirdPet(object):
    def full_lv_pet(self, uid, gid):
        for petId in self.pet_ids()['s']:
            info = self.get_pet(uid, gid, petId)
            if not info:
                continue
            for [_nu, _exp] in info:
                if self.level_info(gid, _exp) == 30:
                    return True
        return False

    def use_info(self, uid, gid):
        key = 'pet:%d:%d' % (gid, uid)
        u_petId, u_nu = Context.RedisCluster.hash_mget(uid, key, 'use_pid', 'use_nu')
        if not u_petId:
            return 0, 0, 0
        u_petId = int(u_petId)

        if u_petId in self.pet_ids()['ac']:
            count = self.get_pet(uid, gid, u_petId)
            if count:
                return u_petId, 0, 0
        elif u_petId in self.pet_ids()['s']:
            info = self.get_pet(uid, gid, u_petId)
            for [_nu, _exp] in info:
                if _nu == int(u_nu):
                    return u_petId, int(u_nu), int(_exp)
        return 0, 0, 0

    def addition(self, uid, gid, info=None):
        conf = Context.Configure.get_game_item_json(gid, 'pet.config')
        if info is None:
            u_petId, u_nu, exp = self.use_info(uid, gid)
        else:
            u_petId, u_nu, exp = info
        if not u_petId:
            return 0

        if u_petId in self.pet_ids()['ac']:
            count = self.get_pet(uid, gid, u_petId)
            if not count:
                return 0
            for pet_info in conf['pet_info']:
                if pet_info['id'] == u_petId:
                    return pet_info['jjcAdd']
        elif u_petId in self.pet_ids()['s']:
            lv = self.level_info(gid, exp)
            for pet_info in conf['pet_info']:
                if pet_info['id'] == u_petId:
                    a = pet_info['jjcAdd'] + pet_info['jjcLvAdd'] * (lv - 1)
                    return a

    def config(self, uid, gid):
        conf = Context.Configure.get_game_item_json(gid, 'pet.config')
        return conf

    def get_pet_conf(self, petId, conf):
        for x in conf['pet_info']:
            if x['id'] == petId:
                return x

    def choice(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_PET_CHOICE | Message.ID_ACK)
        petId = mi.get_param('petId')
        nu = mi.get_param('nu')
        if petId in self.pet_ids()['ac']:
            count = self.get_pet(uid, gid, petId)
            if not count:
                return mo.set_error(1, 'id error')
        elif petId in self.pet_ids()['s']:
            info = self.get_pet(uid, gid, petId)
            have_pet = False
            for [_nu, _exp] in info:
                if _nu == nu:
                    have_pet = True
                    break
            if not have_pet:
                return mo.set_error(2, 'nu error')
        else:
            return mo.set_error(1, 'id error')
        key = 'pet:%d:%d' % (gid, uid)
        if not nu:
            nu = 0
        Context.RedisCluster.hash_mset(uid, key, 'use_pid', petId, 'use_nu', nu)
        return mo

    def up(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_PET_UP | Message.ID_ACK)
        nu = mi.get_param('nu')
        petId = mi.get_param('petId')
        propId = mi.get_param('propId')
        num = mi.get_param('num')
        if not num:
            return mo.set_error(1, 'num error')
        conf = Context.Configure.get_game_item_json(gid, 'pet.config')
        exp = self.get_pet(uid, gid, petId, nu=nu)
        if exp is None:
            return mo.set_error(2, 'id error')
        level = self.level_info(gid, exp)
        if level == 30:
            return mo.set_error(3, 'max level')
        up_exp = 0
        a_num = 0
        a_exp = 0
        max_exp = self.max_exp(gid)
        for [_eId, _num, _exp] in conf['up']:
            if _eId == propId:
                up_exp = _exp * (num / _num)
                a_num = _num
                a_exp = _exp
                break
        if not up_exp:
            return mo.set_error(4, 'args error')
        if exp+up_exp > max_exp:
            n = (max_exp - exp) / a_exp
            if (max_exp - exp) % a_exp:
                n += 1
            num = n * a_num

        real, final = BirdProps.incr_props(uid, gid, propId, -num, 'pet.up')
        if real != -num:
            return mo.set_error(5, 'not enough')
        ex = self.on_up(uid, gid, nu, petId, up_exp)

        p_conf = self.get_pet_conf(petId, conf)
        lv = self.level_info(gid, ex)
        self.update_pet_rank(uid, gid, p_conf['level'], lv, petId)

        mo.set_param('exp', ex)
        return mo

    def on_up(self, uid, gid, nu, petId, exp):
        key = 'pet:%d:%d' % (gid, uid)
        info = Context.RedisCluster.hash_get_json(uid, key, 'pet_count.' + str(petId))
        ex = 0
        for index, [_nu, _exp] in enumerate(info):
            if nu == _nu:
                ex = _exp + exp
                info[index][1] = _exp + exp
        Context.RedisCluster.hash_set(uid, key, 'pet_count.' + str(petId), Context.json_dumps(info))
        return ex

    '''
    def compose(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_PET_COMPOSE | Message.ID_ACK)
        conf = Context.Configure.get_game_item_json(gid, 'pet.config')
        petId1 = mi.get_param('p1')
        petId2 = mi.get_param('p2')
        p1_conf = self.get_pet_conf(petId1, conf)
        count1 = self.get_pet(uid, gid, petId1)
        if petId1 == petId2:
            if not p1_conf or p1_conf['level'] not in [2, 3]:
                return mo.set_error(1, 'id error')
            if count1 < 2:
                return mo.set_error(2, 'count error')
        else:
            p2_conf = self.get_pet_conf(petId2, conf)
            if not p1_conf or not p2_conf or p1_conf['level'] not in [2, 3] \
                    or p2_conf['level'] not in [2, 3]:
                return mo.set_error(1, 'id error')
            count2 = self.get_pet(uid, gid, petId2)
            if count1 < 1 or count2 < 1:
                return mo.set_error(2, 'count error')

        for x in conf['compose']:
            if p1_conf['level'] == x[0]:
                compose_conf = x
                break
        count = compose_conf[1]
        real, final = Context.UserAttr.incr_chip(uid, gid, -count, 'pet.compose')
        if real != -count:
            return mo.set_error(3, 'not enough')
        if petId1 == petId2:
            self.add_pet(uid, gid, petId1, count=-2)
        else:
            self.add_pet(uid, gid, petId1, count=-1)
            self.add_pet(uid, gid, petId2, count=-1)
        if random.random() <= compose_conf[2]:
            _petId = random.choice(compose_conf[3])
        else:
            _petId = random.choice([petId1, petId2])
        self.add_pet(uid, gid, _petId)
        mo.set_param('petId', _petId)
        return mo
    '''

    def pet_info(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_PET_INFO | Message.ID_ACK)
        ac_count = []
        s_info = []
        for petId in self.pet_ids()['ac']:
            count = self.get_pet(uid, gid, petId)
            if count:
                ac_count.append([petId, count])
        for petId in self.pet_ids()['s']:
            info = self.get_pet(uid, gid, petId)
            if info:
                # 排序
                _info = sorted(info, key=lambda p: p[1])
                for [_nu, _exp] in _info:
                    s_info.append([petId, _nu, _exp])

        u_petId, u_nu, _ = self.use_info(uid, gid)
        if u_petId:
            mo.set_param('u_p', u_petId)
            if u_nu:
                mo.set_param('u_n', u_nu)
        if ac_count:
            mo.set_param('ac', ac_count)
        if s_info:
            mo.set_param('s', s_info)
        return mo

    def max_exp(self, gid):
        conf = Context.Configure.get_game_item_json(gid, 'pet.config')
        exp = 0
        for _exp in conf['exp']:
            exp += _exp
        return exp

    def level_info(self, gid, exp):
        conf = Context.Configure.get_game_item_json(gid, 'pet.config')
        a = 0
        level = 1
        for _exp in conf['exp']:
            a += _exp
            if exp >= a:
                level += 1
                continue
            break
        return level

    def hatch_quicken(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_HATCH_QUICKEN | Message.ID_ACK)
        eId = mi.get_param('eId')
        if eId not in BirdProps.pet_egg_ids():
            return mo.set_error(1, 'id error')
        self.up_hatch(uid, gid)

        egg_conf = BirdProps.get_config_by_id(gid, eId)
        hTime = self.get_egg_hTime(uid, gid, eId)
        if not hTime:
            return mo.set_error(2, 'not in hatching')
        now_ts = Time.current_ts()
        _t = egg_conf['hTime'] - (now_ts - hTime)
        count = _t / egg_conf['quicken'] + 1
        real, final = Context.UserAttr.incr_diamond(uid, gid, -count,
                                                    'pet.hatch_quicken')
        if real != -count:
            return mo.set_error(3, 'not enough')
        NewTask.get_diamond_consume_task(uid, count)
        self.set_egg_hTime(uid, gid, eId, hTime=1)
        mo.set_param('d', count)
        return mo

    def hatch_egg(self, uid, gid, mi):
        # 孵化蛋
        mo = MsgPack(Message.MSG_SYS_HATCH_EGG | Message.ID_ACK)
        eId = mi.get_param('eId')
        if eId not in BirdProps.pet_egg_ids():
            return mo.set_error(1, 'id error')
        now_ts = Time.current_ts()
        egg_conf = BirdProps.get_config_by_id(gid, eId)
        self.up_hatch(uid, gid)
        hTime = self.get_egg_hTime(uid, gid, eId)
        if hTime and hTime + egg_conf['hTime'] > now_ts:
            return mo.set_error(2, 'on hatching')
        key = 'props:%d:%d' % (gid, uid)
        num = Context.RedisCluster.hash_get(uid, key, eId)
        if not num or num <= 0:
            return mo.set_error(3, 'egg not enough')
        self.set_egg_hTime(uid, gid, eId)
        return mo

    def up_hatch(self, uid, gid):
        # 刷新蛋孵化信息
        eIds = BirdProps.pet_egg_ids()
        now_ts = Time.current_ts()
        for eId in eIds:
            hTime = self.get_egg_hTime(uid, gid, eId)
            if not hTime:
                continue
            egg_conf = BirdProps.get_config_by_id(gid, eId)
            if hTime + egg_conf['hTime'] > now_ts:
                continue
            # 减蛋
            BirdProps.incr_props(uid, gid, eId, -1, 'pet.up_hatch')
            # 设置孵化时间为0
            self.set_egg_hTime(uid, gid, eId, hTime=0)
            # 加宠物
            petIds = egg_conf['petId']
            petId = random.choice(petIds)
            self.add_pet(uid, gid, petId)

    def pet_ids(self):
        return {
            'ac': [110, 111, 120, 121, 130, 131],
            's': [140, 141]
        }

    def add_pet(self, uid, gid, petId, count=1):
        key = 'pet:%d:%d' % (gid, uid)
        if petId in self.pet_ids()['s']:
            info = Context.RedisCluster.hash_get_json(uid, key, 'pet_count.' + str(petId))
            if not info:
                info = []
            now_ts = Time.current_ts()
            info.append([now_ts, 0])
            Context.RedisCluster.hash_set(uid, key, 'pet_count.' + str(petId), Context.json_dumps(info))
        else:
            Context.RedisCluster.hash_incrby(uid, key, 'pet_count.' + str(petId), count)
        conf = Context.Configure.get_game_item_json(gid, 'pet.config')
        p_conf = self.get_pet_conf(petId, conf)
        rank_lv = p_conf['level']
        if rank_lv == 1:
            rank_lv = 3
        elif rank_lv == 3:
            rank_lv = 1
        self.update_pet_rank(uid, gid, p_conf['level'], 1, petId)

    def pet_rank_info(self, uid, gid):
        score = BirdRank.get_score(uid, gid, 'pet')
        if score is not None:
            score = int(score) / 10000000000
            pet_type_lv = score / 100
            pet_lv = score % 100
            return pet_type_lv, pet_lv
        else:
            return 0, 0

    def update_pet_rank(self, uid, gid, pet_type_lv, pet_lv, petId):
        user_attr = ['nick', 'sex']
        nick, sex = Context.Data.get_attrs(uid, user_attr)
        sex = Tool.to_int(sex, 0)
        vip_level = BirdAccount.get_vip_level(uid, gid)

        cache = {
            'uid': uid,
            'sex': sex,
            'nick': nick,
            'vip': vip_level,
            'petId': petId
        }
        cache_string = Context.json_dumps(cache)
        _pet_type_lv, _pet_lv = self.pet_rank_info(uid, gid)
        if pet_type_lv > _pet_type_lv or (pet_type_lv == _pet_type_lv and pet_lv > _pet_lv):
            score = pet_type_lv * 100 + pet_lv
            score = score * 10000000000 + (10000000000 - Time.current_ts())
            BirdRank.add(uid, gid, 'pet', score, cache_string, 1000)

    def get_pet(self, uid, gid, petId, nu=None):
        key = 'pet:%d:%d' % (gid, uid)
        if petId in self.pet_ids()['ac']:
            return Context.RedisCluster.hash_get_int(uid, key, 'pet_count.' + str(petId), 0)
        else:
            info = Context.RedisCluster.hash_get_json(uid, key, 'pet_count.' + str(petId))
            if not info:
                info = []
            if not nu:
                return info
            exp = None
            for [_nu, _exp] in info:
                if nu == int(_nu):
                    exp = int(_exp)
            return exp

    def get_egg_hTime(self, uid, gid, eId):
        key = 'pet:%d:%d' % (gid, uid)
        hTime = Context.RedisCluster.hash_get_int(uid, key, 'hTime.' + str(eId), 0)
        return hTime

    def set_egg_hTime(self, uid, gid, eId, hTime=None):
        if hTime is None:
            hTime = Time.current_ts()
        key = 'pet:%d:%d' % (gid, uid)
        Context.RedisCluster.hash_set(uid, key, 'hTime.' + str(eId), hTime)


BirdPet = BirdPet()
