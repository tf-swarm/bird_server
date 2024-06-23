# -*- coding:utf-8 -*-
"""
created by cui
"""

import json
from sdk.lib.iapppay.crypto import *

from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time


# 联想平台
WaresInfo = {
    "appvkey": "MIICXQIBAAKBgQCQM/00e7Cx5WmkML/SQEyXGRCypKAkOkH4F+K244F5toDBnXQJGY/0iEG77ABMDGVWkv9oDH/dNif+86mn7dU9/MO2ZtdBzHBCHgguuBS9Qq91ZRVG74vomvgOHialgOdK/EgIXKLHjoNfWbAveg1G2p2rgSWQMJQAXXvCVlJM1QIDAQABAoGBAIrSwgxol25roQwEMmbCp/k+lCim+9RkkWW5+PSAiQEXhVTfs/metkt/cWjshkywEk8KLP+KKP5ZSJ/VC5szB3m3gimW+aOvHA0Pmsuy854N2Zks+lFxMCOHOuNSPMPvuTAMhNy7CzIZ7jUSS4HFUSqNAcc55wTZdYTPW04flQ/xAkEAw3gQCp/NBT0iQhI7q2f6orPdWyzh8E0nuK47GjM7h9Q0qjM2Hv0brA/1ikap7hLsfgh4DpW+b5/KePWL66upXwJBALzbyVDLLFsK0vIErE+YUoATU5XQkyyWCXO3znM9zf+DbxwH5ZqZIxM4tmYXdg9NJOPs+Sp5XJoKVuKf9shBEksCQQCBwQFlDA8cmyhSk6focG1/88XM8E5LJexoO8Af9EJgOA19reEPURU9cpqb36yNzSIPx69qfxybHIdbJCRtnNYhAkAn87bayKBRgjCt0h9Bl0+cmHoOL1lzDSpiuHeMGX8ClqNioqkH022AG3c6kawAAKnVLcRoH9RfIeDPgFeMdXeRAkBKgsxBUJGDveJwQsET9BMS1XSLkHVQpVh7/fRminnRieY9gxx+BVBIICr9B8ImK4w0vcErQpsi5jWvJ5wjdaN2",
    "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfMTPtdqtHd5Up8xRS98yeH9EHBmdSpRNyuiBjYzfHua9P7Wxi5vCcwFfwIjx4hvsfGR5o8AKwKgf/7Wopc16uZC/fipSNeaodFfNcDXB3lgl1Ao4ZpywhFFRKqiQvo68O1VVlivRUWVjawZ3wL7HWHZduO1C2J+q9VyUH7tHTrwIDAQAB",
}

# 三星
WaresInfoSamsung = {
    "appvkey": "MIICXAIBAAKBgQCWaFXXsmt2Dd5+DQBH24bZrRztDo5nQOQIIbaCCgLJSNQ3qj9AIFbGKZfUdCEmP3s1Q6XgGbmB/GevphrF3nIikDpsdE7FupwV1nAZHvdjpZcKffFglM0eu38KhjAVuXoYFbzcSGE64LUb6aH7+IZgrsFV26ToL576UEYP2ubK8wIDAQABAoGAAxpT6wc7QEw48tDB2LmmpobzudA7D9Y+3gwT/8rFE/H0rtFMTL5eC+h/wVpD9M4KdKbYnS7qrMvQN8dtdfeI0zWQHkMJMXh9thZHcQPi49X02Rv6H2w2CzHT5M/QJdXUYAW1gc0fHUfjmULWb6k2JMaGSu7MPyQDV+W6iRYdHYECQQDcKo14JLYiHnrbskOtlxDKPoCgA9PoW2vrhqOELhLRvkSgyx1Kk3DJ+cG1sZUXz0YemSIK36GdgZG0B8oo9HOLAkEAruM3wrSRjIb2oFJqxvrimhSMvYFbADzLEss3WO0/4UGI1lvf0bOVQn6K+OtiZm7GXZaBnvAUiI5HFPdNJWlTOQJBAI8kN2AidiwOpxAJgYjuC6OCKXxfoLmUHsE9gzhgACpPyyzDgeLHo3AdqrynnWiigVNJemGZbekKoaFr4xrne+sCQD7pzm1kt9dt1drmyzK5njr/mYGyvyHevM8N++Mptgk6ohc7BdFSYSeCjkvtoYBn6URRmF+szjYxuLB6Jm6G7UECQCXT/tvxv1vtratReaDPrC1OEhPhkkvTnb8tN9vIUpMvxDNSTJvm+CpXlv5a9iE2KdiiUwFe3aaBdMqqXRHIXxo=",
    "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfueYnGPmWYJv3nFgyXGzpWfAt4sBfczdIc8V1sl9MdZe0s+JHywi2OqIWhAus3z52HhoEZ91JunyNuze/0GQlMd1yLpcnSv/WpRO7CVdGE+D+sMtsxuvkYuouPkIqcs/tTgdthVtP3JefPIKO+oEutqm8gdwN0GCWMYm2T2mIXwIDAQAB",
}

# 联想平台
WaresInfoLenovo = {
    "appvkey": "MIICXQIBAAKBgQCQM/00e7Cx5WmkML/SQEyXGRCypKAkOkH4F+K244F5toDBnXQJGY/0iEG77ABMDGVWkv9oDH/dNif+86mn7dU9/MO2ZtdBzHBCHgguuBS9Qq91ZRVG74vomvgOHialgOdK/EgIXKLHjoNfWbAveg1G2p2rgSWQMJQAXXvCVlJM1QIDAQABAoGBAIrSwgxol25roQwEMmbCp/k+lCim+9RkkWW5+PSAiQEXhVTfs/metkt/cWjshkywEk8KLP+KKP5ZSJ/VC5szB3m3gimW+aOvHA0Pmsuy854N2Zks+lFxMCOHOuNSPMPvuTAMhNy7CzIZ7jUSS4HFUSqNAcc55wTZdYTPW04flQ/xAkEAw3gQCp/NBT0iQhI7q2f6orPdWyzh8E0nuK47GjM7h9Q0qjM2Hv0brA/1ikap7hLsfgh4DpW+b5/KePWL66upXwJBALzbyVDLLFsK0vIErE+YUoATU5XQkyyWCXO3znM9zf+DbxwH5ZqZIxM4tmYXdg9NJOPs+Sp5XJoKVuKf9shBEksCQQCBwQFlDA8cmyhSk6focG1/88XM8E5LJexoO8Af9EJgOA19reEPURU9cpqb36yNzSIPx69qfxybHIdbJCRtnNYhAkAn87bayKBRgjCt0h9Bl0+cmHoOL1lzDSpiuHeMGX8ClqNioqkH022AG3c6kawAAKnVLcRoH9RfIeDPgFeMdXeRAkBKgsxBUJGDveJwQsET9BMS1XSLkHVQpVh7/fRminnRieY9gxx+BVBIICr9B8ImK4w0vcErQpsi5jWvJ5wjdaN2",
    "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfMTPtdqtHd5Up8xRS98yeH9EHBmdSpRNyuiBjYzfHua9P7Wxi5vCcwFfwIjx4hvsfGR5o8AKwKgf/7Wopc16uZC/fipSNeaodFfNcDXB3lgl1Ao4ZpywhFFRKqiQvo68O1VVlivRUWVjawZ3wL7HWHZduO1C2J+q9VyUH7tHTrwIDAQAB",
}

# 应用汇平台
WaresInfoYYH = {
    "appvkey": "MIICXQIBAAKBgQCODRUJ1zR5JW3mZOX+oJq45pepCpIdDfKC28e3nhfIoc9MBhxEKEH5/frZpwe7fwkb/WuBWJZ4N3CfnTJSMbUmrluv0UwLgtxXqpNyKFcgQSm5aLjtg9RKXPS5T8f4RZHiw2dmxZZUQaOEHkOi32vKFj++q6eUR1I1t64f8QoYtQIDAQABAoGAVzqJVMWmH05wsi37XeTZnflb4B3xo43RAbJcbdDS4g0a8qA980yVVyIzTDxZbzWPLnTr8z2nCKNisWEiaX7EsdHWjxb3PKkbbEBr1liwnwJva4mbFhWgFpsZyD1f34QLxyXrD1/LWTvtlWOr8qwFBXWJ7q7Cay0BxwmLOW/eAQECQQDlnkcgLtGbIBfoUYFH70yF/qSqxesAXo74RwdCKsD5inmu6q2jnLoK0A5CnvtvdcYURDf0zY67OTFKpJQ70dPRAkEAnl802eMp33CX0v/rZxDiV6npJgb142x+e84q0crvQ2hcODkbsAqXzS/RC0ryPsc2meRLMcs51wbMbR/rDicjpQJBAJ3xucsRaWzjLo7HQb5RhLnG503wxi2C3aU6dmu1LPh5oCoJk1cvv2kgpC5/XUTWJmJaaoMhwkRWmulVPAHJ24ECQQCF0erlpbaPECOp7geqajDnZDIWqNEC330s/fNenDx6V+d8tny3zuugPKRGB4kUFN8FQEttgsyX7i20k8DZj6blAkBegnlyI26XLdg4nvdoiYsuhKOulBK4b2e6pPmDlvZlNYaiEnqYXFPcePsI2n2lrh5+7en8tAfimHVS13FELgy5",
    "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCId49p6h37XcN43TfMPhCyO4G3fI4FFapa5iNS4cKujF4AKWii5w477QXoLNa2EPOGm1eTjVK1Ct3q9XAkT+JnFX7eN6N6UxBugO8q3x216Z31Ay2H5ixkq6cX/EoJYHkEkW7vNwbc+kWYYR+1lujSeWGKTKgnGNxrVkCOgeZe+wIDAQAB",
}
# 酷派
WaresInfoCoolpad = {
    "appvkey": "MIICWwIBAAKBgQCqNHBQ91/gf1NEdL3vyxwVldvOuGpmShFlrw8N+Y/rz3L35ZKVyyaUHn6gHfC+1FjP+1RBupktdjpsa6MzZhxQGjRQg5VnJGURfdeiA/xPzHVAJzK0yeRK4SngeKo2OKrB9T/BXohJi3SoK7BQlYsCYppijH7hMpUUZIKvlXh9QwIDAQABAoGAdeZPKvbAdk0ci93mN/XU5WriUQbTxTlnZa1m20JVHH6d3/QpnxOTDKU3B4jV3ApR3vf0vHcaZjBwdev1p8QCtaSsbgqqxRE7/svCzx/ivyZxjPcK/zecScxhxM2mlzpBygXAlTfWttvF6inLI2hegm8YSX0wC+OE4ViNf7H9BqkCQQDXXmSCog4YTDv1auvHi4uNgSGYV6h0oFox/pedNdn3r+FDiAkEPjA+tPeu+o9MCa78thUX8FTxS0+FsbzGv/h9AkEAylDHHKat+nI23DUjh6xIJ9REZ5LZS6GCEwvbTDT3QfjuPfQ4/YgY5BrEesNFWlgX7353urASdp5py7v2van4vwJATviWxGvl3TT++2OkZzwdBNsn1XO3GmS+Dfz73TKk5TTB1gBoxfyDtkqnU6seplQarSGbJHcEvqHN3AkrXnmABQJAWeRAQ/OvM6sRww/9RGgA+2luJ1LxJ5CQWeQXwSl7fx2axX5A4C1bWeamzCD9LKIdqHTZv+JBoeDLAxH2FNlzwwJAXOulQMD/BQCY5DqZez1K2ra7TWV+6F1s+uEMW9l7qVCk43Q+PKzWloNlO54jsYEqYGpJ6PrKfN881dNPVnjLLg==",
    "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCdzw/lA++RzOLzKmlu9ID1mjs3DiAqeTit3vXwokoCcD63k1NC/GPMD/RpeAWW/ZTOyHjyeEmNv+mpmRl2Vc02Ixg4yAnJuS5JG23qwvzFvtQIC8sw+KD3LxvJt4dvP9t3tc2IYMM3gsrbc3GfP4zrY0K0t6BIA7Rk9xi45tVH1QIDAQAB",
}


'''
    得到post请求数据   格式：transdata={"appid":"3002575350","appuserid":"koudaiduobao@163.com","cporderid":"55ee3ad5c0dc98896ba2f56f","cpprivate":"pay","currency":"RMB","feetype":0,"money":10.00,"paytype":403,"result":0,"transid":"32051509080933097603","transtime":"2015-09-08+09:33:23","waresid":1}&sign=SysEX4qiACqivH1SlhlvAWJ9ZDh63tVkKUtWx9MsRv6Lj8kmNQAPYfqzdTui/7wN7olAgkgWZ0qfnNrDqXyvMscEGZAg5WrGRH8Luufwbhzz5m9Is2clLM87N+hrrzAekJuTdJwFdyBAFwt4ZrvIzFRRSuyPXnWGkQXK3/4neU4=&signtype=RSA
    然后调用   验签函数
    分割数据 并且把数据传入验签函数中验签  返回值为： bool类型
'''


def pay_callback_yyh(request):
    return do_pay_callback(request, wares_info=WaresInfoYYH)


def pay_callback(request):
    return do_pay_callback(request, wares_info=WaresInfo)


def pay_callback_lenovo(request):
    return do_pay_callback(request, wares_info=WaresInfoLenovo)


def pay_callback_samsung(request):
    return do_pay_callback(request, wares_info=WaresInfoSamsung)


def pay_callback_coolpad(request):
    return do_pay_callback(request, wares_info=WaresInfoCoolpad)


def do_pay_callback(request, wares_info=None):
    if not wares_info:
        wares_info = WaresInfo

    if not request.args.get('transdata'):
        return 'FAILURE'

    reqData = ''
    reqData += 'transdata'
    reqData += '='
    reqData += request.args.get('transdata')[0]
    reqData += '&'

    reqData += 'sign'
    reqData += '='
    reqData += request.args.get('sign')[0]
    reqData += '&'

    reqData += 'signtype'
    reqData += '='
    reqData += request.args.get('signtype')[0]

    transdata = json.loads(request.args.get('transdata')[0])

    orderId = transdata.get('cporderid')
    app_id = transdata.get('appid')
    money = transdata.get('money')
    res = transdata.get('result')
    # userId = int(transdata.get('appuserid'))
    currency = transdata.get('currency')

    orderInfo = Order.getOrderInfo(orderId)
    if not orderInfo:
        return 'FAILURE'

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return 'FAILURE'

    productId = orderInfo['productId']

    if currency != "RMB":
        return 'FAILURE'

    cost = int(orderInfo['cost'])
    if int(money) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return 'FAILURE'

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:        # 可能并没有成功, 需要检查对单
        return 'SUCCESS'

    gameId = int(orderInfo['gameId'])
    userId = int(orderInfo['userId'])

    if res != 0:
        return 'FAILURE'

    crypto = CryptoHelper()
    platpkey = CryptoHelper.importKey(wares_info["platpkey"])
    i= crypto.segmentation_data(reqData,platpkey)
    if not i:
        return 'FAILURE'

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': transdata.get('transid', '')
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return 'SUCCESS'
