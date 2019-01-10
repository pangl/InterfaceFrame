#encoding=utf-8
import requests
import json

class HttpClient(object):
    def __init__(self):
        pass

    def request(self, requestMethod, requestUrl, paramsType,
               requestData = None, headers = None, cookies = None):
        if requestMethod.lower() == "post":
            if paramsType == "form":
                response = self.__post(url = requestUrl, data = json.dumps(eval(requestData)),
                                       headers = headers, cookies = cookies)
                return response
            elif paramsType == "json":
                response = self.__post(url=requestUrl, json = json.dumps(eval(requestData)),
                                       headers = headers, cookies = cookies)
                return response
        elif requestMethod == "get":
            if paramsType == "url":
                request_url = "%s%s" %(requestUrl, requestData)
                response = self.__get(url = request_url,
                                       headers = headers, cookies = cookies)
                return response
            elif paramsType == "params":
                response = self.__get(url=requestUrl, params = requestData,
                                      headers = headers, cookies = cookies)
                return response

    def __post(self, url, data = None, json = None, **kwargs):
        response = requests.post(url = url, data = data, json = json)
        return response

    def __get(self, url, params = None, **kwargs):
        response = requests.get(url = url, params = params)
        return response

if __name__ == '__main__':
    hc = HttpClient()
    res = hc.request("post","http://xxxxxxxxxxx/register/","form",'{"username":"lilysdd12","password":"lily12323","email":"lily@qq.com"}')
    print dir(res)

















