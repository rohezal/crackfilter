#!/usr/bin/python
import math
from gimpfu import *

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

def lineFilter(img, layer):

	gimp.progress_init("Line filter...")

	pdb.gimp_image_undo_group_start(img)
	layer = img.active_layer

	width = layer.width
	height = layer.height

	for a in range(height):
		print("Line: " + str(a))
		gimp.progress_update(float(a) / float(height))            

		for b in range(width):
			#num_channels, pixel = pdb.gimp_drawable_get_pixel(layer, b, a)
			#pixel_value = (pixel[0]*0,)
			pixel_value = (getLeftAndRightPixels(layer, b,a,radius=2),)
			pdb.gimp_drawable_set_pixel(layer, b, a, 1, pixel_value)

        newLayer = gimp.Layer(img, "temp", width, height, layer.type, layer.opacity, layer.mode)
	img.add_layer(newLayer, 1)
	img.remove_layer(newLayer)
	pdb.gimp_displays_flush()
        
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
