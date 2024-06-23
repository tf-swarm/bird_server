# -*- coding:utf-8 -*-
"""
created by cui
"""

from sdk.const import Const
from sdk.modules.user import User
from framework.context import Context
from framework.entity.msgpack import MsgPack
from sdk.modules.account import Account

COOLPAD_URL = 'https://openapi.coolyun.com/oauth2/token'
APPID = '5000003582'
APPKEY = '81d6430320734335aa7895a0a011cf55'


def login(mi, request):
    param = User.getParam(mi, 'accessToken', 'devName')
    if len(param['accessToken']) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
    res = verify_login(param['accessToken'])
    # {"resultCode":"200","resultMsg":"正常 ","loginToken":xxx,"ssoid":123456,"appKey":null,"userName":abc,"email":null,"mobi leNumber":null,"createTime":null,"userStatus":null}

    if not res.get('openid'):
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    gid = param['gameId']
    openid = res.get('openid')
    open_token = res.get('access_token')
    userId = Context.RedisMix.hash_get('coolpad.%s.uid' % gid, openid, None)
    if not userId:
        channel = 'coolpad'
        idType = Const.IDTYPE_COOLPAD
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('coolpad.%s.uid' % gid, openid, userId)
    userId = int(userId)
    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, open_token=open_token, loginChannelId=param['channelid'])


def verify_login(code):
    data = {'grant_type': 'authorization_code', 'client_id': APPID, 'client_secret': APPKEY,
            'code': code, 'redirect_uri': APPKEY}
    res = Context.WebPage.wait_for_json(COOLPAD_URL, method='GET', query=data)
    return res
