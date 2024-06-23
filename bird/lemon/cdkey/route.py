#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: dz
# Create: 2018-05-19

from framework.context import Context
from framework.entity.msgpack import MsgPack
from framework.util.exceptions import ForbiddenException
from framework.util.exceptions import NotFoundException
from framework.util.tool import Time, Tool
from framework.util.tool import Algorithm

import random
import string
import csv

#from lemon.entity.upgrade import Upgrade

#from framework.util.tool import Algorithm
#from sdk.modules.order import Order


class HttpCdKey(object):
    token = None
    gid_1 = "10001"
    gid_2 = "10002"
    gid_3 = "10003"
    def __init__(self):
        self.token = Context.Configure.get_global_item('cdkey.access_key')
        self.current_version = ""
        self.large_version = None
        self.middle_version = None
        self.small_version = None
        self.init_version()
        self.json_path = {
            '/v1/cdkey/checkCode': self.check_sdkey, #检查兑换码
            '/v1/cdkey/addsdkey': self.add_cdkey,
            '/v1/cdkey/export':self.getcdkey,
            '/v1/cdkey/exchange_query': self.query_cdkey,  # 兑换查询
            "/v1/cdkey/queryoverview": self.query_overview,  # 兑换码总览
            '/v1/cdkey/get_version_cdk': self.get_version_cdk,
            '/v1/cdkey/modify_cdkey': self.modify_cdkey,
            '/v1/cdkey/alter_cdkey': self.alter_cdkey,
        }

    def init_version(self):
        self.current_version = Context.Data.get_cdkey_attr(self.gid_1, 'version')
        if not self.current_version:
            self.current_version = '1.0.0'
            Context.Data.set_cdkey_attr(self.gid_1, 'version', self.current_version)
        version_list = self.current_version.split('.')
        self.large_version = int(version_list[0])
        self.middle_version = int(version_list[1])
        self.small_version = int(version_list[2])
        return

    def add_version(self):
        if self.small_version < 9:
            self.small_version += 1
        elif self.middle_version < 9:
            self.middle_version += 1
            self.small_version = 0
        else:
            self.middle_version = 0
            self.small_version = 0
            self.large_version += 1
        version_str = str(self.large_version) + '.' + str(self.middle_version) + '.' + str(self.small_version)
        if len(version_str) < 5:
            return False
        self.current_version = version_str
        Context.Data.set_cdkey_attr(self.gid_1, 'version', self.current_version)
        return True

    def get_version_cdk(self, mi, request):
        code = mi.get_param('version')
        cdk = Context.Data.get_cdkey_all(int(self.gid_3))
        ret = {}
        for k, v in cdk.items():
            dic = Context.json_loads(v)
            if str(dic.get('code'))[:3] == str(code):
                ret[k] = v
        mo = MsgPack(0)
        mo.set_param('cdk', ret)
        version = ".".join(str(i) for i in code)
        info = Context.Data.get_cdkey_attr(self.gid_2, version)
        mo.set_param('info', info)
        return mo

    # id + L + 随机码
    # string模块中的3个函数：string.letters，string.printable，string.printable
    def activation_code(self, id, length=20):
        prefix = hex(int(id))[2:] + 'L'
        length = length - len(prefix)
        chars = string.ascii_letters + string.digits
        return prefix + ''.join([random.choice(chars) for i in range(length)])

    ''' Hex to Dec '''
    def get_id(self, code):
        return str(int(code.upper(), 16))

    def add_cdkey_table_list(self, count):
        index = self.large_version * 1000 * 100000
        index += self.middle_version * 100 * 100000
        index += self.small_version * 10 * 100000
        cdkey_info = {}
        cdkey_list = []
        for i in range(count):
            code_info = {}
            idx = index + i
            code = self.activation_code(idx)
            code_info['code'] = idx
            Context.Data.set_cdkey_attr(self.gid_3, code, Context.json_dumps(code_info))
            cdkey_info.update({idx:code})
            cdkey_list.append(cdkey_info)
            cdkey_info = {}
        return cdkey_list

    def add_cdkey(self, mi, request):
        # dz add record
        Context.Log.debug("cdkey_add_cdkey:", mi)
        Context.Record.add_record_cdkey_add_cdkey(mi)

        _reward = mi.get_param('reward', None)
        count = mi.get_param('count', 0)
        times = mi.get_param('time', None)
        describe = mi.get_param('describe', '')
        channel = mi.get_param('channel', 0)
        phone = mi.get_param('phone', 0)

        if not _reward:
            return MsgPack.Error(0, 1, u'请填写奖励类型')
        if count <= 0:
            return MsgPack.Error(0, 2, u'请填写添加数量')
        if not times:
            return MsgPack.Error(0, 3, u'请填写到期时间')
        if not self.add_version():
            return MsgPack.Error(0, 4, u'添加版本好失败')
        info = {}
        info['count'] = int(count)
        info['end_time'] = times
        info['reward'] = _reward
        info['describe'] = describe
        info['creat_time'] = Time.current_ts()
        info['people'] = phone
        info['channel'] = channel
        Context.Data.set_cdkey_attr(self.gid_2, self.current_version, Context.json_dumps(info))
        cdkey_list = self.add_cdkey_table_list(int(count))
        mo = MsgPack(0)
        mo.set_param('info', cdkey_list)
        return mo

    def alter_cdkey(self, mi, request):
        # dz add record
        Context.Log.debug("cdkey_alter_cdkey:", mi)
        Context.Record.add_record_cdkey_alter_cdkey(mi)

        code = mi.get_param('version')
        ver_info = Context.Data.get_cdkey_attr(self.gid_2, code)
        info_json = Context.json_loads(ver_info)
        info_json.update({"end_time":info_json["creat_time"]})
        Context.Data.set_cdkey_attr(self.gid_2, code, Context.json_dumps(info_json))
        mo = MsgPack(0)
        mo.set_param('result', 0)
        return mo


    def getcdkey(self, mi, request):
        # dz add record
        Context.Log.debug("cdkey_get_cdkey:", mi)
        Context.Record.add_record_cdkey_get_cdkey(mi)

        with open("test.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            # 先写入columns_name
            writer.writerow(["code", "value"])
            # 写入多行用writerows
            ret = Context.Data.get_cdkey_all(int(self.gid_3))
            for k,v in ret.items():
                writer.writerows([[k, v]])
        pass

    def check_sdkey(self, mi, request):
        # dz add record
        Context.Log.debug("cdkey_exchange_cdkey:", mi)
        Context.Record.add_record_cdkey_exchange_cdkey(mi)

        code = mi.get_param('code')
        uid = mi.get_param('userId')
        #code = '623b834LPAQdtJl'
        #uid = 1000029
        mo = MsgPack(0)
        value = Context.Data.get_cdkey_attr(self.gid_3, code, None)
        code_info = {}
        if value != None and not Context.json_loads(value).has_key('uid'):
            value_json = Context.json_loads(value)
            values = value_json.get("code")
            value = int(values/1000000)
            version = str(int(value/100)) + '.' + str(int((value%100)/10)) + '.' +str(int(value%10))
            info = Context.Data.get_cdkey_attr(self.gid_2, version)
            keys = 'cdkey:record:%s:%s' % (Time.current_time('%Y-%m-%d'), version)
            record = Context.RedisCluster.hash_get(uid, keys, uid)
            if info and not record:
                info = Context.json_loads(info)
                reward = info['reward']
                start_time = Tool.to_int(info['creat_time'], 0)
                end_time = Tool.to_int(info['end_time'], 0)
                tm = Time.current_ts()
                if tm < start_time or tm > end_time:
                    mo.set_param('result', 0)
                    return mo
                code_info['uid'] = uid
                code_info['code'] = values
                code_info['ex_time'] = Time.current_time()
                Context.Data.set_cdkey_attr(self.gid_3, code, Context.json_dumps(code_info))
                mo.set_param('result', 1)
                mo.set_param('desc', reward)
                gid = 2
                pipe_args = []
                pipe_args.append('cdkey_use_{}'.format(version))  # 记录本服此类型礼包使用次数
                pipe_args.append(1)
                key = 'game.%d.info.hash' % gid
                Context.RedisMix.hash_mincrby(key, *pipe_args)

                if not reward.has_key('pool'):
                    Context.Data.set_attr_common(uid, keys, uid, code)
            else:
                mo.set_param('result', 2)
                return mo
        else:
            mo.set_param('result', 0)
        return mo

    def modify_cdkey(self, mi, request):
        version = mi.get_param('version')
        cdkey_info = Context.json_loads(Context.Data.set_cdkey_attr(self.gid_2, version))
        if cdkey_info == None:
            return MsgPack.Error(0, 1, u'版本错误')
        mo = MsgPack(0)
        info = mo.get_param('info')
        if info == None or info.get('count') != cdkey_info.get('count') or \
                info.get('end_time') == None or info.get('reward') == None or \
                info.get('describe') == None or info.get('creat_time') == None or \
                info.get('people') == None or info.get('channel') == None:
            return MsgPack.Error(0, 1, u'内容错误')
        else:
            Context.Data.set_cdkey_attr(self.gid_2, version, Context.json_dumps(info))
            mo.set_param('result', 1)
        return mo

    def __check_legal(self, mi):
        gid = mi.get_param('gameId')
        return gid in Context.Global.game_list()

    def check_token(self, gid, mi):
        sign = mi.get_param('sign')
        ts = mi.get_param('ts')
        gid = mi.get_param('gameId')
        line = 'gameId=%d&token=%s&ts=%d' % (gid, self.token, ts)
        _sign = Algorithm.md5_encode(line)
        if sign != _sign:
            Context.Log.error('verify token key failed', _sign, sign)
            return False
        return True

    def onMessage(self, request):
        if request.method.lower() == 'post':
            if request.path in self.json_path:
                data = request.raw_data()
                mi = MsgPack.unpack(0, data)
                Context.Log.debug(mi)
                gid = mi.get_param('gameId')
                if not self.check_token(gid, mi):
                    raise ForbiddenException('no permission access')

                #if not self.__check_legal(mi):
                #    return 'robot'
                # with Context.GData.server_locker:
                return self.json_path[request.path](mi, request)
        try:
            Context.Log.debug('request.path:', request.path)
            data = request.raw_data()
            mi = MsgPack.unpack(0, data)
            Context.Log.debug(mi)
            Context.Log.debug('mi:', mi)
        except:
            Context.Log.debug('error:unpack fail')

        raise NotFoundException('Not Found')

    def query_overview(self, mi, request):
        start = mi.get_param('start')
        end = mi.get_param('end')

        version = Context.Data.get_cdkey_attr(self.gid_1, 'version')
        if not version:
            return MsgPack.Error(0, 1, 'not version')
        version_all = Context.Data.get_cdkey_all(int(self.gid_2))
        cdkey_list = []
        start_day = Time.timestamp_to_datetime(start)
        end_day = Time.timestamp_to_datetime(end)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            for key,value in version_all.items():
                value_json = Context.json_loads(value)
                create_time = Time.timestamp_to_str(value_json["creat_time"])
                if create_time[:10] ==fmt:
                    cdkey_use = Context.RedisMix.hash_get_int('game.2.info.hash', "cdkey_use_{}".format(key), 0)
                    value_json.update({"cdkey_use":cdkey_use})
                    value_json.update({"version": key})
                    cdkey_list.append(value_json)
            start_day = Time.next_days(start_day)
        mo = MsgPack(0)
        mo.set_param('conf', cdkey_list)
        return mo


    def query_cdkey(self, mi, request):
        start = mi.get_param('start')
        end = mi.get_param('end')
        code_conf = Context.Data.get_cdkey_all(int(self.gid_2))
        ret_info = Context.Data.get_cdkey_all(int(self.gid_3))
        code_list = []
        code_info = {}
        for key,values in code_conf.items():
            keys = key.replace('.', '')
            value_json = Context.json_loads(values)
            create_time = value_json["creat_time"]
            if create_time >= start and create_time <= end:
                for ky,val in ret_info.items():
                    val = Context.json_loads(val)
                    if str(val["code"]).startswith(keys, 0, 3):
                        code_info.update(value_json)
                        val.update({"key":ky})
                        code_info.update({"info": val})
                        code_list.append(code_info)
                        code_info = {}
        mo = MsgPack(0)
        mo.set_param('cdkey', code_list)
        return mo


HttpCdKey = HttpCdKey()
