#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-18

import random
from sdk.const import Const
from framework.context import Context
from framework.util.tool import Time
from framework.entity.number_filter import NumberFilter


class Account(object):
    CACHE_DATA_TIMEOUT = 24 * 60 * 60  # 24小时

    def setUserToken(self, uid, gid, session):
        strKey = 'token:%d' % uid
        Context.RedisCache.hash_set(strKey, 'session', session)
        Context.RedisCache.expire(strKey, self.CACHE_DATA_TIMEOUT)

    # 如果是oppo或者华为，从商城信息中获取手机号对应用户id
    def getUserIDFromShopUserInfoMobile(self, mobile, channelid):
        realChannel = channelid.split('_')[0]
        if realChannel != '1004' and realChannel != '1005' and realChannel != '1003' \
                and realChannel != '1007' and realChannel != '1008':
            return None

        ret = Context.RedisCluster.hget_keys('shop:user:*')
        if not ret:
            return None
        for uid in ret:
            uid = uid.split('shop:user:')[1]
            phone = Context.Data.get_shop_attr(uid, 'shop:user', 'phone')
            if mobile == phone:
                reg_channel_id = Context.Data.get_attr(int(uid), 'channelid', '1001_0')
                if realChannel == reg_channel_id.split('_')[0]:
                    Context.Log.debug('getUserIDFromShopUserInfoMobile', uid)
                    return uid
        return None

    def getUserIDByUserName(self, userName, idType, channelid):
        realChannel = channelid.split('_')[0]
        key = 'username:%s:%d:%s' % (realChannel, idType, userName)
        return Context.RedisMix.hash_get_int(key, 'userId')

    def getUserInfo(self, userId):
        attrs = ['userName', 'idType', 'token', 'nick', 'sex', 'avatar', 'deviceId', 'createIp', 'createTime']
        kvs = dict.fromkeys(attrs, None)
        kvs.update(Context.Data.get_attrs_dict(userId, attrs))
        avatar = kvs.get('avatar', '1')
        if len(avatar) >= 3:
            Context.Data.set_attr(userId, 'avatar', '1')
            kvs['avatar'] = '1'
        return kvs

    def createUserInfo(self, userId, dictInfo):
        sex = random.choice([Const.SEX_MAN, Const.SEX_WOMAN])
        if sex == Const.SEX_WOMAN:
            avatar = random.choice(Const.DEFAULT_AVATAR_WOMAN)
        else:
            avatar = random.choice(Const.DEFAULT_AVATAR_MAN)
        value = {'userName': dictInfo['userName'], 'idType': dictInfo['idType'], 'token': dictInfo['token'],
                 'nick': dictInfo['nick'], 'sex': sex, 'avatar': avatar, 'status': 0, 'deviceId': dictInfo['deviceId'],
                 'createIp': dictInfo['createIp'], 'createTime': Time.datetime_now(), 'accessToken': '',
                 'channel': dictInfo['channel'], 'platform': dictInfo['platform'], 'channelid': dictInfo['channelid'], 'subchannel':dictInfo['subchannel'],
                 'imsi': dictInfo['imsi'], 'imei0': dictInfo['imei0'], 'mac': dictInfo['mac'], 'versionName': dictInfo['versionName']}
        if 'openid' in dictInfo:
            value['openid'] = dictInfo['openid']
        return Context.Data.set_attrs_dict(userId, value)

    def createUserName(self, idType, userName, userId, channelid):
        realChannel = channelid.split('_')[0]
        key = 'username:%s:%d:%s' % (realChannel, idType, userName)
        return Context.RedisMix.hash_setnx(key, 'userId', userId)

    def deleteUserName(self, userName, idType, channelid):
        realChannel = channelid.split('_')[0]
        key = 'username:%s:%d:%s' % (realChannel, idType, userName)
        return Context.RedisMix.delete(key)

    def createUser(self, info):
        if info['idType'] not in (Const.IDTYPE_MOBILE, Const.IDTYPE_ROBOT):
            ip_key = 'ip.limit.' + str(info['createIp'])
            limit = Context.Configure.get_global_item_int('ip.limit.user', 5)
            cnt = Context.RedisCache.incrby(ip_key, 1)
            if cnt > limit:
                return None
            if cnt < 3:  # 冗余
                Context.RedisCache.expire_at(ip_key, Time.tomorrow_start_ts())

        uid = Context.GData.get_new_user_id()
        while NumberFilter.check_number(uid):
            Context.Log.report('number.filter:', uid)
            uid = Context.GData.get_new_user_id()
        if not self.createUserName(info['idType'], info['userName'], uid, info['channelid']):
            return None
        if not self.createUserInfo(uid, info):
            self.deleteUserName(info['userName'], info['idType'], info['channelid'])
            return None
        Context.Log.report('user.init:', [uid, info])
        return uid

    def updateUserInfo(self, userId, **kvs):
        return Context.Data.set_attrs_dict(userId, kvs)


Account = Account()
