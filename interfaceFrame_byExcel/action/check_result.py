#encoding=utf-8
import re

class CheckResult(object):
    def __init__(self):
        pass

    @classmethod
    def check(self, responseObj, checkPoint):
        errorKey = {}
        for key, value in checkPoint.items():
            if isinstance(value, (str, unicode)):
                #说明是等值校验
                if responseObj[key] != value:
                    errorKey[key] = responseObj[key]
            elif isinstance(value, dict):
                #说明是需要通过正则表达式去校验
                sourceData = responseObj[key] #接口返回的真是值
                if value.has_key("value"):
                    # 说明是通过正则校验
                    regStr = value["value"]
                    rg = re.match(regStr, "%s" %sourceData)
                    if not rg:
                        errorKey[key] = sourceData
                elif value.has_key("type"):
                    # 说明是校验数据类型
                    typeS = value["type"]
                    if typeS == "N":
                        # 说明是整形
                        if not isinstance(sourceData,(int, long)):
                            errorKey[key] = sourceData
        return errorKey

if __name__ == '__main__':
    r = {"code":"01", "userid":12, "id":"12"}
    c = {"code": "00", "userid":{"type":"N"}, "id":{"value":"\d+"}}
    print CheckResult.check(r, c)




