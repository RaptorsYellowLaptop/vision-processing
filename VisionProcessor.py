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
        blur_output = self.blur(frame, 20)
        print(blur_output)

    def blur(self, frame, blur_radius):
        #using a median filter
 #       ksize = 2 * blur_radius + 1
        #returns a type of array
        return cv2.medianBlur(frame, 3)
    
