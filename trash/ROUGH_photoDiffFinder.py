from PIL import Image, ImageOps, ImageChops
from numpy.ctypeslib import ndpointer

import faulthandler
import numpy as np
import ctypes as ct
import pyautogui 
import os
import cv2 as cv

import random

import sys # only for this demonstration to take cmdline args
IMAGE1 = sys.argv[1]
IMAGE2 = sys.argv[2]

faulthandler.enable()
bits_per_pixel = 8

class BoundingBox:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.pixels = [] # empty initially
	
	def fill(self, sourceImage):
		for currY in range(self.y, self.y + self.height):
			self.pixels.append([])
			for currX in range(self.x, self.x + self.width):
				self.pixels[currY - self.y].append(sourceImage.getpixel((currX,currY)))

def openBoundingBoxes(boundingBoxArray, bpp=None):
	global bits_per_pixel

	if bpp is None:
		bpp = bits_per_pixel
	elif bpp != bits_per_pixel:
		#bcmtest.change_bits_per_pixel(bpp)
		bits_per_pixel = bpp
	
	count = 0
	for boundingBox in boundingBoxArray:
		if boundingBox.width > 0 and boundingBox.height > 0:
			arr = np.array(boundingBox.pixels, dtype=np.uint8)

			count += 1
			newImage = Image.new("RGB",(boundingBox.width, boundingBox.height))
			yCount = -1
			xCount = -1
			for yArr in boundingBox.pixels:
				yCount += 1
				xCount = -1
				for xTup in yArr:
					xCount += 1
					newImage.putpixel((xCount, yCount), xTup)

			newImage.save("BB_{number}_at_{x}x{y}.png".format(number=count, x=boundingBox.x, y=boundingBox.y))
			"""bcmtest.draw_grayscale_array(
				boundingBox.width, boundingBox.height, bpp, arr
			)"""

# CHANGE IMAGE ADDRESSES TO COMPARE DIFFERENT IMAGES
oldScreenshot = Image.open(IMAGE1)
newScreenshot = Image.open(IMAGE2)
diff = ImageChops.difference(oldScreenshot, newScreenshot)

cvNS = np.array(newScreenshot)
cvDiff = np.array(diff)
cannyRes = cv.Canny(cvDiff, 0, 100)
contours, hierarchy = cv.findContours(cannyRes, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

contours = np.array(contours)

minX = minY = 1000000
maxX = maxY = lastXW = lastYH = 0
for contour in contours:
	x,y,w,h = cv.boundingRect(contour)
	if minX > x:
		minX = x
		cv.rectangle(cvDiff,(x,y),(x+w,y+h),(255,255,0),2)
	if minY > y:
		minY = y
		cv.rectangle(cvDiff,(x,y),(x+w,y+h),(255,255,255),2)
	if maxX < x:
		maxX = x
		lastXW = w
		print(x,y,w,h)
		cv.rectangle(cvDiff,(x,y),(x+w,y+h),(255,0,0),2)
	if maxY < y:
		maxY = y
		lastYH = h
		cv.rectangle(cvDiff,(x,y),(x+w,y+h),(0,0,255),2)
	#print(x,y,w,h)
	#cv.rectangle(cvDiff,(x,y),(x+w,y+h),(0,255,0),2)
	#cv.imwrite("cvDiff.png", cvDiff)
print(maxX-minX+lastXW, maxY-minY+lastYH)
cv.rectangle(cvDiff, (minX, minY), (maxX+lastXW, maxY+lastYH), (0, 255, 0), 2) #(maxX-minX+lastXW, maxY-minY+lastYH)
cv.imwrite("cvDiff3.png", cvDiff)

res = cvNS[minY:maxY+lastYH, minX:maxX+lastXW]
newImage = Image.fromarray(res)
newImage.save("test.png")
"""
for i in range(len(contours)):
	color = (255, 255, 255)
	cv.drawContours(drawing, contours, i, color, 2, cv.LINE_8, hierarchy, 0)
# Show in a window
cv.imshow('Contours', drawing)
"""
#diff.save("diff.png")