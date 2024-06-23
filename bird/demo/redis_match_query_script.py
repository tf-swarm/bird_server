#-*- coding:utf8 -*-

import redis
import random
import time
import os
import csv
import json

r = redis.Redis(host='192.168.0.200', port=6379, db= 4)

data_list = ['2019-03-01','2019-03-02','2019-03-03','2019-03-04','2019-03-05','2019-03-06','2019-03-07','2019-03-08','2019-03-09','2019-03-10',
			'2019-03-11','2019-03-12','2019-03-13','2019-03-14','2019-03-15','2019-03-16','2019-03-17','2019-03-18','2019-03-19','2019-03-20',
			'2019-03-21','2019-03-22','2019-03-23','2019-03-24','2019-03-25','2019-03-26','2019-03-27','2019-03-28','2019-03-29','2019-03-30','2019-03-31',
			'2019-04-01','2019-04-02','2019-04-03','2019-04-04','2019-04-05','2019-04-06','2019-04-07','2019-04-08','2019-04-09','2019-04-10',
			'2019-04-11','2019-04-12','2019-04-13','2019-04-14','2019-04-15','2019-04-16','2019-04-17','2019-04-18','2019-04-19','2019-04-20']


def save_cache(dir, name, l):
    cd = os.path.dirname(os.getcwd())
    if not os.path.exists(cd + "/history/%s"%(dir)):
        os.makedirs(cd + "/history/%s"%(dir))
    with open(cd + "/history/%s/%s.csv"%(dir, name), "w+") as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name
        writer.writerow(["uid", "in.chip.match_table.return", 'out.chip.match.table.consume', 'in.chip.match_table.mail.get'])
        # 写入多行用writerows
        for k,v in l.items():
            writer.writerows([[k, v[0], v[1], v[2]]])

def to_int(v, default=None):
    if v is None:
        return default
    return int(v)

for i in data_list:
	c = r.keys('user_daily:1004_0:%s:*'%i)
	ret = {}
	for j in c:
		uid = j.split('user_daily:1004_0:%s:'%i)[1]
		dat = r.hget(j, 'in.chip.match_table.return')
		ticket = r.hget(j, 'out.chip.match.table.consume')
		get = r.hget(j, 'in.chip.match_table.mail.get')
		if dat or ticket or get:
			ret[str(uid)] = [to_int(dat, 0), to_int(ticket, 0), to_int(get, 0)]
	print i, ret
	save_cache(i, int(time.time()), ret)
