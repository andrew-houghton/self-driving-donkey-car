import numpy as np
import cv2


def draw_hsv(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:, :, 0], flow[:, :, 1]
    ang = np.arctan2(fy, fx) + np.pi
    v = np.sqrt(fx * fx + fy * fy)
    hsv = np.zeros((h, w, 3), np.uint8)
    hsv[..., 0] = ang * (180 / np.pi / 2)
    hsv[..., 1] = 255
    hsv[..., 2] = np.minimum(v * 4, 255)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr


if __name__ == '__main__':
    import sys

    try:
        fn = sys.argv[1]
    except:
        fn = 0

    cam = cv2.VideoCapture(fn)
    ret, prev = cam.read()

    prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    show_hsv = True

    cv2.startWindowThread()
    while True:
        ret, img = cam.read()
        vis = img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # apply color mask here
        flow = cv2.calcOpticalFlowFarneback(prevgray, gray, 0.5, 5, 15, 3, 5, 1.1, cv2.OPTFLOW_FARNEBACK_GAUSSIAN)
        prevgray = gray
        if show_hsv:
            gray1 = cv2.cvtColor(draw_hsv(flow), cv2.COLOR_BGR2GRAY)
            cv2.imshow('gray1', gray1)
            thresh = cv2.threshold(gray1, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                (x, y, w, h) = cv2.boundingRect(c)
                if w > 100 and h > 100 and w < 900 and h < 680:
                    cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 255, 0), 4)

            cv2.imshow('Image', vis)

        ch = cv2.waitKey(30) & 0xFF
        print (ch)
        if ch == ord('q'):
            break

    cv2.waitKey(1)
    cv2.destroyAllWindows()
