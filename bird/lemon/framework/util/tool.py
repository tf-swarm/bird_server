#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2014-11-07

import hmac
import time
import datetime
import calendar
import random
import hashlib
import base64
import types
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as pk
from Crypto.Cipher import PKCS1_v1_5


class Time(object):
    @classmethod
    def asctime(cls, p_tuple=None):      # 可读时间转换 "Tue Dec 11 18:07:14 2008"
        return time.asctime(p_tuple)

    @classmethod
    def current_ts(cls, dt=None):        # 获取时间戳 秒
        if dt is None:
            return int(time.time())
        else:
            t = dt.timetuple()
            return int(time.mktime(t))

    @classmethod
    def current_ms(cls, dt=None):       # 获取时间戳 毫秒
        if dt is None:
            return int(time.time() * 1000)
        else:
            t = dt.timetuple()
            return int(time.mktime(t) * 1000)

    @classmethod
    def is_today(cls, s):               # 是否是今天
        tm = time.strptime(s, '%Y-%m-%d %X')
        tm_now = time.localtime()
        return tm.tm_mday == tm_now.tm_mday and tm.tm_year == tm_now.tm_year and tm.tm_mon == tm_now.tm_mon

    @classmethod
    def is_yesterday(cls, s):           # 是否是昨天
        tm = time.strptime(s, '%Y-%m-%d %X')
        tm_yes = time.localtime(int(time.time()) - 3600 * 24)
        return tm.tm_mday == tm_yes.tm_mday and tm.tm_year == tm_yes.tm_year and tm.tm_mon == tm_yes.tm_mon

    @classmethod
    def yesterday_time(cls, ts=None): #前一天
        if ts is None:
            ts = int(time.time())
        tm = ts - 3600 * 24
        tm_yes = cls.timestamp_to_str(tm, '%Y-%m-%d')
        return tm_yes

    @classmethod
    def current_time(cls, fmt='%Y-%m-%d %X'):       # 打印当前时间 精确到秒 的格式显示
        return datetime.datetime.now().strftime(fmt)

    @classmethod
    def datetime_now(cls, fmt='%Y-%m-%d %X.%f'):    # 打印当前时间 精确到秒下的浮点型
        return cls.current_time(fmt)

    @classmethod
    def datetime(cls):                              # 当前时间
        return datetime.datetime.now()

    @classmethod
    def current_localtime(cls, t=None):             # 格式化时间戳为本地时区时间
        if not t:
            t = cls.current_ts()
        return time.localtime(t)

    @classmethod
    def next_days(cls, dt=None, days=1):            # 获取相对days个日期的时间显示
        if dt is None:
            dt = datetime.datetime.now()
        return dt + datetime.timedelta(days=days)

    @classmethod
    def next_days_ts(cls, ts=None, days=1):        # 获取 相对days个日期的时间戳
        if ts is None:
            ts = int(time.time())
        return ts + 86400 * days

    @classmethod
    def prev_days(cls, dt=None, days=-1):
        if dt is None:
            dt = datetime.datetime.now()
        return dt + datetime.timedelta(days=days)

    @classmethod
    def timestamp_to_str(cls, ts, fmt=None):      # 时间戳转换为对应fmt要求表现格式
        t = time.localtime(ts)
        if fmt is None:
            fmt = '%Y-%m-%d %X'
        return time.strftime(fmt, t)

    @classmethod
    def datetime_to_str(cls, dt, fmt=None):     # 时间格式转换为对应fmt要求表现格式
        if fmt is None:
            fmt = '%Y-%m-%d %X'
        return dt.strftime(fmt)

    @classmethod
    def str_to_timestamp(cls, s, fmt=None):     # 字符串时间格式转换为时间戳
        if fmt is None:
            fmt = '%Y-%m-%d %X'
        t = datetime.datetime.strptime(s, fmt).timetuple()
        return int(time.mktime(t))

    @classmethod
    def str_to_datetime(cls, s, fmt=None):      # 字符串时间格式转换为对应fmt时间格式
        if fmt is None:
            fmt = '%Y-%m-%d %X'
        return datetime.datetime.strptime(s, fmt)

    @classmethod
    def timestamp_to_datetime(cls, ts):         # 时间戳转换为日期时间格式
        return datetime.datetime.fromtimestamp(ts)

    @classmethod
    def datetime_to_timestamp(cls, ts):         # 日期时间格式转化为时间戳
        return int(time.mktime(ts.timetuple()))

    @classmethod
    def tomorrow_start_ts(cls, ts=None):        # 明天0点的时间戳
        if ts is None:
            ts = int(time.time())
        now_tm = time.localtime(ts)
        return ts + 86400 - now_tm.tm_hour * 3600 - now_tm.tm_min * 60 - now_tm.tm_sec

    @classmethod
    def today_start_ts(cls, ts=None):           # 今天0点的时间戳
        if ts is None:
            ts = int(time.time())
        now_tm = time.localtime(ts)
        return ts - now_tm.tm_hour * 3600 - now_tm.tm_min * 60 - now_tm.tm_sec

    @classmethod
    def current_week_start_ts(cls, ts=None):
        """ 获取本周开始的时间戳
        """
        if ts is None:
            ts = int(time.time())
        tm = time.localtime(ts)
        return ts - tm.tm_wday * 86400 - tm.tm_hour * 3600 - tm.tm_min * 60 - tm.tm_sec

    @classmethod
    def current_week_left_time(cls, ts=None):   # 本周还剩下多少秒
        tm = time.localtime(ts)
        return (7 - tm.tm_wday) * 86400 - tm.tm_hour * 3600 - tm.tm_min * 60 - tm.tm_sec

    @classmethod
    def pre_week_start_ts(cls, ts=None):        # 上一周开始时间戳
        ts = cls.current_week_start_ts(ts)
        return ts - 86400 * 7

    @classmethod
    def next_week_start_ts(cls, ts=None):       # 下一周开始的时间戳
        ts = cls.current_week_start_ts(ts)
        return ts + 86400 * 7

    @classmethod
    def current_month_start_ts(cls, ts=None):   # 本月开始的时间戳
        if ts is None:
            ts = int(time.time())
        tm = time.localtime(ts)
        return ts - (tm.tm_mday - 1) * 86400 - tm.tm_hour * 3600 - tm.tm_min * 60 - tm.tm_sec

    @classmethod
    def current_month_left_time(cls, ts=None):  # 本月剩余秒
        tm = time.localtime(ts)
        _, days = calendar.monthrange(tm.tm_year, tm.tm_mon)
        return (days - tm.tm_mday + 1) * 86400 - tm.tm_hour * 3600 - tm.tm_min * 60 - tm.tm_sec

    @classmethod
    def pre_month_start_ts(cls, ts=None):       # 上月开始时间戳
        tm = time.localtime(ts)
        if tm.tm_mon > 1:
            dt = datetime.datetime(tm.tm_year, tm.tm_mon - 1, 1)
        else:
            dt = datetime.datetime(tm.tm_year - 1, 12, 1)
        return int(time.mktime(dt.timetuple()))

    @classmethod
    def next_month_start_ts(cls, ts=None):      # 当月开始时间戳
        if ts is None:
            ts = int(time.time())
        tm = time.localtime(ts)
        _, days = calendar.monthrange(tm.tm_year, tm.tm_mon)
        return ts - tm.tm_hour * 3600 - tm.tm_min * 60 - tm.tm_sec + (days - tm.tm_mday + 1) * 86400

    @classmethod
    def up_days(cls, dt=None):                  # 相对2016年1月1日的天数
        if dt is None:
            dt = datetime.date.today()
        return (dt - datetime.date(2016, 1, 1)).days

    @classmethod
    def weekday(cls, today=True, year=None, month=None, day=None):      # 此日期是星期几
        if today:
            d = datetime.datetime.now()
        else:
            d = datetime.datetime(year, month, day)
        return d.weekday()

    @classmethod
    def timestamp_from_hms(cls, hms, now_dt=None):                      # 获取距离对应时间now_dt, 对应时分秒hms 的时间戳
        if now_dt is None:
            now_dt = datetime.datetime.now()
        prefix = cls.datetime_to_str(now_dt, '%Y-%m-%d')
        return cls.str_to_timestamp('%s %s' % (prefix, hms))

    @classmethod
    def at_this_time(cls, start, end, now_dt=None):                     # 是否在此日期范围内
        if now_dt is None:
            now_dt = datetime.datetime.now()
        prefix = cls.datetime_to_str(now_dt, '%Y-%m-%d')
        now_ts = cls.current_ts(now_dt)
        start_ts = cls.str_to_timestamp('%s %s' % (prefix, start))
        end_ts = Time.str_to_timestamp('%s %s' % (prefix, end))
        if start_ts <= now_ts <= end_ts:
            return True
        return False

    @classmethod
    def month_days(cls, year, month):                               # 获取本月有多少天
        _, days = calendar.monthrange(year, month)
        return days

    @classmethod
    def between_days(cls, ts):                                      # 获取当前时间与传入时间戳相差日
        create_ts = cls.today_start_ts(ts)
        today_ts = cls.today_start_ts()
        t1 = today_ts - create_ts
        if not t1:
            return 0
        return t1/(60*60*24)


class Tool(object):
    @classmethod
    def dict2list(cls, dt):
        lt = []
        if isinstance(dt, dict):
            for k, v in dt.iteritems():
                lt.append(k)
                lt.append(v)
        return lt

    @classmethod
    def list2dict(cls, lt):
        dt = {}
        if isinstance(lt, list):
            length = len(lt)
            while length > 1:
                dt[lt[length - 2]] = lt[length - 1]
                length -= 2
        return dt

    @classmethod
    def make_dict(cls, keys, values):
        dt = {}
        for k, v in zip(keys, values):
            dt[k] = v
        return dt

    @classmethod
    def make_list(cls, keys, values):
        lt = []
        for k, v in zip(keys, values):
            lt.append(k)
            lt.append(v)
        return lt

    @classmethod
    def list_merge(cls, l1, l2):
        l = []
        for i, j in zip(l1, l2):
            l.append(i)
            l.append(j)
        return l

    @classmethod
    def to_int(cls, v, default=None):
        if v is None:
            return default
        return int(v)

    @classmethod
    def to_float(cls, v, default=None):
        if v is None:
            return default
        return float(v)


class Algorithm(object):
    @classmethod
    def choice_by_ratio(cls, l, total, func=None):      # 概率计算获取
        if not l or not isinstance(l, list):
            raise Exception('param illegal')

        rand = random.randint(1, total)
        accumulator = 0
        for i, one in enumerate(l):
            if func:
                ratio = func(one)
            else:
                ratio = one
            accumulator += int(ratio * total)
            if rand <= accumulator:
                return i, one

        index = random.randrange(0, len(l))
        return index, l[index]

    @classmethod
    def md5_encode(cls, s):             # md5 加密
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()

    @classmethod
    def hmac_encode(cls, key, s):       # md5 加密 带密钥
        myhmac = hmac.new(key)
        myhmac.update(s)
        return myhmac.hexdigest()

    @classmethod
    def md5_decode(cls, s):             # md5 解密
        return hashlib.md5(s).hexdigest()

    @classmethod
    def base64_encode(cls, s):          # base64方式加密
        return base64.b64encode(s)

    @classmethod
    def base64_decode(cls, s):
        return base64.b64decode(s)

    @classmethod      # ali
    def verify_rsa(cls, publickey, data, signature):        # rsa校验
        key = RSA.importKey(publickey)
        h = SHA256.new()
        h.update(data)
        verifier = pk.new(key)
        if verifier.verify(h, base64.b64decode(signature)):
            return True
        return False

    @classmethod
    def verify_rsa_oppo(cls, publickey, data, signature):
        key = RSA.importKey(publickey)
        h = SHA.new(data)
        verifier = pk.new(key)
        if verifier.verify(h, base64.b64decode(signature)):
            return True
        return False

    @classmethod
    def rsa_sign(cls, privatekey, data):                    # rsa 签名
        key = RSA.importKey(privatekey)
        h = SHA.new(data)
        signer = pk.new(key)
        signn = signer.sign(h)
        signn = base64.b64encode(signn)
        return signn

    @classmethod
    def rsa_base64_decrypt(cls, privatekey, data):
        # 未使用
        key = RSA.importKey(privatekey)
        cipher = PKCS1_v1_5.new(key)
        return cipher.decrypt(base64.b64decode(data),
                              Random.new().read(15 + SHA.digest_size))

    @classmethod
    def hmac_sha1(cls, token, data):
        return hmac.new(token, data, hashlib.sha1)

    def smart_str(cls, s, encoding='utf-8', strings_only=False, errors='strict'):
        """
        Returns a bytestring version of 's', encoded as specified in 'encoding'.

        If strings_only is True, don't convert (some) non-string-like objects.
        """
        if strings_only and isinstance(s, (types.NoneType, int)):
            return s
        if not isinstance(s, basestring):
            try:
                return str(s)
            except UnicodeEncodeError:
                if isinstance(s, Exception):
                    # An Exception subclass containing non-ASCII data that doesn't
                    # know how to print itself properly. We shouldn't raise a
                    # further exception.
                    return ' '.join([cls.smart_str(arg, encoding, strings_only,
                                               errors) for arg in s])
                return unicode(s).encode(encoding, errors)
        elif isinstance(s, unicode):
            return s.encode(encoding, errors)
        elif s and encoding != 'utf-8':
            return s.decode('utf-8', errors).encode(encoding, errors)
        else:
            return s


if __name__ == "__main__":
    print Time.is_today('2015-06-11 11:00:15')
    print Time.is_today('2015-06-12 11:00:15')
    print Time.is_yesterday('2015-06-11 11:00:15')
    print Time.is_yesterday('2015-06-12 11:00:15')
    print Time.str_to_timestamp('2016-10-04 11:00:15')
