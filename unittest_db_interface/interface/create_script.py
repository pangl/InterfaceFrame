#encoding=utf-8
from utils.db_handler import DB
from utils.static_final import *

#写新文件的方法
def new_file(apiInfo, api_case_list):   # apiInfo:调用哪个接口，api_case_list:这个接口的全部用例
    with open(SCRIPT_PATH + "\\" + apiInfo[1] + "_test.py", "w") as fp:
        # 生成文件时添加个标识(_test)，这样执行时只会执行标识结尾的文件。否则不会执行。
        # ----写入头文件----
        fp.write(code_head) # 写入头文件

        # ----写入class名称,初始化信息
        if apiInfo[5] == 1: # apiInfo[5]：interface_api表中的rely_db列，等于1标识依赖数据库
            # 表示需要连接数据库
            fp.write(class_head_db %(apiInfo[1].title(), apiInfo[0], apiInfo[2]))
            #传递的内容分别是类名，注释，url
        else:
            # 不需要连接数据库情景
            fp.write(class_head % (apiInfo[1].title(), apiInfo[0], apiInfo[2]))
            # apiInfo[1].title() 把apiInfo[1]里的内容，首字母变成大写

        # ----写入类方法内容----
        param_code = ""
        for idx, case in enumerate(api_case_list, 1):   # 循环api_case_list表，并生成索引号，从1开始
            if case[3]: # case[3]：interface_test_case表中的rely_data列，判断是否需要进行依赖数据的处理
                # 说明需要获取依赖数据
                param_code = '''payload = self.dbd.param_completed(%s, %s)''' %(eval(case[2]), eval(case[3]))
                #调用public_info的param_completed方法，获取并处理依赖数据
            else:
                # 不需要进行依赖数据处理
                param_code = '''payload = %s''' %case[2]
            store_code = ""
            if case[6]:
                # 需要写入存储依赖数据
                store_code = '''self.dbd.store_data(%s, %s, %s, %s, %s)''' %(int(case[1]), int(case[0]), case[6],case[2] if case[2] else None, "result")
                # 'result'对应static_final里对应响应函数的result值
            if case[7]:
                store_code += check_code %case[7]
            if apiInfo[3] == "post":    #判断请求方式，apiInfo[3]=r_method列
                fp.write(post_code %(apiInfo[1] + "_" + str(idx),str(idx), param_code, store_code))
                # 传递方法名，测试用例的索引号，post请求传递的参数，数据存储（和检查点）
            elif apiInfo[3] == "get":
                fp.write(get_code % (apiInfo[1] + "_" + str(idx), str(idx), param_code, store_code))

        # ----写入类的尾方法内容----
        if apiInfo[5] == 1:
            fp.write(class_end_db)
        fp.write(code_end)
        fp.close()

def create_script():
    db = DB()
    # 从数据库获取需要执行的api列表
    apiList = db.get_api_list()     #获取sql文件中interface_api表的内容。返回一个列表对象。
    for api in apiList:             #逐个处理interface_api表的内容
        # 根据api_id获取该接口的测试用例
        api_case_list = db.get_api_case(api[0]) #调用get_api_case方法，通过api_id其所在行的用例内容。api[0]：api_id所在的列
        print api_case_list
        new_file(api[1:7], api_case_list)   #api[1:7]传递列，api_case_list：传递整个interface_api表


if __name__ == "__main__":
    create_script()