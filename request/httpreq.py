from db import *
from ip import IP
import urlparse
import os

def_method={'get':0,'post':0,'put':0,'head':0,'connect':0,'unknow':0}
def_type={'url_app':0,'url_static':0,'url_video':0,'url_zip':0,'url_doc':0,'url_other':0}
def_code = {'status_200':0,'status_206':0,'status_302':0,'status_304':0,'status_400':0,'status_403':0,'status_404':0,'status_500':0,'status_502':0,'status_503':0,'status_unknow':0}

class Request(object):
    def __init__(self,db,reqs):
        self.tid = reqs['tid']
        self.line = reqs['line']
        self.ip = reqs['ip']
        self.method = 'unknow' if reqs['method'] =='' else reqs['method']
        self.url = reqs['url']
        self.bytes = reqs['bytes']
        self.status = reqs['status']
        self.db = db


    def do_req(self,tid,ip):
        rs = self.db.table("t_requests").select("id").where('tid = ? and ip = ?',tid,ip).fetchone()
        if rs is None:
            return self.new_req(tid)
        else:
            id = rs[0]
            md = self.method.lower()

            mdstr = 'unknow=unknow+1'
            if def_method.get(md,-1)==0:
                mdstr = md+'='+md+'+1'

            strcode = 'status_unknow=status_unknow+1'
            status = 'status_'+self.status
            if def_code.get(status,-1)==0:
                strcode=status+'='+status+'+1'

            flow_byte='flow_byte=flow_byte+'+self.bytes

            strtp = 'url_other=url_other+1'
            tp = self.__get_type(self.url)
            if def_type.get(tp,-1)==0:
                strtp = tp+'='+tp+'+1'

            sql= 'update t_requests set '+mdstr+','+strcode+','+flow_byte+','+strtp+ ',ipcount=ipcount+1 where id='+str(id)

            self.db.execute(sql,False)

    def new_req(self,tid):
        md = self.__req_method(self.method)
        cd = self.__req_status(self.status)
        tp = self.__req_type(self.url)
        oIP = IP(self.db,self.ip)

        self.db.table("t_requests").insert(tid = tid,
                                           line = self.line,
                                           ip = self.ip,
                                           ipcount = 1,
                                           country = oIP.ipinfo['country'],
                                           city = oIP.ipinfo['city'],
                                           get = md['get'],
                                           post = md['post'],
                                           put = md['put'],
                                           head = md['head'],
                                           connect=md['connect'],
                                           unknow=md['unknow'],
                                           status_200=cd['status_200'],
                                           status_206=cd['status_206'],
                                           status_302=cd['status_302'],
                                           status_304=cd['status_304'],
                                           status_400=cd['status_400'],
                                           status_403=cd['status_403'],
                                           status_404=cd['status_404'],
                                           status_500=cd['status_500'],
                                           status_502=cd['status_502'],
                                           status_503=cd['status_503'],
                                           status_unknow=cd['status_unknow'],
                                           flow_byte = self.bytes,
                                           url_app=tp['url_app'],
                                           url_static = tp['url_static'],
                                           url_video = tp['url_video'],
                                           url_zip = tp['url_zip'],
                                           url_doc = tp['url_doc'],
                                           url_other = tp['url_other'])
        self.db.execute(None,False)

    def __get_type(self,url):
        url = urlparse.urlparse(url)
        ext = os.path.splitext(url.path)[1]
        app = ['.php', '.asp', '.aspx', '.jsp', '']
        static = ['.js', '.html', 'css', '.jpg', '.png', '.gif', '.svg', '.ttf', '.woff', '.eot', 'ico']
        video = ['.mp4', '.mp3', '.mpeg', '.flv', '.movie', '.ogg', '.avi']
        zip = ['.zip', '.gz', '.rar', '.bz2', '.7z']
        doc = ['.doc', '.docx', '.rtf', '.pdf', '.wps', '.xls', '.xlsx', '.ppt', '.pptx']
        tp = ''
        if ext in app:
            tp = 'url_app'
        elif ext in static:
            tp = 'url_static'
        elif ext in video:
            tp = 'url_video'
        elif ext in zip:
            tp = 'url_zip'
        elif ext in doc:
            tp = 'url_doc'
        else:
            tp = 'url_other'
        return tp

    def __req_type(self,url):
        tp = self.__get_type(url)
        type=def_type.copy()
        isin = type.get(tp, -1)
        if isin == 0:
            type[tp] = 1
        return type

    def __req_method(self,method):
        m=def_method.copy()
        md = method.lower()
        isin = m.get(md,-1)
        if isin==0:
            m[md]=1
        return m

    def __req_status(self,status):
        code = def_code.copy()
        cd='status_'+status
        isin = code.get(cd, -1)
        if isin == 0:
            code[cd] = 1
        return code