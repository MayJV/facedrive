# _*_ coding:utf-8 _*_
import json
import os
import traceback
import numpy as np
import face_recognition


from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views import generic

from FaceDriving.settings import TOLERANCE
from facedeep.tools import responseTools, FaceTools
from facedeep.tools.ConRedis import RedisTT

# 单条比对
class FaceCompare(generic.CreateView):
    def post(self, request, *args, **kwargs):
        reJson = {}
        result = False
        person = ''
        driveName = request.POST.get('driveName')
        filePath = request.POST.get('filePath')

        if not driveName or not filePath:
            responseTools.responseCode(reJson, '400')
            return JsonResponse(reJson)
        print(filePath)
        # print(os.path.exists('/data/facedb/drive1/海洋.jpg'))

        # print(os.path.exists(filePath.decode("gb2312")))
        # print(os.path.exists(u'{}'.format(filePath)))
        if not os.path.exists(filePath):
            responseTools.responseCode(reJson, '404')
            return JsonResponse(reJson)

        try:
            redisClient = RedisTT()

            code = FaceTools.jpg2FeatureCode(filePath)
            if len(code) < 1:
                responseTools.responseCode(reJson, '201')
                return JsonResponse(reJson)

            if 'checkFace' == driveName:
                responseTools.responseCode(reJson, '200')

            queryList = redisClient.queryRedis(driveName)
            # todo

            if queryList:
                codeDB = []
                redisJson = json.loads(queryList[0])
                codeLists = redisJson.get('codeList')
                nameList = redisJson.get('nameList')
                if codeLists:
                    for codeList in codeLists:
                        codeDB.append(np.asarray(codeList))
                    resultList = face_recognition.compare_faces(codeDB, code, tolerance=TOLERANCE)
                    if True in resultList:
                        result = True
                        index = resultList.index(True)
                        person = nameList[index]

        except Exception as e:
            print(traceback.format_exc())
            print('input====', driveName, '   ', filePath)
            responseTools.responseCode(reJson, '202')

        reJson['result'] = result
        reJson['person'] = person
        reJson['driveName'] = driveName
        responseTools.responseCode(reJson, '200')
        return JsonResponse(reJson)

# 批量比对
class BatchFaceCompare(generic.CreateView):
    def post(self, request, *args, **kwargs):
        reJson = {}
        result = []
        person = []
        driveName = request.POST.get('driveName')
        filePathList = request.POST.get('filePath')

        if not driveName or not filePathList:
            responseTools.responseCode(reJson, '400')
            return JsonResponse(reJson)

        try:
            # 从 redis 读取特征码 集合
            redisClient = RedisTT()
            queryList = redisClient.queryRedis(driveName)
            codeDB = []
            if queryList:
                redisJson = json.loads(queryList[0])
                codeLists = redisJson.get('codeList')
                nameList = redisJson.get('nameList')
                if codeLists:
                    for codeList in codeLists:
                        codeDB.append(np.asarray(codeList))
            else:
                responseTools.responseCode(reJson, '203')
                return JsonResponse(reJson)

            # 遍历 路径集合
            for filePath in filePathList:
                if not os.path.exists(filePath):
                    responseTools.responseCode(reJson, '404')
                    return JsonResponse(reJson)

                code = FaceTools.jpg2FeatureCode(filePath)
                if len(code) < 1:
                    result.append(False)
                    person.append(None)
                    continue

                resultList = face_recognition.compare_faces(codeDB, code, tolerance=TOLERANCE)
                if True in resultList:
                    result.append(True)
                    index = resultList.index(True)
                    person.append(nameList[index])
                else:
                    result.append(False)
                    person.append(None)

        except Exception as e:
            print(traceback.format_exc())
            print('input====', driveName, '   ', filePathList)
            responseTools.responseCode(reJson, '202')

        reJson['result'] = result
        reJson['person'] = person
        reJson['driveName'] = driveName
        responseTools.responseCode(reJson, '200')
        return JsonResponse(reJson)

