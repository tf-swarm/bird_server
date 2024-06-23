# -*- coding=utf-8 -*-
import os, csv, time

fo = open("game-bird-20002.log", "r")


keys = ['数据观测：当前玩家剩余鸟蛋数', '1000024']

def save_cache(dir, name, l):
    cd = os.path.dirname(os.getcwd())
    if not os.path.exists(cd + "/history/%s"%(dir)):
        os.makedirs(cd + "/history/%s"%(dir))
    with open(cd + "/history/%s/%s.csv"%(dir, name), "w+") as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name
        writer.writerow(["时间", '用户账号', '用户鸟蛋'])
        # 写入多行用writerows
        for v in l:
            writer.writerows([[v[0], v[1], v[2]]])

lst = []

for line in fo.readlines():
    b_contains = True
    for key in keys:
        if key not in line:
            b_contains = False
            break

    if b_contains:
        times = line[:23]
        strs = line.split(keys[0])[1]
        tmp = strs.split(' ')
        lst.append([times, tmp[1], int(tmp[2])])

save_cache('test', int(time.time()), lst)
 
# 关闭文件
fo.close()
