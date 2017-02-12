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
NetworkTables.initialize(server='10.17.11.76')

#create the field to talk to on the network table
class NTClient(object):
    angle_difference = ntproperty('/Raspberry Pi/angle difference', 0)

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
x = True
while x:
    print("while loop entered")
    img = get_image()
    print("image gotten")
    center_point = [160, 120]
    current_point = pipeline.process(img)
    #negative means turn left, positive means turn right
    pixel_difference = center_point[0] - current_point[0]  
    #4.7761 pixels per degree
    angle_difference = (float)(pixel_difference) / 4.7761
    n.angle_difference = angle_difference
    print(n.angle_difference)
#    x = False
