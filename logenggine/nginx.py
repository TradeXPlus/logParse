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
# ^(?P<ip>[\d.]+)\s-\s([-\w]+)\s\[(?P<date>\d+)\/(?P<month>\w+)\/(?P<year>\d+)\:(?P<time>\S+)\s(\+\d+)\]\s\"(?P<method>\w*)(?P<request>.*)\"\s(?P<status>\d+)\s(?P<bytes>\d+)\s\"(?P<referer>.+)\"\s\"(?P<agent>.*)\"([-,\s\d.]*)$
# hdchurch      ^([\d.]+)\s-\s([-\w]+)\s\[(\d+)\/(\w+)\/(\d+)\:(\S+)\s(\+\d+)\]\s\"(\w*)(.*)\"\s(\d+)\s(\d+)\s\"(.+)\"\s\"(.*)\"\s([-,\s\d.]*)\s\"(.*)\"$
#nginx default ^(%s)\s-\s([-\w]+)\s\[(%s)\/(%s)\/(%s)\:(%s)\s(\+\d+)\]\s\"(%s)(%s)\"\s(%s)\s(%s)\s\"(%s)\"\s\"(%s)\"([-,\s\d.]*)$

nginxLogPattern = re.compile(r"^(%s)\s-\s([-\w]+)\s\[(%s)\/(%s)\/(%s)\:(%s)\s(\+\d+)\]\s\"(%s)(%s)\"\s(%s)\s(%s)\s\"(%s)\"\s\"(%s)\"([-,\s\d.]*)$" %(
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
    re_userAgent ), re.VERBOSE)


class nginxLog(webLog):
    def __init__(self,file,pattern=nginxLogPattern):
        webLog.__init__(self,file,pattern)
