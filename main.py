#!/usr/bin/env python
#-*- coding:utf-8 –*-

import sys,os
import datetime
import argparse
import GVAR
from report.excel import excelChart

def logObject(logFile,logType = 'nginx'):
    oLog = None
    if logType == 'apache':
        from logenggine.apache import apacheLog
        oLog = apacheLog(logFile)
    elif logType == 'nginx':
        from logenggine.nginx import nginxLog
        oLog = nginxLog(logFile)
    else:
        from logenggine.iis import iisLog
        oLog = iisLog(logFile)

    return oLog

def app_path():
    application_path = ''
    if getattr(sys, '_MEIPASS', False):
        application_path = os.path.join(sys._MEIPASS, '')
    elif __file__:
        application_path = os.path.dirname(__file__)
    # unknown if still necessary
    if application_path == '':
        application_path = os.path.dirname(os.path.realpath(__file__))
    #if "~" in application_path:
    #    application_path = win32api.GetLongPathName(application_path)
    return application_path

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description='Diannao51 web log analysis.')
    parser.add_argument("-f", "--logfile", action='store', help="log file to analysis.", default='access.log')
    parser.add_argument("-t", "--logtype", action='store', help="which type of zhe log:apache|nginx|iis", default='nginx')
    parser.add_argument("-u", "--baseurl", action='store', help="log for website domain url", default='http://www.diannao51.com')
    parser.add_argument('--version', action='version', version='%(prog)s version: ' + GVAR.VERSION)

    args = parser.parse_args()
    logfile = args.logfile
    logtype = args.logtype
    logurl = args.baseurl

    GVAR.APP_Path = app_path()

    starttime = datetime.datetime.now()
    oLog = logObject(logfile,logtype)
    oLog.logfile(logurl)

    endtime = datetime.datetime.now()
    allTime = (endtime - starttime).seconds
    print('log analysis time: %ss=%dm' % (allTime, allTime / 60))

    oLogChart = excelChart(logfile+'.db3')
    oLogChart.chart_visit(logurl,endtime.strftime('%Y%m'))
    oLogChart.close()

    endtime = datetime.datetime.now()
    allTime = (endtime - starttime).seconds
    print('all time: %ss=%dm' % (allTime, allTime / 60))