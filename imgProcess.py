#!/usr/bin/python3

import numpy as np
import cv2
from scipy import ndimage

img = cv2.imread("counter.png");
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,200,250,apertureSize = 3)
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
'''
def rotate(rotateDegree):
	rows,cols = edges.shape
	M = cv2.getRotationMatrix2D((cols/2,rows/2),rotateDegree,1)

	dst = cv2.warpAffine(edges,M,(cols,rows))

def rotate(image, angle):
	image_center = tuple(np.array(image.shape)/2)
	rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1)
	result = cv2.warpAffine(image, rot_mat, image.shape, flag=cv2.INTER_LINEAR)
	return result
'''
skew_deg = detectSkew()
#rotate(img,skew_deg)
# rotate the image in order to read the number correctly 
rotated = ndimage.rotate(img, skew_deg)
cv2.imshow("rotated", rotated)

cv2.imshow("rotatedEdge.png",edges)

#cv2.namedWindow('counter', cv2.WINDOW_NORMAL)
cv2.imshow('counter', img)


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
		cv2.rectangle(rotated, (X,Y),(X+W,Y+H),(0,255,0),2)
		print(type(bound))
		print(bound)
#print(len(boundingBoxes) )
#print( len(filteredContours))

cv2.imshow("rotaedREC.png",	rotated)

#-----------------------findAlignedBoxes --------------------------------------------

def findAlignedBoxes(boundBoxes):
	result = [];
	result.append(boundBoxes[0])
	for i in range(len(boundBoxes)):
		boundBefore = boundBoxes[i]
		[x,y,w,h] = boundBefore
		if(boundBefore != boundBoxes[len(boundBoxes)-1]):
			boundAfter = boundBoxes[i+1]
			[x1,y1,w1,h1] =boundAfter
		if(abs(y - y1) < digitYAlighment and abs(h - h1) < 5 ):
			if(boundBefore != boundBoxes[len(boundBoxes)-1]):
				result.append(boundAfter)
	return result;

alignedBoundBoxes = ((),)

for i in range(len(boundingBoxes)):
	temps = findAlignedBoxes(boundingBoxes);
	if (len(temps) > len(alignedBoundBoxes)):
		alignedBoundBoxes = temps

for i in range(len(alignedBoundBoxes)):
	print(type(alignedBoundBoxes[i]))
	print(alignedBoundBoxes[i])
	[xF,yF,wF,hF] = alignedBoundBoxes[i]
	cv2.rectangle(rotated, (xF,yF),(xF+wF,yF+hF),(0,0,255),2)
cv2.imshow("rotaedRECFilter.png",	rotated)

# sort it left to right 


cv2.imshow('edgesAffined.png', edgesAffined)

k = cv2.waitKey(0)
if k == 27: 			# wait for ESC key to exit
	cv2.destroyAllWindows()
elif k == ord('s'):		# wait for 's' to save and exit
	cv2.imwrite('grayedCounter.png', img)
	cv2.imwrite('rotatedimg.png', rotated)
	cv2.destroyAllWindows()


