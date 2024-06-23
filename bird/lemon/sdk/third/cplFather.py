#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: hwz
# Create: 2018-09-13

from framework.context import Context
from framework.util.tool import Algorithm, Time

class CplFather(object):
    def __init__(self):
        pass

    @classmethod
    def check_sign(cls, sign, sign_str):
        our_sign = Algorithm.md5_encode(sign_str)
        if sign == our_sign:
            return True
        return False

    @classmethod
    def query_channel_user_date(cls, imei, channel_id):

        ret_keys = 'user_daily:%s:%s:*' % (channel_id, Time.current_time('%Y-%m-%d'))
        keys = Context.RedisStat.hget_keys(ret_keys)
        uid_list = []
        for j in keys:
            uid = int(j.split(':')[3])
            imsi = Context.Data.get_attr(uid, 'imei0')
            if imsi == str(imei):
                uid_list.append(uid)
        if uid_list:
            Context.Log.debug('query_channel_user_datexxx', min(uid_list))
            return min(uid_list)
        return

    def get_coupon_date(self, uid, cid):
        silver_coupon = 0
        pay_total = 0
        for i in xrange(6, 32):
            ret_keys = 'user_daily:%s:%s:%d' % (cid, '2020-07-%02d'%i, uid)
            ret_keys2= '%s.pay.user.pay_total'%cid
            pay_total += Context.RedisStat.hash_get_int(ret_keys, ret_keys2, 0)
            stat_day = Context.RedisStat.hash_getall(ret_keys)
            for k, v in stat_day.items():
                if k.startswith('in.coupon.'):
                    silver_coupon += int(v)
        return pay_total, silver_coupon

