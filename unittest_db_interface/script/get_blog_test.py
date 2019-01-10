#encoding=utf-8
import unittest, requests
from interface.public_info import *
import os, sys,json

class Get_Blog(unittest.TestCase):
    """查询博文"""
    def setUp(self):
        self.base_url = "http://xxxxxxxxxx/getBlogContent/"


    def test_get_blog_1(self):
        """1"""
        payload = 2
        r = requests.get(self.base_url + str(payload))
        result = r.json()
        self.assertEqual(r.status_code, 200)
        

if __name__ == '__main__':
    unittest.main()
