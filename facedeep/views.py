# _*_ coding:utf-8 _*_
import json
import os
import traceback
import numpy as np
import face_recognition
import requests
import json

from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views import generic

from FaceDriving.settings import TOLERANCE, AK
from facedeep.tools import responseTools, FaceTools
from facedeep.tools.ConRedis import RedisTT

# 单条比对
from jpg2redis import writeToRedis
import logging


class FaceCompare(generic.CreateView):
    def post(self, request, *args, **kwargs):
        reJson = {}
        result = False
        score = None
        person = ''
        driveName = request.POST.get('driveName')
        filePath = request.POST.get('filePath')

        if not driveName or not filePath:
            responseTools.responseCode(reJson, '400')
            return JsonResponse(reJson)
        logging.warning(filePath)
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

            if queryList:
                codeDB = []
                redisJson = json.loads(queryList[0])
                codeLists = redisJson.get('codeList')
                nameList = redisJson.get('nameList')
                # 对应驾校名下有 特征库
                if codeLists:
                    for codeList in codeLists:
                        codeDB.append(np.asarray(codeList))
                    logging.warning(nameList)
                    core = face_recognition.face_distance(codeDB, code).tolist()
                    logging.warning(core)
                    # 提取最接近的照片

                    # resultList = face_recognition.compare_faces(codeDB, code, tolerance=TOLERANCE)
                    # if True in resultList:
                    #     result = True
                    #     index = resultList.index(True)
                    #     person = nameList[index]
                    # score = min(core)
                    for bindex in range(len(core)):
                        if core[bindex] <= TOLERANCE:
                            score = core[bindex]
                            print('score-----' + str(score))
                            person = nameList[bindex]
                            ispass = getBaiDuScore('/usr/local/upload/' + driveName + '/tezhengku/' + person + '.jpg', filePath)
                            if ispass:
                                result = True
                                break
                            else:
                                score = 0.69
                                person = ''

                    if not result:
                        score = min(core)
                        person = ''


            else:
                responseTools.responseCode(reJson, '203')
                return JsonResponse(reJson)

        except Exception as e:
            print(traceback.format_exc())
            print('input====', driveName, '   ', filePath)
            responseTools.responseCode(reJson, '202')

        reJson['result'] = result
        reJson['score'] = score
        reJson['person'] = person
        reJson['driveName'] = driveName
        responseTools.responseCode(reJson, '200')
        return JsonResponse(reJson)


def getBaiDuScore(jpg1, jpg2):
    logging.warning('http://127.0.0.1:8090' + jpg1 + '='+ jpg2)
    respone = requests.get('http://127.0.0.1:8090' + jpg1 + '='+ jpg2)
    loads = json.loads(respone.text)
    logging.warning(loads)
    data = loads.get('data')
    if 'score' in data.keys():
        score = float(data.get('score'))
        if score >= 80:
            return True
    else:
        return False



# 批量比对
class BatchFaceCompare(generic.CreateView):
    def post(self, request, *args, **kwargs):
        reJson = {}
        result = []
        person = []
        driveName = request.POST.get('driveName')
        filePathList = request.POST.get('filePath').split(',')

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
                print('PATH: ==' + filePath + '==')
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

# 构建人脸库
class BuildFace(generic.CreateView):
    def post(self, request, *args, **kwargs):
        reJson = {}
        ak = request.POST.get('ak')
        driveName = request.POST.get('driveName')
        if not ak or not driveName:
            responseTools.responseCode(reJson, '400')
            return JsonResponse(reJson)

        try:
            if not os.path.exists('/usr/local/upload/' + driveName + '/tezhengku'):
                responseTools.responseCode(reJson, '404')
                return JsonResponse(reJson)

            if AK != ak:
                responseTools.responseCode(reJson, '401')
                return JsonResponse(reJson)

            writeToRedis('/usr/local/upload/' + driveName)

        except Exception as e:
            print(traceback.format_exc())
            print('input====', driveName, '   ',ak )
            responseTools.responseCode(reJson, '202')

        responseTools.responseCode(reJson, '200')
        return JsonResponse(reJson)

    def get(self, request, *args, **kwargs):
        reJson = {}
        ak = str(request.GET.get('ak'))
        driveName = str(request.GET.get('driveName'))
        if not ak or not driveName:
            responseTools.responseCode(reJson, '400')
            return JsonResponse(reJson)

        try:
            if not os.path.exists('/usr/local/upload/' + driveName + '/tezhengku'):
                responseTools.responseCode(reJson, '404')
                return JsonResponse(reJson)

            if AK != ak:
                responseTools.responseCode(reJson, '401')
                return JsonResponse(reJson)

            writeToRedis('/usr/local/upload/' + driveName)
        except Exception as e:
            print(traceback.format_exc())
            print('input====', driveName, '   ',ak )
            responseTools.responseCode(reJson, '202')

        responseTools.responseCode(reJson, '200')
        return JsonResponse(reJson)
