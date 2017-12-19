#!/usr/bin/python3

import numpy as np
import cv2
from PIL import Image
from scipy import ndimage
import pytesseract
import pymysql.cursors
import pymysql
from time import gmtime, strftime
import urllib.request, urllib.parse
import requests

img = cv2.imread("counter2.png");
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#edges = cv2.Canny(gray,200,250,apertureSize = 3)
edges = cv2.Canny(gray,100,200,apertureSize = 3)
lines = cv2.HoughLines(edges, 1, np.pi/180,140)

def drawLines(lines):
	for i in range(len(lines)):
		rho = lines[i][0]
		theta = lines[i][1]
		a = np.cos(theta) 
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 1000*(-b))
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))

		cv2.line(img,(x1,y1),(x2,y2),(0,0,255),1)
	cv2.imwrite('houghlines2.png',img)
cv2.imshow("gray.png", gray);
#detect the skew of the image by finding almost (+- 30 deg) horizontal lines
def detectSkew():
	edges = cv2.Canny(gray,200,250,apertureSize = 3)
	#find line
	lines = cv2.HoughLines(edges, 1, np.pi/180,140)

	# filter lines bu theta and compute average
	filteredLines = []
	theta_min = 60 * np.pi/180
	theta_max = 120 * np.pi/180
	theta_avr = 0
	theta_deg = 0

	for i in range(len(lines)):
		theta = lines[i][0][1];
		if(theta > theta_min and theta < theta_max):
			filteredLines.append(lines[i][0])
			theta_avr += theta
	if(len(filteredLines) > 0):
		theta_avr /= len(filteredLines)
		theta_deg = (theta_avr / np.pi*180) - 90;
		print("detectSkew: {}". format(theta_deg))
	else:
		print('failed to detect skiw !')
	drawLines(filteredLines)
	return theta_deg;

skew_deg = detectSkew()
#rotate(img,skew_deg)
# rotate the image in order to read the number correctly 
rotated = ndimage.rotate(img, skew_deg)
#cv2.imshow("rotated", rotated)

#cv2.imshow("rotatedEdge.png",edges)

#cv2.namedWindow('counter', cv2.WINDOW_NORMAL)
#cv2.imshow('counter', img)


# find Contours -----------------------
#canny() for edge of the rotaing image and clone it 
grayAffined = cv2.cvtColor(rotated,cv2.COLOR_BGR2GRAY)
edgesAffined = cv2.Canny(grayAffined,200,250,apertureSize = 3)
edgesAffinedCopy = edgesAffined.copy()

imgContours, npaContours, npaHierarchy = cv2.findContours(edgesAffinedCopy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#filter contours by size of bouding rectangles

digitMinHeight = 10;
digitMaxHeight = 190;
digitYAlighment = 10
boundingBoxes = []
filteredContours = []
for npaContour in npaContours:
	bound=cv2.boundingRect(npaContour)
	[X, Y, W, H]  = bound
	if(H > digitMinHeight and H < digitMaxHeight and W > 5 and W < H):
		boundingBoxes.append(bound)
		filteredContours.append(npaContour)
		#cv2.rectangle(rotated, (X,Y),(X+W,Y+H),(0,255,0),2)######################################################################
		#print(type(bound))
		#print(bound)
#print(len(boundingBoxes) )
#print( len(filteredContours))

#cv2.imshow("rotaedREC.png",	rotated)

#-----------------------findAlignedBoxes --------------------------------------------
def findAlignedBoxes(boundBoxes):
	result = [];
	for i in range(len(boundBoxes)):
		[x,y,w,h] =boundBoxes[i]
		print("i : ")
		print(boundBoxes[i])
		if(boundBoxes[i] != boundBoxes[-1]):
			n =i+1
			[x1,y1,w1,h1] =boundBoxes[n]
			if(abs(y - y1) < digitYAlighment and abs(h - h1) < 5  ):
				result.append(boundBoxes[i])
				result.append(boundBoxes[n])
				print(result)
	return result
			
sorted_by_Y = sorted(boundingBoxes, key=lambda tup: tup[1]);
print("sorted_by_Y : ")
print(sorted_by_Y)
alignedBoundBoxes = '' # ((),)

def split_alignedBoxes(tempsArray):
	sortedTemps = sorted(tempsArray, key=lambda tup: tup[1]);
	sumY = 0
	array = []
	for i in range(len(sortedTemps)):
		sumY += sortedTemps[i][1];
	print(sumY / float(len(sortedTemps)))
	for i in range(len(sortedTemps)):
		if ((sortedTemps[i][1] + sortedTemps[i+1][1])/float(2) >= sumY / float(len(sortedTemps))):
			return sortedTemps[0:i+1], sortedTemps[i+1:]		
		else:
			array.append(sortedTemps[i])
	return array
for i in range(len(sorted_by_Y)):
	temps = []
	#print('temps1')
	#print(temps)
	#print(npaHierarchy)
	temps = findAlignedBoxes(sorted_by_Y);
	#findAlignedBoxes(boundingBoxes,temps);
	print('temps2')
	print(temps)
	temps = list(set(temps))
	#if len(split_alignedBoxes(temps)>1): for i in len(split_alignedBoxes(temps)>1: 
	arrayMaybe = split_alignedBoxes(temps)
	print('arrays')
	print(len(arrayMaybe))
	#print(array2)
	tempsArray = []
	if (len(arrayMaybe)==1):
		tempsArray = arrayMaybe		
	else: 
		for i in range(len(arrayMaybe)):
			if len(tempsArray)<len(arrayMaybe[i]):
				tempsArray =  arrayMaybe[i]
	alignedBoundBoxes = tempsArray	
	#alignedBoundBoxes = arrayMaybe[0] if (len(arrayMaybe[0])>len(arrayMaybe[1])) else arrayMaybe[1]
	#if (len(temps) > len(alignedBoundBoxes)):
	#	alignedBoundBoxes = temps
#print('temps')
#print(temps)

print('alignedBoundBoxes')
print(alignedBoundBoxes)

# sort alignedBoundBoxes left to right 
sorted_by_X = sorted(alignedBoundBoxes, key=lambda tup: tup[0]);
print("sorted_by_X : ")
print(sorted_by_X)

testText = ''
# KNN nearest neighbors
for i in range(len(sorted_by_X)):
	#print(type(alignedBoundBoxes[i]))
	#print(alignedBoundBoxes[i])
	[xF,yF,wF,hF] = sorted_by_X[i]
	#cv2.rectangle(rotated, (xF,yF),(xF+wF,yF+hF),(0,0,255),2)###############################
	imgROI = rotated[yF: yF + hF, xF: xF + wF]  	#crop data from affined edges
	cv2.imwrite("image" + str(i)+ ".png",imgROI)
	im = Image.open("image" + str(i)+ ".png")
	gr = im.convert('L')
	bw = gr.point(lambda x: 0 if x<128 else 255, '1')
	im.save("imgeBW" + str(i) + ".png")
	#erosion
	imgErosion = cv2.imread("imgeBW" + str(i) + ".png",0)
	kernel = np.ones((4,3),np.uint8)
	erosion = cv2.erode(imgErosion,kernel,iterations = 1)
	cv2.imwrite("imageE" + str(i)+ ".png",erosion)
	im.load()
	#testText = pytesseract.image_to_string(im, config='outputbase digits')
	testText += str(pytesseract.image_to_string(Image.open("imageE" + str(i)+ ".png"), 
		config='-psm 10 -eom 3 -c tessedit_char_whitelist=0123456789'))
	#print(pytesseract.image_to_string(Image.open("imageE" + str(i)+ ".png"), 
			#config='-psm 10 -eom 3 -c tessedit_char_whitelist=0123456789'))
print("contuer : " + testText)
testText = int(testText)

cv2.imshow("rotaedRECFilterAF.png", rotated)
cv2.imwrite("rotaedRECFilterAF.png", rotated)

cv2.imshow('edgesAffined.png', edgesAffined)

# connect to database & insert data to it
f0 = "%Y%m%d%H%M%S"
f1 = '%Y-%m-%d %H:%M:%S'
now = strftime(f1,gmtime());

data = {'dataCaptureOCR':testText, 'timeCaptureOCR':now, 'idUtilisateur':4}
data = bytes( urllib.parse.urlencode( data ).encode() )
handler = urllib.request.urlopen( 'http://www.kwapp.eu/connect/insertOCR.php', data )
print( handler.read().decode( 'utf-8' ))

k = cv2.waitKey(0)
if k == 27: 			# wait for ESC key to exit
	cv2.destroyAllWindows()
elif k == ord('s'):		# wait for 's' to save and exit
	cv2.imwrite('grayedCounter.png', img)
	cv2.imwrite('rotatedimg.png', rotated)
	cv2.destroyAllWindows()


# qizil yishilda katek sizghan yerni uchiriwettim waxtinche
