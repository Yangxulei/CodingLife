# 颜色映射
def rgb(red, green, blue):
    return 16 + (red * 36) + (green * 6) + blue

# 设置输出样式
def set_style(fg=None, bg=None, bold=None):
    # 将参数设置为空 end='' 消除自动换行
    print(_set_style(fg, bg, bold), end='')

# 实现设置输出样式
def _set_style(fg=None, bg=None, bold=''):
    result = ''
    if fg:
        result += '\x1b[38;5;%dm' % fg
    if bg:
        result += '\x1b[48;5;%dm' % bg
    if bold:
        result += '\x1b[1m'
    return result

# 重置颜色
def reset_color():
    print(_reset_color(), end='')

# 实现重置颜色
def _reset_color():
    return '\x1b[0m'

# 打印字符
def print_color(*args, **kwargs):
    fg = kwargs.pop('fg', None)
    bg = kwargs.pop('bg', None)
    bold = kwargs.pop('bold', None)
    set_style(fg, bg, bold)
    print(*args, **kwargs)
    reset_color()