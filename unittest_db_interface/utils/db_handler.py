#-*-coding:utf-8-*-
#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import MySQLdb
from config_handler import ConfigParse

class DB(object):
    def __init__(self):
        self.db_conf = ConfigParse().get_db_conf()  #获取db信息
        # 通过connect方法连接mysql数据库
        self.conn = MySQLdb.connect(
            host = self.db_conf["host"],
            port = self.db_conf["port"],
            user = self.db_conf["user"],
            passwd = self.db_conf["password"],
            db = self.db_conf["db"],
            charset = "utf8"
        )
        self.cur = self.conn.cursor()   #获取操作数据库的游标

    def close_connect(self):
        # 关闭数据连接
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_api_list(self):
        #获得api list
        sqlStr = "select * from interface_api where status=1"   #获取status值为1的，1表示执行。0表示不执行。
        self.cur.execute(sqlStr)        #执行sqlstr语句
        # 返回tuple对象
        apiList = list(self.cur.fetchall()) #取出执行后的结果，并转换成list
        return apiList

    def get_api_case(self, api_id):
        #获取测试用例
        sqlStr = "select * from interface_test_case where api_id=%s" %api_id
        #通过api_id获取所有用例，即获取一个接口的全部用例
        self.cur.execute(sqlStr)
        api_case_list = list(self.cur.fetchall())
        return api_case_list

    def get_rely_data(self, api_id, case_id):
        #获取依赖数据
        sqlStr = "select data_store from interface_data_store where api_id=%s and case_id=%s" %(api_id, case_id)
        #依赖的是哪个接口（api_id）的哪个用例（case_id）
        self.cur.execute(sqlStr)
        # 字典对象
        rely_data = eval((self.cur.fetchall())[0][0])
        return rely_data

if __name__ == '__main__':
    db = DB()
    print db.get_api_list()
    print db.get_rely_data(1,1)
