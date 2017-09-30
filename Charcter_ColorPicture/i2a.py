import subprocess
from colors import *
from PIL import Image,ImageEnhance
from docopt import docopt


#FIEL ：图像文件路径名，这是必须项
#options ：可选项
#help ：获取帮助文档
#version ：获取程序版本号
#colors ：程序默认是转换成黑白字符画，通过该选项指定转换为彩色字符画
#constract ：调整图像对比度，默认值为 1.5 ，将影响最终转换效果
#bold ：指定使用粗体显示字符
#alt-chars ：指定使用另一套字符集进行映射


_version = '1.0'

#根据自己需要调整
_ASCII =  "@80GCLft1i;:,."
_ASCII_2 = "QORMNWBDHK@$U8&AOKYBZGPXgE4dVhgSqm6pF523yfwCJ#TnuLjz7oeat1[]!?I}*{srlcxvi)><\\)|\"/+=^;,;`_-`."

#i图像转彩色字符函数
def display_output(arguments):
	pass
def main():
	# 获取命令行参数解析之后的字典
	arguments = docopt(_doc_,version=_version_)
	# 若没有 FILE 参数，则打印帮助信息
	# 若有则进行转换工作
	if arguments['FILE']：
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
	#以字符的个数为单位，获取当前终端的行数和列数
	try:
	_HEIGHT, _WIDTH = map(int, subprocess.check_output('stty','size')).split())
	except:
		_HEIGHT,_WIDTH = 50,50
	
 # 按比例缩放图像
	aspect_ratio = im.size[0] / im.size[1]
	scaled_height = _WIDTH /aspect_ratio
	scaled_width = _HEIGHT * aspect_ratio * 2

# 计算调整之后的图像的宽高
	width = scaled_width
	heigth = scaled_height
	if scaled_width > _WIDTH:
		width = int(_WIDTH)
		heigth = int(scaled_height/2)
	elif scaled_height > _HEIGHT:
		width = int(scaled_width)
		heigth = int(_HEIGHT)

	# 将图像长宽转换为指定值
	# resample 参数可选，指定了在变换图像大小过程中的采样方式，为了保证转变之后的图像质量，我们采用 PIL.Image.ANTIALIAS 选项指定高质量的采样滤波器。
	im = im.resize((width,height),resample = Image.ANTIALIAS)

# 创建 PIL.ImageEnhance.Contrast 对象，用于调整对比度
	enhancer = ImageEnhance.Contrast(im)
	im = enhancer.enhance(float(arguments['--contrast']))

# 获取 im 的图像数据
# 返回值为 list 对象
	img = im.getdata()
# 将图像转换为灰阶图
	im = im.convert('L')
# 定义前景色与背景色
	bg = rgb(0,0,0)
	fg = rgb(5,5,5)
# 是否加粗显示字符
	bold = None
	if arguments['__bold']
		bold = True
	else:
		bold = False
# 用于计数当前在第几列打印
	row_len = 0
# 遍历每个像素点
	for (count,i) in enumerate(im.getdata()):
		# 将像素值映射到相应的字符
		ascii_char = _ASCII[int((i/255.0)*(len(_ASCII)-1))]

		# 若要求转成彩色字符
		if arguments['--colors']:
			# 颜色映射
			color = rgb(int((img[count][0]/255.0)*5),int((img[count][1]/255.0)*5),int((img[count][2]/255.0)*5))
			# 背景色设置为该颜色
			bg = color
			# 前景色置位黑色
			fg = rgb(0,0,0)
			# 打印字符
			print_color(ascii_char,end='',fg=fg,bg=bg,bold=bold)

		row_len += 1
		# 当列数等于终端宽的时候进行换行，并将 row_len 重新置 1
		if row_len = width:
			row_len = 0
			print('')


