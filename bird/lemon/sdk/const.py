#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-09-23

from framework.entity import const


class Const(const.Const):
    # 通用错误
    E_USER_LOCKED = -100
    ES_USER_LOCKED = "user locked"
    E_NOT_LOGIN = -101
    ES_NOT_LOGIN = "not login"
    E_EXCEPTION = -102
    ES_EXCEPTION = "internal exception"
    E_BAD_URL = -103
    ES_BAD_URL = "bad url"
    E_BAD_REDIS = -104
    ES_BAD_REDIS = "bad redis"
    E_BAD_CONFIG = -105
    ES_BAD_CONFIG = "bad config"

    # 定义ID类型
    IDTYPE_ROBOT = 10          # 机器人
    IDTYPE_USERNAME = 11       # 用户名登陆
    IDTYPE_GUEST = 12          # 游客用户类型
    IDTYPE_MOBILE = 13         # 手机用户类型
    IDTYPE_QiHoo360 = 14       # 360
    IDTYPE_XIAOMI = 15       # KSYUN_MI 金山云 小米sdk
    IDTYPE_ANZHI = 16          # 安智
    IDTYPE_GUOPAN = 17         # 果盘
    IDTYPE_CCPAY = 18          # 虫虫
    IDTYPE_PAPA = 19           # 啪啪
    IDTYPE_YINGYONGHUI = 20    # 应用汇
    IDTYPE_DROI = 21           # 卓易
    IDTYPE_XUNLEI = 22         # 迅雷
    IDTYPE_OPPO = 23           # oppo
    IDTYPE_COOLPAD = 24        # 酷派
    IDTYPE_WANDOUJIA = 25      # 豌豆荚
    IDTYPE_MEIZU = 26          # 魅族
    IDTYPE_BAZHANG7723 = 27    # 7723
    IDTYPE_EGAME = 28          # 爱游戏
    IDTYPE_VIVO = 29           # VIVO
    IDTYPE_LESHI = 30          # 乐视
    IDTYPE_TONGBUTUI = 31      # 同步推
    IDTYPE_7659 = 32           # 7659
    IDTYPE_hxpay = 33          # yufutong
    IDTYPE_YESSHEN = 34        # 夜神

    IDTYPE_SDK = 35     # sdk 登录


    # 定义密码类型
    PASSWORD_TYPE_TEXT = 0
    PASSWORD_TYPE_MD5 = 1

    SEX_MAN = 0
    SEX_WOMAN = 1

    MAX_AVATAR_NUMBER = 2
    DEFAULT_AVATAR_MAN = ['1']
    DEFAULT_AVATAR_WOMAN = ['2']
    AVATAR_MAN = ['1','3']
    AVATAR_WOMAN = ['2','4']
    AVATAR_ALL = ['5','6']

    MEIZU_APPID = '3099526'
    MEIZU_SECRETKEY = '0lBdZ9s9cvkUne17HhhszBxiKhDnBccc'

    VIVO_APPID = '990c94a3cb238244a4e54ea658f57431'
    VIVO_CPID = '20160603211453353712'
    VIVO_CPKEY = 'e756296d1a962c7151a6ea86bfd583ab'
    VIVO_URL = 'https://pay.vivo.com.cn/vivoPay/getVivoOrderNum'

    BAIDU_SECRET = 'G9FEQ4gzXB0Qt4lbg9ziwoSeg7sr4cpG'


    HUAWEI_APPID = '100589301'
    HUAWEI_USERID = '890086000102192605'
    HUAWEI_PUBLICKEY = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwd+jt3EO41AM5ozOmP5lbKyqoFNFpaO0WuartxUJNqmXE4iQAVggto3wS61G165gFb3oK113xpB337YDpeI3mJV4wWR8vPFeQYDVuUNMpSrJmn+7tk4tF0o8dmV9QkYIeEkmRsVaZhVYAhnWuTxsCRs/1XP2MHoV2dzojzpGD4K2A5o29c2BgmZ2qHlRBJO1lRG6iabJjN1zZ/z/dLg4bQzcqnu4BXTkH5KTlFKTleVXVPmh/ijtHe1f/yqE383gj9+l+S21kfiun1g+uE6SH/D0DdOOx7vFCc0NHaeDY7y4rHxzeIkjQW4MeldmVYRXcK942/Tozrd7OgCU4MFoVQIDAQAB
-----END PUBLIC KEY-----'''

    HUAWEI_PRIVATEKEY = '''-----BEGIN RSA PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDB36O3cQ7jUAzmjM6Y/mVsrKqgU0Wlo7Ra5qu3FQk2qZcTiJABWCC2jfBLrUbXrmAVvegrXXfGkHfftgOl4jeYlXjBZHy88V5BgNW5Q0ylKsmaf7u2Ti0XSjx2ZX1CRgh4SSZGxVpmFVgCGda5PGwJGz/Vc/YwehXZ3OiPOkYPgrYDmjb1zYGCZnaoeVEEk7WVEbqJpsmM3XNn/P90uDhtDNyqe7gFdOQfkpOUUpOV5VdU+aH+KO0d7V//KoTfzeCP36X5LbWR+K6fWD64TpIf8PQN047Hu8UJzQ0dp4NjvLisfHN4iSNBbgx6V2ZVhFdwr3jb9OjOt3s6AJTgwWhVAgMBAAECggEAKHo74UnulNEa0GvnmpPKs0Tdnvmj2fBy8GOmyGPQ96Oy0jY58r3mnpbF69byqodSsldjCOLL5h41mPSUkGbJusbCXoZPcNdoGX7/oF2HvBhR3Tr8AxURXwJ12zZXT6X1kL+dCTudIyEjrdSdOzF9UO1qh3NdnENxGnp/55+ADy6bH6LK8T+fYSMJ2DAytJrFWb+48xmEvPpobnjP6j/bPlu9m5gyGs/QVhCf/WFahDu/23MNtAwPRycyzmr/O3dXcZFdNWf/95Oud1DjI7KlViQI2A3LgG4CI4kAOFbiB2yIb/FnvATywDCoVWOYdYnGFRf6ATtx9yl5tObOrAQUgQKBgQDnbWWKKptZxp0CI/kDI/ypA8eR/nEZk95utbDWzHzG1roFgY5zcMynL0LyWYv6K8jEv8PeAct/0kA9jeXPdThLjSEYMLIrL2/LR4jTDep73T0fm67aMjJpMLKb395aUgP/RIOe0hKIZWGrY/QdbWLti7PkNi9q+Y703eA5Kw/d4QKBgQDWdXdJw67SkrZMEFC6c4sFEvZ6I3nxLyNmfhM83LKOkF/TTKpU25Evc5hjsceOLYti6F/u/yg2Iu/osaHZr2L0zeTf8K9gjwg5G1D5alWMlRw1qHHVajI3/aPZLyJqc+EG2ptrwfjThxAXtWGVx+1opLcL5aMBqoLuTUyJ+zQQ9QKBgQC2WZ2Tc6T65SNbx2pzDg0MQ70hjQIi7D9srl8LsQ50QkdLBV1wGqY26WdvvB0uXweP96XmrTVinxEdL0yv3aYg6a/09pG8s2D8JH5sBmAHfzilSi9JIBpWhheF+KykMFGT9rFbGB2gOXnu6RA1i7ZShCyXmhZczQzWZmlBwmt7IQKBgG+1JhqlNDX5N72tLe/A6aQN+ZcrTYRk0mK7vxePue5qo49zurGS4TA/XRxo6RJVBOrTMc1S2UZBsoeZpz21jq0HZnWDcEaymkzsvqP8UG126gfFIu5Qb7IcizFAzQN4MrmYOybJFexQyQAgeaFET5SXX8VxqxPeFm88kma5E6jVAoGBANte7hEcBhbjGDHyOSo3Mtms8x3FaqK7LCHL4N0Sh96zlz7VhjZZWdiBATy2X1SJJuqWPnUW0ZhGAJGCXrrpMGHUNXIopmvArLG1+DfiyhlCZPYLNyOAp7UXzxCUCx0t/CDOhNIb9LslI6O4CXp/qIlFhkYIb/fEfPsY0eH7KODK
-----END RSA PRIVATE KEY-----'''
