'''two moule for user story 10.4.3
   simple usage:
   my_detector = moving_detector()
   #we need two frame to calculate optical flow
   #flow shows the direction vector
   #hsv shows the rectangular box
   flow , hsv = my_detector.show_flow(prev,cur) 
    '''
from detect_pck.color_detector import color_detector
from detect_pck.dynamic_object_detector import moving_detector
