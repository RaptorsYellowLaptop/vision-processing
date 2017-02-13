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
#        cv2.imshow('blur', blur_output)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()

        hsv_output = self.hsv_threshold(blur_output)
#        cv2.imshow('hsv threshold', hsv_output)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()

        contours = self.find_contours(hsv_output, False)

        filtered_contours = self.filter_contours(contours, blur_output)

        center_points = self.find_center(filtered_contours, blur_output)
        return center_points

    def blur(self, source):
        #using a median filter
        return cv2.medianBlur(source, 9) #magic!
    

    def hsv_threshold(self, source):
        #current exposure setting on axis camera: 8
        hue = [120.0, 150.0]
        sat = [0, 255.0]
        val = [0, 170.0]
        #convert to HSV colorspace
        out = cv2.cvtColor(source, cv2.COLOR_BGR2HSV)
        return cv2.inRange(source, (hue[0], sat[0], val[0]), (hue[1], sat[1], val[1]))


    def find_contours(self, source, external_only):
        if(external_only):
            mode = cv2.RETR_EXTERNAL
        else:
            mode = cv2.RETR_TREE #or LIST
        method = cv2.CHAIN_APPROX_SIMPLE
        im2, contours, hierarchy = cv2.findContours(source, mode=mode, method=method)
#        cv2.drawContours(source, contours, -1, (255, 0 , 0), 1)
#        cv2.imshow('contours', im2)
#        cv2.waitKey(0)
        #when the garbage collector comes for you, there is no hope
#        cv2.destroyAllWindows()
        return contours


    def filter_contours(self, input_contours, image_underlay):
        output = []
        min_solidity = 80
        max_solidity = 100
        min_ratio = 2.3
        max_ratio = 3.0
        for contour in input_contours:
            #(x, y) is the top left coordinate of the image
            x,y,w,h = cv2.boundingRect(contour)
            ratio = (float)(w) / h
#            print(ratio)
            if(ratio < min_ratio or ratio > max_ratio):
                continue
            area = cv2.contourArea(contour)
            hull = cv2.convexHull(contour)
            contour_area = cv2.contourArea(hull)
            if(contour_area > 0):
                solid = 100 * area / cv2.contourArea(hull)
#                print(solid)
                if (solid < min_solidity or solid > max_solidity):
                    continue
            else:
                continue
            output.append(contour)
#        cv2.drawContours(image_underlay, output, -1, (255, 0 , 0), 3)
#        cv2.imshow('contours', image_underlay)
#        cv2.waitKey(0)
        #when the garbage collector comes for you, there is no hope
#        cv2.destroyAllWindows()
        return output


    def find_center(self, filtered_contours, image_underlay):
        center_points = []
        largest_contour = [0, 0]
        for contour in filtered_contours:
            x,y,w,h = cv2.boundingRect(contour)
            center_width = (int)(x + (w / 2))
            center_height = (int)(y + (h / 2))
            coordinate = [center_width, center_height]
            i = 0
            for point in coordinate:
                if (point > largest_contour[i]):
                    if(i == 0):
                        i = i + 1
                        continue
                    else:
                        center_points = coordinate
                else:
                    break
#            cv2.circle(image_underlay, (center_width, center_height), 1, (255, 0, 0), -1)
#        cv2.imshow('centers', image_underlay)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
        return center_points
    
