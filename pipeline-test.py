import numpy
import math
import cv2
#this is python 3 specific
import urllib.request
from enum import Enum
from VisionProcessor import VisionProcessor
from GripPipeline import GripPipeline
from networktables import NetworkTable

frame = cv2.VideoCapture('https://frc:frc@10.17.11.11/mjpg/video.mjpg')

if(frame == None):
    print("error: camera not found. check connection")
pipeline = GripPipeline()
#pipeline = VisionProcessor()

#frame = cv2.imread('download.jpg', 1)

print("pipeline created")

def get_image():
    ret, img_array = frame.read()
#    img_array = frame
    return img_array
x = True
while x:
    print("while loop entered")
    img = get_image()
    print("image gotten")
    pipeline.process(img)
#    print(img)
    print("processed")
    x = False
