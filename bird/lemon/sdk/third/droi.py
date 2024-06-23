#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-05-23

from sdk.const import Const
from sdk.modules.user import User
from sdk.modules.order import Order
from sdk.modules.account import Account
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm
from framework.entity.msgpack import MsgPack


class Droi(object):
    app_id = '2772'
    login_url = 'http://open.zhuoyi.com/phone/index.php/ILoginAuth/auth'
    server_key = '8fdfa5dedad2cdbe35e1c16faf92218f'

    def verify_login(self, uid, token):
        param = {
            'uid': uid,
            'access_token': token,
            'app_id': int(self.app_id)
        }
        s = 'uid=%s&access_token=%s&app_id=%s&key=%s' % (uid, token, self.app_id, self.server_key)
        sign = Algorithm.md5_encode(s)
        param['sign'] = sign
        response = Context.WebPage.wait_for_json(self.login_url, query=param, method='GET')
        if int(response['code']) == 0:
            return True
        else:
            return False

    def parse(self, dt):
        Context.Log.debug(dt)
        param = {
            "Recharge_Id": dt.get('Recharge_Id'),
            "App_Id": dt.get('App_Id'),
            "Uin": dt.get('Uin'),
            "Urecharge_Id": dt.get('Urecharge_Id'),
            "Extra": dt.get('Extra'),
            "Recharge_Money": dt.get('Recharge_Money'),
            "Recharge_Gold_Count": dt.get('Recharge_Gold_Count'),
            "Pay_Status": dt.get('Pay_Status'),
            "Create_Time": dt.get('Create_Time'),
            "Sign": dt.get('Sign')
        }
        return param

    def check_sign(self, sign, param):
        if sign:
            copy_param = Context.copy_json_obj(param)
            del copy_param['Sign']
            query_param = [(k, v) for k, v in copy_param.items() if v is not None]
            query_param.sort(key=lambda item: item[0])
            s = Context.Strutil.url_encode(query_param) + self.server_key
            _sign = Algorithm.md5_encode(s)
            if _sign == sign:
                return Order.state_verify_success
        return Order.state_verify_failed_sign

    def login(self, mi, request):
        param = User.getParam(mi, 'accessToken', 'uid', 'devName', 'nickName')
        result = self.verify_login(param['uid'], param['accessToken'])
        if not result:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

        gid = param['gameId']
        openid = param['uid']
        userId = Context.RedisMix.hash_get('droi.%s.uid' % gid, openid)
        if not userId:
            channel = 'droi'
            idType = Const.IDTYPE_DROI
            userId = User.register(param, request, openid, idType, channel)
            if not userId:
                return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
            Context.RedisMix.hash_set('droi.%s.uid' % gid, openid, userId)
        userId = int(userId)
        userInfo = Account.getUserInfo(userId)

        return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])

    def pay_callback(self, request):
        args = request.get_args()
        param = self.parse(args)

        if param['Pay_Status'] != '1':
            return 'success'

        orderId = param['Urecharge_Id']
        price = param['Recharge_Money']
        parseInfo = Order.parse_order(orderId)
        if not parseInfo:
            return 'failure'

        orderInfo = Order.getOrderInfo(orderId)
        Context.Log.debug('orderInfo-----', orderInfo)
        if not orderInfo:
            return 'failure'

        state = int(orderInfo['state'])
        if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
            return 'success'

        cost = int(orderInfo['cost'])
        if int(float(price)) != cost:
            Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
            return 'failure'

        userId = int(orderInfo['userId'])
        gameId = int(orderInfo['gameId'])
        channel = orderInfo['channel']
        productId = orderInfo['productId']

        if not Order.judge_exist_product_id(2, productId):
            Context.Log.error('productId not exist', orderId, productId)
            return 'failure'

        result = self.check_sign(param['Sign'], param)
        Order.updateOrder(orderId, state=result)
        if result != Order.state_verify_success:
            return 'failure'

        Order.updateOrder(orderId, state=Order.state_pre_deliver)
        kvs = {
            'payTime': param['Create_Time'],
            'deliverTime': Time.current_time(),
            'thirdOrderId': param['Recharge_Id']
        }
        if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
            kvs['state'] = Order.state_deliver_success
        else:
            kvs['state'] = Order.state_deliver_failed

        Order.updateOrder(orderId, **kvs)
        return 'success'


Droi = Droi()
