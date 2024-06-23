#!/usr/bin/env python
# -*- coding=utf-8 -*-

from framework.interface import ICallable, IContext
from framework.util.tool import Time, Tool


class MysqlDB(ICallable, IContext):
    player_field = 'match'
    format = '%Y-%m-%d'

    # 将
    def insert_mysql_daily_data(self, uid, daily, data):
        uid_daily = "%s_%s"%(uid, daily)
        sql_str = "INSERT into user_daily_data(uid_daily, daily_data) VALUES ('{0}','{1}')".format(uid_daily, data)
        self.ctx.Log.info(sql_str)
        cur = self.ctx.MysqlDB.cursor()
        try:
            cur.execute(sql_str)
            self.ctx.MysqlDB.commit()
        except:
            cur.fetchall()
            cur.close()
            return False
        cur.fetchall()
        cur.close()
        return True

    def on_timer_daily_data(self):
        now_ts = Time.datetime()
        if now_ts.hour == 2 and now_ts.minute == 19:
            all_keys = self.ctx.RedisStat.hget_keys('user_daily:*')
            day_30 = 25*24*3600
            cs = Time.current_ts()
            for item in all_keys:
                key_lst = item.split(':')
                user_id = key_lst[3]
                day_str = key_lst[2]
                daily = Time.str_to_timestamp(day_str, '%Y-%m-%d')
                if daily + day_30 < cs:
                    daily_dict = self.ctx.RedisStat.hash_getall(item)
                    daily_data = self.ctx.json_dumps(daily_dict)
                    ret = self.insert_mysql_daily_data(user_id, day_str, daily_data)
                    if ret:
                        self.ctx.RedisStat.delete(item)

MysqlData = MysqlDB()
