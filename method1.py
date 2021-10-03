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
ABSPATH = sys.argv[3]
SAVEFLAG = bool(int(sys.argv[4]))

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

			if SAVEFLAG:
				print("Saving from Method 1...")
				newImage.save("{absPath}/METHOD1/METHOD1_{number}_{x}x{y}.png".format(absPath=ABSPATH, number=count, x=boundingBox.x, y=boundingBox.y))
			"""bcmtest.draw_grayscale_array(
				boundingBox.width, boundingBox.height, bpp, arr
			)"""

# CHANGE IMAGE ADDRESSES TO COMPARE DIFFERENT IMAGES
oldScreenshot = Image.open(IMAGE1)
newScreenshot = Image.open(IMAGE2)
diff = ImageChops.difference(oldScreenshot, newScreenshot)
diff.save("diff.png")

columnHasSomething = False
xMin = diff.width
yMin = diff.height
xMax = yMax = 0
boundingBoxArray = []
countSince = 0
for x in range(diff.width):
	columnHasSomething = False
	for y in range(diff.height):
		currPixel = diff.getpixel((x,y))
		if currPixel != (0,0,0):
			columnHasSomething = True
			countSince = 0
		if columnHasSomething:
			if currPixel != (0,0,0):
				if xMin > x:
					xMin = x
				if xMax < x:
					xMax = x
				if yMin > y:
					yMin = y
				if yMax < y:
					yMax = y
	if columnHasSomething:
		if currPixel != (0,0,0):
			if xMin > x:
				xMin = x
			if xMax < x:
				xMax = x
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