import cv2
import numpy
import math
from enum import Enum

class VisionProcessor:
    #I don't like the way the GRIP pipeline is acting so I'm writing my own

    '''
what to do:
constants should all be defined at the beginning for easy access
get the frame from the camera
blur the image with a median filter and correct radius
convert to an hsv image
apply hsv threshold
find contours in the image
filter the contours according to the preset sizes
publish/return contours somehow (networktables??)
    '''
        
    def process(self, frame):
        blur_output = self.blur(frame)
        print(blur_output)

    def blur(self, source):
        #using a median filter
        return cv2.medianBlur(frame, 9)
    
    def hsv_threshold(self, source):
        #current exposure setting on axis camera: 8
        hue = [120.0, 179.0]
        sat = [0, 255.0]
        val = [0, 255.0]

        out = cv2.cvtColor(source, cv2.COLOR_BGR2HSV)
        return cv2.inRange(source, (hue[0], sat[0], val[0]), (hue[1], sat[1], val[1]))

    def find_contours(source, external_only):
        if(external_only):
            mode = cv2.RETR_EXTERNAL
        else:
            mode = cv2.RETR_LIST
        method = cv2.CHAIN_APPROX_SIMPLE
        im2, contours, hierarchy = cv2.findContours(source, mode=mode, method=method)
        cv2.imshow('contours', im2)
        cv2.waitKey(0)
        #when the garbage collector comes for you, there is no hope
        cv2.destroyAllWindows()
        return contours

    
    
