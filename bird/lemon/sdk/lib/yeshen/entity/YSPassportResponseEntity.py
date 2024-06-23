# coding=utf-8
__author__ = 'pan'

from sdk.lib.yeshen.entity.YSBaseEntity import YSBaseEntity


class YSPassportResponseEntity(YSBaseEntity):
    def __init__(self):
        YSBaseEntity.__init__(self)
        self.errNum = "null"  # 错误码
        self.errMsg = "null"  # 错误信息
        self.transdata = None  # 业务数据

    def setErrNum(self, errNum):
        self.errNum = errNum

    def getErrNum(self):
        return self.errNum

    def setErrMsg(self, errMsg):
        self.errMsg = errMsg

    def getErrMsg(self):
        return self.errMsg

    def setTransdata(self, transdata):
        self.transdata = transdata

    def getTransdata(self):
        return self.transdata

    def toString(self):
        return "YSPassportResponseEntity [errNum=" + self.errNum + ", errMsg=" + self.errMsg + ", transdata=" + \
               self.transdata + "]"