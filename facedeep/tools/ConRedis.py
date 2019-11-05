# _*_ coding:utf-8 _*_
import json

from FaceDriving.settings import *
import redis

class RedisTT(object):
    def __init__(self):
        self.r = redis.Redis(host=REDIS_IP, port=6397, decode_responses=True,password=REDIS_PAWD)

    def insertRedis(self,keyName,jsonStr):
        self.r.lpush(keyName,jsonStr)

    def queryRedis(self,keyName):
        return self.r.lrange(keyName, 0, -1)


if __name__ == '__main__':
    tt = RedisTT()
    query_redis = tt.queryRedis('d3')
    print(type(query_redis))

r = RedisTT().r
bm = {'a':['aa','ddd']}
r.lpush('d3',json.dumps(bm))

# r.delete('d3')
print(r.lrange('d3',0,-1))
#
# import face_recognition
#
# picture_of_me = face_recognition.load_image_file("/root/no.jpg")
# my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
#
# bm = {'a':my_face_encoding.tolist()}
# r.lpush('d3',json.dumps(bm))
# print(np.asarray(array))