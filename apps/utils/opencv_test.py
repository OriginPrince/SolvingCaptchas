# _*_ encoding:utf-8 _*_
# author:ElegyPrincess

import cv2 as cv

img=cv.imread("D:/picture/02100312.jpg")
cv.namedWindow("Image")
cv.imshow("Image",img)
cv.waitKey(0)
cv.destroyAllWindows()