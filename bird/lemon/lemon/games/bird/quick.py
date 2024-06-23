#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-23

import random
from const import Enum
from const import Message
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Tool
from lemon.entity.quick import Quick
from lemon.entity.account import Account
from framework.entity.msgpack import MsgPack
from props import BirdProps
from account import BirdAccount
from mail import Mail


class BirdQuick(Quick):
    def onMessage(self, cmd, uid, gid, mi):
        mo = None
        if cmd == Message.MSG_SYS_QUICK_START | Message.ID_REQ:
            mo = self.__on_quick_start(uid, gid, mi)
        elif cmd == Message.MSG_SYS_QUICK_TABLE_INFO | Message.ID_REQ:
            mo = self.__get_table_info(uid, gid, mi)
        elif cmd == Message.MSG_SYS_QUICK_VILLAGE_TABLE | Message.ID_REQ:
            mo = self.__get_village_table(uid, gid, mi)

        #-----------------------VIP---------------------------------------
        elif cmd == Message.MSG_SYS_VIP_TABLE_CREATE | Message.ID_REQ:
            mo = self.__create_vip_table(uid, gid, mi)
        elif cmd == Message.MSG_SYS_VIP_TABLE_LIST | Message.ID_REQ:
            mo = self.__get_vip_table_all(uid, gid)
        elif cmd == Message.MSG_SYS_VIP_TABLE_REFRESH | Message.ID_REQ:
            mo = self.__on_refresh_vip_table_list(uid, gid, mi)
        elif cmd == Message.MSG_SYS_VIP_TABLE_JOIN | Message.ID_REQ:
            mo = self.__on_join_vip_table(uid, gid, mi)
        #-----------------------VIP---------------------------------------


        #----------------------MATCH--------------------------------------
        elif cmd == Message.MSG_SYS_MATCH_READY | Message.ID_REQ:
            mo = self.__start_match(uid, gid, mi)
        elif cmd == Message.MSG_SYS_MATCH_START | Message.ID_REQ:
            mo = self.__enter_match_table(uid, gid, mi)
        elif cmd == Message.MSG_SYS_MATCH_QUIT | Message.ID_REQ:
            mo = self.__quit_match_enter(uid, gid, mi)
        elif cmd == Message.MSG_SYS_MATCH_GET_STATUS | Message.ID_REQ:
            mo = self.__get_player_match_status(uid, gid, mi)
        # ----------------------MATCH--------------------------------------

        if isinstance(mo, MsgPack):
            Context.GData.send_to_connect(uid, mo)

    def __check_location(self, uid, gid, mo, now_ts):
        result, location = Context.Online.get_location(uid, gid)
        if not result:
            return False, mo.set_error(Enum.quick_start_failed_unknown, 'info illegal')
        if location:
            is_valid = True
            status = location['status']
            fresh_time = location['fresh_ts']
            if status == Enum.location_status_dispatch and now_ts - fresh_time > 30:
                is_valid = False

            if not is_valid:
                Context.Log.info('check data status, kick off', uid, gid, location)
                res = self.__kick_off(uid, gid, location['table_id'])
                Context.Log.info('check data status, kick off', uid, gid, res)
            else:   # maybe reconnect
                mo.set_param('serverId', location['serverId'])
                mo.set_param('roomType', location['room_type'])
                mo.set_param('tableId', location['table_id'])
                mo.set_param('seatId', location['seat_id'])
                return False, mo
        return True, mo

    def __get_table_list(self, gid, room_type, play_mode):
        key = 'relax_quick:%d:%d:%d' % (gid, room_type, play_mode)
        table_list = Context.RedisCache.set_range(key)
        return (int(tid) for tid in table_list)

    def __on_quick_start(self, uid, gid, mi):

        Context.Log.info(uid, 'req quick start with', mi)
        mo = MsgPack(Message.MSG_SYS_QUICK_START | Message.ID_ACK)
        room_type = mi.get_param('roomType', 0)
        play_mode = mi.get_param('playMode', Enum.play_mode_common)

        status = Context.RedisCache.hash_get_int('smart_game:%d' % uid, 'status', 0)
        if status > 0:
            return mo.set_error(0, u"你正在进行第三方小游戏，请稍后再试")

        now_ts = Time.current_ts()
        res1, res2 = self.__check_location(uid, gid, mo, now_ts)
        if not res1:
            return res2

        if room_type in [201, 202, 203]:
            play_mode = Enum.play_mode_common
        elif room_type in[209]:
            play_mode = Enum.play_mode_vip

        chip = Context.UserAttr.get_chip(uid, gid, 0)
        barrel_level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level')

        barrel_new_room = Tool.to_int(Context.Configure.get_game_item_json(gid, 'barrel.new.room'), 7)
        if barrel_level < barrel_new_room:
            room_type = 200
        room_type, desc = self.__find_available_room(uid, gid, chip, room_type)
        # 如果返回的room_type不是房间号，返回error。
        if room_type not in (200, 201, 202, 203, 211, 231):
            return mo.set_error(room_type, desc)

        if play_mode > Enum.play_mode_village or play_mode < Enum.play_mode_common:
            return mo.set_error(110, 'error play mode')

        # 有区号 表示 选得是高手场 手动选房
        area_id = mi.get_param('r', 0)
        _t_id = mi.get_param('t', 0)
        _table_id = 0

        # 分配玩家
        leave_limit = Context.Data.get_game_attr_json(uid, gid, 'leave_limit')
        limit_tid_list = []
        limit_t = False
        if leave_limit:
            table_limit_times = Tool.to_int(Context.Configure.get_game_item_json(gid, 'table.limit.times'), 20)
            limit_dict = {}
            for k,v in leave_limit.items():
                if now_ts - int(v) < table_limit_times:
                    limit_t = True
                    limit_tid_list.append(int(k))
                    limit_dict[str(k)] = v
            Context.Data.set_game_attr(uid, gid, 'leave_limit', Context.json_dumps(limit_dict))

        # 房间选择需要重新写
        table_list = self.__get_table_list(gid, room_type, play_mode)
        for table_id in table_list:
            if limit_t and table_id in limit_tid_list:
                continue

            key = 'relax_table:%d:%d' % (gid, table_id)
            attrs = ['status', 'fresh_ts', 'serverId', 'seat0', 'seat1', 'seat2', 'seat3']

            kvs = Context.RedisCache.hash_mget_as_dict(key, *attrs)
            if len(attrs) != len(kvs):
                Context.Log.error('get table info failed', uid, gid, room_type, table_id, kvs)
                continue

            server_id = int(kvs['serverId'])
            if server_id < 0:
                Context.Log.info('table server_id error', uid, gid, room_type, table_id, server_id)
                continue

            fresh_time = int(kvs['fresh_ts'])

            if now_ts - fresh_time > 300:
                self.__check_table(gid, room_type, table_id, now_ts)

            seat_id = self.__join_table(uid, gid, room_type, play_mode, table_id)
            if seat_id < 0:
                Context.Log.error('join_table failed!', uid, gid, room_type, table_id)
                continue

            Context.Online.set_location(uid, gid, server_id, room_type, table_id, seat_id, 0, now_ts,
                                        play_mode=play_mode)
            mo.set_param('serverId', server_id)
            mo.set_param('roomType', room_type)
            mo.set_param('tableId', table_id)
            mo.set_param('seatId', seat_id)
            mo.set_param('playMode', play_mode)
            Context.Log.info('join table', uid, gid, server_id, room_type, table_id, server_id, play_mode)
            return mo

        # new table
        table_id = self.get_free_table(gid)
        server_id = self.__select_server(uid, gid, table_id, room_type)
        if not server_id:
            Context.Log.error('select server failed', uid, gid, room_type)
            return mo.set_error(Enum.quick_start_failed_unknown, 'no server found')


        self.__create_table(gid, room_type, play_mode, table_id, server_id, now_ts)
        seat_id = self.__join_table(uid, gid, room_type, play_mode, table_id)
        if seat_id < 0:
            Context.Log.error('join_table failed!', uid, gid, room_type, table_id)
            return mo.set_error(Enum.quick_start_failed_unknown, 'json table failed')

        Context.Online.set_location(uid, gid, server_id, room_type, table_id, seat_id, 0, now_ts, play_mode=play_mode)
        mo.set_param('serverId', server_id)
        mo.set_param('roomType', room_type)
        mo.set_param('tableId', table_id)
        mo.set_param('seatId', seat_id)
        mo.set_param('playMode', play_mode)
        Context.Log.info('create location info', uid, gid, server_id, room_type, table_id, seat_id, play_mode)
        return mo

    def __find_available_room(self, uid, gid, chip, room_type):
        room_config = Context.Configure.get_room_config(gid)
        barrel_level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level', 1)
        vip = BirdAccount.get_vip_level(uid, gid)
        if room_type:
            # room
            for conf in room_config:
                if room_type == conf['room_type']:
                    chip_min = conf.get('chip_min', -1)
                    if chip_min > 0 and chip < chip_min:
                        return Enum.quick_start_failed_chip_small, u'鸟蛋不足'
                    chip_max = conf.get('chip_max', -1)
                    if chip > chip_max > 0:
                        return Enum.quick_start_failed_chip_big, u'鸟蛋限制'
                    min_vip = conf.get('vip_limit', -1)
                    if vip < min_vip:
                        return Enum.quick_start_failed_vip_limit, u'vip限制'

                    level_min = conf.get('level_min', -1)
                    if level_min > 0 and barrel_level < level_min:
                        return Enum.quick_start_failed_barrel_small, u'炮倍不足，1000炮倍才可以进入竞技场'
                    level_max = conf.get('level_max', -1)
                    if barrel_level > level_max > 0:
                        return Enum.quick_start_failed_barrel_big, u'炮倍限制'
                    return room_type, ''

                return room_type, ''

        # 自动匹配房间, 不包括比赛
        rcs = set()
        for conf in room_config:
            chip_min = conf.get('chip_min', -1)
            if chip_min > 0 and chip < chip_min:
                continue
            chip_max = conf.get('chip_max', -1)
            if chip > chip_max > 0:
                continue
            level_min = conf.get('level_min', -1)
            if level_min > 0 and barrel_level < level_min:
                continue
            level_max = conf.get('level_max', -1)
            if barrel_level > level_max > 0:
                continue
            rcs.add(conf['room_type'])
        if not rcs:
            return Enum.quick_start_failed_unknown, u'未知错误'
        else:
            rcs = sorted(rcs)
            if len(rcs) == 2:
                return rcs[0], ''
            return rcs[-1], ''

    def __kick_off(self, uid, gid, tid):
        if tid > 0:
            res = Context.RedisCache.execute_lua_alias('kick_off', uid, gid, 4, tid)
        else:
            res = Context.RedisCache.execute_lua_alias('kick_off', uid, gid, 4, 0)
        return res

    def __check_vip_table(self, uid, gid, table_id):
        key = 'relax_table:%d:%d' % (gid, table_id)
        room_type = Context.RedisCache.hash_get(key, 'room_type')
        if Tool.to_int(room_type, 0) != 209:
            return False
        attrs = ['seat0', 'seat1', 'seat2', 'seat3']
        values = Context.RedisCache.hash_mget(key, *attrs)
        for i in values:
            uid = Tool.to_int(i, 0)
            if uid > 1000000:
                return True
        self.__kick_off(uid, gid, table_id)
        return False

    def __check_table(self, gid, room_type, table_id, now_ts):
        attrs = ['seat0', 'seat1', 'seat2', 'seat3']
        key = 'table:%d:%d' % (gid, table_id)
        values = Context.RedisCache.hash_mget(key, *attrs)
        for attr, value in zip(attrs, values):
            if value is None:
                Context.Log.error(table_id, 'table info not find field', attr)
                return False
            uid = int(value)
            if uid <= 0:
                continue
            result, location = Context.Online.get_location(uid, gid)
            if not result or not location:
                continue
            if table_id != location['table_id']:
                res = self.__kick_off(uid, gid, location['table_id'])
                Context.Log.error('kick off user', uid, gid, room_type, table_id, res, location)
                continue

            status = location['status']
            fresh_time = location['fresh_ts']
            if status == Enum.location_status_dispatch:
                if now_ts - fresh_time > 15*60:
                    res = self.__kick_off(uid, gid, table_id)
                    Context.Log.error('kick off user', uid, gid, room_type, table_id, res, location)
            return True

    def __join_table(self, uid, gid, room_type, play_mode, table_id):
        attrs = [uid, gid, room_type, table_id, 4, play_mode]
        res = Context.RedisCache.execute_lua_alias('join_table', *attrs)
        Context.Log.info('user join table', uid, gid, room_type, table_id, res)
        return res[0]

    def __select_server(self, uid, gid, table_id, room_type):
        if gid not in Context.GData.map_room_type:
            Context.Log.error('no game_server found', uid, gid)
            return False
        if room_type not in Context.GData.map_room_type[gid]:
            Context.Log.error('no room_type found', uid, gid, room_type)
            return False
        ss = Context.GData.map_room_type[gid][room_type]
        server_id = ss[table_id % len(ss)]
        if server_id not in Context.GData.map_server_info:
            Context.Log.error('not found the server', uid, gid, room_type, server_id)
            return False
        return server_id

    def __create_table(self, gid, room_type, play_mode, table_id, server_id, now_ts, opener=None, vt_id=None, vid=None):
        key = 'relax_table:%d:%d' % (gid, table_id)
        kvs = {
            'serverId': server_id,
            'room_type': room_type,
            'play_mode': play_mode,
            'status': Enum.table_status_free,
            'seat0': 0,
            'seat1': 0,
            'seat2': 0,
            'seat3': 0,
            'fresh_ts': now_ts,
            'vid': vid,
        }
        if opener:
            kvs['opener'] = opener
            kvs['vt_id'] = vt_id

        barrel_max = 500
        relax_config = Context.Configure.get_room_config(gid)
        for conf in relax_config:
            if room_type == conf['room_type']:
                barrel_max = conf.get('barrel_max1', 500)
        table_pool = barrel_max * 1250
        kvs['table_pool'] = table_pool
        Context.RedisCache.hash_mset(key, **kvs)
        return True

    def __get_table_info(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_QUICK_TABLE_INFO | Message.ID_ACK)
        area_id = mi.get_param('r', 0)
        if not area_id:
            area_id = 1001

        table_info = []
        area_info = []
        area_key = 'area:%d:%d' % (gid, area_id)
        kvs = Context.RedisCache.hash_getall(area_key)
        play_mode = Enum.play_mode_task
        table_list1 = self.__get_table_list(gid, 203, play_mode)
        table_list2 = self.__get_table_list(gid, 203, play_mode)
        table_list3 = self.__get_table_list(gid, 203, play_mode)
        table_list4 = self.__get_table_list(gid, 203, play_mode)
        table_l = [table_list1, table_list2, table_list3, table_list4]

        full_tables = []
        full_table_info = kvs.get("full_table_info")
        now = Time.current_ts()
        if full_table_info:
            full_tables = Context.json_loads(full_table_info)
            if now - full_tables[0] >= 30 * 60:
                full_tables = []

        table_ids = []
        for num, table_list in enumerate(table_l):
            _table_list = []
            for xx in table_list:
                _table_list.append(xx)
            num += 1
            for _t in range(1, 51):
                if _t in table_ids:
                    continue
                if _t in full_tables:
                    table_ids.append(_t)
                    table_info.append([_t, 4])
                    continue
                t_id = kvs.get(str(_t))
                if not t_id:
                    continue
                if int(t_id) in _table_list:
                    table_info.append([_t, num])
                    table_ids.append(_t)
        table_ids1 = [now]
        if not full_tables and len(table_info) < 25:
            l = random.randint(10, 15)
            while True:
                r = random.randint(1, 50)
                if r in table_ids:
                    continue
                table_ids1.append(r)
                table_ids.append(r)
                table_info.append([r, 4])
                if len(table_ids1) > l:
                    break
            Context.RedisCache.hash_set(area_key, 'full_table_info', Context.json_dumps(table_ids1))

        if area_id == 1001:
            for _a in range(1001, 1005):
                area_key = 'area:%d:%d' % (gid, _a)
                kvs = Context.RedisCache.hash_getall(area_key)
                nu = 0
                for num, table_list in enumerate(table_l):
                    _table_list = []
                    for xx in table_list:
                        _table_list.append(xx)
                    num += 1
                    for _t in range(1, 51):
                        t_id = kvs.get(str(_t))
                        if not t_id:
                            continue
                        if int(t_id) in _table_list:
                            nu += num
                full_table_info = kvs.get("full_table_info")
                now = Time.current_ts()
                if full_table_info:
                    full_tables = Context.json_loads(full_table_info)
                    if now - full_tables[0] < 30 * 60:
                        nu += (len(full_tables)-1)*4
                area_info.append([_a, nu])
        area_info1 = []
        for [_a, num] in area_info:
            num = num/50 + 1
            if num == 5:
                num = 4
            if num == 0:
                num = 1
            area_info1.append([_a, num])
        mo.set_param('r', area_info1)
        mo.set_param('t', table_info)
        return mo

    def __get_village_table(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_QUICK_VILLAGE_TABLE | Message.ID_ACK)
        data = Context.Data.get_game_attrs(uid, gid, ['vid'])
        vid = data[0]
        if not vid:
            return mo.set_error(8, '您所在公会已解散或您已被踢出公会')

        key = 'village_room:%s:%s' % (gid, vid)
        _kvs = Context.RedisCache.hash_getall(key)
        kvs = {}
        for k, v in _kvs.items():
            v = int(v)
            _id = v % 100000
            _state = v / 100000
            kvs[int(k)] = [_id, _state]

        play_mode = Enum.play_mode_village
        table_list1 = self.__get_table_list(gid, 231, play_mode)
        table_list2 = self.__get_table_list(gid, 231, play_mode)
        table_list3 = self.__get_table_list(gid, 231, play_mode)
        table_list4 = self.__get_table_list(gid, 231, play_mode)
        table_l = [table_list1, table_list2, table_list3, table_list4]

        table_ids = []
        table_info = []
        for num, table_list in enumerate(table_l):
            _table_list = []
            for xx in table_list:
                _table_list.append(xx)
            num += 1
            for _t in range(1, 51):
                if _t in table_ids:
                    continue
                if _t not in kvs:
                    continue
                [_id, _state] = kvs[_t]
                if _id in _table_list:
                    table_info.append([_t, _state,  num])
                    table_ids.append(_t)

        mo.set_param('table_info', table_info)
        return mo

    def __create_vip_table(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_VIP_TABLE_CREATE | Message.ID_ACK)
        vip_room_config = Context.Configure.get_game_item_json(gid, 'vip_room.config')
        vip_room_level = Tool.to_int(vip_room_config.get('vip_room_level'))
        vip = BirdAccount.get_vip_level(uid, gid)
        if vip < vip_room_level:
            return mo.set_error(1, u'你的VIP等级不足，无法开启VIP房。')

        room_type = mi.get_param('roomType')
        play_mode = mi.get_param('playMode', Enum.play_mode_vip)
        pwd = mi.get_param('pwd', None)
        multi = Tool.to_int(mi.get_param('multi'), 1)

        now_ts = Time.current_ts()

        barrel_level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level')
        barrel_multi = BirdAccount.trans_barrel_level(gid, barrel_level)
        if barrel_multi < multi:
            return mo.set_error(2, u'您设置的最低炮倍限制过高，请重新设置。')

        real, final = BirdProps.incr_props(uid, gid, 220, -1, 'create.vip.table')
        if real != -1:
            vip_room_price = Tool.to_int(vip_room_config.get('vip_room_price'))
            real, final = Context.UserAttr.incr_chip(uid, gid, -vip_room_price, 'create.vip.table')
            if real != -vip_room_price:
                return mo.set_error(3, u'鸟蛋不足，是否前往商城购买。')

        match_status = Context.MatchDB.get_match_player_status(uid)
        if match_status:
            mo.set_error(2, u'您正在竞技场中')
            Context.GData.send_to_connect(uid, mo)

        # 分配玩家
        leave_limit = Context.Data.get_game_attr_json(uid, gid, 'leave_limit')
        limit_tid_list = []
        limit_t = False
        if leave_limit:
            table_limit_times = Tool.to_int(Context.Configure.get_game_item_json(gid, 'table.limit.times'), 20)
            limit_dict = {}
            for k, v in leave_limit.items():
                if now_ts - int(v) < table_limit_times:
                    limit_t = True
                    limit_tid_list.append(int(k))
                    limit_dict[str(k)] = v
            Context.Data.set_game_attr(uid, gid, 'leave_limit', Context.json_dumps(limit_dict))
        table_list = self.__get_table_list(gid, room_type, play_mode)
        for table_id in table_list:
            if limit_t and table_id in limit_tid_list:
                continue

            key = 'relax_table:%d:%d' % (gid, table_id)
            attrs = ['status', 'fresh_ts', 'serverId', 'seat0', 'seat1', 'seat2', 'seat3', 'pwd']

            kvs = Context.RedisCache.hash_mget_as_dict(key, *attrs)
            #if len(attrs) != len(kvs):
            #    Context.Log.error('get table info failed', uid, gid, room_type, table_id, kvs)
            #    continue

            server_id = int(kvs.get('serverId', -1))
            if server_id < 0:
                Context.Log.info('table server_id error', uid, gid, room_type, table_id, server_id)
                continue

            Context.Log.debug('xxxx', table_id, kvs['seat0'], kvs['seat0'], kvs['seat0'], kvs['seat0'], kvs.get('pwd', None))
            if int(kvs['seat0']) != 0 or int(kvs['seat1']) != 0 \
                    or int(kvs['seat2']) != 0 or int(kvs['seat3']) != 0\
                    or kvs.get('pwd', None) is not None:
                continue

            fresh_time = int(kvs['fresh_ts'])
            if now_ts - fresh_time > 300:
                self.__check_table(gid, room_type, table_id, now_ts)

            if play_mode == Enum.play_mode_vip:
                key = 'relax_table:%d:%d' % (gid, table_id)
                kvs = {
                    'serverId': server_id,
                    'room_type': room_type,
                    'play_mode': play_mode,
                    'status': Enum.table_status_free,
                    'seat0': 0,
                    'seat1': 0,
                    'seat2': 0,
                    'seat3': 0,
                    'fresh_ts': now_ts,
                }
                kvs['pwd'] = pwd
                kvs['multi'] = multi
                Context.RedisCache.hash_mset(key, **kvs)

            seat_id = self.__join_table(uid, gid, room_type, play_mode, table_id)
            if seat_id < 0:
                Context.Log.error('join_table failed!', uid, gid, room_type, table_id)
                return mo.set_error(Enum.quick_start_failed_unknown, 'json table failed')
            Context.Online.set_location(uid, gid, server_id, room_type, table_id, seat_id, 0, now_ts,
                                        play_mode=play_mode)

            village_room_key = 'vip_room:%s' % (gid)
            Context.RedisCache.hash_set(village_room_key, table_id, uid)
            mo.set_param('serverId', server_id)
            mo.set_param('roomType', room_type)
            mo.set_param('tableId', table_id)
            mo.set_param('seatId', seat_id)
            return mo

        table_id = self.get_free_table(gid)
        server_id = self.__select_server(uid, gid, table_id, room_type)

        if play_mode == Enum.play_mode_vip:
            key = 'relax_table:%d:%d' % (gid, table_id)
            kvs = {
                'serverId': server_id,
                'room_type': room_type,
                'play_mode': play_mode,
                'status': Enum.table_status_free,
                'seat0': 0,
                'seat1': 0,
                'seat2': 0,
                'seat3': 0,
                'fresh_ts': now_ts,
            }
            kvs['pwd'] = pwd
            kvs['multi'] = multi
            Context.RedisCache.hash_mset(key, **kvs)

        self.__create_table(gid, room_type, play_mode, table_id, server_id, now_ts)
        seat_id = self.__join_table(uid, gid, room_type, play_mode, table_id)
        if seat_id < 0:
            Context.Log.error('join_table failed!', uid, gid, room_type, table_id)
            return mo.set_error(Enum.quick_start_failed_unknown, 'json table failed')
        Context.Online.set_location(uid, gid, server_id, room_type, table_id, seat_id, 0, now_ts, play_mode=play_mode)
        village_room_key = 'vip_room:%s' % (gid)
        Context.RedisCache.hash_set(village_room_key, table_id, uid)
        mo.set_param('serverId', server_id)
        mo.set_param('roomType', room_type)
        mo.set_param('tableId', table_id)
        mo.set_param('seatId', seat_id)
        return mo

    def __on_join_vip_table(self, uid, gid, mi):
        room_type = mi.get_param('roomType')
        play_mode = mi.get_param('playMode')
        table_id = mi.get_param('table_id')
        send_pwd = mi.get_param('pwd', None)
        mo = MsgPack(Message.MSG_SYS_VIP_TABLE_JOIN | Message.ID_ACK)

        pwd, multi = Context.RedisCache.hash_mget('relax_table:%d:%d' % (gid, int(table_id)), 'pwd', 'multi')
        if pwd:
            if str(pwd) != str(send_pwd):
                return mo.set_error(1, u'密码错误，请确认后重新输入。')
        if multi:
            barrel_level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level')
            barrel_multi = BirdAccount.trans_barrel_level(gid, barrel_level)
            if barrel_multi < int(multi):
                return mo.set_error(2, u'您的炮倍等级未达到该房间的最低炮倍要求，您可以在战斗中升级您的炮倍。')

        match_status = Context.MatchDB.get_match_player_status(uid)
        if match_status:
            mo.set_error(2, u'您正在竞技场中')
            Context.GData.send_to_connect(uid, mo)

        seat_id = self.__join_table(uid, gid, room_type, play_mode, table_id)
        server_id = self.__select_server(uid, gid, table_id, room_type)
        now_ts = Time.current_ts()
        if seat_id < 0:
            Context.Log.error('join_table failed!', uid, gid, room_type, table_id)
            return mo.set_error(Enum.quick_start_failed_unknown, u'房间人数已满')
        Context.Online.set_location(uid, gid, server_id, room_type, table_id, seat_id, 0, now_ts, play_mode=play_mode)
        mo.set_param('serverId', server_id)
        mo.set_param('roomType', room_type)
        mo.set_param('tableId', table_id)
        mo.set_param('seatId', seat_id)
        return mo

    def __get_vip_table_all(self, uid, gid):
        mo = MsgPack(Message.MSG_SYS_VIP_TABLE_LIST | Message.ID_ACK)
        table_info = self.__get_all_vip_table_date(uid, gid)
        mo.set_param('table_info', table_info)
        return mo

    def __get_all_vip_table_date(self, uid, gid):
        ret = Context.RedisCache.hash_getall('vip_room:2')
        data = []
        for i in ret:
            room_id = int(i)
            if not self.__check_vip_table(uid, gid, room_id):
                continue
            kvs = {'room_id':room_id}
            _kvs = Context.RedisCache.hash_getall('relax_table:2:%d'%room_id)
            if _kvs.has_key('pwd') and len(str(_kvs['pwd'])) >= 6:
                kvs['pwd'] = 1
            if _kvs.has_key('seat0'):
                id = int(_kvs['seat0'])
                if id > 1000000:
                    avatar = Context.Data.get_attr(id, 'avatar', '1')
                    kvs['seat0'] = {'id': id, 'avatar': avatar}
            if _kvs.has_key('seat1'):
                id = int(_kvs['seat1'])
                if id > 1000000:
                    avatar = Context.Data.get_attr(id, 'avatar', '1')
                    kvs['seat1'] = {'id': id, 'avatar': avatar}
            if _kvs.has_key('seat2'):
                id = int(_kvs['seat2'])
                if id > 1000000:
                    avatar = Context.Data.get_attr(id, 'avatar', '1')
                    kvs['seat2'] = {'id': id, 'avatar': avatar}
            if _kvs.has_key('seat3'):
                id = int(_kvs['seat3'])
                if id > 1000000:
                    avatar = Context.Data.get_attr(id, 'avatar', '1')
                    kvs['seat3'] = {'id': id, 'avatar': avatar}
            data.append(kvs)
        return data


    def __on_refresh_vip_table_list(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_VIP_TABLE_REFRESH | Message.ID_ACK)
        mou = MsgPack(Message.MSG_SYS_VIP_TABLE_LIST | Message.ID_ACK)
        table_data = self.__get_all_vip_table_date(uid, gid)

        room_list = mi.get_param('roomList')
        Context.Log.info('wzgt', room_list, table_data)

        Flag = False
        data = []

        if len(table_data) != len(room_list):
            mou.set_param('table_info', table_data)
            Context.GData.send_to_connect(uid, mou)
            return
        for i in room_list:
            table_id = i.get('room_id')
            if not self.__check_vip_table(uid, gid, table_id):
                mou.set_param('table_info', table_data)
                Context.GData.send_to_connect(uid, mou)
                return

            _kvs = Context.RedisCache.hash_getall('relax_table:2:%d' % table_id)
            if not _kvs:
                mou.set_param('table_info', table_data)
                Context.GData.send_to_connect(uid, mou)
                return

            seat0 = Tool.to_int(i.get('seat0'), 0)
            seat1 = Tool.to_int(i.get('seat1'), 0)
            seat2 = Tool.to_int(i.get('seat2'), 0)
            seat3 = Tool.to_int(i.get('seat3'), 0)

            kvs = {'room_id': table_id}
            if _kvs.has_key('pwd') and len(str(_kvs['pwd'])) >= 6:
                kvs['pwd'] = 1
            if _kvs.has_key('seat0'):
                id = Tool.to_int(_kvs['seat0'])
                if id != seat0:
                    Flag = True
                if id > 1000000:
                    avatar = Context.Data.get_attr(id, 'avatar', '1')
                    kvs['seat0'] = {'id': id, 'avatar': avatar}
            if _kvs.has_key('seat1'):
                id = Tool.to_int(_kvs['seat1'])
                if id != seat1:
                    Flag = True
                if id > 1000000:
                    avatar = Context.Data.get_attr(id, 'avatar', '1')
                    kvs['seat1'] = {'id': id, 'avatar': avatar}
            if _kvs.has_key('seat2'):
                id = Tool.to_int(_kvs['seat2'])
                if id != seat2:
                    Flag = True
                if id > 1000000:
                    avatar = Context.Data.get_attr(id, 'avatar', '1')
                    kvs['seat2'] = {'id': id, 'avatar': avatar}
            if _kvs.has_key('seat3'):
                id = Tool.to_int(_kvs['seat3'])
                if id != seat3:
                    Flag = True
                if id > 1000000:
                    avatar = Context.Data.get_attr(id, 'avatar', '1')
                    kvs['seat3'] = {'id': id, 'avatar': avatar}
            data.append(kvs)
        if not Flag:
            mo.set_param('empty', 0)
            return mo
        mo.set_param('table_info', data)
        return mo

    def __get_player_match_status(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_MATCH_GET_STATUS | Message.ID_ACK)
        match_info = Context.MatchDB.get_match_data('player', str(uid))
        if match_info: # 退出重进
            match_id = Tool.to_int(match_info.get('match_id'))
            level = Tool.to_int(match_info.get('level'))
            status = Tool.to_int(Context.MatchDB.get_match_data(str(level), match_id, 'status'), 0)
            table_id = Tool.to_int(match_info.get('table_id'))
            if status <= 1 or not table_id:
                mo.set_param('status', Enum.match_status_ready)
                Context.GData.send_to_connect(uid, mo)
                return
            mo = MsgPack(Message.MSG_SYS_MATCH_START | Message.ID_ACK)
            room_type = 211
            play_mode = Enum.play_mode_match

            seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7 = Context.MatchDB.get_match_seat_info(level, match_id)
            if uid in [seat0, seat1, seat2, seat3]:
                table_index = 0
            else:
                table_index = 1

            server_id = self.__select_server(uid, gid, table_id, room_type)
            seat_id = self.__join_table(uid, gid, room_type, play_mode, table_id)
            now_ts = Time.current_ts()
            Context.Online.set_location(uid, gid, server_id, room_type, table_id, seat_id, 0, now_ts,
                                        play_mode=play_mode)
            mo.set_param('serverId', server_id)
            mo.set_param('roomType', room_type)
            mo.set_param('tableId', table_id)
            mo.set_param('seatId', seat_id)
            mo.set_param('playMode', play_mode)
            mo.set_param('level', level)
            mo.set_param('match_id', match_id)
            mo.set_param('table_index', table_index)
            Context.GData.send_to_connect(uid, mo)
            return
        else:
            mo.set_param('status', 0)
            Context.GData.send_to_connect(uid, mo)
            return

    def __start_match(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_MATCH_READY | Message.ID_ACK)
        normal_config = Context.Configure.get_game_item_json(gid, 'match.normal.config')
        open_time_1 = Tool.to_int(normal_config['start_1'])
        close_time_1 = Tool.to_int(normal_config['end_1'])
        open_time_2 = Tool.to_int(normal_config['start_2'])
        close_time_2 = Tool.to_int(normal_config['end_2'])
        open = Tool.to_int(normal_config.get('open'), 1)
        now_ts = Time.datetime()
        if open <= 0 or now_ts.hour < open_time_1 or (now_ts.hour >= close_time_1 and now_ts.hour < open_time_2) or \
                now_ts.hour > close_time_2:
            return mo.set_error(3, u'竞技场尚未开启')
        vip = BirdAccount.get_vip_level(uid, gid)
        if vip < 1:
            return mo.set_error(1, u'你的VIP等级不足，无法开启进入竞技场。')

        level = mi.get_param('level')

        rank_reward = Context.Configure.get_game_item_json(gid, 'match.rank.reward')
        cost = Tool.to_int(rank_reward[str(level)]['cost'])
        real, final = Context.UserAttr.incr_chip(uid, gid, -cost, 'match.table.consume')
        if real != -cost:
            return mo.set_error(3, u'鸟蛋不足，是否前往商城购买。')

        match_id = self.get_free_match(gid, level) #获取可用的比赛房（没有会创建）
        seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7 = Context.MatchDB.get_match_seat_info(level, match_id)
        for k,v in enumerate([seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7]):
            keys = 'seat%d'%k
            if v <= 0:
                Context.MatchDB.set_match_data(str(level), match_id, keys, uid)
                break
        Context.MatchDB.set_match_data('player', str(uid), 'match_id', match_id)
        Context.MatchDB.set_match_data('player', str(uid), 'level', level)

        seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7 = Context.MatchDB.get_match_seat_info(level, match_id)
        seat_list = []
        for i in [seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7]:
            if i > 1000000:
                seat_list.append(i)
        if len(seat_list) >= 8: #房间人数已满
            for i in (seat_list):
                mo.set_param('status', Enum.match_status_enter)
                mo.set_param('level', level)
                mo.set_param('match_id', match_id)
                Context.GData.send_to_connect(i, mo)
            Context.MatchDB.set_match_data(str(level), str(match_id), 'status', Enum.match_status_enter)
        else:
            mo.set_param('status', Enum.match_status_ready)
            Context.GData.send_to_connect(uid, mo)
        return

    def __enter_match_table(self, uid, gid, mi):
        level = mi.get_param('level')
        match_id = mi.get_param('match_id')

        mo = MsgPack(Message.MSG_SYS_MATCH_START | Message.ID_ACK)
        db_match_id = Context.MatchDB.get_match_data('player', str(uid), 'match_id')
        if int(match_id) != Tool.to_int(db_match_id):
            return mo.set_error(Enum.quick_start_failed_unknown, 'match_id not through check')

        now_ts = Time.current_ts()
        room_type = 211
        play_mode = Enum.play_mode_match
        table_id, create, table_index = self.__get_user_table_id(uid, gid)
        server_id = self.__select_server(uid, gid, table_id, room_type)
        if create:
            self.__create_table(gid, room_type, play_mode, table_id, server_id, now_ts)
        seat_id = self.__join_table(uid, gid, room_type, play_mode, table_id)

        Context.MatchDB.set_match_data('player', str(uid), 'table_id', table_id)

        normal_config = Context.Configure.get_game_item_json(gid, 'match.normal.config')
        bullet = normal_config['bullet'][0]

        Context.MatchDB.set_match_data('player', str(uid), 'bullet', bullet)
        Context.MatchDB.set_match_data('player', str(uid), 'point', 0)

        if seat_id < 0:
            Context.Log.error('join_table failed!', uid, gid, room_type, table_id)
            return mo.set_error(Enum.quick_start_failed_unknown, 'json table failed')

        Context.Online.set_location(uid, gid, server_id, room_type, table_id, seat_id, 0, now_ts,
                                    play_mode=play_mode)
        mo.set_param('serverId', server_id)
        mo.set_param('roomType', room_type)
        mo.set_param('tableId', table_id)
        mo.set_param('seatId', seat_id)
        mo.set_param('playMode', play_mode)
        mo.set_param('level', level)
        mo.set_param('match_id', match_id)
        mo.set_param('table_index', table_index)
        Context.GData.send_to_connect(uid, mo)
        return

    def __get_user_table_id(self, uid, gid):
        match_id, level = Context.MatchDB.get_match_data('player', str(uid), 'match_id', 'level')
        create = False
        seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7 = Context.MatchDB.get_match_seat_info(level, match_id)
        if uid in [seat0, seat1, seat2, seat4]:
            table_id = Context.MatchDB.get_match_data(str(level), str(match_id), 'table_id_0')
            table_index = 0
            if int(table_id) <= 0:
                create = True
                table_id = self.get_match_free_table(gid)
                Context.MatchDB.set_match_data(str(level), str(match_id), 'table_id_0', table_id)
        else:
            table_id = Context.MatchDB.get_match_data(str(level), str(match_id), 'table_id_1')
            table_index = 1
            if int(table_id) <= 0:
                create = True
                table_id = self.get_match_free_table(gid)
                Context.MatchDB.set_match_data(str(level), str(match_id), 'table_id_1', table_id)
        return int(table_id), create, table_index

    def __quit_match_enter(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_MATCH_QUIT | Message.ID_ACK)
        match_id, level = Context.MatchDB.get_match_data('player', str(uid), 'match_id', 'level')
        if match_id == None or level == None:
            return mo.set_error(0, u'你还没有参加此次竞技场')
        Context.RedisMatch.delete('match:player:%d' % (uid))
        seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7 = Context.MatchDB.get_match_seat_info(level, match_id)
        match_num = 0
        for k, v in enumerate([seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7]):
            if v == uid:
                Context.MatchDB.set_match_data(str(level), str(match_id), 'seat%d'%k, 0)
                match_num += 1
            if v <= 1000000:
                match_num += 1
        match_rank_reward = Context.Configure.get_game_item_json(gid, 'match.rank.reward')
        cost = match_rank_reward[level]['cost']
        if match_num >= 8:
            Context.RedisMatch.delete('match:%s:%s' % (str(level), str(match_id)))

        times = Time.current_ts()
        reward_p = {'chip': cost}
        ret = Mail.add_mail(uid, gid, times, 11, reward_p, -1)
        if ret:
            Mail.send_mail_list(uid, gid)
        return mo.set_param('success', 1)

BirdQuick = BirdQuick()
