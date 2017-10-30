import numpy as np
import cv2
import os

def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis

def warp_flow(img, flow):
    h, w = flow.shape[:2]
    flow = -flow
    flow[:,:,0] += np.arange(w)
    flow[:,:,1] += np.arange(h)[:,np.newaxis]
    res = cv2.remap(img, flow, None, cv2.INTER_LINEAR)
    return res

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

    cam = cv2.VideoCapture('output.avi')
    ret, prev = cam.read()

    prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    show_hsv = True
    count = 0
    cv2.startWindowThread()
    while True:
        ret, img = cam.read()
        if ret == False:
            break
        vis = img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # apply color mask here

        flow = cv2.calcOpticalFlowFarneback(prevgray, gray, 0.5, 5, 15, 3, 5, 1.1, cv2.OPTFLOW_FARNEBACK_GAUSSIAN)
        prevgray = gray
        flow_img = draw_flow(gray, flow)
        cv2.imshow('flow', flow_img)

        if show_hsv:
            gray1 = cv2.cvtColor(draw_hsv(flow), cv2.COLOR_BGR2GRAY)
            #cv2.imshow('gray1', gray1)

            thresh = cv2.threshold(gray1, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                # modify parameters for detecting close objects.
                (x, y, w, h) = cv2.boundingRect(c)
                if w > 100 and h > 100 and w < 200 and h < 300:
                    cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 0, 255), 4)

            cv2.imshow('Image', vis)
            # move_name = 'move' + str(count) + '.jpg'
            # flow_path = '/Users/Travis/Documents/move_img/'
            # cv2.imwrite(os.path.join(flow_path, move_name), vis)
            # print(move_name + 'saved')
            count += 1

        ch = cv2.waitKey(30) & 0xFF
        if ch == ord('q'):
            break

    cv2.waitKey(1)
    cv2.destroyAllWindows()
