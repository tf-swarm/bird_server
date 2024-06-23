#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-18

import random
from sdk.const import Const
from sdk.lib.yuntongxun import CCPRestSDK
from sdk.modules.entity import Entity
from sdk.modules.account import Account
from framework.entity.msgpack import MsgPack
from framework.context import Context


class Mobile(object):
    verify_code_timeout = 30 * 60

    def __request_verify_code(self, gid, mobile):
        config = Context.Configure.get_game_item_json(gid, 'sms.config')
        rest = CCPRestSDK.REST(config['serverIP'], config['serverPort'], config['softVersion'])
        rest.setAccount(config['accountSid'], config['accountToken'])
        rest.setAppId(config['appId'])

        verifyCode = random.randint(100000, 999999)

        for tempId in config['tempId_arr']:
            result = rest.sendTemplateSMS(mobile, [str(verifyCode), '30'], tempId)
            Context.Log.debug('---------sms1', result)
            if result['statusCode'] == '000000':
                key = 'sms:%d:%s' % (gid, mobile)
                Context.RedisCache.hash_set(key, 'verifyCode', verifyCode)
                Context.RedisCache.expire(key, self.verify_code_timeout)
                return True

        Context.Log.debug('---------sms', result)
        return False

    def checkVerifyCode(self, gameId, mobile, toVerifyCode):
        key = 'sms:%d:%s' % (gameId, mobile)
        verifyCode = Context.RedisCache.hash_get(key, 'verifyCode')
        if verifyCode:
            if str(toVerifyCode) == verifyCode:
                Context.RedisCache.delete(key)
                return True
        return False

    def getVerifyCode(self, mi, request):
        gid = mi.get_param('gameId')
        mobile = mi.get_param('mobile')
        isCheck = int(mi.get_param('isCheck', 0))
        channelid = mi.get_param('channelid', '999_0')
        if not Entity.checkMobile(mobile):
            return MsgPack.Error(0, 1, 'mobile invalid')

        if isCheck == 1:
            idType = Const.IDTYPE_MOBILE
            userId = Account.getUserIDByUserName(mobile, idType, channelid)
            if userId:
                return MsgPack.Error(0, 2, 'mobile exists')
            userId = Account.getUserIDFromShopUserInfoMobile(mobile, channelid)
            if userId:
                return MsgPack.Error(0, 2, 'mobile exists')

        if not self.__request_verify_code(gid, mobile):
            return MsgPack.Error(0, 3, 'send failed')

        return MsgPack(0)

    def transferred_Code(self, mi, request):
        gid = mi.get_param('gameId')
        mobile = mi.get_param('mobile')
        channelid = mi.get_param('channelid', '999_0')
        if not Entity.checkMobile(mobile):
            return MsgPack.Error(0, 1, 'mobile invalid')

        idType = Const.IDTYPE_MOBILE
        userId = Account.getUserIDByUserName(mobile, idType, channelid)
        if userId:
            return MsgPack.Error(0, 2, 'mobile exists')

        userId = Account.getUserIDFromShopUserInfoMobile(mobile, channelid)
        if not userId:
            return MsgPack.Error(0, 3, 'mobile not exists in Shop')

        if not self.__request_verify_code(gid, mobile):
            return MsgPack.Error(0, 4, 'send failed')

        return MsgPack(0)

Mobile = Mobile()
