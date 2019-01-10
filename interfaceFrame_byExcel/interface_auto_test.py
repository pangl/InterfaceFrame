#encoding=utf-8
import requests
import json
from utils.ParseExcel import ParseExcel
from config.public_data import *
from utils.HttpClient import HttpClient
from action.get_rely import GetKey
from action.data_store import RelyDataStore
from action.check_result import CheckResult
from action.write_test_result import write_result

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
	parseE = ParseExcel() 	# 调用utils的ParseExcel()类，处理excel文件
	parseE.loadWorkBook(file_path)	#将excel文件加载到内存，并获取其workbook对象
	sheetObj = parseE.getSheetByName(u"API")	#获取名称为API的sheet
	activeList = parseE.getColumn(sheetObj, API_active)
	#获取API sheet中active列,返回一个tuple。API_active在全局变量中设置
	for idx, cell in enumerate(activeList[1:], 2):
		#enumerate生成键值对，activeList[1:]表示从第一行开始遍历，2表示起始编号为2
		if cell.value == "y":
			# 遍历active列设置为y所在的行
			# 需要执行的接口所在行的行对象
			rowObj = parseE.getRow(sheetObj, idx)				# 获取active为y的每一行的内容，返回一个tuple
			apiName = rowObj[API_apiName - 1].value				# 获取ApiName列值，如register，login等
			requestUrl = rowObj[API_requestUrl - 1].value		# 获取requestUrl列值，如http://xxxxx/
			requestMethod = rowObj[API_requestMothod - 1].value	# 获取requestMothod列值,如post，get等
			paramsType = rowObj[API_paramsType - 1].value		# 获取paramsType列值，如form，json等
			apiTestCaseFileName = rowObj[API_apiTestCaseFileName - 1].value	# 获取APITestCase列值，如注册用例，登录用例等

			# 下一步读用例sheet表，准备执行测试用例
			caseSheetObj = parseE.getSheetByName(apiTestCaseFileName)
			# 根据上面存储的sheet名（apiTestCaseFileName）获取该sheet对象
			caseActiveObj = parseE.getColumn(caseSheetObj, CASE_active)
			# 获取上面sheet的active列，返回一个元祖对象
			for c_idx, col in enumerate(caseActiveObj[1:], 2):
				if col.value == "y":
					# 遍历获取active列设置为y所在的行
					# 说明此case行需要执行
					caseRowObj = parseE.getRow(caseSheetObj, c_idx) 		# 获取行号为c_idx行的全部内容，返回一个元组
					requestData = caseRowObj[CASE_requestData - 1].value	# 获取requestData对应的内容
					relyData = caseRowObj[CASE_relyData - 1].value			# 获取relyData对应的内容
					dataStore = caseRowObj[CASE_dataStore - 1].value		# 获取dataStore对应的内容
					checkPoint = caseRowObj[CASE_checkPoint - 1].value		# 获取checkPoint对应的内容
					if relyData:
						# 如果relydata有内容
						# 发送接口请求之前，先做依赖数据的处理
						requestData = "%s" %GetKey.get(eval(requestData), eval(relyData))
						# 将relyData指定的内容，按照requestData格式，生成一个新的requestData
					# 拼接接口请求参数，发送接口请求
					httpC = HttpClient()
					print apiTestCaseFileName,'--->','requestMethod:',requestMethod, 'requestUrl:',requestUrl, \
						'paramsType:',paramsType, 'requestData:',requestData
					response = httpC.request(requestMethod = requestMethod,
								  requestUrl = requestUrl,
								  paramsType = paramsType,
								  requestData = requestData
								  )
					print apiTestCaseFileName,'--->','response.json:',response.json()
					# 结果：{u'username': u'srsdcx01', u'code': u'01'}
					if response.status_code == 200:		#如果响应成功
						responseData = response.json()
						#将response内容设置成json类型，如{u'username': u'srsdcx01', u'code': u'01'}
						# 存储依赖数据
						if dataStore:#按照datastore的格式，存储依赖数据(requestData和responseData)
							RelyDataStore.do(eval(dataStore),apiName, c_idx - 1, eval(requestData),responseData)
						# 比对结果
						if checkPoint != None:
							errorKey = CheckResult.check(responseData, eval(checkPoint))
							#调用checkresult类，检查responseData是否存在checkPoint
							print 'main --->errorkey:',errorKey
						else:
							errorKey = {}
						write_result(parseE, caseSheetObj,responseData, errorKey, c_idx)
						#将responseData, errorKey, Status写入excel中
					else:
						print 'main --->response.status_code:',response.status_code
					print '------------------------------------------------'
				else:
					print apiTestCaseFileName,'---> 用例被忽略执行'
		else:
			print "接口被设置忽略执行"

if __name__ == '__main__':
	main()

