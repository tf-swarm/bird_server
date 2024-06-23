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

month_info = {
	'open': 1,
	'channel_id':['1001_0','1001_1','1001_2','1001_3','1001_4','1001_5','1003_0','1003_1','1004_0''1004_1','1005_0','1005_1','1006_0','1007_0','1007_1','1008_0','1008_1','1000_0','1000_1','1000_2','1000_3'],
	'detail': u'月卡大升级',
	'price': 50,
	'total_price': 400,
	'return': 400,
	'auto_shot': 30,
	'rw':{
		'chip': 10000, #24000,
		'diamond': 10, #9,
		'props': [{'id': 202, 'count': 5}],
	},
}

msgpack = {
	'gameId':gameId,
	'sign':getSign(),
	'ts':int(getTs()),
	'pid': 2,
	'ret': month_info,
}

content = json.dumps(msgpack)

url = 'http://192.168.0.200:9000/v2/shell/gm/checkcoin'
headers = {'content-type': "application/json"}
r = requests.post(url, data = content, headers = headers )

print type(r.status_code), r.text
