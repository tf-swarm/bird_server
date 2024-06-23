# coding=utf-8
__author__ = 'pan'

from sdk.lib.yeshen.entity.YSBaseResponseEntity import YSBaseResponseEntity


class YSPayResponseEntity(YSBaseResponseEntity):
    def __init__(self):
        YSBaseResponseEntity.__init__(self)
        self.appId = "null"  # 应用ID，在nox 平台上申请获取的
        self.uid = "null"  # 用户ID
        self.payStatus = "null"  # 支付状态1待支付 2成功 3失败
        self.goodsTitle = "null"  # 商品名称
        self.goodsOrderId = "null"  # 商品订单
        self.goodsDesc = "null"  # 商品描述
        self.orderMoney = "null"  # 订单金额
        self.orderId = "null"  # 订单号
        self.orderTime = "null"  # 订单时间
        self.privateInfo = "null"  # 用户私有信息
        self.appName = "null"  # 应用名称

    def getAppId(self):
        return self.appId

    def setAppId(self, appId):
        self.appId = appId

    def getUid(self):
        return self.uid

    def setUid(self, uid):
        self.uid = uid

    def getPayStatus(self):
        return self.payStatus

    def setPayStatus(self, payStatus):
        self.payStatus = payStatus

    def getGoodsTitle(self):
        return self.goodsTitle

    def setGoodsTitle(self, goodsTitle):
        self.goodsTitle = goodsTitle

    def getGoodsOrderId(self):
        return self.goodsOrderId

    def setGoodsOrderId(self, goodsOrderId):
        self.goodsOrderId = goodsOrderId

    def getGoodsDesc(self):
        return self.goodsDesc

    def setGoodsDesc(self, goodsDesc):
        self.goodsDesc = goodsDesc

    def getOrderMoney(self):
        return self.orderMoney

    def setOrderMoney(self, orderMoney):
        self.orderMoney = orderMoney

    def getOrderId(self):
        return self.orderId

    def setOrderId(self, orderId):
        self.orderId = orderId

    def getOrderTime(self):
        return self.orderTime

    def setOrderTime(self, orderTime):
        self.orderTime = orderTime

    def getPrivateInfo(self):
        return self.privateInfo

    def setPrivateInfo(self, privateInfo):
        self.privateInfo = privateInfo

    def getAppName(self):
        return self.appName

    def setAppName(self, appName):
        self.appName = appName

    def toString(self):
        return "YSPayResponseEntity [appId=" + self.appId + ", uid=" + self.uid + ", payStatus=" + str(self.payStatus) + \
               ", goodsTitle=" + self.goodsTitle + ", goodsOrderId=" + self.goodsOrderId + ", goodsDesc=" + self.goodsDesc \
               + ", orderMoney=" + str(self.orderMoney) + ", orderId=" + self.orderId + ", orderTime=" + str(self.orderTime) + \
               ", privateInfo=" + self.privateInfo + ", appName=" + self.appName + "]"
