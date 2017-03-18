import subprocess
from colors import *
from PIL import Image,ImageEnhance
from docopt import docopt

_version = '1.0'

_ASCII =  "@80GCLft1i;:,."
_ASCII_2 = "QORMNWBDHK@$U8&AOKYBZGPXgE4dVhgSqm6pF523yfwCJ#TnuLjz7oeat1[]!?I}*{srlcxvi)><\\)|\"/+=^;,;`_-`."

#image to color char function
def display_output(arguments):
	pass
def main():
	#
	arguments = docopt(_doc_,version=_version_)
	
	if arguments['FILE']
	   	display_output(arguments)
	else:	
		print(_doc_)
if _name_ == '_main_':
	main()

def display_output(arguments):
	global _ASCII
	if arguments['--alt-chars']:
		_ASCII = _ASCII_2
	try:
		#load images
		im = Image.open(arguments['FILE'])
	except:
		raise IOError('Unable to open the file')
	#color to RGBA
	im = im.convert('RGBA')
	#
	try:
	_HEIGHT, _WIDTH = map(int, subprocess.check_output('stty','size')).split())
	except:
		_HEIGHT,_WIDTH = 50,50
	
	#
	aspect_ratio = im.size[0] / im.size[1]
	scaled_height = _WIDTH /aspect_ratio
	scaled_width = _HEIGHT * aspect_ratio * 2
	
	#
	width = scaled_width
	heigth = scaled_height
	if scaled_width > _WIDTH:
		width = int(_WIDTH)
		heigth = int(scaled_height/2)
	elif scaled_height > _HEIGHT:
		width = int(scaled_width)
		heigth = int(_HEIGHT)
	
	im = im.resize((width,height),resample = Image.ANTIALIAS)
	
	enhancer = ImageEnhance.Contrast(im)
	im = enhancer.enhance(float(arguments['--contrast']))

	img = im.getdata()
	
	im = im.convert('L')

	bg = rgb(0,0,0)
	fg = rgb(5,5,5)
	
	bold = None
	if arguments['__bold']
		bold = True
	else:
		bold = False
	
	row_len = 0
	
	for (count,i) in enumerate(im.getdata()):
		
		ascii_char = _ASCII[int((i/255.0)*(len(_ASCII)-1))]
		if arguments['--colors']:
			color = rgb(int((img[count][0]/255.0)*5),int((img[count][1]/255.0)*5),int((img[count][2]/255.0)*5))
			bg = color
			fg = rgb(0,0,0)
		print_color(ascii_char,end='',fg=fg,bg=bg,bold=bold)
		row_len += 1

		if row_len = width:
			row_len = 0
			print('')


