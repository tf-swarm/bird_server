#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-10-15

from sdk.modules.user import User
from sdk.modules.mobile import Mobile
from sdk.modules.order import Order
from framework.context import Context
from framework.entity.msgpack import MsgPack
from framework.util.exceptions import NotFoundException
from sdk.third import q360
from sdk.third import oppo
from sdk.third import vivo
from sdk.third import vivo_ad
from sdk.third import weixin
from sdk.third import ali
from sdk.third import huawei
from sdk.third import yyb
from sdk.third.smart_game import SmartGame
from sdk.third.xiaozhuo import XiaoZhuoAccess


class HttpSdk(object):
    def __init__(self):
        self.json_path = {
            '/v1/user/getVerifyCode': Mobile.getVerifyCode,     # fix client bug
            '/v1/mobile/getVerifyCode': Mobile.getVerifyCode,
            '/v1/user/registerByMobile': User.registerByMobile,
            '/v1/user/upgradeByMobile': User.upgradeByMobile,
            '/v1/user/registerByUserName': User.registerByUserName,
            '/v1/user/upgradeByUserName': User.upgradeByMobile, #User.upgradeByUserName,
            '/v1/user/loginByMobile': User.loginByMobile,
            '/v1/user/loginBySdk': self.loginBySdk,
            '/v1/user/loginByGuest': User.loginByGuest,             #没有账号的快速登陆
            '/v1/user/loginByAccessToken': User.loginByAccessToken, #已有账号的快速登陆
            '/v1/user/resetPassword': User.resetPasswd,
            '/v1/user/modifyUserInfo': User.updateUserInfo,
            '/v1/order/create': Order.createOrder,
            '/v1/order/deliver': Order.deliverOrder,
            '/v2/order/unifiedOrderPay': self.unifiedOrderPay,   # 类似微信的预订单，统一下单步骤
            '/v2/transferred/getVerifyCode': Mobile.transferred_Code,  # 转服gm获取验证码
            '/v2/user/transferred': User.transferred_info,  # 转服gm绑定
            '/v2/gm/player/ResetPassword': User.gmResetPassword,  # gm修改玩家密账
        }

        # 第三方回调
        self.callback_path = {
            '/v2/third/callback/q360/pay': q360.pay_callback,
            '/v2/third/callback/oppo/pay': oppo.pay_callback,
            '/v2/third/callback/vivo/pay': vivo.pay_callback,
            '/v2/third/callback/vivo_ad/pay': vivo_ad.pay_callback,
            '/v2/third/callback/weixin/pay': weixin.pay_callback,
            '/v2/third/callback/alipay/pay': ali.pay_callback,
            '/v2/third/callback/huawei/pay': huawei.pay_callback,
            '/v2/third/callback/yyb/pay': yyb.pay_callback,

        }

        # 小游戏接口
        self.smart_game_path = {
            '/v2/third/getUserInfo': SmartGame.getUserInfo,
            '/v2/third/notifyGameResult': SmartGame.notifyGameResult,
            '/v2/third/leave_game': SmartGame.leave_game,
        }

        self.channel_query_path = {

            '/Cpl/repeat': XiaoZhuoAccess.QueryUserExist,
            '/Cpl/search': XiaoZhuoAccess.QueryWinCoin,
        }

    def unifiedOrderPay(self, mi, request):
        channelid = mi.get_param('channelid', '999_0')
        nPayType = mi.get_param('paytype', 0)
        #productId = mi.get_param('pid', '0')
        #shop_config = Context.Configure.get_game_item_json(2, 'shop.config')
        #if channelid == '2000_1' and productId not in shop_config['chip'] and productId not in shop_config['diamond'] and productId not in shop_config['weapon']:
        #    uid = mi.get_param('uid', 0)
        #    pay_total = Context.Data.get_game_attr_int(uid, 2, 'pay_total', 0)
        #    if pay_total < 200:
        #        return MsgPack.Error(0, 8, '需要达到VIP2才可购买该礼包')

        if channelid == '2000_1':
            if nPayType == 1:
                return weixin.unifiedOrderPay(mi, request)
            elif nPayType == 2:
                return ali.unifiedOrderPay(mi, request)
        elif channelid == '1003_0':  # yyb
            return yyb.unifiedOrderPay(mi,request)
        elif channelid == '1004_0':  # oppo
            return oppo.unifiedOrderPay(mi, request)
        elif channelid == '1005_0':  # huawei
            return huawei.unifiedOrderPay(mi, request)
        elif channelid == '1007_2':  # vivo_ad
            return vivo_ad.unifiedOrderPay(mi, request)
        elif channelid == '1007_0':  # vivo
            return vivo.unifiedOrderPay(mi, request)
        elif channelid == '1008_0':  # qh360
            return q360.unifiedOrderPay(mi, request)
        elif channelid == '1100_0':
            from sdk.third import applepay
            return applepay.unifiedOrderPay(mi, request)
        elif channelid == '1000_0' or channelid == '1100_0':
            from framework.entity.globals import Global
            #Context.Log.debug('Global.local_ip', Global.local_ip())
            if '192.168.0.' in Global.local_ip():
                return yyb.unifiedOrderPay(mi, request)


        return MsgPack.Error(0, -1)

    def loginBySdk(self, mi, request):
        param = mi.get_param('channelid', '999_0')
        channelInfo = param.split('_')
        if param == '2000_1':  # 官方微信登录 陆总微信登录
            return weixin.login(mi, request)
        elif channelInfo[0] == '1003':       # 应用宝渠道登录
            return yyb.login(mi, request)
        elif channelInfo[0] == '1004':      # oppo
            return oppo.login(mi, request)
        elif channelInfo[0] == '1005':      # oppo
            return huawei.login(mi, request)
        elif channelInfo[0] == '1007':      # oppo
            return vivo.login(mi, request)
        elif channelInfo[0] == '1008':      # q360
            return q360.login(mi, request)

        return MsgPack.Error(0, User.error_invalid_username, User.desc_invalid_username)

    def __check_legal(self, mi):
        gid = mi.get_param('gameId')
        return gid in Context.Global.game_list()

    def onMessage(self, request):
        if request.method.lower() == 'post':
            if request.path in self.json_path:
                data = request.raw_data()
                mi = MsgPack.unpack(0, data)
                Context.Log.debug(mi)
                if not self.__check_legal(mi):
                    return 'robot'
                # with Context.GData.server_locker:
                return self.json_path[request.path](mi, request)

        if request.path in self.callback_path:
            with Context.GData.server_locker:
                return self.callback_path[request.path](request)

        if request.path in self.smart_game_path:
            with Context.GData.server_locker:
                if request.getClientIP() == '47.99.245.158':

                    data = request.raw_data()
                    mi = MsgPack.unpack(0, data)
                    return self.smart_game_path[request.path](mi)

        if request.path in self.channel_query_path:
            args = request.get_args()
            return self.channel_query_path[request.path](args)

        raise NotFoundException('Not Found')


HttpSdk = HttpSdk()
