#encoding=utf-8
from config.public_data import REQUEST_DATA,RESPONSE_DATA
from utils.md5_encrypt import md5_encrypt

class GetKey(object):
    def __init__(self):
        pass

    @classmethod
    def get(cls, dataSource, relyData):
        data = dataSource.copy()
        for key, value in relyData.items():
            if key == "request":
                # 说明应该取REQUEST_DATA获取值
                for k, v in value.items():
                    interfaceName, case_id = v.split("->")
                    # val = REQUEST_DATA[interfaceName.decode("utf-8")][case_id][k]
                    val = REQUEST_DATA[interfaceName][case_id][k]
                    if k == "password":
                        data[k] = md5_encrypt(val)
                    else:
                        data[k] = val
            elif key == "response":
                # 说明应该去RESPONSE_DATA获取值
                for k, v in value.items():
                    interfaceName, case_id = v.split("->")
                    data[k] = RESPONSE_DATA[interfaceName][case_id][k]
        return data

if __name__ == '__main__':
    REQUEST_DATA = {}
    RESPONSE_DATA = {}
    s = {"username":"","password":""}
    rely = {"request":{"username":"用户注册->1","password":"用户注册->1"}}
    print GetKey.get(s, rely)


