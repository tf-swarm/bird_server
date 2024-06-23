# -*- coding:utf-8 -*-
"""
created by cui
"""

from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm


APPKEY = '153a47e3e374003a72348e5e30992701'
APPID = 'i4617'


def pay_callback(request):

    req = request.get_args()
    user_id = req.get('user_id')
    role_id = req.get('role_id')
    order_id = req.get('order_id')
    money = req.get('money')
    orderId = req.get('userData')
    _time = req.get('time')
    sign = req.get('sign')

    orderInfo = Order.getOrderInfo(orderId)
    if not orderInfo:
        return -6

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return -6

    productId = orderInfo['productId']

    cost = int(orderInfo['cost'])
    if int(money) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return -6

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:        # 可能并没有成功, 需要检查对单
        return 0

    gameId = int(orderInfo['gameId'])
    userId = int(orderInfo['userId'])

    sign_data = user_id + role_id + order_id + money + _time + APPKEY
    _sign = Algorithm.md5_encode(sign_data)
    if sign != _sign:
        return -1

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': order_id
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return 0
