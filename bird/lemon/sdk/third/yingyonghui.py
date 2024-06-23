# -*- coding:utf-8 -*-
"""
created by cui
"""

from sdk.const import Const
from sdk.modules.user import User
from framework.context import Context
from framework.entity.msgpack import MsgPack
from sdk.modules.account import Account

URL = 'http://api.appchina.com/appchina-usersdk/user/v2/get.json'

APPID = '5001233615'
LOGINID = '11987'
LOGINKEY = 'ySRwFi73B8K1DODN'


def login(mi, request):
    param = User.getParam(mi, 'accessToken', 'devName')
    if len(param['accessToken']) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
    res = verify_login(param['accessToken'])

    if res.get('status') != 0 or res.get('message') != 'OK':
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    res_data = res.get('data')
    gid = param['gameId']
    openid = res_data.get('user_id')
    # user_name = result.get('name')
    userId = Context.RedisMix.hash_get('yingyonghui.%s.uid' % gid, openid, None)
    if not userId:
        channel = 'yingyonghui'
        idType = Const.IDTYPE_YINGYONGHUI
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('yingyonghui.%s.uid' % gid, openid, userId)
    userId = int(userId)
    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])


def verify_login(ticket):
    data = {'ticket': ticket, 'login_id': LOGINID, 'login_key': LOGINKEY}
    res = Context.WebPage.wait_for_json(URL, postdata=data)
    return res
