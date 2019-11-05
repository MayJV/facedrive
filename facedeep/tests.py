from django.test import TestCase

# Create your tests here.
import numpy as np
li = [False,False,True]
index = li.index(True)
print(index)

l1 = []
l2 = ['dd','dddd']
l1.append(l2)
print(l1)

# a = np.array([2,3,4])
a = None
if len(a) > 0 :
    print(11111111)
