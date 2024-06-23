# coding=utf-8
__author__ = 'pan'


class NoxConstant(object):
    QUERY_PAY_RESULT_URL = "https://pay.yeshen.com/ws/payapi/v3/trade/query"
    QUERY_PASSPORT_RESULT_URL = "https://passport.bignox.com/sso/o2/validation"
    PARAM_SIGN = "sign"
    PARAM_APP_ID = "appid"
    SUCCESS = '0'
    FAILED = '-1'
    MSG_SUCCESS = "SUCCESS"
    MSG_FAILURE = "FAILURE"
    MSG_PASSPORT_VALID = "1"
    MSG_PASSPORT_INVALID = "0"
    SIGN_MD5_TYPE = "MD5"
    INPUT_CHARSET = "utf-8"

    YESHEN_PUBLIC_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5FLkp9rQ/o4GlZDwPbHuBwTlkh4syOoKytCRcxX1KNwxFxPB5BwPRNuCY+x/VcgMjt/D8xyj0VnidlihuTBOT18kjcg/Ouhk83dt0maXVJ4lA3Rmq3FN4gzXR0ZQe021wfSbElCAlHt2Y5xIh34X8N1LNabYpHnmHiTcnOnseIZGqRNObRXduGDTm7i4UZeK77OGw/uwK0Piqp09V/lTkPExHq9sugXoYo6cIlNFLX0f330gydlQTFCeWIfg74Z3m8LEt/Vytq0WoVJqtbuLhcpBtB2cK8yET5Cw71Z/f1TQismhXwUVpBmYwRuhMg2YAtwbrQAihkydowQTDyhSfQIDAQAB"

    def __init__(self):
        pass
