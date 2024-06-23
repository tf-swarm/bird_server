#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: hwz
# Create: 2018-09-13

from framework.context import Context
from framework.util.tool import Time, Tool

from framework.entity.msgpack import MsgPack
from framework.util.tool import Algorithm

token = 'aXh4b28ubWVAZ21haWwuY29tCg=='

PRIVATE_KEY_DICT = {
    '10000': '3hjjsf33232sdfsfksdf23'
}

DOUDIZHU_KEY = 'third_game:ddz'

class SmartGame(object):
    def getUserInfo(self, mi):
        game_id = mi.get_param('mgid', 0)
        uid = mi.get_param('uid', 0)
        # extend = mi.get_param('extend', '')
        token = Context.RedisCache.hash_get('smart_game:%d' % uid, 'token', '')
        sign = mi.get_param('sign', '')

        str_gid = str(game_id)
        if not PRIVATE_KEY_DICT.has_key(str_gid):
            ret = {'ret': 1001}
            return MsgPack(0, ret)

        nick = Context.Data.get_attr(uid, 'nick', '')
        if nick == None:
            ret = {'ret': 1001}
            return MsgPack(0, ret)

        private_key = PRIVATE_KEY_DICT.get(str_gid)
        data = {
            'mgid': game_id,
            'uid': uid,
            'token': token,
            'private_key': private_key,
        }
        if not self.check_sign(sign, data):
            ret = {'ret': 1002}
            return MsgPack(0, ret)

        status = Context.RedisCache.hash_get_int('smart_game:%d' % uid, 'status', 0)
        if status > 0:
            ret = {'ret': 1002}
            return MsgPack(0, ret)

        chip = Context.Data.get_game_attr_int(uid, 2, 'chip', 0)
        diamond = Context.Data.get_game_attr_int(uid, 2, 'diamond', 0)
        ret = {'ret': 0}
        ret['nick'] = nick
        ret['chip'] = chip
        ret['diamond'] = diamond

        Context.RedisCache.hash_set('smart_game:%d'%uid, 'status', 1)
        game_info = {'chip': chip, 'gid': game_id, 'diamond': diamond, 'ts': Time.current_ts()}
        Context.RedisCache.hash_set('smart_game:%d' % uid, 'game_info', Context.json_dumps(game_info))

        return MsgPack(0, ret)

    def notifyGameResult(self, mi):
        game_id = mi.get_param('mgid', 0)
        uid = mi.get_param('uid', 0)
        token = Context.RedisCache.hash_get('smart_game:%d' % uid, 'token', '')
        sign = mi.get_param('sign', '')

        str_gid = str(game_id)
        pid = mi.get_param('pid', 0)
        if not PRIVATE_KEY_DICT.has_key(str_gid):
            ret = {'ret': 1001}
            return MsgPack(0, ret)
        private_key = PRIVATE_KEY_DICT.get(str_gid)

        chip = mi.get_param('chip', 0)
        diamond = mi.get_param('diamond', 0)

        data = {
            'mgid': game_id,
            'uid': uid,
            'token': token,
            'private_key': private_key,
            'chip': chip,
            'diamond': diamond,
        }

        if not self.check_sign(sign, data):
            detail = {
                'success': 0,
                'ts': Time.current_ts(),
                'info':'check sign default'
            }
            self.set_detail_data(game_id, uid, pid, detail)

            ret = {'ret': 1002}
            return MsgPack(0, ret)

        status = Context.RedisCache.hash_get_int('smart_game:%d' % uid, 'status', 0)
        game_info = Context.RedisCache.hash_get_json('smart_game:%d' % uid, 'game_info', {})
        if status > 0 and game_info.get('gid') != game_id: # 游戏状态对不上
            detail = {
                'success': 0,
                'status': status,
                'gid':game_id,
                'real_gid':game_info.get('gid'),
                'ts': Time.current_ts(),
                'info':'gameId status not match'
            }
            self.set_detail_data(game_id, uid, pid, detail)
            ret = {'ret': 0}
            ret['chip'] = chip
            ret['diamond'] = diamond
            return MsgPack(0, ret)

        chip_win = mi.get_param('chip_win', 0)
        diamond_win = mi.get_param('diamond_win', 0)

        times = mi.get_param('time', 0)
        extend = mi.get_param('extend', '')
        g_base = mi.get_param('g_base', '')

        error = False
        if game_info.get('chip') + chip_win != chip:
            chip_win = chip - game_info.get('chip')
            error = True

        if game_info.get('diamond') + diamond_win != diamond:
            diamond_win = diamond - game_info.get('diamond')
            error = True

        game_info['chip'] = chip
        game_info['diamond'] = diamond
        Context.RedisCache.hash_set('smart_game:%d' % uid, 'game_info', Context.json_dumps(game_info))

        real, final = Context.UserAttr.incr_chip(uid, 2, chip_win, 'smart_game_%s'%(str(game_id)))
        if real != chip_win:# 金蛋不够
            detail = {
                'success': 0,
                'chip':chip,
                'chip_win': chip_win,
                'real_chip': Context.Data.get_game_attr_int(uid, 2, 'chip', 0),
                'ts': Time.current_ts(),
                'info': 'chip not enough'
            }
            self.set_detail_data(game_id, uid, pid, detail)
            ret = {'ret': 0}
            ret['chip'] = chip
            ret['diamond'] = diamond
            return MsgPack(0, ret)
        real, final = Context.UserAttr.incr_diamond(uid, 2, diamond_win, 'smart_game_%s'%(str(game_id)))
        if real != diamond_win:# 钻石不够
            detail = {
                'success': 0,
                'diamond':diamond,
                'diamond_win': diamond_win,
                'real_diamond': Context.Data.get_game_attr_int(uid, 2, 'diamond', 0),
                'ts': Time.current_ts(),
                'info':'diamond not enough'
            }
            self.set_detail_data(game_id, uid, pid, detail)
            ret = {'ret': 0}
            ret['chip'] = chip
            ret['diamond'] = diamond
            return MsgPack(0, ret)

        detail = {
            'success':1,
            'chip':chip,
            'w_chip':chip_win,
            'diamond': diamond,
            'w_diamond': diamond_win,
            'ts': Time.current_ts()
        }
        if error:# 异常订单标记
            detail['error'] = 1
        self.set_detail_data(game_id, uid, pid, detail)

        ret = {'ret': 0}
        ret['chip'] = chip
        ret['diamond'] = diamond
        return MsgPack(0, ret)

    def set_detail_data(self, gid, uid, pid, detail):
        if gid == 10000:
            keys = DOUDIZHU_KEY
        else:
            return
        db_keys = '%s:%s:%d' % (keys, Time.current_time('%Y-%m-%d'), uid)
        Context.Log.info('set_detail_data', db_keys, pid, detail)
        Context.RedisCache.hash_setnx(db_keys, pid, Context.json_dumps(detail))
        return


    def leave_game(self, mi):

        game_id = mi.get_param('mgid', 0)
        uid = mi.get_param('uid', 0)
        token = Context.RedisCache.hash_get('smart_game:%d' % uid, 'token', '')
        sign = mi.get_param('sign', '')
        pid_list = mi.get_param('pid_list', '')

        str_gid = str(game_id)
        if not PRIVATE_KEY_DICT.has_key(str_gid):
            ret = {}
            return MsgPack(0, ret)
        private_key = PRIVATE_KEY_DICT.get(str_gid)

        data = {
            'mgid': game_id,
            'uid': uid,
            'token': token,
            'private_key': private_key,
        }

        if not self.check_sign(sign, data):
            ret = {'ret': 1002}
            return MsgPack(0, ret)

        status = Context.RedisCache.hash_get_int('smart_game:%d' % uid, 'status', 0)
        game_info = Context.RedisCache.hash_get_json('smart_game:%d' % uid, 'game_info', {})
        if status > 0 and game_info.get('gid') != game_id:
            ret = {'ret': 1002}
            return MsgPack(0, ret)

        Context.RedisCache.hash_set('smart_game:%d' % uid, 'status', 0)
        err_list = self.get_detail_status(game_id, uid, pid_list)
        ret = {'ret': 0, 'lose_list': err_list}

        self.send_to_leave(uid, game_id)
        return MsgPack(0, ret)

    def get_detail_status(self, gid, uid, pid_list):
        if gid == 10000:
            keys = DOUDIZHU_KEY
        else:
            return pid_list
        ret_list = []
        for i in pid_list:
            ret = Context.RedisCache.hash_get('%s:%s:%d' % (keys, Time.current_time('%Y-%m-%d'), uid),i)
            if ret == None:
                two_ret = Context.RedisCache.hash_get('%s:%s:%d' % (keys, Time.timestamp_to_str(Time.current_ts()-3600*24,
                                                                                          '%Y-%m-%d'), uid), i)
                if two_ret == None:
                    ret_list.append(i)
        return ret_list


    def check_sign(self, sign, data):
        keys = data.keys()
        keys.sort()

        sign_data = []
        for key in keys:
            v = data.get(key)
            sign_data.append('%s=%s'%(key, str(v)))
        sign_str = '&'.join(sign_data)
        our_sign = Algorithm.md5_encode(sign_str)
        if sign == our_sign:
            return True
        Context.Log.error('check sign error', data, sign, our_sign, sign_data)
        return False

    def send_to_leave(self, userId, gameId):
        deliver_url = Context.Global.http_game() + '/v1/game/smart_game/leave'
        param = {
            'uid': userId,
            'gameId': 2,
            'mgid': gameId,
        }
        mo = MsgPack(0, param)
        result = Context.WebPage.wait_for_json(deliver_url, postdata=mo.pack(), timeout=10)
        return 'error' not in result

SmartGame = SmartGame()
