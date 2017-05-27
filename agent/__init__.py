#!/usr/bin/env python
# coding=utf-8
import os,re
import json
import GVAR

def load_agents(json_file):
    agents_dict = {}
    iteritems = lambda dikt: dikt.iteritems()
    with open(json_file) as json_content:
        for root, root_list in iteritems(json.load(json_content)):
            agents_dict[root]=root_list
    return agents_dict

#JSON_FILE = os.path.join(GVAR.APP_Path,'resource/user.agent')
#AGENT_DICT = load_agents(JSON_FILE)
AGENT_DICT = {
    "device": {
      "pc": ["Windows NT","Macintosh","Windows+NT"],
      "mobile": ["Mobile"],
      "spider": ["Googlebot","bingbot","Baiduspider","Sogou web spider","360Spider","JikeSpider","YisouSpider"]
        },
    "os": {
         "ios": ["Mac OS X","Mac+OS+X"],
         "osx": ["Macintosh"],
         "android":["Android"],
         "windows":["Windows NT","Windows+NT"],
         "linux":["X11"]
       },
    "browser":{
          "ie":["MSIE"],
          "edge":["Edge","EDGE"],
          "firefox":["Firefox"],
          "opera":["Opera"],
          "safari":["Safari"],
          "chrome":["Chrome"],
          "qq":["QQBrowser"],
          "weixin":["MicroMessenger"],
          "uc":["UCBrowser"],
          "baidu":["baiduboxapp"]
       }
}

AppleWebKit = re.compile(r'^.*AppleWebKit\/([\d.]+).*Safari\/([\d.]+)$')
Default_Device = {'mobile':0,'pc':0,'spider':0,'ios':0,'osx':0,'android':0,'windows':0,'linux':0,'ie':0,'edge':0,'firefox':0,'opera':0,'safari':0,'chrome':0,'qq':0,'weixin':0,'uc':0,'baidu':0}

class Agent(object):
    def __init__(self, agent_str,agents=AGENT_DICT):
        self.input_agent = agent_str
        #except:
        #    self.input_agent = agent_str
        #    print type(agent_str)
        matchs = AppleWebKit.match(agent_str)
        if matchs != None:
            allGroups = matchs.groups()
            if allGroups[0] == allGroups[1]:
                str = agent_str.replace("AppleWebKit/"+allGroups[0],'')
                str = str.replace("Safari/" + allGroups[0], '')
                self.input_agent = str
        self.re_agent = agents

    def get_device(self):
        for devicetype in self.re_agent['device']: #devicetype -> mobile,pc,spider
            relist = list(self.re_agent['device'][devicetype])
            for re in relist:
                if self.input_agent.find(re) >= 0:
                    return devicetype
        return None

    def get_os(self):
        for ostype in self.re_agent['os']: #devicetype -> ios,windows,mac
            relist = list(self.re_agent['os'][ostype])
            for re in relist:
                if self.input_agent.find(re) >= 0:
                    return ostype
        return None

    def get_browser(self):
        aglist = self.input_agent.split(' ')
        if aglist[-1] is not None:
            bs = aglist[-1].split('/')[0].lower()
            if self.re_agent['browser'].get(bs) is not None:
                return bs
        for bstype in self.re_agent['browser']: # devicetype -> ie,edge,firefox
            relist = list(self.re_agent['browser'][bstype])
            for re in relist:
                if self.input_agent.find(re) >= 0:
                    return bstype
        return None

    def do_agent(self,db,tid):
        rs = db.table("t_agents").select("id").where('tid = ?', tid).fetchone()
        if rs is None:
            return self.new_agent(db, tid)
        else:
            id = rs[0]
            device = Default_Device.copy()
            dc = self.get_device()
            os = self.get_os()
            bs = self.get_browser()

            ups = []
            if device.get(dc, -1) == 0:
                ups.append(dc+'='+dc+'+ 1')
            if device.get(os, -1) == 0:
                ups.append(os + '=' + os + '+ 1')
            if device.get(bs, -1) == 0:
                ups.append(bs + '=' + bs + '+ 1')
            if len(ups) == 0:
                return
            sql = 'update t_agents set '+','.join(ups)+' where id='+str(id)
            db.execute(sql, False)

    def new_agent(self,db,tid):
        device = Default_Device.copy()
        dc = self.get_device()
        os = self.get_os()
        bs = self.get_browser()
        if device.get(dc,-1) == 0:
            device[dc] = 1
        if device.get(os,-1) == 0:
            device[os] = 1
        if device.get(bs,-1) == 0:
            device[bs] = 1

        db.table('t_agents').insert(tid=tid,
                                    mobile=device['mobile'],
                                    pc=device['pc'],
                                    spider=device['spider'],
                                    ios=device['ios'],
                                    osx=device['osx'],
                                    android=device['android'],
                                    windows=device['windows'],
                                    linux=device['linux'],
                                    ie=device['ie'],
                                    edge=device['edge'],
                                    firefox=device['firefox'],
                                    opera=device['opera'],
                                    safari=device['safari'],
                                    chrome=device['chrome'],
                                    qq=device['qq'],
                                    weixin=device['weixin'],
                                    uc=device['uc'],
                                    baidu=device['baidu'])
        db.execute(None, False)
