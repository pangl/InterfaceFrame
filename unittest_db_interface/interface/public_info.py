#encoding=utf-8
import MySQLdb
from utils.config_handler import ConfigParse
from datetime import datetime
from utils.Md5_encrypt import md5_encrypt

class DB_Data(object):
    def __init__(self):
        self.db_conf = ConfigParse().get_db_conf()
        self.conn = MySQLdb.connect(
            host=self.db_conf["host"],
            port=self.db_conf["port"],
            user=self.db_conf["user"],
            passwd=self.db_conf["password"],
            db=self.db_conf["db"],
            charset="utf8"
        )
        # 设置数据库变更自动提交
        self.conn.autocommit(1)
        self.cur = self.conn.cursor()
        
    def close_connect(self):
        # 关闭数据连接
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_rely_data(self, api_id, case_id):
        sqlStr = "select data_store from interface_data_store where api_id=%s and case_id=%s" %(api_id, case_id)
        self.cur.execute(sqlStr)
        # 字典对象
        rely_data = eval((self.cur.fetchall())[0][0])
        return rely_data

    def has_rely_data(self, api_id, case_id):   #判断依赖数据是否存在
        # 生成查找依赖数据的sql语句
        sqlStr = "select data_store from interface_data_store where api_id=%s and case_id=%s" %(api_id, case_id)
        # 获取受影响的条数，0表示没有查到数据，>0表示至少有一条数据
        affect_num = self.cur.execute(sqlStr)
        # 返回受影响的条数
        return affect_num

    def in_store_data(self, api_id, case_id, storeData):#向interface_data_store写入内容
        '''向数据库写入依赖数据'''
        # 判断数据库中是否已存在这条数据
        has_data = self.has_rely_data(api_id, case_id)  #使用has_rely_data方法，通过api_id, case_id为条件判断
        if has_data:
            # 数据库中已经存在这条数据，直接更新data_store字段即可
            sqlStr = "update interface_data_store set data_store=\"%s\", ctime=\"%s\" where api_id=%s and case_id=%s"
            self.cur.execute(sqlStr %(storeData, datetime.now(), api_id, case_id))
        else:
            # 数据库中不存在这条数据，需要添加
            sqlStr = "insert into interface_data_store value(%s, %s, \"%s\", \"%s\")"
            self.cur.execute(sqlStr %(api_id, case_id, storeData, datetime.now()))

    def param_completed(self, param, rely_data):  #param：原始的参数，rely_data：依赖的数据（interface_data_store中的内容）
        """处理依赖数据，时请求参数完整化"""
        paramSource = param.copy()
        for key, value in rely_data.items():
            api_id, case_id = key.split("->")
            #获取依赖数据的位置。api_id, case_id用于定位获取interface_data_store表中的哪个内容
            relyData = self.get_rely_data(int(api_id), int(case_id))    #获取到具体的依赖数据
            for k, v in relyData.items():   #将依赖数据的内容，按照原始内容的格式重新赋值
                if paramSource.has_key(k):
                    paramSource[k] = v
        return paramSource                  #返回新生成的内容

    def store_data(self, api_id, case_id, storeReg, requestData = None, responseData = None):
        # 按照interface_data_store表的内容传入数据。
        # storeReg：传入的格式。requestData，responseData为具体传入的内容。
        """存储依赖数据"""
        storeData = {}
        for key, value in storeReg.items():
            if requestData and key == "request":
                for i in value:
                    if requestData.has_key(i):
                        if i == "password": #将密码转换为md5加密后的值
                            storeData[i] = md5_encrypt(requestData[i])
                        else:
                            storeData[i] = requestData[i]
            elif responseData and key == "response":
                for j in value:
                    if responseData.has_key(j):
                        if j == "password":
                            storeData[j] = md5_encrypt(responseData[j])
                        else:
                            storeData[j] = responseData[j]
        # 将依赖数据写入数据库
        self.in_store_data(api_id, case_id, storeData)


if __name__ == "__main__":
    dbd = DB_Data()
    param = {'username': 'world123', 'password': 'world1324'}
    rely_data = {"1->1":["username"]}
    #print dbd.param_completed(param,rely_data)
    dbd.store_data(2, 1, {"request":["userid","token","password"]},{"userid":12, "token":"sdfwerwqec243","password":"sf23sd"})


