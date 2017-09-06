
# Python program to demonstrate erosion and
# dilation of images.
import cv2
import numpy as np
import cv
# Reading the input image
img = cv2.imread("/Users/Travis/PycharmProjects/training_data_pre_processing/example_backgroud.jpeg",0)
kernel = np.ones((5, 5), np.uint8)
print type(img)
# The first parameter is the original image,
# kernel is the matrix with which image is
# convolved and third parameter is the number
# of iterations, which will determine how much

retval2,threshold2 = cv2.threshold(img,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# img_erosion = cv2.erode(img, kernel, iterations=1)
# img_openning = cv2.dilate(img_erosion, kernel, iterations=1)
# img_dialation_of_openning = cv2.dilate(img_openning, kernel, iterations=1)
cv2.imshow('Input', img)
cv2.imshow('thresholded',threshold2)



#cv2.imshow('Erosion', img_erosion)
#cv2.imshow('openning', img_openning)
#cv2.imshow('img_dialation_of_openning', img_dialation_of_openning)

cv2.waitKey(10000)