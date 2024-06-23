#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: cui

import random
from framework.context import Context
from framework.entity.msgpack import MsgPack
from framework.entity.const import Message
from framework.util.tool import Time
from account import BirdAccount
from lemon.games.bird.newtask import NewTask


class BirdPokeMole(object):
    def in_poker_mole(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_IN_POKE_MOLE | Message.ID_ACK)
        lock = BirdAccount.check_global_lock(uid, gid)
        if lock:
            return mo.set_error(1, u'您当前正在%s游戏中，请稍后再试' % lock['name'])
        return mo

    def get_config(self, uid, gid):
        _conf = Context.Configure.get_game_item_json(gid, 'poke_mole.config')
        conf = Context.copy_json_obj(_conf)
        for x in conf['hammer']:
            if x.get('drop') and x['id'] != 7:
                del x['drop']
            del x['id']
        del conf['online_num']
        del conf['coupon']
        return conf

    '''def poke_mole(self, uid, gid, mi):
        # 打地鼠
        # 获取当前场景
        # id 是否对应当前场景
        # 如果是普通场景
        # 扣钱 加钱
        # 如果是鸟蛋潮
        # 加钱
        mo = MsgPack(Message.MSG_SYS_POKE_MOLE | Message.ID_ACK)
        h_id = mi.get_param('i')
        conf = Context.Configure.get_game_item_json(gid, 'poke_mole.config')
        if h_id > 8 or h_id < 1:
            return mo.set_error(1, 'id error')
        h_conf = conf['hammer'][h_id-1]
        info = self.get_info(uid, gid, conf)
        scene_type, chip_ts, chip_num, mp_chip, mp_hammer, coupon_num = info

        if scene_type == 2 and h_id != 7:
            return mo.set_error(1, 'id error')
        if 4 <= h_id <= 6 and mp_hammer >= conf['mp_hammer']:
            return mo.set_error(4, u'能量已满')
        if h_id <= 6:
            price = h_conf['price']
            real, final = Context.UserAttr.incr_chip(uid, gid, -price,
                                                     'game.poke.mole')
            if real != -price:
                return mo.set_error(2, 'lack chip')

        key = "poke_mole:%d:%d" % (gid, uid)
        drop = 0
        vip_level = BirdAccount.get_vip_level(uid, gid)
        drop_x = 1
        cf = 0
        if conf['vip'].get(vip_level):
            drop_x += conf['vip'].get(vip_level)

        if 1 <= h_id <= 6:
            drop = self.drop(h_conf)
            if drop:
                if h_id == 6:
                    drop *= drop_x
                real, final = Context.UserAttr.incr_chip(uid, gid, drop,
                                                         'game.poke.mole')
                if drop > 0:
                    NewTask.get_chip_task(uid, drop, 'game.poke.mole')
            # 紫金锤额外掉落话费卷
            if drop and h_id == 6:
                if random.random() <= conf['coupon'][1] and\
                        coupon_num+conf['coupon'][0] <= conf['coupon'][2]:
                    coupon = conf['coupon'][0]
                    _, cf = Context.UserAttr.incr_coupon(uid, gid,
                                                         conf['coupon'][0],
                                                         'game.poke.mole')
                    if coupon_num:
                        Context.RedisCluster.hash_incrby(uid, key, 'coupon',
                                                         coupon_num+coupon)
                    else:
                        Context.RedisCluster.hash_mset(uid, key, 'coupon', coupon,
                                                       'coupon_ts', Time.current_ts())
            if h_id <= 3:
                ff = Context.RedisCluster.hash_incrby(uid, key, 'mp_chip',
                                                 price)
                Context.Stat.incr_daily_data(gid, 'poke_mole:mp_chip',
                                             price-drop)
                mo.set_param('mc', ff)
            else:
                ff = Context.RedisCluster.hash_incrby(uid, key, 'mp_hammer',
                                                 price)
                Context.Stat.incr_daily_data(gid, 'poke_mole:mp_hammer',
                                             price-drop)
                mo.set_param('mh', ff)
            Context.Stat.incr_daily_data(gid, 'poke_mole:chip', price-drop)
        elif h_id == 7:
            drop = h_conf['drop'] * drop_x
            real, final = Context.UserAttr.incr_chip(uid, gid, drop,
                                                     'game.poke.mole')
            if drop > 0:
                NewTask.get_chip_task(uid, drop, 'game.poke.mole')
            Context.RedisCluster.hash_incrby(uid, key, 'chip_num', 1)
            Context.Stat.mincr_daily_data(gid, 'poke_mole:mp_chip', -drop,
                                          'poke_mole:chip', -drop)
        else:  # h_id == 8:
            if mp_hammer < conf['mp_hammer']:
                return mo.set_error(3, 'lack mp_hammer')
            drop = self.drop(h_conf)
            real, final = Context.UserAttr.incr_chip(uid, gid, drop,
                                                     'game.poke.mole')
            if drop > 0:
                NewTask.get_chip_task(uid, drop, 'game.poke.mole')
            Context.RedisCluster.hash_set(uid, key, 'mp_hammer', 0)
            Context.Stat.mincr_daily_data(gid, 'poke_mole:mp_hammer', -drop,
                                          'poke_mole:chip', -drop)
        if drop:
            mo.set_param('c', drop)
            mo.set_param('h', mi.get_param('h'))

        if drop >= 1000000:
            name = [u'木锤', u'石锤', u'铁锤', u'银锤', u'金锤', u'紫金锤', u'木锤', u'雷神锤']
            v = Context.Data.get_attrs(uid, ['nick'])
            bulletin = 2
            led = u'恭喜%s在打地鼠中使用%s获得了%s鸟蛋！' % (unicode(v[0], 'utf-8'), name[h_id-1], drop)
            mo1 = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
            mo1.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
            Context.GData.broadcast_to_system(mo1)
        if cf:
            mo.set_param('co', coupon)
            mo.set_param('cf', cf)
        mo.set_param('fc', final)
        mo.set_param('i', h_id)
        return mo
        '''

    def drop(self, conf):
        r = random.random()
        num = 0
        for x in conf['drop']:
            num += x[1]
            if num >= r:
                return x[0]
        return 0

    def get_info(self, uid, gid, conf):
        key = "poke_mole:%d:%d" % (gid, uid)
        kvs = Context.RedisCluster.hash_getall(uid, key)

        chip_ts = int(kvs.get('chip_ts', 1))
        mp_chip = int(kvs.get('mp_chip', 0))
        mp_hammer = int(kvs.get('mp_hammer', 0))
        chip_num = int(kvs.get('chip_num', 0))
        _scene_type = int(kvs.get('scene_type', 1))
        _coupon_ts = int(kvs.get('coupon_ts', 1))
        _coupon = int(kvs.get('coupon', 0))

        scene_type = 1
        if _scene_type == 2 and chip_ts + conf['hammer'][6]['lo'] > Time.current_ts()\
                and chip_num < conf['hammer'][6]['max_num']:
            scene_type = 2
        if _scene_type == 2 and scene_type == 1:
            Context.RedisCluster.hash_mset(uid, key, 'scene_type', 1,
                                           'mp_chip', 0, 'chip_num', 0)
            mp_chip = 0
            chip_num = 0
        if not Time.is_today(Time.timestamp_to_str(_coupon_ts)):
            _coupon = 0
        return scene_type, chip_ts, chip_num, mp_chip, mp_hammer, _coupon

    def poker_mole_info(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_POKE_MOLE_INFO | Message.ID_ACK)
        conf = Context.Configure.get_game_item_json(gid, 'poke_mole.config')
        info = self.get_info(uid, gid, conf)
        scene_type, chip_ts, chip_num, mp_chip, mp_hammer, _ = info
        if scene_type == 2:
            mo.set_param('s', scene_type)
            mo.set_param('ts', chip_ts)
        mo.set_param('cp', mp_chip)
        mo.set_param('hp', mp_hammer)
        return mo

    def poke_mole_ol(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_POKE_MOLE_OL | Message.ID_ACK)
        conf = Context.Configure.get_game_item_json(gid, 'poke_mole.config')
        key = 'poke_mole:%d' % gid
        num, ts = Context.RedisMix.hash_mget(key, 'num', 'ts')
        _ts = Time.current_ts()
        if not ts or _ts > int(ts)+conf['online_num'][2]*60:
            num = random.randint(conf["online_num"][0], conf["online_num"][1])
            Context.RedisMix.hash_mset(key, 'num', num, 'ts', _ts)
        else:
            num = int(num)
        num = num + random.randint(0, 8)-4
        mo.set_param('ol', num)
        return mo

    def change_scene(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_POKE_MOLE_CHANGE | Message.ID_ACK)
        key = "poke_mole:%d:%d" % (gid, uid)
        scene_type = mi.get_param('s')
        conf = Context.Configure.get_game_item_json(gid, 'poke_mole.config')
        info = self.get_info(uid, gid, conf)
        _scene_type, chip_ts, chip_num, mp_chip, mp_hammer, _ = info
        if scene_type == 1:
            if _scene_type == 2:
                Context.RedisCluster.hash_mset(uid, key, 'scene_type', 1,
                                               'mp_chip', 0, 'chip_num', 0)
        else:  # scene_type == 2
            if _scene_type == 2:
                return mo.set_error(1, 'id error')
            if mp_chip < conf['mp_chip']:
                return mo.set_error(2, 'lack mp_chip')
            Context.RedisCluster.hash_mset(uid, key, 'scene_type', 2,
                                           'chip_ts', Time.current_ts())
        return mo


BirdPokeMole = BirdPokeMole()
