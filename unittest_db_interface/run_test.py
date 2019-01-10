#encoding=utf-8
import time, sys
sys.path.append('./script')
from utils.HTMLTestRunner import HTMLTestRunner
from unittest import defaultTestLoader
from interface.create_script import create_script
import sys
reload(sys)
sys.setdefaultencoding("utf8")

# 生成测试脚本
create_script()

if __name__ == "__main__":
    # 执行测试用例
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    # 指定测试用例为当前文件夹下的 script 目录
    test_dir = './script'
    testsuit = defaultTestLoader.discover(test_dir, pattern='*_test.py')
    # defaultTestLoader.discover 查找指定目录中_test.py结尾的文件，将它加为待执行用例组
    filename = './report/' + now + '_result.html'   #生成测试报告的文件名
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,title='接口自动化测试',description='接口自动化测试结果报告')
    # 写入结果报告的文件，设置报告名称，报告的描述
    runner.run(testsuit)    #执行用例
    fp.close()
