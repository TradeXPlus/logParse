#!/usr/bin/env python
#-*- coding:utf-8 –*-

import re
from . import webLog

re_ip = r"?P<ip>[\d.]+"
re_date = r"?P<date>\d+"
re_month = r"?P<month>\w+"
re_year = r"?P<year>\d+"
re_time = r"?P<time>\S+"
re_method = r"?P<method>\w*"
re_request = r"?P<request>.*"
re_status = r"?P<status>\d+"
re_bodyBytes = r"?P<bytes>\d+"
re_referer = r"?P<referer>.+"
re_userAgent = r"?P<agent>.*"

'''
    apache combind log format
    ^([\d.]+)\s([w.-]+)\s([w.-]+)\s\[(\d+)\/(\w+)\/(\d+)\:(\S+)\s(\+\d+)\]\s\"(\w*)(.*)\"\s(\d+)\s(\d+)\s\"(.+)\"\s\"(.*)\"$
    1.	113.128.150.111
    2.	-
    3.	-
    4.	01
    5.	May
    6.	2017
    7.	15:47:47
    8.	+0800
    9.	GET
    10.	/uploadfile/2011/0627/20110627025134760.jpg HTTP/1.1
    11.	200
    12.	176058
    13. refer
    14. agents
    
    ^(%s)\s-\s([-\w]+)\s\[(%s)\/(%s)\/(%s)\:(%s)\s(\+\d+)\]\s\"(%s)(%s)\"\s(%s)\s(%s)\s\"(%s)\"\s\"(%s)\"([-,\s\d.]*)$
'''


apacheLogPattern = re.compile(r"^(%s)\s([w.-]+)\s([w.-]+)\s\[(%s)\/(%s)\/(%s)\:(%s)\s(\+\d+)\]\s\"(%s)(%s)\"\s(%s)\s(%s)\s\"(%s)\"\s\"(%s)\"$" %(
    re_ip,
    re_date,
    re_month,
    re_year,
    re_time,
    re_method,
    re_request,
    re_status,
    re_bodyBytes,
    re_referer,
    re_userAgent), re.VERBOSE)

class apacheLog(webLog):

    def __init__(self, file, pattern=apacheLogPattern):
        webLog.__init__(self,file, pattern)
