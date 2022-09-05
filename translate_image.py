import numpy as np
import imageio
import sys
import os
import math
import matplotlib.pyplot as plt
from PIL import Image
import blessed
import colorsys
from blessed import Terminal


#print(new)
def splitup(img,pixSize):
	new = []
	for j in range(int(img.shape[0]/pixSize)):
		new.append([])
		for i in range(int(img.shape[1]/pixSize)):
			new[-1].append([])
	for i in range(img.shape[1]):
		for j in range(img.shape[0]):
			blocki = int(i/pixSize)-1
			blockj = int(j/pixSize)-1
			new[blockj][blocki].append(img[j,i])
	return np.array(new)

def averageout(img):
	img1 = np.array(img)
	for i in range(img.shape[1]):
		for j in range(img.shape[0]):
			img[j][i]=np.mean(img1[j][i],axis=0)

	return img

#new = np.ones(new1.shape)
def blowup(img,pixSize,new_size):
	blowup = np.zeros((new_size))
	for i in range(blowup.shape[1]):
		for j in range(blowup.shape[0]):
			blowup[j][i] = img[j][i]

	return blowup

def display(filename,term):


	print(term.white_on_black(""))

	img = Image.open(filename)
	img = np.array(img)
	old_shape  = img.shape

	pixSize = int(img.shape[1]/term.width)
	print(pixSize)

	img = averageout(splitup(img,pixSize))
	print(img.shape[0])
	print(img.shape[1])

	#img = blowup(img,pixSize,(img.shape[0],img.shape[1],3))
	img = blowup(img,pixSize,(term.height-8,term.width,3))
	#img = blowup(img,pixSize,old_shape)
	print(img.shape)

	img = np.array(img,dtype=np.uint8)
	fig = plt.figure()
	plt.imshow(img)
	i = Image.fromarray(img,mode="RGB")
	#i.show()
	#quit()
	print(img.shape)
	#Terminal().on_color_rgb(*tuple((90,10,100)))
	for i in range(img.shape[0]):
		line = ''
		for j in range(img.shape[1]):
			#with Terminal().location(y=j,x=i):
			line += term.on_color_rgb(int(img[i,j,0]),int(img[i,j,1]),int(img[i,j,2]))+' '
		print(line)
