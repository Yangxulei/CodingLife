#-*- coding: utf-8 -*-


from os import path
from wordcloud import WordCloud
import os
d = path.dirname(__file__)

font=os.path.join(os.path.dirname(__file__), "DroidSansFallbackFull.ttf")

# 读文本
#text = open(path.join(d, 'constitution.txt')).read()
text = open(u"santi.txt").read().decode('gbk')

# 创建词云图像
wordcloud = WordCloud(font_path=font).generate(text)



import matplotlib.pyplot as plt
plt.imshow(wordcloud)
plt.axis("off")

# 设置字体尺寸
wordcloud = WordCloud(font_path=font,max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

# 没有 matplotlib的方法
#image = wordcloud.to_image()
#image.show()
