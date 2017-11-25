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
k = cv2.waitKey(0)


if k == 27: 			# wait for ESC key to exit
	cv2.destroyAllWindows()
elif k == ord('s'):		# wait for 's' to save and exit
	cv2.imwrite('grayedCounter.png', img)
	cv2.destroyAllWindows()


'''
digits = [];
digits.clear();

# convert to gray
cvtColor(_img, _imgGray, CV_BGR2GRAY);

# initial rotation to get the digits up --------------muhim emes manga
rotate(_config.getRotationDegrees());

# detect and correct remaining skew (+- 30 deg)
float skew_deg = detectSkew();
rotate(skew_deg);

# find and isolate counter digits
findCounterDigits();
'''