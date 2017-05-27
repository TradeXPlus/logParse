import os
import pygeoip
import GVAR

IP_FILE = os.path.join(GVAR.APP_Path,'resource/GeoLiteCity.dat')

class IP(object):
    def __init__(self,db,ip,ipdatebase=IP_FILE):
        self.db = db
        self.ipinfo = {}
        geoip = pygeoip.GeoIP(ipdatebase)
        info = geoip.record_by_addr(ip)
        if info is None:
            self.ipinfo['country'] = 'unknow'
            self.ipinfo['city'] = 'unknow'
        else:
            self.ipinfo['country'] = 'unknow' if info['country_code'] is None else info['country_code']
            self.ipinfo['city'] = 'unknow' if info['city'] is None else info['city']

    def get_ipid(self,tid,ip):
        rs = self.db.table("t_ip").select("id").where('tid = ? AND ip = ?',tid,ip).fetchone()
        if rs is None:
            return 0
        else:
            id = rs[0]
            self.db.execute('update t_ip set count=count+1 where id='+str(id),False)
            return id

    def count_ip(self,ipid):
        sql = 'update t_ip set count=count+1 where id=' + str(ipid)
        # print sql
        self.db.execute(sql , False)

    def new_ip(self,tid,ip):
        self.db.table("t_ip").insert(tid=tid,
                                     ip=ip,
                                     country=self.ipinfo['country'],
                                     city=self.ipinfo['city'],
                                     count=1)
        self.db.execute(None,False)