# -*- coding:utf-8 -*-
"""
created by cui
"""

from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time, Tool

from framework.entity.msgpack import MsgPack
import httplib
import json
import base64

URL_SANDBOX = 'https://sandbox.itunes.apple.com/verifyReceipt'
URL_RELEASE = 'https://buy.itunes.apple.com/verifyReceipt'

# 主动查询订单
def orderquery(orderId, token):
    json_data = Context.json_loads(token)

    #Context.Log.debug('decodedJson', decodedJson)   # 测试查看
    #f producId == xxx and status ==0 and environment != "Sandbox"
    #    transaction_id

    receipt = json_data['Payload']  # base64.b64encode(Context.json_dumps(json_data))
    pay_receipt = json.dumps({"receipt-data": receipt})
    result = Context.WebPage.wait_for_json(URL_SANDBOX, postdata=pay_receipt)
    Context.Log.debug('result', result)
    if result['status'] == 0: # 支付成功
        #if result['environment'] == 'Sandbox':
        #    return 0
        orderInfo = Order.getOrderInfo(orderId)
        thirdOInfo = result['receipt']['in_app'][0]
        if thirdOInfo['product_id'] == orderInfo['productId']:    # 同样的产品类型
            data = Context.RedisStat.list_range('order:2:%s:user' % orderInfo['userId'], 0, -1)
            for orderid in data:
                order_info = Context.RedisPay.hash_getall('order:' + orderid)
                if order_info['thirdOrderId'] == thirdOInfo['transaction_id']:  # 已完成订单
                    return -1
            kvs = {
                'thirdOrderId': thirdOInfo['transaction_id']
            }
            Order.updateOrder(orderId, **kvs)
            return 1

        return 0
    #    return 0
    return 0

def unifiedOrderPay(mi, request):
    gid = mi.get_param('gameId', 2)
    productId = mi.get_param('pid', '0')
    uid = mi.get_param('uid', 0)
    payType = 3 #mi.get_param('paytype', 3)  # 第三方支付方式
    if not Order.judge_exist_product_id(2, productId):
        return MsgPack.Error(0, 1, 1)  # 无此产品
    # 获取产品信息
    #productInfo = product_config[productId]
    dt = Time.datetime()
    # 生成订单id
    order_info = Order.otherCreateOrder(gid, uid, productId, "applepay", "ios")
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
    dictInfo['price'] = int(float(order_info.get_param('price')) * 10)
    return MsgPack(0, dictInfo)

