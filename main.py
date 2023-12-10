import cv2 as cv
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
from pictures import pictuter

os.chdir(os.path.dirname(os.path.dirname(__file__)))

hsv_filter = HsvFilter(116,129,0,179,255,255,0,0,255,0)

#loop_time = time()
def run(wincap, flag=False, loop_time = time()):
    pictures = pictuter
    hsv_filter = HsvFilter(116,129,0,179,255,255,0,0,255,0)
    vision_limestone = Vision(pictures)
    while(flag):
        screenshot = wincap.get_screenshot()
        processed_image = vision_limestone.apply_hsv_filter(screenshot, hsv_filter)
        rectangles = vision_limestone.find(processed_image, 0.8)
        output_image = vision_limestone.draw_rectangles(processed_image, rectangles)

        #cv.imshow('Captured', screenshot)
        #cv.imshow('Matches', output_image)

        #print('FPS {}'.format(1 / (time() - loop_time)))
        #loop_time = time()

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            flag = False
            return 0