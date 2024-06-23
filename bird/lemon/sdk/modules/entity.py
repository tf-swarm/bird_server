#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-18

import re
from binascii import b2a_hex
from binascii import a2b_hex
from Crypto.Cipher import AES
from framework.util.tool import Algorithm
from sdk.const import Const


class Entity(object):
    key = 'qilecryptkey3596'
    mode = AES.MODE_CBC

    @classmethod
    def encrypt(cls, text):
        cryptor = AES.new(cls.key, cls.mode, b'0000000000000000')
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            text += ('\0' * add)
        elif count > length:
            add = (length - (count % length))
            text += ('\0' * add)
        ciphertext = cryptor.encrypt(text)
        return b2a_hex(ciphertext)

    @classmethod
    def decrypt(cls, text):
        cryptor = AES.new(cls.key, cls.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

    @classmethod
    def logined(cls, request):
        """是否已经登录"""
        try:
            if request.getSession().isLogined():
                return True
        except:
            pass
        return False

    @classmethod
    def checkDeviceID(cls, strDeviceID):
        if len(strDeviceID) < 1:
            return False
        return True

    @classmethod
    def checkUserName(cls, strUser):
        if len(strUser) == 0:
            return False
        if strUser.find("select") >= 0:
            return False
        return True

    @classmethod
    def checkPassword(cls, strPass):
        if len(strPass) < 6:
            return False
        strValid = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~!@#$%^&*()_+-=[]{}"
        for c in strPass:
            if c not in strValid:
                return False
        return True

    @classmethod
    def checkNick(cls, nick):
        if len(nick) == 0:
            return False
        if nick.find('select') >= 0:
            return False
        return True

    @classmethod
    def checkEmail(cls, strEmail):
        if len(strEmail) == 0:
            return True
        if strEmail.find("select") >= 0:
            return False
        return re.match(r"^[a-zA-Z0-9]+[a-zA-Z0-9_\.\-]*[a-zA-Z0-9]+@([a-zA-Z0-9]+\.)+[a-zA-Z]{2,}$", strEmail,
                        re.VERBOSE)

    @classmethod
    def checkMobile(cls, strMobile):
        return bool(re.match(r"(1)(\d{10})$", strMobile, re.VERBOSE))

    @classmethod
    def encodePassword(cls, user, passwd):
        if isinstance(user, unicode):
            user = user.encode('utf-8')
        return Algorithm.md5_encode(str(user) + str(passwd))

    @classmethod
    def baidu_get_sign(cls, param):
        sign_data = ''
        keys = ['appid', 'orderid', 'amount', 'unit', 'status', 'channel']
        for key in keys:
            v = param.get(key)
            if type(v) == int:
                v = str(v)
            if type(v) == unicode:
                v = v.encode('utf8')
            sign_data += v
        sign = Algorithm.md5_encode(sign_data + Const.BAIDU_SECRET)
        return sign

    @classmethod
    def huawei_sign_data(cls, param):
        keys = param.keys()
        keys.sort()
        if 'sign' in keys:
            keys.remove('sign')
        if 'signType' in keys:
            keys.remove('signType')
        sign_data = ''
        for k in sorted(keys, key=str.lower):
            v = param.get(k)
            if v is None:
                continue
            if sign_data:
                sign_data += '&'
            sign_data += k
            sign_data += '='
            if type(v) == int:
                v = str(v)
            if type(v) == unicode:
                v = v.encode('utf8')
            sign_data += v
        return sign_data

    @classmethod
    def huawei_get_sign(cls, param):
        sign_data = cls.huawei_sign_data(param)
        sign = Algorithm.rsa_sign(Const.HUAWEI_PRIVATEKEY, sign_data)
        return sign

    @classmethod
    def huawei_verify_sign(cls, param):
        sign_data = cls.huawei_sign_data(param)
        return Algorithm.verify_rsa(Const.HUAWEI_PUBLICKEY, sign_data, param['sign'])

    @classmethod
    def meizu_get_sign(cls, param):
        keys = param.keys()
        keys.sort()
        if 'sign' in keys:
            keys.remove('sign')
        if 'sign_type' in keys:
            keys.remove('sign_type')
        sign_data = ''
        for key in keys:
            v = param.get(key)
            if sign_data:
                sign_data += '&'
            sign_data += key
            sign_data += '='
            if type(v) == int:
                v = str(v)
            if type(v) == unicode:
                v = v.encode('utf8')
            sign_data += v
        sign = Algorithm.md5_encode(sign_data + ':' + Const.MEIZU_SECRETKEY)
        return sign

    @classmethod
    def vivo_get_sign(cls, param):
        keys = param.keys()
        keys.sort()
        if 'signMethod' in keys:
            keys.remove('signMethod')
        if 'signature' in keys:
            keys.remove('signature')
        sign_data = ''
        for key in keys:
            v = param.get(key)
            if v == None or v == '':
                continue
            if sign_data:
                sign_data += '&'
            sign_data += key
            sign_data += '='
            if type(v) == int:
                v = str(v)
            if type(v) == unicode:
                v = v.encode('utf8')
            sign_data += v
        _CPKEY = Algorithm.md5_encode(Const.VIVO_CPKEY)
        sign = Algorithm.md5_encode(sign_data + '&' + _CPKEY)
        return sign


Entity = Entity()
