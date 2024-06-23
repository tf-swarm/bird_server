# -*- coding=utf-8 -*-

import datetime
import time
import random
import json
import requests
import md5

gameId = 2
token = 'aXh4b28ubWVAZ21haWwuY29tCg=='
private_key = '3hjjsf33232sdfsfksdf23'

def getTs():
	return time.time()

def getSign(index = 1):
    if index == 1:
        dat = {
            'mgid': 10000,
            'uid': 1000034,
            'token': token,
            'private_key': private_key,
        }
    else:
        dat = {
            'mgid': 10000,
            'uid': 1000010,
            'token': token,
            'private_key': private_key,
            'chip':1235,
            'diamond':612
        }
    keys = dat.keys()
    keys.sort()

    sign_data = []
    for key in keys:
        v = dat.get(key)
        sign_data.append('%s=%s'%(key, str(v)))
    sign_str = '&'.join(sign_data)

    a = md5.md5(sign_str)
    sign = a.hexdigest()
    return sign

##############     ----------------getUserInfo----------------     ##################

# msgpack = {
# 	'mgid':10000,
# 	'uid':1000010,
# 	'token':token,
# 	'sign':getSign(),
# }

# content = json.dumps(msgpack)

# url = 'http://47.92.72.109:8080/v2/third/getUserInfo'
# headers = {'content-type': "application/json"}
# r = requests.post(url, data = content, headers = headers)

# print type(r.status_code), r.text

##############     ----------------notifyGameResult----------------     ##################


# msgpack = {
#     'mgid':10000,
#     'uid':1000010,
#     'token':token,
#     'sign':getSign(2),
#     'chip_win': 0,
#     'chip': 1235,
#     'diamond_win': 100,
#     'diamond': 612,
#     'pid':100000005,
# }

# content = json.dumps(msgpack)

# url = 'http://47.92.72.109:8080/v2/third/notifyGameResult'
# headers = {'content-type': "application/json"}
# r = requests.post(url, data = content, headers = headers)

# print type(r.status_code), r.text

##############     ----------------leave_game----------------     ##################s


msgpack = {
    'mgid':10000,
    'uid':10000134,
    'token':token,
    'sign':getSign(),
}

content = json.dumps(msgpack)

url = 'http://47.92.72.109:8080/v2/third/leave_game'
headers = {'content-type': "application/json"}
r = requests.post(url, data = content, headers = headers)

print type(r.status_code), r.text


