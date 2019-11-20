# __*__ coding:utf-8 __*__

def responseCode(inDict,code):
    if "200" == code:
        inDict['code'] = "200"
        inDict['msg'] = "success"
    elif "202" == code:
        inDict['code'] = "202"
        inDict['msg'] = "Accepted 已经接受请求，但处理尚未完成"
    elif "400" == code:
        inDict['code'] = "400"
        inDict['msg'] = "Bad Request 参数错误"
    elif "404" == code:
        inDict['code'] = "404"
        inDict['msg'] = "图片路径不正确"
    elif "201" == code:
        inDict['code'] = "202"
        inDict['msg'] = "没有识别到人脸"
    elif "203" == code:
        inDict['code'] = "400"
        inDict['msg'] = "driveName人脸库不存在"




