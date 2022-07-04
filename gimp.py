#!/usr/bin/python
import math
import numpy as np

from pkgutil import get_data
from gimpfu import *

def createResultLayer(image,name,result):
	rlBytes=np.uint8(result).tobytes();
	rl=gimp.Layer(image,name,image.width,image.height,image.active_layer.type,100,NORMAL_MODE)
	region=rl.get_pixel_rgn(0, 0, rl.width,rl.height,True)
	region[:,:]=rlBytes
	image.add_layer(rl,0)
	gimp.displays_flush()

def channelData(layer):#convert gimp image to numpy
    region=layer.get_pixel_rgn(0, 0, layer.width,layer.height)
    pixChars=region[:,:] # Take whole layer
    bpp=region.bpp
    # return np.frombuffer(pixChars,dtype=np.uint8).reshape(len(pixChars)/bpp,bpp)
    return np.frombuffer(pixChars,dtype=np.uint8).reshape(layer.height,layer.width,bpp)

def getLeftAndRightPixels(layer, b,a,radius=2):

	width = layer.width
	height = layer.height
	average = 0

	if (b-radius < 0) or (b+radius+1 > width):
		return 0

	c, center_pixel = pdb.gimp_drawable_get_pixel(layer, b, a)

	if(center_pixel[0] < 2):
		return 0

	for index in range(b-radius, b+radius+1):
		num_channels, pixel = pdb.gimp_drawable_get_pixel(layer, index, a)
		average = average + pixel[0]

	average = average / (2*radius+1)
	return average

def getLineAverage(pixels, b,a, radius=2):

	#print(pixels.shape)
	height, width, bpp = pixels.shape

	

	average = 0

	if (b-radius < 0) or (b+radius+1 > width):
		return 0

	center_pixel = pixels[a][b][0]

	print(center_pixel)

	if(center_pixel < 2):
		return 0

	#end_flag = False

	#if(center_pixel >= 2):
	#	end_flag = True

	for index in range(b-radius, b+radius+1):
		pixel = pixels[a][index][0]
		average = average + pixel
		#if(end_flag):
		#	print(str(pixel) + "("+str(type(pixel)) +")" + ": " + str(average) )

	average = average / (2*radius+1)

	return average	

def lineFilter(img, layer):

	gimp.progress_init("Line filter...")

	pdb.gimp_image_undo_group_start(img)
	layer = img.active_layer

	width = layer.width
	height = layer.height

	region=layer.get_pixel_rgn(0, 0, width,width)
	pixels = channelData(layer)
	filtered_pixels = np.copy(pixels)
	
	#print(pixels.ndim)
	filtered_pixels.fill(0)

	for a in range(height):
		gimp.progress_update(float(a) / float(height))
		for b in range(width):
			filtered_pixels[a][b][0] = getLineAverage(pixels,b,a)
			#filtered_pixels[a][b] = pixels[a][b]

	createResultLayer(img,"Lines",filtered_pixels)

		
	# for a in range(height):
	# 	print("Line: " + str(a))
	# 	gimp.progress_update(float(a) / float(height))            

	# 	for b in range(width):
	# 		#num_channels, pixel = pdb.gimp_drawable_get_pixel(layer, b, a)
	# 		#pixel_value = (pixel[0]*0,)
	# 		pixel_value = (getLeftAndRightPixels(layer, b,a,radius=2),)
	# 		pdb.gimp_drawable_set_pixel(layer, b, a, 1, pixel_value)

    #     newLayer = gimp.Layer(img, "temp", width, height, layer.type, layer.opacity, layer.mode)
	# img.add_layer(newLayer, 1)
	# img.remove_layer(newLayer)
	# pdb.gimp_displays_flush()
        
	pdb.gimp_progress_end()
	pdb.gimp_image_undo_group_end(img)


register(
	"python_line_filter",
	"Make the specified layer look like it is printed on cloth",
	"Make the specified layer look like it is printed on cloth",
	"GITZ",
	"GITZ",
	"2022",
	"<Image>/Filters/Generic/Linefilter",
	"GRAY",
	[],
	[],
	lineFilter)

main()