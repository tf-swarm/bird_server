#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__author__ = 'xiaomi passport (xiaomi-account-dev@xiaomi.com)'

'''
Python client SDK for xiaomi Open API
'''

from XMHttpClient import XMHttpClient
import xiaomi_conf
from urlparse import urljoin
from XMUtils import XMUtils
import time

class XMOAuthClient(XMHttpClient):

    OAUTH2_PATH = {'authorize': '/oauth2/authorize', 'token':'/oauth2/token'}

    def __init__(self, clientId, clientSecret, redirectUri):
        XMHttpClient.__init__(self, xiaomi_conf.VerifySession_URL)
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.redirectUri = redirectUri
        self.xmUtils = XMUtils()


    def getAuthorizeEndpoint(self):
        if not self.url:
            raise Exception("oauth url error", self.url)

        return urljoin(self.url, self.OAUTH2_PATH['authorize'])

    def getTokenEndpoint(self):
        if not self.url:
            raise Exception("oauth url error", self.url)

        return urljoin(self.url, self.OAUTH2_PATH['token'])


    def getAuthorizeUrl(self, responseType='code', display='',state='', scope=[]):
        params = {}
        params['client_id'] = self.clientId
        params['response_type'] = responseType
        params['redirect_uri'] = self.redirectUri

        if display:
            params['display'] = display
        if scope:
            params['scope'] = ' '.join(scope).strip()
        if state:
            params['state'] = state

        return self.getAuthorizeEndpoint() + '?' + self.buildQueryString(params)


    def getAccessTokenByAuthorizationCode(self, code):
        # Get access token  by authorization code.
        params = {}
        params['client_id'] = self.clientId
        params['client_secret'] = self.clientSecret
        params['redirect_uri'] = self.redirectUri
        params['grant_type'] = 'authorization_code'
        params['code'] = code
        params['token_type'] = 'mac'

        return self.getAccessToken(params);

    def getAccessTokenByRefreshToken(self, refreshToken):
        # Get access token  by refresh token.
        params = {}
        params['client_id'] = self.clientId
        params['client_secret'] = self.clientSecret
        params['redirect_uri'] = self.redirectUri
        params['grant_type'] = 'refresh_token'
        params['refresh_token'] = refreshToken
        params['token_type'] = 'mac'

        return self.getAccessToken(params)

    def getAccessToken(self, params):
        res = XMHttpClient.get(self, self.OAUTH2_PATH['token'], params)
        jsonObject = XMHttpClient.safeJsonLoad(self, res.read())
        return jsonObject

    def CheckIsLogin(self, uid, session):
        params = {}
        params['appId'] = self.clientId
        params['session'] = session
        params['uid'] = uid
        params['signature'] = self.xmUtils.buildSignature(params, self.clientSecret)
        return self.getErrCode(params)

    def getErrCode(self, params):
        res = XMHttpClient.get(self, '', params)
        data = res.read()
        jsonObject = XMHttpClient.safeJsonLoad(self, data)
        return jsonObject

    def getTBCode(self, params):
        res = XMHttpClient.get(self, '', params)
        data = res.read()
        return data

    def CheckIsLogin91(self, uid, session):
        XMHttpClient.set_pro_url(self, xiaomi_conf.Session_URL_91)
        params = {}
        params['AppId'] = self.clientId
        params['Act'] = 4  # 登录的act编号
        params['Uin'] = uid
        params['SessionId'] = session
        params['Sign'] = self.xmUtils.buildSignature_91(params, self.clientSecret)
        return self.getErrCode(params)

    def CheckIsLoginTB(self, session):
        XMHttpClient.set_pro_url(self, xiaomi_conf.Session_URL_TB)
        params = {}
        params['k'] = session
        return self.getTBCode(params)

    def CheckIsLoginAS(self, token):
        XMHttpClient.set_pro_url(self, xiaomi_conf.Session_URL_AS)
        params = {}
        params['token'] = token
        return self.getErrCode(params)

    def CheckIsLoginPP(self, sid):
        XMHttpClient.set_pro_url(self, xiaomi_conf.Session_URL_PP)
        params = {}
        params['id'] = int(time.time())
        params['service'] = "account.verifySession"
        params['data'] = {'sid': sid}
        params['game'] = {'gameId': int(self.clientId)}
        params['encrypt'] = "md5"
        params['sign'] = self.xmUtils.buildSignature_PP(sid, self.clientSecret)
        print "params::", params
        return self.postErrCode(params)

    def postErrCode(self, params):
        res = XMHttpClient.post(self, '', params,  header={'content-type':'text/plain'})
        jsonObject = XMHttpClient.safeJsonLoad(self, res.read(),)
        return jsonObject
