#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-05-06

import copy
import json
import os
import csv
import random
import pymysql
from DBUtils.PooledDB import PooledDB
from framework.util.locker import LockAttr
from framework.util.log import Logger
from framework.util.strutil import Strutil
from framework.util.tool import Time
from framework.dao.db_cluster import RedisCluster
from framework.dao.db_single import RedisSingle
from framework.entity.configure import Configure
from framework.entity.const import Const
from framework.entity.const import Enum
from framework.entity.const import FlagType
from framework.entity.const import Message
from framework.entity.daily import Daily
from framework.entity.data import Data
from framework.entity.gdata import GData
from framework.entity.globals import Global
from framework.entity.online import Online
from framework.entity.stat import Stat
from framework.entity.match import MatchDB
from framework.entity.dmysql import MysqlData
from framework.entity.userattr import UserAttr
from framework.entity.webpage import WebPage
from framework.entity.cffiloader import CFFILoader
from framework.entity.keyword_filter import KeywordFilter
from framework.entity.activity import Activity
from framework.entity.record import Record

class Context(object):
    def __init__(self):
        self.RedisConfig = RedisSingle()
        self.RedisCluster = RedisCluster()
        self.RedisMix = RedisSingle()
        self.RedisPay = RedisSingle()
        self.RedisCache = RedisSingle()
        self.RedisStat = RedisSingle()
        self.RedisActivity = RedisSingle()
        self.RedisRecord = RedisSingle()
        self.RedisMatch = RedisSingle()

        self.Log = Logger
        self.GData = GData
        self.Configure = Configure
        self.UserAttr = UserAttr
        self.Data = Data
        self.Daily = Daily
        self.Stat = Stat
        self.Activity = Activity
        self.Record = Record
        self.MatchDB = MatchDB
        self.Strutil = Strutil
        self.Global = Global
        self.WebPage = WebPage
        self.Online = Online
        self.CFFILoader = CFFILoader
        self.MysqlData = MysqlData

        self.LockAttr = LockAttr
        self.Message = Message
        self.FlagType = FlagType
        self.Enum = Enum
        self.Const = Const
        self.Time = Time
        self.KeywordFilter = KeywordFilter
        self.MysqlDB = None

    @classmethod
    def json_loads(cls, s, ex=False):
        """
        @param ex: 兼容老数据, 慎用, 禁止将dict, list, set, tuple等类型的数据直接str成字符串
        """
        try:
            return json.loads(s)
        except Exception, e:
            if ex:
                return eval(s)
            else:
                raise e

    @classmethod
    def save_cache(cls, dir, name, l):
        cd = os.path.dirname(os.getcwd())
        if not os.path.exists(cd + "/history/%s"%(dir)):
            os.makedirs(cd + "/history/%s"%(dir))
        with open(cd + "/history/%s/%s.csv"%(dir, name), "w+") as csvfile:
            writer = csv.writer(csvfile)
            # 先写入columns_name
            writer.writerow(["code", "value"])
            # 写入多行用writerows
            for k,v in l.items():
                writer.writerows([[k, v]])

    @classmethod
    def hide_name(cls, name):
        if name == None or name == "":
            return u''
        if not isinstance(name, unicode):
            name = unicode(name, 'utf-8')
        if len(name) >= 2:
            return u"**%s" % (name[-2:])
        elif len(name) >= 1:
            return u"**%s" % (name[-1])

    @classmethod
    def json_dumps(cls, o, **kwargs):
        if 'separators' not in kwargs:
            kwargs['separators'] = (',', ':')
        return json.dumps(o, **kwargs)

    @classmethod
    def copy_json_obj(cls, j):
        t = json.dumps(j)
        return json.loads(t)

    @classmethod
    def copy_obj(cls, o):
        return copy.deepcopy(o)

    @classmethod
    def get_module(cls, gid, name, default=None):
        from lemon import classMap
        _cls = classMap.get(gid, {})
        return _cls.get(name, default)

    # 随机分配红包的
    @classmethod
    def randBonus(cls, min, total, num):
        if num == 1:
            return [total], [total, 0]
        sums = 0
        pre = []
        surplus = []
        total = float(total)
        num = int(num)
        if num < 1:
            return
        if num == 1:
            return
        i = 1
        totalMoney = total
        while (i < num):
            max = totalMoney - min * (num - i)
            if num - i >= 1:
                k = num - i
                max = max / k
                money = random.randint(int(min * 100), int(max * 100))
                moneys = float(money) / 100
                totalMoney = totalMoney - moneys
                pre.append(int(moneys))
                surplus.append(int(totalMoney))
                i += 1
        pre.append(int(totalMoney))
        surplus.append(0)
        for n in pre:
            sums = sums + n
        residue = int(total) - sums
        if residue < 0:
            pre[num - 1] += residue
            surplus[num - 2] += residue
        if residue > 0:
            pre[num - 1] += residue
            surplus[num - 2] += residue

        random.shuffle(pre)
        return pre, surplus

    def tasklet(self):
        from framework.entity.manager import TaskManager
        return TaskManager.current()

    def init_ctx(self):
        for name in dir(self):
            if name.startswith('__'):
                continue
            obj = getattr(self, name)
            _init_ctx = getattr(obj, 'init_ctx', None)
            if callable(_init_ctx):
                _init_ctx()
        setattr(self, 'init_ctx', None)
        self.LockAttr.lock(self)

    def create_mysql_pool(self):
        db_config = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "passwd": "123456",
            "db": "server_cache",
            "charset": "utf8"
        }
        spool = PooledDB(pymysql, 5, **db_config)
        self.MysqlDB = spool.connection()
        self.create_mysql_table()
        return

    def create_mysql_table(self):
        # 创建用户每日数据表---------
        sql_str = "create table if not exists user_daily_data(" \
                        "uid_daily varchar(40) NOT NULL unique, daily_data json NOT NULL);"
        cur = self.MysqlDB.cursor()
        cur.execute(sql_str)
        cur.fetchall()
        cur.close()
        # 创建用户每日数据表---------
        # 新表添加写下面+++++++++
        return

    def init_with_redis_json(self, redis_json, init_config=True):
        if init_config:
            self.RedisConfig.connect(redis_json['config'])
        self.RedisCluster.connect(redis_json['cluster'])
        self.RedisMix.connect(redis_json['mix'])
        self.RedisPay.connect(redis_json['pay'])
        self.RedisStat.connect(redis_json['stat'])
        self.RedisCache.connect(redis_json['cache'])
        self.RedisActivity.connect(redis_json['activity'])
        self.RedisRecord.connect(redis_json['record'])
        self.RedisMatch.connect(redis_json['match'])
        # self.create_mysql_pool()
        setattr(self, 'init_with_redis_json', None)
        setattr(self, 'init_with_redis_key', None)

    def init_with_redis_key(self, redis_key):
        if isinstance(redis_key, str):
            host, port, db = redis_key.split(':')
        else:
            host, port, db = redis_key['host'], redis_key['port'], redis_key['db']
        self.RedisConfig.connect(host, port, db)
        redis_json = self.Configure.get_global_item_json('redis.config')
        self.init_with_redis_json(redis_json, False)

    def load_lua_script(self):
        if getattr(self, 'init_with_redis_json', None):
            raise Exception('not init ctx')
        alias_sha = self.Configure.get_global_item_json('redis.lua')
        if alias_sha:
            for alias, sha in alias_sha.iteritems():
                self.RedisCluster.add_lua_alias(alias, sha)
                self.RedisMix.add_lua_alias(alias, sha)
                self.RedisPay.add_lua_alias(alias, sha)
                self.RedisStat.add_lua_alias(alias, sha)
                self.RedisCache.add_lua_alias(alias, sha)
                self.RedisActivity.add_lua_alias(alias, sha)
                self.RedisRecord.add_lua_alias(alias, sha)
                self.RedisMatch.add_lua_alias(alias, sha)

Context = Context()
Context.init_ctx()
