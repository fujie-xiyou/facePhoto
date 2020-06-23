# coding=utf-8
# 导入相应的python包
import cv2


def variance_of_laplacian(image):
    """
    计算图像的laplacian响应的方差值
    """
    return cv2.Laplacian(image, cv2.CV_64F).var()


def is_blurred(imagePath):
    # 读取图片
    image = cv2.imread(imagePath)
    # 将图片转换为灰度图片
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 计算灰度图片的方差
    fm = variance_of_laplacian(gray)
    print("fm = {}".format(fm))
    return fm < 100
