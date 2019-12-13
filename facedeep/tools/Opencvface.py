#!coding:utf-8
import cv2
import sys

'''
   人脸检测
'''

DEFINITION_NUM = 70

'''
	检测人脸
'''
def readFace(filepath):
	reBool = True
	img = cv2.imread(filepath)  # 读取图片
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换灰色

	# OpenCV人脸识别分类器
	classifier = cv2.CascadeClassifier("/usr/local/lib64/python3.6/site-packages/cv2/data/haarcascade_frontalface_default.xml")
	color = (0, 255, 0)  # 定义绘制颜色
	# 调用识别人脸
	faceRects = classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
	if len(faceRects) > 0:  # 大于0则检测到人脸
		# print('检测到人脸')
		# definitionScore(filepath) #进行清晰度检测
		pass
	else:
		# print('没有检测到人脸')
		reBool = False
	if reBool:
		imageVar = int(cv2.Laplacian(gray, cv2.CV_64F).var())
		if imageVar > DEFINITION_NUM:
			# print('清晰度合格')
			pass
		else:
			# print('图片模糊')
			reBool = False
	return reBool

'''
	检测人脸清晰度
'''
def definitionScore(imgPath):
	image = cv2.imread(imgPath)
	img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	imageVar = int(cv2.Laplacian(img2gray, cv2.CV_64F).var())
	if imageVar > DEFINITION_NUM:
		print('清晰度合格')
	else:
		print('图片模糊')

# if __name__ == '__main__':
# 	path = sys.argv[1]
# 	face = readFace(path)
# 	if face:
# 		print('图片合格')
# 	else:
# 		print('图片不合格')
#
