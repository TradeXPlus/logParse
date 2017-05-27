#!/usr/bin/env python
# coding=utf-8
import os
import json
import GVAR

try:
    from urlparse import urlparse, parse_qsl
    iteritems = lambda dikt: dikt.iteritems()
    text_type = unicode
except ImportError:  # urlparse was renamed urllib.parse in Python 3
    from urllib.parse import urlparse, parse_qsl
    iteritems = lambda dikt: dikt.items()
    text_type = str


def load_referers(json_file):
    referers_dict = {}
    with open(json_file) as json_content:
        for medium, conf_list in iteritems(json.load(json_content)):
            for referer_name, config in iteritems(conf_list):
                params = None
                if 'parameters' in config:
                    params = list(map(text_type.lower, config['parameters']))
                for domain in config['domains']:
                    referers_dict[domain] = {
                        'name': referer_name,
                        'medium': medium
                    }
                    if params is not None:
                        referers_dict[domain]['params'] = params
    return referers_dict

JSON_FILE = os.path.join(GVAR.APP_Path,'resource/search.engine')
REFERERS = load_referers(JSON_FILE)
T_FIELDS={'no_refer':0,'internal':0,'unknow':0,'baidu':0,'google':0,'so360':0,'yandex':0,'sogou':0,'bing':0,'taobao':0,'naver':0,'alibaba':0,'ask':0,'yahoo':0,'zhongsou':0,'aol':0}

class Referer(object):
    def __init__(self,ref_url, curr_url=None, referers=REFERERS):
        self.known = False
        self.referer = None
        self.medium = 'unknown'
        self.search_parameter = None
        self.search_term = None
        self.referers = referers

        ref_uri = urlparse(ref_url)
        ref_host = ref_uri.hostname
        self.known = (ref_uri.scheme in ['http', 'https'] and
                      ref_host is not None)
        self.uri = ref_uri

        if not self.known:
            return

        if curr_url:
            curr_uri = urlparse(curr_url)
            curr_host = curr_uri.hostname
            if curr_host == ref_host:
                self.medium = 'internal'
                return

        referer = self._lookup_referer(ref_host)

        if not referer:
            return

        self.referer = referer['name']
        self.medium = referer['medium']

        if referer['medium'] == 'search':
            if 'params' not in referer or not referer['params']:
                return
            for param, val in parse_qsl(ref_uri.query):
                if param.lower() in referer['params']:
                    self.search_parameter = param
                    self.search_term = val

    def _lookup_referer(self, ref_host):
        referer = None
        for dot_domain in self.referers:
            if (ref_host.find(dot_domain) > 0):
                referer = self.referers[dot_domain]
                break

        return referer

    def do_refer(self,db,tid):
        rs = db.table("t_refer").select("id").where('tid = ?',tid).fetchone()
        if rs is None:
            return self.new_refer(db,tid)
        else:
            id = rs[0]
            fd = T_FIELDS.copy()
            media = self.medium
            #print media,self.referer
            sqlstr = 'unknow=unknow+1'
            if self.uri.hostname is None:
                sqlstr = 'no_refer=no_refer+1'
            elif fd.get(media, -1) == 0:
                sqlstr = media+'='+media+'+1'
            elif media == 'search' and fd.get(self.referer, -1) == 0:
                sqlstr = self.referer + '=' + self.referer + '+1'
            else:
                pass
            sql = 'update t_refer set '+sqlstr+' where id=' + str(id)
            db.execute(sql, False)

    def new_refer(self,db,tid):
        fd = T_FIELDS.copy()
        media = self.medium
        if self.uri.hostname is None:
            fd['no_refer']=1
        elif fd.get(media,-1)==0:
            fd[media] = 1
        elif media=='search' and fd.get(self.referer,-1)==0:
            fd[self.referer] = 1
        else:
            pass
        db.table("t_refer").insert(tid=tid,
                                      no_refer=fd['no_refer'],
                                      internal=fd['internal'],
                                      unknow=fd['unknow'],
                                      baidu=fd['baidu'],
                                      google=fd['google'],
                                      so360=fd['so360'],
                                      yandex=fd['yandex'],
                                      sogou=fd['sogou'],
                                      bing=fd['bing'],
                                      taobao=fd['taobao'],
                                      naver=fd['naver'],
                                      alibaba=fd['alibaba'],
                                      ask=fd['ask'],
                                      yahoo=fd['yahoo'],
                                      zhongsou=fd['zhongsou'],
                                      aol=fd['aol'])
        db.execute(None, False)


    def do_keyword(self,db,tid):
        kw = self.search_term
        if self.medium=='search' and kw is not None:
            try:
                kw = kw.decode('UTF8')
            except UnicodeDecodeError:
                kw = kw.decode('GBK')

            rs = db.table("t_keyword").select("id").where('tid = ? AND kw = ?',tid,kw).fetchone()
            if rs is None:
                return self.new_keyword(db, tid)
            else:
                id = rs[0]
                sql = 'update t_keyword set kwcount=kwcount+1 where id=' + str(id)
                db.execute(sql, False)

    def new_keyword(self,db,tid):
        kw=self.search_term
        try:
            kw = kw.decode('UTF8')
        except UnicodeDecodeError:
            kw = kw.decode('GBK')
        db.table("t_keyword").insert(tid=tid,
                                     kw=kw,
                                     kwcount=1)
        #print db.sql
        db.execute(None, False)