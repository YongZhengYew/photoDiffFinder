from PIL import Image, ImageOps, ImageChops
from numpy.ctypeslib import ndpointer

import faulthandler
import numpy as np
import ctypes as ct
import pyautogui 
import os

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
#diff.save("diff.png")

rowHasSomething = False
xMin = diff.width
yMin = diff.height
xMax = yMax = 0
boundingBoxArray = []
countSince = 0
for y in range(diff.height):
	rowHasSomething = False
	for x in range(diff.width):
		currPixel = diff.getpixel((x,y))
		if currPixel != (0,0,0):
			rowHasSomething = True
			countSince = 0
		if rowHasSomething:
			if currPixel != (0,0,0):
				if xMin > x:
					xMin = x
				if xMax < x:
					xMax = x
				if yMin > y:
					yMin = y
				if yMax < y:
					yMax = y
	if rowHasSomething:
		if currPixel != (0,0,0):
			if yMin > y:
				yMin = y
			if yMax < y:
				yMax = y
	else:
		countSince += 1
		if countSince == 1:
			boundingBoxArray.append(BoundingBox(xMin, yMin, xMax-xMin, yMax-yMin))
			yMin = diff.height
			xMin = diff.width
			yMax = xMax = 0
		else:
			pass

for boundingBox in boundingBoxArray:
	boundingBox.fill(newScreenshot)

openBoundingBoxes(boundingBoxArray)