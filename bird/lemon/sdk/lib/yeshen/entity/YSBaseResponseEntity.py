# coding=utf-8
__author__ = 'pan'

from sdk.lib.yeshen.entity.YSBaseEntity import YSBaseEntity


class YSBaseResponseEntity(YSBaseEntity):
    def __init__(self):
        YSBaseEntity.__init__(self)
        self.errNum = 'null'  # 错误码
        self.errMsg = 'null'  # 错误信息
        self.sign = 'null'  # 签名

    def setErrNum(self, errNum):
        self.errNum = errNum

    def getErrNum(self):
        return self.errNum

    def setErrMsg(self, errMsg):
        self.errMsg = errMsg

    def getErrMsg(self):
        return self.errMsg

    def setSign(self, sign):
        self.sign = sign

    def getSign(self):
        return self.sign
