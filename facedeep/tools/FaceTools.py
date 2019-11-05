# _*_ coding:utf-8 _*_
import face_recognition

from FaceDriving.settings import ALLOWED_EXTENSIONS

'''
   jpg 提取特征码
'''

def jpg2FeatureCode(jpgPath):
    if '.' in jpgPath and jpgPath.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        picture = face_recognition.load_image_file(jpgPath)
        face_encoding_list = face_recognition.face_encodings(picture)
        if len(face_encoding_list) == 0:
            print('未检测到人脸: ' + jpgPath )
        else:
            return face_encoding_list[0]

    else:
        print('文件格式不对：' + jpgPath)