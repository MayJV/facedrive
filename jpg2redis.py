# _*_ coding:utf-8 _*_
'''
    人脸库建立
   jpg 提取特征值 存入redis
'''

import json
import os
import sys

from facedeep.tools import FaceTools
from facedeep.tools.ConRedis import RedisTT

'''
    遍历文件
'''
def listJPGFiles(path):
    reList = []
    if os.path.exists(path):
        listdir = os.listdir(path)
        for nodedir in listdir:
            if not os.path.isdir(path + '/' + nodedir):
                reList.append(path + '/' + nodedir)
    else:
        print("ERROR: path is not true!!!!")
    return reList

'''
    读取文件夹 下图片 特征码存入redis
'''
def writeToRedis(path):
    keyName = path.split('/')[-1]
    jpgPaths = listJPGFiles(path + '/tezhengku')

    inDict = {}
    codeList = []
    nameList = []
    for jpgPath in jpgPaths:
        print('read jpg : ' + jpgPath)
        splitFile = jpgPath.split('/')
        jpgName = splitFile[len(splitFile) - 1].split('.')[0]
        code = FaceTools.jpg2FeatureCode(jpgPath)
        if len(code) > 0:
            codeList.append(code.tolist())
            nameList.append(jpgName)

    inDict['codeList'] = codeList
    inDict['nameList'] = nameList
    tt = RedisTT()
    tt.r.delete(keyName)
    print(keyName)
    tt.insertRedis(keyName, json.dumps(inDict, ensure_ascii=False))


if __name__ == '__main__':
    path = sys.argv[1]
    if not path :
        print("python3.6 jpg2redis.py /data/facedb/drive1")
        exit(2)
    writeToRedis(path)


