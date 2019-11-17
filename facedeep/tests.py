from django.test import TestCase

# Create your tests here.
import numpy as np

from facedeep.tools.ConRedis import RedisTT

li = [False,False,True]
index = li.index(True)
print(index)


l2 = ['dd','dddd']
l2.append('ccc')

print(l2)
l1 = []

for i in l2:
    l1.append(i)
print(l1)



r = RedisTT().r
print(r.lrange('drive1',0,-1))
