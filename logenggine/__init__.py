#!/usr/bin/env python
#-*- coding:utf-8 –*-

import fileinput
from db import SqliteHelper
from parsetime import Parsetime
from request import Request
from referer import Referer
from agent import Agent
from os import path
from sys import exit

__all__ = ['webLog','nginxLog','apacheLog']

class webLog(object):
    def __init__(self,file,pattern):
        if not path.isfile(file):
            print "Log file is not exists.Please use app_nmae --help command for help."
            exit(1)
        self.log_file = file
        self.rePattern = pattern
        self.db = SqliteHelper(file+".db3")
        self.db.open()
        self.__init_db()

    def __init_db(self):
        sql="""CREATE TABLE IF NOT EXISTS [t_time](
            [id] INTEGER PRIMARY KEY NOT NULL, 
            [year] INT, 
            [month] SMALLINT, 
            [week] SMALLINT, 
            [weekday] SMALLINT, 
            [day] INT, 
            [hour] SMALLINT);

        CREATE UNIQUE INDEX IF NOT EXISTS [dt_ymdh]
        ON [t_time](
            [year], 
            [month], 
            [day], 
            [hour]);

        CREATE TABLE IF NOT EXISTS [t_requests](
            [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            [tid] INTEGER, 
            [line] INTEGER,
            [ip] VARCHAR(16), 
            [country] VARCHAR(16), 
            [city] VARCHAR(16), 
            [ipcount] INT,
            [get] INT, 
            [post] INT, 
            [put] INT, 
            [head] INT, 
            [connect] INT, 
            [unknow] INT, 
            [status_200] INT, 
            [status_206] INT,
            [status_302] INT, 
            [status_304] INT, 
            [status_400] INT, 
            [status_403] INT, 
            [status_404] INT, 
            [status_500] INT, 
            [status_502] INT, 
            [status_503] INT, 
            [status_unknow] INT, 
            [flow_byte] BIGINT, 
            [url_app] INT, 
            [url_static] INT, 
            [url_video] INT, 
            [url_zip] INT, 
            [url_doc] INT, 
            [url_other] INT);

        CREATE INDEX IF NOT EXISTS [rq_tid]
            ON [t_requests](
                [tid]);

        CREATE INDEX IF NOT EXISTS [rq_ip]
            ON [t_requests](
                [ip]);

        CREATE TABLE IF NOT EXISTS [t_refer](
            [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            [tid] INTEGER, 
            [no_refer] INT, 
            [internal] INT, 
            [unknow] INT, 
            [baidu] INT, 
            [google] INT, 
            [so360] INT, 
            [yandex] INT, 
            [sogou] INT, 
            [bing] INT, 
            [taobao] INT, 
            [naver] INT, 
            [alibaba] INT, 
            [ask] INT, 
            [yahoo] INT, 
            [zhongsou] INT, 
            [aol] INT);

        CREATE INDEX IF NOT EXISTS [refer_tid]
        ON [t_refer](
            [tid]);

        CREATE TABLE IF NOT EXISTS [t_keyword](
            [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            [tid] INTEGER, 
            [kw] VARCHAR(32), 
            [kwcount] INT);

        CREATE INDEX IF NOT EXISTS [kw_tid]
        ON [t_keyword](
            [tid]);

        CREATE TABLE IF NOT EXISTS [t_agents](
            [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            [tid] INTEGER, 
            [mobile] INT, 
            [pc] INT, 
            [spider] INT, 
            [ios] INT, 
            [osx] INT, 
            [android] INT, 
            [windows] INT, 
            [linux] INT, 
            [ie] INT, 
            [edge] INT, 
            [firefox] INT, 
            [opera] INT, 
            [safari] INT, 
            [chrome] INT, 
            [qq] INT, 
            [weixin] INT, 
            [uc] INT, 
            [baidu] INT);

        CREATE INDEX IF NOT EXISTS [agents_tid]
        ON [t_agents](
            [tid]);"""
        dsql=sql.split("\n\n")
        for sql in dsql:
            self.db.execute(sql)

    def __init_tid(self):
        rows = self.db.table("t_time").select("id").fetchall()
        t_time_tid = {'0':0}
        for row in rows:
            t_time_tid[str(row[0])] = row[0]
        return t_time_tid

    def logfile(self,curr_host=None):
        t_time_tid = self.__init_tid()
        lineId,tid,ipid = 0,0,0

        for line in fileinput.input(self.log_file):
            lineId += 1
            if line[-2:] == "\r\n":     #将windows结尾格式改成Unix格式
                line = line[:-2] + "\n"
            matchs = self.rePattern.match(line)
            if matchs != None:
                ip = matchs.group("ip")
                date = matchs.group("date")
                month = matchs.group("month")
                year =  matchs.group("year")
                time =  matchs.group("time")
                method =  matchs.group("method")
                request =  matchs.group("request")
                #query = matchs.group("query")
                status = matchs.group("status")
                bytes = matchs.group("bytes")
                referer = matchs.group("referer")
                agent = matchs.group("agent")

                # ------ t_time
                oDt =Parsetime(self.db,year,month,date,time)
                logdt = str(oDt.dt['stamp'])
                if t_time_tid.get(logdt,-1) == -1:
                    oDt.new_time()
                    tid = oDt.dt['stamp']
                    t_time_tid[logdt] = tid
                else:
                    tid = t_time_tid.get(logdt)

                # ------- t_request
                #print query
                url = request
                request = url.split(' ')
                if(len(request)>1):
                    url=request[1]
                reqjson = {
                    'tid':tid,
                    'line':lineId,
                    'ip':ip,
                    'method':method,
                    'status':status,
                    'url':url,
                    'bytes':bytes
                }
                oReq = Request(self.db,reqjson)
                oReq.do_req(tid,ip)

                # ---- t_refer
                if int(status) == 200:
                    oRefer = Referer(referer,curr_host)
                    oRefer.do_refer(self.db,tid)
                    oRefer.do_keyword(self.db,tid) # -----keyword

                oAgent = Agent(agent)
                oAgent.do_agent(self.db,tid)
                #break
                #print lineId
        self.db.commit()
        fileinput.close()
