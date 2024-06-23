# -*- coding:utf-8 -*-
"""
created by cui
"""

from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from sdk.modules.entity import Entity

APPID = '8451424'
APPKEY = 'Wei1SfBDP84rCVs8428VvPwX'


def parse(dt):
    # appid=134&orderid=tzqgEpl6luIxdwp&amount=100&unit=fen&jfd=478&status=success&paychannel=ct_sfdx&phone=15305000062&channel=CUCC&from=gsdk&sign=145d1821d9ac5d4381fd6f568034f65d&extchannel=17575&cpdefinepart=cporderinfo
    Context.Log.debug(dt)

    param = {
        "appid": dt.get('appid', ''),
        "orderid": dt.get('orderid', ''),
        "amount": dt.get('amount', ''),
        "unit": dt.get('unit', ''),
        "jfd": dt.get('jfd', ''),
        "status": dt.get('status', ''),
        "paychanne": dt.get('paychanne', ''),
        "phone": dt.get('phone', ''),
        "channel": dt.get('channel', ''),
        "from": dt.get('from', ''),
        "sign": dt.get('sign', ''),
        "extchannel": dt.get('extchannel', ''),
        "cpdefinepart": dt.get('cpdefinepart', ''),
    }
    return param


def check_sign(param):
    sign = Entity.baidu_get_sign(param)
    if sign == param['sign']:
        return Order.state_verify_success
    return Order.state_verify_failed_sign


def pay_callback(request):
    args = request.get_args()
    param = parse(args)

    short_order_id = param['cpdefinepart']
    orderId = Order.get_order_id(short_order_id)
    if orderId is None:
        return 100

    price = param['amount']
    status = param['status']
    unit = param['unit']

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return 100

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return 200

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return 'success'

    if status != 'success':
        return 300

    cost = int(orderInfo['cost'])
    if unit == 'fen':
        cost *= 100
    if int(float(price)) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return 5000

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        return 6000

    result = check_sign(param)
    Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        return 7000

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': param['orderid']
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return 'success'
