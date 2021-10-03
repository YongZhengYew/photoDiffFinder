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
SAVEFLAG = bool(int(sys.argv[4]))

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
	res = cvNS[y:y+h, x:x+w]
	newImage = Image.fromarray(res)

	if SAVEFLAG:
		print("Saving from Method 3...")
		newImage.save("{absPath}/METHOD3/METHOD3_{x}x{y}.png".format(absPath=ABSPATH, x=x, y=y))

# RESULTS
# X coordinate: minX
# Y coordinate: minY
# array = res