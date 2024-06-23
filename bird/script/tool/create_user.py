#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-04-26

from sdk.const import Const
from framework.context import Context
from sdk.modules.entity import Entity
from sdk.modules.account import Account
from framework.entity.manager import TaskManager


class Creater(object):
    @classmethod
    def create_by_mobile(cls, gid, mobile, passwd, platform, channel):
        deviceId = 'xxxxxxxxxxxxxxxx'
        channelid = '888_0'
        # 先查表，判断用户存不存在
        idType = Const.IDTYPE_MOBILE
        userId = Account.getUserIDByUserName(mobile, idType, channelid)
        if userId:
            return False

        # 插入用户数据
        imsi = ''
        versionName = ''
        mac = ''

        strMd5Pass = Entity.encodePassword(mobile, passwd)
        dictInfo = {'idType': idType, 'deviceId': deviceId, 'userName': mobile, 'nick': 'test',
                    'createIp': '127.0.0.1', 'token': strMd5Pass, 'guest': 0,
                    'channel': channel, 'platform': platform, 'channelid': channelid,
                    'imsi': imsi, 'versionName': versionName, 'mac': mac}
        userId = Account.createUser(dictInfo)
        if not userId:
            return False

        key, field = 'game.%d.info.hash' % gid, '%s.new.user.count' % channel
        Context.RedisMix.hash_incrby(key, field, 1)
        Context.Stat.incr_daily_data(channelid, field, 1)

        return True


def main(gid, count, mobile, channel, platform):
    Context.Log.open_std_log()
    # Context.Log.set_level(Context.Log.BI)
    Context.init_with_redis_key('127.0.0.1:6379:0')
    pwd = channel + '123456'
    while count > 0:
        success = Creater.create_by_mobile(gid, str(mobile), pwd, platform, channel)
        if success:
            count -= 1
            print mobile, pwd
        mobile += 1
    TaskManager.end_loop()


if __name__ == '__main__':
    import sys
    # Context.Log.open_std_log()
    # Context.Log.set_level(Context.Log.BI)
    gid = int(sys.argv[1])
    assert gid == 2
    count = int(sys.argv[2])
    mobile = int(sys.argv[3])
    platform = 'android'
    if len(sys.argv) > 5:
        platform = sys.argv[4]
    if platform not in ('android', 'ios'):
        raise Exception('error platform')

    channel = 'qifan'
    if len(sys.argv) > 6:
        channel = sys.argv[5]
    if not channel:
        raise Exception('error channel')

    TaskManager.add_simple_task(main, gid, count, mobile, channel, platform)
    TaskManager.start_loop()
