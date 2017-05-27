#!/usr/bin/env python
# coding=utf-8

import sqlite3

class SqliteHelper(object):
    def __init__(self, filename):
        """
            构造方法
            参数: filename 为SQLite3 数据库文件名
        """
        self.file_name = filename

    def open(self):
        """
            打开数据库并设置游标
        """
        self.connection = sqlite3.connect(self.file_name)
        self.connection.text_factory = str
        self.cursor = self.connection.cursor()
        return self

    def close(self):
        """
            关闭数据库，注意若不显式调用此方法，
            在类被回收时也会尝试调用
        """
        if hasattr(self, "connection") and self.connection:
            self.connection.close()

    def __del__(self):
        """
            析构方法，做一些清理工作
        """
        self.close()

    def commit(self):
        """
            提交事务
            SELECT语句不需要此操作，默认的execute方法的
            commit_at_once设为True会隐式调用此方法，
            否则就需要显示调用本方法。
        """
        self.connection.commit()

    def table(self, *args):
        """
            设置查询的表，多个表名用逗号分隔
        """
        self.tables = args
        self.tables_snippet = self.__concat_keys(self.tables)
        return self

    def fetchone(self, sql=None):
        """
            取一条记录
        """
        self.execute(sql, False)
        return self.cursor.fetchone()

    def fetchall(self, sql=None):
        """
            取所有记录
        """
        self.execute(sql, False)
        return self.cursor.fetchall()

    def __concat_keys(self,keys):
        kw = ['MAX', 'MIN', 'COUNT', 'DISTINCT', 'AVG', 'SUM']
        r = "[" + "],[".join(keys) + "]"
        for k in kw:
            if k in r.upper():
                return ','.join(keys)
        return r

    def __wrap_fields(self,fields):
        for key, value in fields.items():
            fields[key] = value
        return fields

    def __concat_fields(self,fields):
        fstr = []
        for key, value in fields.items():
            fstr.append(key+' = ?')
            self.sql_params.append(value)
        return ','.join(fstr)

    def execute(self, sql=None, commit_at_once=True):
        """
            执行SQL语句
            参数:
                sql  要执行的SQL语句，若为None，则调用构造器生成的SQL语句。
                commit_at_once 是否立即提交事务，如果不立即提交，
                对于非查询操作，则需要调用commit显式提交。
        """
        if not sql:
            if self.current_token == "INSERT":
                params = tuple(self.body_fields.values())
                self.cursor.execute(self.sql, params)
            elif self.current_token == "DELETE":
                pass
            elif self.current_token == "UPDATE":
                self.cursor.execute(self.sql, tuple(self.sql_params))
            elif self.current_token == "SELECT":
                self.cursor.execute(self.sql,tuple(self.sql_params))
            else:
                self.cursor.execute(self.sql)
        else:
            self.cursor.execute(sql)
        if commit_at_once:
            self.commit()

    def __build(self):
        self.sql_params = []
        {
            "SELECT": self.__select,
            "INSERT": self.__insert,
            "UPDATE": self.__update,
            "DELETE": self.__delete
        }[self.current_token]()

    def select(self, *args):
        self.current_token = "SELECT"
        self.body_keys = args
        self.__build()
        return self

    def __select(self):
        template = "SELECT %(keys)s FROM %(tables)s"
        body_snippet_fields = {
            "tables": self.tables_snippet,
            "keys": self.__concat_keys(self.body_keys),
        }
        self.sql = template % body_snippet_fields

    def insert(self, **kwargs):
        self.current_token = "INSERT"
        self.body_fields = self.__wrap_fields(kwargs)
        self.__build()
        return self

    def __insert(self):
        template = "INSERT INTO %(tables)s (%(keys)s) VALUES (%(values)s)"
        body_snippet_fields = {
            "tables": self.tables_snippet,
            "keys": self.__concat_keys(list(self.body_fields.keys())),
            "values": ','.join('?' * len(self.body_fields.values()))
        }
        self.sql = template % body_snippet_fields

    def update(self, **kwargs):
        self.current_token = "UPDATE"
        self.body_fields = self.__wrap_fields(kwargs)
        self.__build()
        return self

    def __update(self):
        template = "UPDATE %(tables)s SET %(fields)s"
        body_snippet_fields = {
            "tables": self.tables_snippet,
            "fields": self.__concat_fields(self.body_fields)
        }
        self.sql = template % body_snippet_fields

    def delete(self, *conditions):
        self.current_token = "DELETE"
        self.__build()
        # if *conditions:
        self.where(*conditions)
        return self

    def __delete(self):
        template = "DELETE FROM %(tables)s"
        body_snippet_fields = {
            "tables": self.tables_snippet
        }
        self.sql = template % body_snippet_fields

    def where(self,whereSql,*whereParams):
        self.sql += ' where '+whereSql
        for v in whereParams:
            self.sql_params.append(v)
        return self