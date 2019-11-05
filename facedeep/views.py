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
from facedeep.tools import responseTools, FaceTools
from facedeep.tools.ConRedis import RedisTT


class FaceCompare(generic.CreateView):
    def post(self, request, *args, **kwargs):
        reJson ={}
        result = False
        person = ''
        driveName = request.POST.get('driveName')
        filePath = request.POST.get('filePath')

        if not driveName or not filePath:
            responseTools.responseCode(reJson, '400')
            return JsonResponse(reJson)
        if not os.path.exists(filePath):
            responseTools.responseCode(reJson, '404')
            return JsonResponse(reJson)

        try:
            redisClient = RedisTT()

            code = FaceTools.jpg2FeatureCode(filePath)
            if len(code) < 1:
                responseTools.responseCode(reJson, '201')
                return JsonResponse(reJson)

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
                    resultList = face_recognition.compare_faces(codeDB, code)
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
        return JsonResponse(reJson)