# import the necessary packages
import numpy as np
import cv2
import os
# load the image
#img = cv2.imread("red_object1.jpg")

def createMask(img) :
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define the list of boundaries (red) #need to be modified.
    lower_range = np.array([0, 100, 100], dtype=np.uint8)
    upper_range = np.array([17, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_range, upper_range)

    kernel = np.ones((5, 5), np.uint8)
    # morphological closing (fill small holes in the foreground)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.erode(mask, kernel, iterations=1)

    # morphological opening (remove small objects from the foreground)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)





    return mask

# cv2.imshow('mask', mask)
# cv2.imshow('image', img)
# cv2.imwrite('mask.bmp',mask)

cam = cv2.VideoCapture('output.avi')
cv2.startWindowThread()
count = 0
while (1):
    ret, img = cam.read()
    if ret == False:
        break
    vis = img.copy()
    cv2.imshow('frame',vis)

    mask = createMask(img)
    cv2.imshow('mask', mask)
    mask_name = 'mask' + str(count) + '.png'
    cv2.imshow('Image', vis)
    mask_path = '/Users/Travis/Documents/color_detect_img/'
    cv2.imwrite(os.path.join(mask_path, mask_name), mask)
    print (mask_name+ 'saved')
    cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('cnt',img)

    count += 1
    ch = cv2.waitKey(30) & 0xFF
    if ch == ord('q'):
        break

cv2.waitKey(1)
cv2.destroyAllWindows()
