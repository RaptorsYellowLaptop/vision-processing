#!/usr/bin/python3

import numpy
import math
import cv2
#this is python 3 specific
import urllib.request
from enum import Enum
from VisionProcessor import VisionProcessor
from GripPipeline import GripPipeline
from networktables import NetworkTables
import time
import logging
from networktables.util import ntproperty

#proper networktables setup
logging.basicConfig(level=logging.DEBUG)
connected = False
while(connected == False):
    try:
        NetworkTables.initialize(server='10.17.11.76')
        connected = True
    except:
        connected = False
            

#create the field to talk to on the network table
class NTClient(object):
    angle_difference = ntproperty('/Raspberry Pi/angle difference', 0)
    distance_from_target = ntproperty('/Raspberry Pi/distance from target', 0)
    counter = ntproperty('/Raspberry Pi/reliability counter', 0)

n = NTClient()

frame = cv2.VideoCapture('https://frc:frc@10.17.11.11/mjpg/video.mjpg')

if(frame == None):
    print("error: camera not found. check connection")
#pipeline = GripPipeline()
pipeline = VisionProcessor()


print("pipeline created")

def get_image():
    ret, img_array = frame.read()
#    cv2.imwrite("frame.jpg", img_array)
    return img_array

def find_distance(width, y):
    #distances are in inches
    KNOWN_WIDTH = 17.0
    KNOWN_DISTANCE = 132.0
    KNOWN_PIXELS = 26.0
    KNOWN_ALTITUDE = 50.0

    focal_length = (KNOWN_PIXELS * KNOWN_DISTANCE)/KNOWN_WIDTH
    hypotenuse = (KNOWN_WIDTH * focal_length)/width
#    distance = (KNOWN_WIDTH * focal_length)/width

    #0.2125 degrees per pixel vertical
    theta = ((0.2125) * (240 - y)) - 25 #magic!

    print("theta")
    print(theta)
    
    distance = KNOWN_ALTITUDE * (math.tan((math.pi / 2) - math.radians(theta)))
    
    return distance

    

    
x = True
while x:
    print("while loop entered")
    img = get_image()
#    cv2.imwrite("img.jpg", img)
    print("image gotten")
    center_point = [160, 120]
    try:
'''        file = open('/home/pi/python/output.txt', 'a') '''
        current_point, size, y = pipeline.process(img)
        #negative means turn left, positive means turn right
        pixel_difference = center_point[0] - current_point[0]
        #4.7761 pixels per degree
        angle_difference = (float)(pixel_difference) / 4.7761
        n.angle_difference = angle_difference     
        target_width = size[0]
        target_height = size[1]
        distance = find_distance(target_width, y)
        n.distance_from_target = distance
        n.counter += 1
'''        print("angle")
        file.write("angle: ")
        print(n.angle_difference)
        file.write(str(angle_difference))
        print(" distance: ")
        file.write("distance")
        print(distance)
        file.write(str(distance))
        file.write("\n")
        file.close() '''
    except UnboundLocalError:
        print(":(")
    except (TypeError, cv2.error) as e:
        print(":(")
    
#    x = False
