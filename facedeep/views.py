from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import generic


class TargetSubGraph(generic.CreateView):
    def post(self, request, *args, **kwargs):
        reJson = {'code':'200','data':'df1d5f4d5f4s5f1s4'}
        return JsonResponse(reJson)