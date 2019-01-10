#encoding=utf-8
import os

#工程的根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#数据库配置文件绝对路径
config_path = BASE_DIR + "/config/db_config.ini"

# 测试脚本文件存放目录
SCRIPT_PATH = BASE_DIR + "/script"

#存放代码头
code_head = '''#encoding=utf-8
import unittest, requests
from interface.public_info import *
import os, sys,json
'''

# 无数据库链接时
# %s类名需要自定义，"""%s"""为备注信息，生成测试报告时要使用 #url不能写死，也需要后续传递，注意带引号
class_head = '''
class %s(unittest.TestCase):
    """%s"""
    def setUp(self):
        self.base_url = "%s"
'''

# 有数据库链接时
# %s类名需要自定义，"""%s"""为备注信息，生成测试报告时要使用 #url不能写死，也需要后续传递，注意带引号
class_head_db = '''
class %s(unittest.TestCase):
    """%s"""
    def setUp(self):
        self.dbd = DB_Data()
        self.base_url = "%s"
'''

# 有数据库链接时
class_end_db = '''
    def tearDown(self):
        self.dbd.close_connect()
'''

code_end = '''
if __name__ == '__main__':
    unittest.main()
'''

# post请求代码
# 第一个%s 用于放入数据存储和测试数据，第二%s用于存放检查点check_point内容，但不是非必须的。
# status_code=200是必须进行断言
post_code = '''
    def test_%s(self):
        """%s"""
        %s
        r = requests.post(self.base_url, data = json.dumps(payload))
        result = r.json()
        self.assertEqual(r.status_code, 200)
        %s
'''

# 与post_code区别，r = requests.get(self.base_url + str(payload))通过拼接生成url，post为传参生成
get_code = '''\n
    def test_%s(self):
        """%s"""
        %s
        r = requests.get(self.base_url + str(payload))
        result = r.json()
        self.assertEqual(r.status_code, 200)
        %s
'''

check_code = '''
        check_point = %s
        for key,value in check_point.items():
            self.assertEqual(result[key], value, msg = u"字段【{}】: expection: {}, reality: {}".format(key, value, result[key]))
'''