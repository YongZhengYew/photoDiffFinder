from PIL import Image, ImageOps, ImageChops
from numpy.ctypeslib import ndpointer

import faulthandler
import numpy as np
import ctypes as ct
import pyautogui 
import os
import cv2 as cv

import sys # only for this demonstration to take cmdline args
IMAGE1 = sys.argv[1]
IMAGE2 = sys.argv[2]
ABSPATH = sys.argv[3]

faulthandler.enable()
bits_per_pixel = 8

# CHANGE IMAGE ADDRESSES TO COMPARE DIFFERENT IMAGES
oldScreenshot = Image.open(IMAGE1)
newScreenshot = Image.open(IMAGE2)
diff = ImageChops.difference(oldScreenshot, newScreenshot)

cvNS = np.array(newScreenshot)
cvDiff = np.array(diff)
cannyRes = cv.Canny(cvDiff, 0, 100)
contours, hierarchy = cv.findContours(cannyRes, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

contours = np.array(contours, dtype=object)

minX = minY = 1000000
maxX = maxY = lastXW = lastYH = 0
for contour in contours:
	x,y,w,h = cv.boundingRect(contour)
	if minX > x:
		minX = x
	if minY > y:
		minY = y
	if maxX < x:
		maxX = x
		lastXW = w
	if maxY < y:
		maxY = y
		lastYH = h

res = cvNS[minY:maxY+lastYH, minX:maxX+lastXW]
newImage = Image.fromarray(res)


# RESULTS
# X coordinate: minX
# Y coordinate: minY
# array = res
#newImage.save("{absPath}/METHOD3/METHOD3_{x}x{y}.png".format(absPath=ABSPATH, x=minX, y=minY))