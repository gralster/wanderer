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
	imgout = np.zeros((img.shape[0],img.shape[1],3))
	for i in range(img.shape[1]):
		for j in range(img.shape[0]):
			imgout[j][i]=np.mean(img1[j][i],axis=0)

	return imgout

#new = np.ones(new1.shape)
def crop(img,pixSize,new_size):
	crop = np.zeros((new_size))
	#if len(img[1,1]) >3:
	#	img = np.delete(img,4,axis=0)
	for i in range(crop.shape[1]):
		for j in range(crop.shape[0]):
			crop[j][i] = img[j][i]
	return crop

def blowup(img,new_size):
	xscale = img.shape[1]/new_size[1]
	yscale = img.shape[0]/new_size[0]
	blowup = np.zeros((new_size))
	for i in range(blowup.shape[1]):
		for j in range(blowup.shape[0]):
			blowup[j][i] = img[int(j*yscale)][int(i*xscale)]
	return blowup
def display_fullscreen(filename,term):


	print(term.white_on_black(""))

	img = Image.open(filename)
	img = np.array(img)
	old_shape  = img.shape

	pixSize = int(img.shape[1]/term.width)
	print(pixSize)

	img = averageout(splitup(img,pixSize))
	print(img.shape[0])
	print(img.shape[1])

	#img = crop(img,pixSize,(img.shape[0],img.shape[1],3))
	img = crop(img,pixSize,(term.height-8,term.width,3))
	#img = crop(img,pixSize,old_shape)
	#print(img.shape)

	img = np.array(img,dtype=np.uint8)

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

def isnear(a,b,tolerance):
	diff = a-b
	if a-b < 0:
		diff = diff*-1
	if diff < tolerance:
		return True
	else:
		return False

def clear_bg(img,init_colour,fin_colour):
	r = init_colour[0]
	g = init_colour[1]
	b = init_colour[2]

	tolerance = 90

	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if(isnear(int(img[i,j,0]),r,tolerance) and isnear(int(img[i,j,1]),g,tolerance) and isnear(int(img[i,j,2]),b,tolerance)):
				img[i,j,0]=fin_colour[0]
				img[i,j,1]=fin_colour[1]
				img[i,j,2]=fin_colour[2]
	return img


def display_small(filename,term,width,bg=(255,255,255),pos=(0,0)):

	img = Image.open(filename)

	img = img.convert("RGB")

	img = np.array(img)

	old_shape  = img.shape
	pixSize = int(img.shape[1]/width)
	img = averageout(splitup(img,pixSize))
	img = np.array(img,dtype=np.uint8)

	tolerance = 90
	for i in range(img.shape[0]):
		line = ''
		for j in range(img.shape[1]):
			if(isnear(int(img[i,j,0]),bg[0],tolerance) and isnear(int(img[i,j,1]),bg[1],tolerance) and isnear(int(img[i,j,2]),bg[2],tolerance)):
				line += term.black(" ")
			else:
				line += term.on_color_rgb(int(img[i,j,0]),int(img[i,j,1]),int(img[i,j,2]))+' '
		with term.location(y=pos[0]+i,x=pos[1]):
			print(line)

def display_pix(filename,term,bg=(255,255,255),pos=(0,0),scaleup=1):

	img = Image.open(filename)
	img = img.convert("RGB")
	img = np.array(img)
	width = len(img)

	old_shape  = img.shape
	pixSize = 1
	#img = averageout(splitup(img,pixSize))
	if scaleup!=1:
		img = blowup(img,(img.shape[0]*scaleup,img.shape[1]*scaleup,3))
	img = np.array(img,dtype=np.uint8)

	#i = Image.fromarray(img,mode="RGB")
	#i.show()
	tolerance = 90
	for i in range(img.shape[0]):
		line = ''
		for j in range(img.shape[1]):
			if(isnear(int(img[i,j,0]),bg[0],tolerance) and isnear(int(img[i,j,1]),bg[1],tolerance) and isnear(int(img[i,j,2]),bg[2],tolerance)):
				line += term.white_on_black(" ")
			else:
				line += term.on_color_rgb(int(img[i,j,0]),int(img[i,j,1]),int(img[i,j,2]))+' '
		with term.location(y=pos[0]-int(img.shape[0]/2)+i,x=pos[1]-int(img.shape[1]/2)):
			print(line)
