#!/usr/bin/env python
#-*- coding:utf-8 –*-

import os
import xlsxwriter
from db import SqliteHelper

SQLiteDB='access.log.db3'
Cols = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

class excelChart(object):
    def __init__(self,sqldb=SQLiteDB):
        if not os.path.isfile(sqldb):
            print 'DB file is not exists.'
            exit(1)
        self.db = SqliteHelper(sqldb)
        self.db.open()

        filebase=os.path.splitext(sqldb)[0]
        self.workBook = xlsxwriter.Workbook(filebase+'.xlsx')
        self.format_cell = self.workBook.add_format({'align': 'center','valign': 'vcenter','border': 0,'font_size':12,'font_name':u'微软雅黑','bold': True})
        self.format_table_header = self.workBook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'border': 1,'shrink':1, 'font_size': 10,'font_color':'#262626', 'font_name': u'微软雅黑','bold': True})
        self.format_table_row0 = self.workBook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'border': 1,'shrink':1, 'bg_color':'#EAEAEA','font_size': 10,'font_color':'#262626', 'font_name': u'微软雅黑'})
        self.format_table_row1 = self.workBook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'border': 1,'shrink':1, 'font_size': 10, 'font_color': '#262626', 'font_name': u'微软雅黑'})
        self.format_area_split = self.workBook.add_format({'bottom': 6,'bottom_color':'#5B9BD5'})



    def close(self):
        self.db.close()
        self.workBook.close()

    def chart_visit(self,weburl,datemonth):
        self.sheetFWL = self.workBook.add_worksheet(u'月报')
        # self.sheetFWL.set_landscape()   # 设置页面横版布局
        self.sheetFWL.set_margins(left=0.25,right=0.25,top=0.65,bottom=0.65)    #设置打印页边距
        self.sheetFWL.set_header(u'&L电脑无忧服务器日志分析月报&R'+datemonth, {'margin': 0.25})   # 页眉
        self.sheetFWL.set_footer('&L', {'margin': 0.25})
        self.sheetFWL.center_horizontally() # 打印居中
        self.sheetFWL.merge_range('A1:L1', weburl+u'访问月报', self.format_cell)
        self.sheetFWL.merge_range('M1:W1', u'高风险异常访问Top10', self.format_cell)
        self.sheetFWL.set_row(0, 18)
        self.sheetFWL.set_column('A:A', 7.8)
        self.sheetFWL.set_column('B:B', 11.4)
        self.sheetFWL.set_column('C:C', 11.4)
        self.sheetFWL.set_column('D:D', 0.3)
        self.sheetFWL.set_column('L:L', 2.25)

        self.sheetFWL.merge_range('A17:L17','',self.format_area_split)
        self.sheetFWL.merge_range('A33:L33', '', self.format_area_split)
        self.sheetFWL.merge_range('A67:W67', '', self.format_area_split)

        self.xlsx_tcountry()
        self.xlsx_tcity()
        self.xlsx_tip()
        self.xlsx_noGET()
        self.xlsx_bitPOST()
        self.xlsx_smallhttp200()
        self.xlsx_bithttp404()
        self.xlsx_onlyapp()
        self.xlsx_refer()
        self.xlsx_kwtop10(0,56)
        self.xlsx_device()
        self.xlsx_os()
        self.xlsx_browser()

    def _get_data(self,SQL,getLen=8,kcount=True,mflow=True):
        rows = self.db.fetchall(SQL)
        i = 0
        data = []
        other = [u'OTHER', 0, 0]
        for row in rows:
            i += 1
            if i < getLen:
                r = list(row)
                r[1] = r[1] / 1000 if kcount else r[1]
                r[2] = r[2] / 1048576 if mflow else r[2]
                data.append(r)
            else:
                other[1] = other[1] + row[1]
                other[2] = other[2] + row[2]
        other[1] = other[1]/1000 if kcount else other[1]
        other[2] = other[2]/1048576 if mflow else other[2]
        data.append(other)
        return data

    def _cell(self,col,row):
        return Cols[col]+str(row)

    def _exls_table(self,title,data,beginRow=3,beginCol=0,isSum=True):
        self.sheetFWL.write_row(self._cell(beginCol,beginRow), title, self.format_table_header)

        i=0
        for row in data:
            i+=1
            self.sheetFWL.write_row(self._cell(beginCol,i+beginRow), row, self.format_table_row1 if i % 2==0 else self.format_table_row0)
        if isSum:
            f = self.format_table_row1 if (i + 1) % 2 == 0 else self.format_table_row0
            self.sheetFWL.write_row(self._cell(beginCol,i+beginRow+1), [u'合计'],f)
            self.sheetFWL.write_formula(self._cell(beginCol+1,i+1+beginRow),
                                        '=SUM(' + self._cell(beginCol+1,beginRow+1) + ':' + self._cell(beginCol+1,i+beginRow)+')', f)
            self.sheetFWL.write_formula(self._cell(beginCol+2,i+1+beginRow),
                                        '=SUM(' +self._cell(beginCol+2,beginRow+1) + ':' + self._cell(beginCol+2,i+beginRow)+')', f)

    def _exls_ipstatus(self,title,sql,beginRow=3,beginCol=12,colLen=10):
        self.sheetFWL.merge_range(self._cell(beginCol,beginRow)+':'+self._cell(beginCol+10,beginRow), title, self.format_table_header)
        data = self._get_data(sql,colLen+1 , False, False)
        ip = [U'IP地址']
        ct = [u'次数']
        fw = [u'流量']
        i = 0
        for row in data:
            i += 1
            ip.append(row[0])
            ct.append(row[1])
            fw.append(row[2])
            if i == colLen:
                break
        self._exls_table(ip, [ct, fw], beginRow+1, beginCol, False)

    def _exls_chart(self,chart_title,chart_y,chart_y2,beginRow=3,endRow=11,beginCol=0,insertPos='E3'):
        column_chart = self.workBook.add_chart({'type': 'column'})
        column_chart.add_series({
            'name': u'=月报!'+self._cell(beginCol+1,beginRow),
            'categories': u'=月报!'+self._cell(beginCol,beginRow+1)+':'+self._cell(beginCol,endRow),
            'values': u'=月报!'+self._cell(beginCol+1,beginRow+1)+':'+self._cell(beginCol+1,endRow),
            'pattern': {
                'pattern': 'narrow_horizontal',
                'fg_color': '#5B9BD5',
                'bg_color': '#DEEBF7'
            },
            'border': {'color': '#5B9BD5'},
            'gap': 100,
        })
        line_chart = self.workBook.add_chart({'type': 'line'})
        line_chart.add_series({
            'name': u'=月报!'+self._cell(beginCol+2,beginRow),
            'categories': u'=月报!'+self._cell(beginCol,beginRow+1)+':'+self._cell(beginCol,endRow),
            'values': u'=月报!'+self._cell(beginCol+2,beginRow+1)+':'+self._cell(beginCol+2,endRow),
            'y2_axis': 1,
        })
        line_chart.set_y2_axis({'name': chart_y2, 'name_font': {'name': u'微软雅黑', 'size': 10}})

        column_chart.combine(line_chart)
        column_chart.set_title({'name':chart_title, 'name_font': {'name': u'微软雅黑', 'size': 12}})
        # column_chart.set_x_axis({'name': u'国别'})
        column_chart.set_y_axis({'name':chart_y, 'name_font': {'name': u'微软雅黑', 'size': 10}})
        column_chart.set_legend({'position': 'bottom'})
        column_chart.set_size({'width': 465,'height':256})
        self.sheetFWL.insert_chart(insertPos, column_chart)

    ###
    # 按照国家进行统计
    ###

    def xlsx_tcountry(self):
        t1_title = [u'访问国家', u'访问资源（K）', u'流量（M）']
        sql = 'select country,sum(ipcount) as ct,sum(flow_byte) as fl from t_requests group by country order by fl desc'
        t1_data = self._get_data(sql)
        self._exls_table(t1_title, t1_data)
        self._exls_chart(u'访问国家分析', u'访问资源(千次)', u'数据流量（M）')

    ###
    # 按照城市进行统计
    ###
    def xlsx_tcity(self):
        t1_title = [u'访问城市', u'访问资源（K）', u'流量（M）']
        sql = 'select city,sum(ipcount) as ct,sum(flow_byte) as fl from t_requests group by city order by fl desc'
        t1_data = self._get_data(sql)
        self._exls_table(t1_title,t1_data,19,0)
        self._exls_chart(u'访问城市分析', u'访问资源(千次)', u'数据流量（M）', 19, 27, 0, 'E19')

    ###
    # 按IP访问
    ###
    def xlsx_tip(self):
        sql='select ip,sum(ipcount) as ct,sum(flow_byte) as flow from t_requests group by ip order by flow desc'
        t1_title = [u'访问ip', u'访问资源', u'TOP流量（M）']
        t1_data = self._get_data(sql,10,False)
        self._exls_table(t1_title, t1_data, 35, 0)
        sql = 'select ip,sum(ipcount) as ct,sum(flow_byte) as flow from t_requests group by ip order by ct desc'
        t1_title = [u'访问ip', u'TOP访问', u'流量（M）']
        t1_data = self._get_data(sql,10,False)
        self._exls_table(t1_title, t1_data, 35, 5)

    ###
    # 非Get方式访问IP
    ###
    def xlsx_noGET(self):
        sql = 'select ip,sum(ipcount) as ct,sum(flow_byte) as byte from t_requests where get=0 group by ip  order by byte desc'
        self._exls_ipstatus(u'无GET方式访问',sql,3,12,10)

    ###
    # POST方式IP TOP10
    ###
    def xlsx_bitPOST(self):
        sql='select ip,sum(ipcount) as ct,sum(flow_byte) as byte from t_requests where post>100 group by ip  order by ct desc'
        self._exls_ipstatus(u'POST方式访问IP TOP10', sql, 8, 12, 10)

    ###
    # HTTP 200 状态少于其他状态统计
    ###
    def xlsx_smallhttp200(self):
        sql='select ip,sum(ipcount) as ct,sum(flow_byte) as byte from t_requests where status_200<(status_206+status_302+status_304+status_400+status_403+status_404+status_500+status_502+status_503+status_unknow) group by ip  order by ct desc'
        self._exls_ipstatus(u'HTTP 200 状态少于其他状态统计', sql, 13, 12, 10)

    ###
    # HTTP 404 状态较大IP
    ###
    def xlsx_bithttp404(self):
        sql='select ip,sum(ipcount) as ct,sum(flow_byte) as byte from t_requests where status_404>100 group by ip  order by ct desc'
        self._exls_ipstatus(u'HTTP 404 IP次数TOP10', sql, 18, 12, 10)

    ###
    # 访问纯脚本，没有访问静态资源IP
    ###
    def xlsx_onlyapp(self):
        sql='select ip,sum(ipcount) as ct,sum(flow_byte) as byte from t_requests where url_app>100 and url_static=0 group by ip  order by ct desc'
        self._exls_ipstatus(u'访问纯脚本程序，无静态资源访问IP', sql, 23, 12, 10)

    ###
    # 访问来源饼图
    ###
    def _xlsx_pie(self,title,sql,chart_title,startCol=0,startRow=48,endRow=55,insertCell='E48'):
        row = self.db.fetchone(sql)
        chart = self.workBook.add_chart({'type': 'pie'})
        data = [title,row,]
        self.sheetFWL.write_row(self._cell(startCol, startRow), [u'项目',u'数据'], self.format_table_header)
        self.sheetFWL.write_column(self._cell(startCol,startRow+1), data[0],self.format_table_row0)
        self.sheetFWL.write_column(self._cell(startCol+1,startRow+1), data[1],self.format_table_row1)
        chart.add_series({
            'categories':  u'=月报!'+self._cell(startCol,startRow+1)+':'+self._cell(startCol+1,endRow),
            'values': u'=月报!'+self._cell(startCol+1,startRow+1)+':'+self._cell(startCol+1,endRow),
            'data_labels': {'percentage': True,'category' : True},
        })

        chart.set_title({'name':chart_title,'name_font': {'name': u'微软雅黑', 'size': 12}})
        chart.set_size({'width': 465, 'height': 360})
        self.sheetFWL.insert_chart(insertCell, chart)

    def xlsx_refer(self):
        sql = 'select sum(baidu),sum(google),sum(so360),sum(sogou),sum(bing),sum(unknow) from t_refer'
        fro = [u'Baidu', u'Google', u'360搜索', u'Soguo', u'必应', u'其他']
        self._xlsx_pie(fro,sql,u'搜索引擎引导数据分析',0,48,54,'E48')

    ###
    # 热门搜索关键字
    ###
    def xlsx_kwtop10(self,startCol,startRow):
        sql = 'select kw,sum(kwcount) as ct from t_keyword group by kw order by ct desc'
        self.sheetFWL.merge_range(self._cell(startCol, startRow) + ':' + self._cell(startCol + 1, startRow), u'搜索热门关键字TOP10',
                                  self.format_table_header)
        #self.sheetFWL.write_row(self._cell(startCol, startRow+1), [u'关键字', u'次数'], self.format_table_header)
        data = self.db.fetchall(sql)
        i = 0
        for row in data:
            i += 1
            r=list(row)
            r[0] = r[0].decode('UTF8')
            self.sheetFWL.write_row(self._cell(startCol, i + startRow), r,
                                    self.format_table_row1 if i % 2 == 0 else self.format_table_row0)
            if i==10:
                break

    ###
    # 终端设备
    ###
    def xlsx_device(self):
        sql = 'select sum(mobile),sum(pc),sum(spider) from t_agents'
        fro = [u'移动终端', u'电脑PC', u'网络蜘蛛']
        self._xlsx_pie(fro, sql, u'访问设备统计', 0, 69, 72, 'E69')

    ###
    # 操作系统
    ###
    def xlsx_os(self):
        sql = 'select sum(ios),sum(osx),sum(android),sum(windows),sum(linux) from t_agents'
        fro = [u'IOS', u'OSX', u'Android',u'Windows',u'Linux']
        self._xlsx_pie(fro, sql, u'访问操作系统统计', 12, 48, 53, 'P48')

    ###
    # 浏览器系统
    ###
    def xlsx_browser(self):
        sql = 'select sum(ie),sum(edge),sum(firefox),sum(safari),sum(chrome),sum(qq),sum(weixin),sum(baidu),sum(uc) from t_agents'
        fro = [u'IE', u'EDGE', u'Firefox', u'Safari', u'Chrome',u'QQ浏览器',u'微信',u'百度浏览器',u'UC']
        self._xlsx_pie(fro, sql, u'访问操作系统统计', 12, 69, 78, 'P69')
