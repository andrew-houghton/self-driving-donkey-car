import cv2
import os
import numpy as np
#only work for python3
def getimpaths(datapath):
    paths = []
    for dir in os.listdir(datapath):
        try:
            for filename in os.listdir(os.path.join(datapath, dir)):
                paths.append(os.path.join(datapath, dir, filename))
        except:
            pass

    return paths

paths = getimpaths('/Users/Travis/Documents/flow_img/')
#print (paths)


# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID') # Be sure to use lower case
out = cv2.VideoWriter('test.avi', fourcc, 20.0, (500, 500))
count = 0
for dir in paths:
    if dir == '/Users/Travis/Documents/flow_img/img/.DS_Store' :
        continue
    frame = cv2.imread(dir)

    print (np.shape(frame))
    #out.write(frame) # Write out frame to video

    cv2.imshow('video',frame)
    count += 1
    print (count)
    if count == 500:
        break
    if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
        break



# Release everything if job is finished
out.release()
cv2.destroyAllWindows()

