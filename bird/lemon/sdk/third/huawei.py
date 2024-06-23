# -*- coding:utf-8 -*-
"""
created by cui
"""

from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from sdk.modules.entity import Entity
from sdk.modules.user import User
from sdk.const import Const
from framework.entity.msgpack import MsgPack
from sdk.modules.account import Account

APPID = '8451424'
APPKEY = 'Wei1SfBDP84rCVs8428VvPwX'

URL_NOTIFY_PAY = 'http://xmttbn.zxyzttbn.com:8080/v2/third/callback/huawei/pay'

def login(mi, request):
    param = User.getParam(mi, 'uid')
    nick = param['nick']
    gid = param['gameId']
    openid = param['uid']
    paramChannel = param['channelid']
    realChannel = paramChannel.split('_')[0]
    userId = Context.RedisMix.hash_get('%s.%s.uid' % (realChannel, gid), openid, None)

    if not userId:
        param['nick'] = nick
        channel = paramChannel
        idType = Const.IDTYPE_SDK
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('%s.%s.uid' % (realChannel, gid), openid, userId)

    userId = int(userId)
    userInfo = Account.getUserInfo(userId)
    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, True, openid=openid, loginChannelId=param['channelid'])

# 获取预订单
def unifiedOrderPay(mi, request):
    gid = mi.get_param('gameId', 2)
    productId = mi.get_param('pid', '0')
    uid = mi.get_param('uid', 0)
    payType = 3 #mi.get_param('paytype', 3)  # 第三方支付方式
    if not Order.judge_exist_product_id(gid, productId):
        return MsgPack.Error(0, 1, 1)  # 无此产品
    # 获取产品信息
    #productInfo = product_config[productId]
    dt = Time.datetime()
    # 生成订单id
    order_info = Order.otherCreateOrder(gid, uid, productId, "huawei", "android")
    if order_info.is_error():
        return MsgPack.Error(0, 8, 'order create fail')

    order_id = order_info.get_param('orderId')

    kvs = {
        'thirdOrderId': 0,
        'paytype': payType
    }
    Order.updateOrder(order_id, **kvs)

    dictInfo = {}
    dictInfo['pid'] = productId
    dictInfo['orderid'] = order_id
    dictInfo['paytype'] = payType
    dictInfo['p_name'] = order_info.get_param('title')
    dictInfo['p_desc'] = order_info.get_param('title')
    dictInfo['price'] = order_info.get_param('price')

    return MsgPack(0, dictInfo)

def parse(dt):
    # result=0&userName=900086000010001040&productName=Pre01_Support01&payType=4&amo unt=0.01&orderId=A20151208134103929B26A41&notifyTime=1449556782720&requestId=1000 00000000000116&signType=RSA256&sign=HlOkSVtPfyr3hguNIRbdWLDSeBHst5vQjIqvQ9E9d7XE 2YvicdiE57j5C7Mep2OkXO6jlAsry13zo8acw4bFYA%3D%3D
    Context.Log.debug(dt)

    param = {
        "result": dt.get('result'),
        "userName": dt.get('userName'),
        "productName": dt.get('productName'),
        "payType": dt.get('payType'),
        "amount": dt.get('amount'),
        "orderId": dt.get('orderId'),
        "notifyTime": dt.get('notifyTime'),
        "requestId": dt.get('requestId'),
        "bankId": dt.get('bankId'),
        "orderTime": dt.get('orderTime'),
        "tradeTime": dt.get('tradeTime'),
        "accessMode": dt.get('accessMode'),
        "spending": dt.get('spending'),
        "extReserved": dt.get('extReserved'),
        "sysReserved": dt.get('sysReserved'),
        "signType": dt.get('signType'),
        "sign": dt.get('sign'),
    }
    return param


def check_sign(param):
    if Entity.huawei_verify_sign(param):
        return Order.state_verify_success
    return Order.state_verify_failed_sign


def pay_callback(request):
    args = request.get_args()
    param = parse(args)

    if param['result'] != '0':
        return 0
    orderId = param['requestId']
    price = param['amount']

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return 99

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return 99

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return 0

    cost = float(orderInfo['cost'])
    if float(price) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return 99

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        return 99

    result = check_sign(param)
    Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        return 1

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': param['orderId']
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, orderInfo['paytype']):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return 0
