# -*- coding: utf-8 -*-
from pymysql import *


class MysqlHelper(object):
    # 数据库连接参数，可以定义多个，比如conn_params1，conn_params2，用于连接多个数据库，在类实例化时指定
    conn_params = {'host': '192.168.100.244', 'port': 3306, 'user': 'root', 'passwd': 'Abcd@123', 'db': 'jhzn',
                    'charset': 'utf8'}

    # 类的构造函数，主要用于类的初始化
    def __init__(self, conn_params):
        self.__host = conn_params['host']
        self.__port = conn_params['port']
        self.__db = conn_params['db']
        self.__user = conn_params['user']
        self.__passwd = conn_params['passwd']
        self.__charset = conn_params['charset']

    # 建立数据库连接和打开游标
    def __connect(self):
        self.__conn = connect(host=self.__host, port=self.__port, db=self.__db, user=self.__user, passwd=self.__passwd,
                              charset=self.__charset)
        self.__cursor = self.__conn.cursor()

    # 关闭游标和关闭连接
    def __close(self):
        self.__cursor.close()
        self.__conn.close()

    # 取一条数据
    def get_one(self, sql, params):
        result = None
        try:
            self.__connect()
            self.__cursor.execute(sql, params)
            result = self.__cursor.fetchone()
            self.__close()
        except Exception as e:
            print(e)
            return e
        return result

    # 取所有数据
    def get_all(self, sql, params):
        lst = ()
        try:
            self.__connect()
            self.__cursor.execute(sql, params)
            lst = self.__cursor.fetchall()
            self.__close()
        except Exception as e:
            print(e)
            return e
        return lst

    # 增加数据
    def insert(self, sql, params):
        return self.__edit(sql, params)

    # 修改数据
    def update(self, sql, params):
        return self.__edit(sql, params)

    # 删除数据
    def delete(self, sql, params):
        return self.__edit(sql, params)

    # 写数据操作具体实现，增删改操作都是调用这个方法来实现，这是个私有方法，不允许类外部调用
    def __edit(self, sql, params):
        count = 0
        try:
            self.__connect()
            count = self.__cursor.execute(sql, params)
            self.__conn.commit()
            self.__close()
        except Exception as e:
            print(e)
            return e
        return count
