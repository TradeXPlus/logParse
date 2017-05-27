#!/usr/bin/env python
#-*- coding:utf-8 –*-

import re
from . import webLog

re_ip = r"?P<ip>[\d.]+"
re_date = r"?P<date>\d+"
re_month = r"?P<month>\d+"
re_year = r"?P<year>\d+"
re_time = r"?P<time>\S+"
re_method = r"?P<method>\w*"
re_request = r"?P<request>.*"
re_request1 = r".*"
re_status = r"?P<status>\d+"
re_bodyBytes = r"?P<bytes>\d+"
re_referer = r"?P<referer>.+"
re_userAgent = r"?P<agent>.*"

# ^(%s)\s-\s([-\w]+)\s\[(%s)\/(%s)\/(%s)\:(%s)\s(\+\d+)\]\s\"(%s)(%s)\"\s(%s)\s(%s)\s\"(%s)\"\s\"(%s)\"([-,\s\d.]*)
#  #Fields: date time cs-method cs-uri-stem cs-uri-query c-ip cs(User-Agent) cs(Referer) sc-status sc-bytes cs-bytes
# 2017-05-04 01:28:34 GET / - 114.95.253.58 Mozilla/5.0+(Windows+NT+5.1)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/45.0.2454.101+Safari/537.36 http://www.tdx.com.cn/url/jump.asp?setcode=1&code=603385 200 13908 436
# ^([\d.]+)-(\d+)-(\d+)\s(\S+)\s(\w*)\s(.*)\s(.*)\s([\d.]+)\s(.*)\s(.+)\s(\d+)\s(\d+)\s(\d+)$

iisLogPattern = re.compile(r"^(%s)-(%s)-(%s)\s(%s)\s(%s)\s(%s)\s(%s)\s(%s)\s(%s)\s(%s)\s(%s)\s(%s)\s(\d+)$" %(
    re_year,
    re_month,
    re_date,
    re_time,
    re_method,
    re_request,
    re_request1,
    re_ip,
    re_userAgent,
    re_referer,
    re_status,
    re_bodyBytes), re.VERBOSE)


class iisLog(webLog):
    def __init__(self,file,pattern=iisLogPattern):
        webLog.__init__(self,file,pattern)
