# coding=utf-8
__author__ = 'pan'

import json
from sdk.lib.yeshen.utils.AlgorithmUtil import AlgorithmUtil
from sdk.lib.yeshen.utils.NoxConstant import NoxConstant
from sdk.lib.yeshen.utils.HttpClientUtil import HttpClientUtil
from sdk.lib.yeshen.entity.YSPayResponseEntity import YSPayResponseEntity
from sdk.lib.yeshen.entity.YSPassportResponseEntity import YSPassportResponseEntity
from sdk.lib.yeshen.entity.YSQueryPayEntity import YSQueryPayEntity


class NoxSDKServer(object):
    def __init__(self, appId, appKey):
        self.appId = appId
        self.appKey = appKey

    def getNotifyResult(self, params):
        algorithm = AlgorithmUtil(self.appKey)
        verify = algorithm.verify_rsa_sign(params, NoxConstant.YESHEN_PUBLIC_KEY)
        if verify:
            payEntity = YSPayResponseEntity()
            payEntity.dict_to_object(params)
            return payEntity
        else:
            raise ValueError('验证签名失败')

    def getPayResultByYeshenOrderId(self, yeshenOrderId, privateKey):
        queryPayEntity = YSQueryPayEntity()
        queryPayEntity.setAppId(self.appId)
        queryPayEntity.setOrderId(yeshenOrderId)
        return self._getPayResult(queryPayEntity, privateKey)

    def getPayResultByMchOrderId(self, mchOrderId, privateKey):
        queryPayEntity = YSQueryPayEntity()
        queryPayEntity.setAppId(self.appId)
        queryPayEntity.setGoodsOrderId(mchOrderId)
        return self._getPayResult(queryPayEntity, privateKey)

    def _getPayResult(self, queryPayEntity, privateKey):
        payEntity = YSPayResponseEntity()
        try:

            query_dict = queryPayEntity.convert_to_dict()

            algorithm = AlgorithmUtil(self.appKey)
            sign = algorithm.build_rsa_sign(query_dict, privateKey)
            query_dict['sign'] = sign
            retJsonStr = HttpClientUtil.post(NoxConstant.QUERY_PAY_RESULT_URL, json.dumps(query_dict))
            retDict = json.loads(retJsonStr)
            verify = algorithm.verify_rsa_sign(retDict, NoxConstant.YESHEN_PUBLIC_KEY)
            if verify:
                payEntity.dict_to_object(retDict)
                return payEntity
            else:
                raise ValueError("验证签名失败")

        except Exception as ex:
            import traceback

            traceback.print_exc()
            pass

        return payEntity

    def validate(self, accessToken, uid):
        resultEntity = YSPassportResponseEntity()
        try:
            paramsJoin = "?accessToken=" + accessToken + "&uid=" + uid + "&appId=" + self.appId
            resultJson = HttpClientUtil.get(NoxConstant.QUERY_PASSPORT_RESULT_URL + paramsJoin)
            if resultJson:
                resultEntity.dict_to_object(json.loads(resultJson))

        except Exception as e:
            import traceback

            traceback.print_exc()
        return resultEntity
