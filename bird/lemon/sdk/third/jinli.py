# -*- coding:utf-8 -*-
"""
created by cui
"""

from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm


publickey = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCM22u3lJmMVi1t/+JKKCaccnsbrSrOj+CbVif7vh4sfm+JRcLnxxRei5JK4KWuREtXTtM70YMY7hWJXP/rc80VrKkZoUaOi8t4FggtJdhBHC/blEZD2wG+drNsmWkYkDSLgTIPr6IoyuO0MNRMl/Plw15v4MlvRMHY3sWMgNKp1wIDAQAB
-----END PUBLIC KEY-----'''


def parse(dt):
    Context.Log.debug(dt)
    param = {
        "api_key": dt.get('api_key'),
        "close_time": dt.get('close_time', ''),
        "create_time": dt.get('create_time', ''),
        "deal_price": dt.get('deal_price', 0),
        "out_order_no": dt.get('out_order_no', ''),
        "pay_channel": dt.get('pay_channel', 0),
        "submit_time": dt.get('submit_time', ''),
        "user_id": dt.get('user_id', ''),
        "sign": dt.get('sign', ''),
    }
    return param


def check_sign(param):
    keys = param.keys()
    keys.sort()
    keys.remove('sign')
    sign_data = ''
    for key in keys:
        if sign_data:
            sign_data += '&'
        sign_data += key
        sign_data += '='
        sign_data += param.get(key, '')
    if Algorithm.verify_rsa(publickey, sign_data, param['sign']):
        return Order.state_verify_success
    return Order.state_verify_failed_sign


def pay_callback(request):
    args = request.get_args()
    param = parse(args)

    orderId = param['out_order_no']
    price = param['deal_price']

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return 'failed'

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return 'failed'

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return 'success'

    cost = int(orderInfo['cost'])
    if int(float(price)) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return 'failed'

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    channel = orderInfo['channel']
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        return 'failed'

    result = check_sign(param)
    Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        return 'failed'

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return 'success'
