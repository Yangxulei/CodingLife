#
def rgb(red,green,blue):
	return 16 + (red*36) + (green * 6) + blue

def set_style(fg=None,bg=None,bold=None):
	result = ''
	if fg:
		result += '\x1b[38;5;%dm' %fg
	if bg:
		result += '\x1b[48;5;%dm' % bg
	if bold:
		result += '\x1b[1m'
	return result

def _reset_color():
	return '\x1b[0m'

def print_color(*args,**kwargs):
	fg = kwargs.pop('fg',None)
	bg = kwargs.pop('bg',None)
	bold = kwargs.pop('bold',None)
	set_style(fg,bg,bold)
	print(*args,**kwargs)
	reset_color()


