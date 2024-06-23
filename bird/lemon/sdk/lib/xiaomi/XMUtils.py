#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__author__ = 'xiaomi passport (xiaomi-account-dev@xiaomi.com)'

'''
Python client SDK for xiaomi Open API
'''

import random
import sys
import time
import hmac, hashlib
from urllib import quote

class XMUtils():
    '''
     获取一个随机字符串
     获取随机nonce值 : 格式为  随机数:分钟数
    '''
    def getNonce(self):
        r = random.randint(-sys.maxint, sys.maxint)
        m = (int)(time.time() / 60)
        return '%d:%d' % (r, m)

    '''
    构造mac type签名串
    '''
    def getSignString(self, params):
        sign = []
        paramsKeys = params.keys()
        paramsKeys.sort()
        items = []
        for key in paramsKeys:
            items.append("%s=%s" % (key, params.get(key)))

        if items:
            sign.append('&'.join(items))
        else:
            sign.append('')

        return ''.join(sign) + ''

    '''
     mac type签名算法
    '''
    def buildSignature(self, params, secret):
        signString = self.getSignString(params)
        #signString = "appId=2882303761517246109&session=gPWFI2HY2cj8lGcE&uid=27187826"
        #secret = "guOw3xGn73uzXw8yKO2xZg=="
        h = hmac.new(str(secret), str(signString), hashlib.sha1)
        s = h.digest()
        signature = s.encode("hex")
        #pass#print "e452f939aefb32a8590999acf1cac297aaf9c001"
        pass#print signature
        return signature

    def buildSignature_91(self, params, secret):
        signString = "".join([str(params.get('AppId')), str(params.get('Act')), str(params.get('Uin')),\
                     str(params.get('SessionId')), str(secret)])
        print "signString", signString
        sign = hashlib.md5()
        sign.update(signString)
        sign = sign.hexdigest()
        print "sign::", sign
        return sign

    '''
     获取mac type access token请求api的头部信息
    '''
    def buildMacRequestHead(self, accessToken, nonce, sign):
        macHeader = 'MAC access_token="%s", nonce="%s",mac="%s"' % (quote(accessToken), nonce, quote(sign))
        header = {}
        header['Authorization'] = macHeader
        return header

    def buildSignature_PP(self, sid, secret):
        signString = "".join(["sid=", str(sid), str(secret)])
        print "signString", signString
        sign = hashlib.new("md5", signString).hexdigest()
        print "sign::", sign
        return sign
