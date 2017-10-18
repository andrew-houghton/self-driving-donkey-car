# import the necessary packages
import numpy as np
import cv2
# load the image
img = cv2.imread("red_object1.jpg")
print (type(img))
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# define the list of boundaries
lower_range = np.array([169, 100, 100], dtype=np.uint8)
upper_range = np.array([189, 255, 255], dtype=np.uint8)

mask = cv2.inRange(hsv, lower_range, upper_range)

kernel = np.ones((5,5), np.uint8)

#morphological opening (remove small objects from the foreground)
mask = cv2.erode(mask, kernel, iterations=1)
mask = cv2.dilate(mask, kernel, iterations=1)

#morphological closing (fill small holes in the foreground)
mask = cv2.dilate(mask, kernel, iterations=1)
mask = cv2.erode(mask, kernel, iterations=1)


cv2.imshow('mask', mask)
cv2.imshow('image', img)
cv2.imwrite('mask.bmp',mask)
while (1):
    k = cv2.waitKey(0)
    if (k == 27):
        break

cv2.destroyAllWindows()
