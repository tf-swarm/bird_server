#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: hwz
# Create: 2018-09-13

from framework.context import Context
from framework.util.tool import Time, Tool
from framework.entity.msgpack import MsgPack
from cplFather import CplFather

token = 'asdfasdximaoxiaozhuoxx4JH34756'

class XiaoZhuoAccess(CplFather):
    def __init__(self):
        super(XiaoZhuoAccess, self).__init__()

    def QueryUserExist(self, mi):
        channel = mi.get('channel')
        sign = mi.get('sign')
        imei = mi.get('imei')

        sign_str = ''
        sign_str += (str(imei)+str(channel)+token)
        sign_check = self.check_sign(sign, sign_str)
        if not sign_check:
            ret = {'status':'0', 'msg': u"签名错误"}
            return MsgPack(0, ret)

        if str(channel) != '1':
            ret = {'status':'3', 'msg': u"渠道标识不存在"}
            return MsgPack(0, ret)

        uid = self.query_channel_user_date(imei, '2000_1')
        if uid:
            channel_id = Context.Data.get_attr(int(uid), 'channelid', '1001_0')
            sub_channel_id = Context.Data.get_attr(int(uid), 'subchannelid', '0')
            if channel_id != '2000_1' and sub_channel_id != '1':
                ret = {'status': '5', 'msg': u"该设备已在其它平台注册使用"}
                return MsgPack(0, ret)
            ret = {
                    'status': '1',
                    'msg': u"用户存在",
                    'uid':str(uid),
                    'IMEI':imei,
                    'registerdate':Time.current_ts()
            }
            return MsgPack(0, ret)
        ret = {'status': '4', 'msg': u"用户不存在"}
        return MsgPack(0, ret)


    def QueryWinCoin(self, mi):
        uid = Tool.to_int(mi.get('uid'), 0)
        channel = mi.get('channel')
        sign = mi.get('sign')

        sign_str = (str(uid) + str(channel) + token)
        sign_check = self.check_sign(sign, sign_str)
        if not sign_check:
            ret = {'status':'0', 'msg': u"查询失败"}
            return MsgPack(0, ret)

        channel_id = Context.Data.get_attr(int(uid), 'channelid', '1001_0')
        sub_channel_id = Context.Data.get_attr(int(uid), 'subchannelid', '1001_0')
        if not channel_id or channel_id != '2000_1' and sub_channel_id != '1':
            ret = {'status': '4', 'msg': u"该设备已在其它平台注册使用"}
            return MsgPack(0, ret)

        ret = {}
        ret['status'] = '1'
        ret['msg'] = u'查询成功'
        ret['nickname'] = str(Context.Data.get_attr(uid, 'nick', ''))
        ret['uid'] = str(uid)
        pay_total, sc = self.get_coupon_date(uid, channel_id)
        ret['coupon'] = str(sc)
        create_time = Context.Data.get_attr(uid, 'createTime')
        ct = Time.str_to_timestamp(create_time[:10], '%Y-%m-%d')
        ret['pay_total'] = str(pay_total)
        if ct < '2020-07-06':
            ret['is_new'] = '0'
        else:
            ret['is_new'] = '1'

        # createTime = str(Context.Data.get_attr(int(uid), "createTime"))[:19]
        # create_ts = Time.str_to_timestamp(createTime)
        # is_new = 1
        # if create_ts < 1577635200:
        #     is_new = 0
        # ret['is_new'] = str(is_new)
        return MsgPack(0, ret)


XiaoZhuoAccess = XiaoZhuoAccess()





