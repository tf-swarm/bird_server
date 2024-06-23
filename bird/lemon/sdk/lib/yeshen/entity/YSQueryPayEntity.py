# coding=utf-8
__author__ = 'pan'

from sdk.lib.yeshen.entity.YSBaseEntity import YSBaseEntity


class YSQueryPayEntity(YSBaseEntity):
    def __init__(self):
        YSBaseEntity.__init__(self)
        self.appId = "null"  # 应用ID，在nox 平台上申请获取的
        self.goodsOrderId = "null"  # 用户自定义订单
        self.orderId = "null"  # 订单编号

    def getAppId(self):
        return self.appId

    def setAppId(self, appId):
        self.appId = appId

    def setGoodsOrderId(self, goodsOrderId):
        self.goodsOrderId = goodsOrderId

    def getGoodsOrderId(self):
        return self.goodsOrderId

    def setOrderId(self, orderId):
        self.orderId = orderId

    def getOrderId(self):
        return self.orderId

    def toString(self):
        return "YSQueryPayEntity [appId=" + self.appId + ", goodsOrderId=" + self.goodsOrderId + ", orderId=" + self.orderId + "]"