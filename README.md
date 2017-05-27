# logParse 日志分析

## 用法
logParse -h 可以查看详细帮助
usage: logParse [-h] [-f LOGFILE] [-t LOGTYPE] [-u BASEURL] [--version]

Diannao51 web log analysis.

optional arguments:
  -h, --help            show this help message and exit
  -f LOGFILE, --logfile LOGFILE
                        log file to analysis.
                        
  -t LOGTYPE, --logtype LOGTYPE
                        which type of zhe log:apache|nginx|iis
                        
  -u BASEURL, --baseurl BASEURL
                        log for website domain url
                     
  --version             show program's version number and exit
  
## 举例说明
1、分析http://diannao51.com 站点的Apache日志
logParse -f access.log -t apache -u http://diannao51.com

2、分析http://diannao51.com 站点的nginx日志
logParse -f access.log -t nginx -u http://diannao51.com

3、分析http://diannao51.com 站点的iis日志
logParse -f access.log -t iis -u http://diannao51.com

根据服务器日志类型，选择参数进行分析。
