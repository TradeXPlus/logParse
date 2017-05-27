#!/usr/bin/env python
# coding=utf-8
from time import strftime,strptime
from datetime import datetime, timedelta

MONTHS = ['01','02','03','04','05','06','07','08','09','10','11','12']

class Parsetime(object):
    def __init__(self,db,year,month,date,time):    # time为 hh:mm:ss格式
        time_str = '%s%s%s %s' % (year, month, date, time)
        if month in MONTHS: # 处理IIS日期
            dt = datetime.strptime(time_str, '%Y%m%d %H:%M:%S')
            dt = dt+timedelta(hours=8)  # 转换为北京时间
        else:
            dt = datetime.strptime(time_str, '%Y%b%d %H:%M:%S')
        dt = dt.timetuple()
        self.dt = {}
        self.dt['stamp'] = int(strftime("%Y%m%d%H", dt))
        self.dt['year'] = strftime("%Y", dt)
        self.dt['month'] = int(strftime("%m", dt))
        self.dt['week'] = int(strftime("%U", dt))
        self.dt['weekday'] = int(strftime("%w", dt))
        self.dt['day'] = int(strftime("%j", dt))
        self.dt['hour'] = int(strftime("%H", dt))
        self.db = db

    # 根据年月日时间，查找tid，如果没有，则建立
    def do_time(self):
        rs = self.db.table("t_time").select("id").where('id = ?',self.dt['stamp']).fetchone()
        if rs is None:
            self.new_time()
            return self.dt['stamp']
        else:
            return rs[0]

    def new_time(self):
        self.db.table("t_time").insert(id=self.dt['stamp'],
                                       year=self.dt['year'],
                                       month=self.dt['month'],
                                       week=self.dt['week'],
                                       weekday=self.dt['weekday'],
                                       day=self.dt['day'],
                                       hour=self.dt['hour'])
        self.db.execute(None,False)