# -*- coding=utf-8 -*-

import datetime
import time
import random
import json
import requests
import md5

gameId = 2;
protected = 'aXh4b28ubWVAZ21haWwuY29tCg==';

time1 = datetime.date.today()
time2 = time1 - datetime.timedelta(days=7)

time1 = time1.strftime('%Y-%m-%d')
time2 = time2.strftime('%Y-%m-%d')

def getTs():
	return time.time()

def getSign():
	time1 = int(getTs())
	signString = "gameId=%d&token=%s&ts=%s"%(gameId, protected, str(time1))
	a = md5.md5(signString)
	sign = a.hexdigest()
	print sign
	return sign
	
msgpack = {
	'gameId':gameId,
	'sign':getSign(),
	'ts':int(getTs()),
	'userId':1001390,
	'productId': '101112',

}

content = json.dumps(msgpack)

url = 'http://192.168.0.210:9000/v1/shell/gm/reward/pay'
headers = {'content-type': "application/json"}
r = requests.post(url, data = content, headers = headers )

print type(r.status_code), r.text