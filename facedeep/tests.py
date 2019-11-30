import os
import traceback

from django.http import JsonResponse
from django.test import TestCase

# Create your tests here.
import numpy as np
from django.views import generic

from facedeep.tools import responseTools


class BuildFace(generic.CreateView):

    def get(self, request, *args, **kwargs):
        print('---------------')
        reJson = {}
        ak = str(request.GET.get('ak'))
        driveName = str(request.GET.get('driveName'))
        print('driveName:' + driveName)
        print('ak:' + ak)
        if not ak or not driveName:
            responseTools.responseCode(reJson, '400')
            return JsonResponse(reJson)

        try:

            # writeToRedis('/usr/local/upload/' + driveName)
            print('driveName:' + driveName)
            print('ak:' + ak)

        except Exception as e:
            print(traceback.format_exc())
            print('input====', driveName, '   ',ak )
            responseTools.responseCode(reJson, '202')

        responseTools.responseCode(reJson, '200')
        return JsonResponse(reJson)
