#encoding=utf-8
import unittest, requests
from interface.public_info import *
import os, sys,json

class User_Registration(unittest.TestCase):
    """用户注册"""
    def setUp(self):
        self.dbd = DB_Data()
        self.base_url = "http://xxxxxxxx/register/"

    def test_user_registration_1(self):
        """1"""
        payload = {"username":"lilip21151","password":"lilip2115","email":"lilip@qq.com"}
        r = requests.post(self.base_url, data = json.dumps(payload))
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.dbd.store_data(1, 1, {"request":["username","password"],"response":["code"]}, {"username":"lilip21151","password":"lilip2115","email":"lilip@qq.com"}, result)
        check_point = {"code":"00"}
        for key,value in check_point.items():
            self.assertEqual(result[key], value, msg = u"字段【{}】: expection: {}, reality: {}".format(key, value, result[key]))


    def tearDown(self):
        self.dbd.close_connect()

if __name__ == '__main__':
    unittest.main()
