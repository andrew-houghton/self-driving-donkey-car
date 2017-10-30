"""low and up means the lower and upper range of hsv of objects'color
 
 """

import numpy as np
import cv2

class color_detector:
    def __init__(self):
        name = 'color'

    def create_mask(self,img,low,up):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # define the list of boundaries (red) #need to be modified.
        lower_range = np.array([low, 100, 100], dtype=np.uint8)
        upper_range = np.array([up, 255, 255], dtype=np.uint8)

        mask = cv2.inRange(hsv, lower_range, upper_range)

        kernel = np.ones((5, 5), np.uint8)
        # morphological closing (fill small holes in the foreground)
        mask = cv2.dilate(mask, kernel, iterations=1)
        mask = cv2.erode(mask, kernel, iterations=1)

        # morphological opening (remove small objects from the foreground)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)
        return mask

    def draw_mask(self,img,low = 0,up = 17):
        mask = self.create_mask(img,low,up)
        cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('cnt', img)
        return img

