import cv2 as cv
import numpy as np
import os
import buttons
from hsvfilter import HsvFilter
from pictures import pictuter
import random
import time

press_buttons = {'1':buttons.up, '2':buttons.down, '3':buttons.right, '4':buttons.left,
                 '9':buttons.down, '10':buttons.up, '11':buttons.left, '12':buttons.right,
                 '5':buttons.upr, '6':buttons.downl, '7':buttons.downr, '8':buttons.upl,
                 '14':buttons.space}

class Vision:

    TRACKBAR_WINDOW = "Trackbars"

    pictures = None
    method = None


    def __init__(self, pictures, method = cv.TM_CCOEFF_NORMED):
        self.pictures = pictuter
        self.method = method

    
    def find(self, haystack_img, threshold=0.5):
        #haystack_img = cv.imread(haystack_img, cv.IMREAD_UNCHANGED)
        rectangles = []
        presses = {}
        i=1
        for picture in self.pictures:
            #filename = os.path.basename(needle_img_path)[:-4]
            filename = str(i)
            i+=1
            #if 'green' in needle_img_path:
            #    filename += 'g'
            #needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
            needle_img = picture
            # Save the dimensions of the needle image
            needle_w = needle_img.shape[1]
            needle_h = needle_img.shape[0]

            # There are 6 methods to choose from:
            # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
            method = cv.TM_CCOEFF_NORMED
            result = cv.matchTemplate(haystack_img, needle_img, self.method)
            #np.set_printoptions(threshold=sys.maxsize)
            #print(result)
            # Get the all the positions from the match result that exceed our threshold
            locations = np.where(result >= threshold)
            locations = list(zip(*locations[::-1]))
            #print(locations)

            # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
            # locations by using groupRectangles().
            # First we need to create the list of [x, y, w, h] rectangles
        
            for loc in locations:
                rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
                # Add every box to the list twice in order to retain single (non-overlapping) boxes
                rectangles.append(rect)
                #rectangles.append(rect)
                

                presses[(filename, result[int(loc[1])][int(loc[0])])] = rect[0]
                presses = dict(sorted(presses.items(), key=lambda x: x[1]))
                #print(presses)
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        #print(rectangles)
        filtered_presses = {}
        for key, value in presses.items():
            should_delete = False
            first_member, second_member = key
            for other_key, other_value in presses.items():
                if abs(other_value - value) <= 10 and other_key[1] > second_member:
                    should_delete = True
                    break
            if not should_delete:
                filtered_presses[key] = value
        keys_to_delete = []
        inmed = []
        #print(presses)
        for i in rectangles:
            keys_to_delete = []
            #print(i)
            inmed.append(i[0])
            #print(inmed)
            for k in list(filtered_presses.values()):
                if k not in inmed:
                    keys_to_delete.append(k)
            #print(keys_to_delete)
            #print(presses)
        for j in keys_to_delete:
            if j in filtered_presses:
                del filtered_presses[j]
        #print(filtered_presses)
        #for k, v in presses.items():

        '''
        !!!!!!!!!!!!!!!
        '''
        time.sleep(0.05)
        for k, v in filtered_presses.items():
            if k[0] != "14":
                perem = random.uniform(0.02, 0.04)
                press_buttons[k[0]](perem)
        '''
        !!!!!!!!!!!!!!!
        '''

        #flag = False
        #for v in presses.values():
        #    if 'g' in v:
        #        flag = True
        #    if v == '14':
        #        press_buttons[v]()

        return rectangles
    
    def click_points(self, rectangles):
        points = []
        
        for (x, y, w, h) in rectangles:
            # Determine the center position
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # Save the points
            points.append((center_x, center_y))
        return points
    
    def draw_rectangles(self, haystack_img, rectangles):
        line_color = (0,255,0)
        line_type = cv.LINE_4
        for (x,y,w,h) in rectangles:
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                                lineType=line_type, thickness=2)
        return haystack_img
    
    def draw_crosshairs(self, haystack_img, points):
        marker_color = (255,0,255)
        marker_type = cv.MARKER_CROSS
        for (center_x, center_y) in points:
            cv.drawMarker(haystack_img, (center_x, center_y), 
                                color=marker_color, markerType=marker_type, 
                                markerSize=40, thickness=2)
        return haystack_img
    

    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)
        def nothing(position):
            pass
        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        # Set default value for Max HSV trackbars
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)
        # trackbars for increasing/decreasing saturation and value
        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, nothing)


    def get_hsv_filter_from_controls(self):
        # Get current positions of all trackbars
        hsv_filter = HsvFilter()
        hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
        return hsv_filter
    
    def apply_hsv_filter(self, original_image, hsv_filter=None):
        # convert image to HSV
        hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

        # if we haven't been given a defined filter, use the filter values from the GUI
        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()

        # add/subtract saturation and value
        h, s, v = cv.split(hsv)
        s = self.shift_channel(s, hsv_filter.sAdd)
        s = self.shift_channel(s, -hsv_filter.sSub)
        v = self.shift_channel(v, hsv_filter.vAdd)
        v = self.shift_channel(v, -hsv_filter.vSub)
        hsv = cv.merge([h, s, v])

        # Set minimum and maximum HSV values to display
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
        # Apply the thresholds
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        # convert back to BGR for imshow() to display it properly
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        return img

    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c
