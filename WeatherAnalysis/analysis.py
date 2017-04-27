# -*- coding: utf-8 -*-
import inline as inline
import numpy as np
import pandas as pd
import datetime
%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from sklearn.svm import SVR
from scipy.optimize import fsolve

df_ferrara = pd.read_csv('ferrara_270615.csv')
df_milano = pd.read_csv('milano_270615.csv')
df_mantova = pd.read_csv('mantova_270615.csv')
df_ravenna = pd.read_csv('ravenna_270615.csv')
df_torino = pd.read_csv('torino_270615.csv')
df_asti = pd.read_csv('asti_270615.csv')
df_bologna = pd.read_csv('bologna_270615.csv')
df_piacenza = pd.read_csv('piacenza_270615.csv')
df_cesena = pd.read_csv('cesena_270615.csv')
df_faenza = pd.read_csv('faenza_270615.csv')

# 取出我们要分析的温度和日期数据
y1 = df_milano['temp']
x1 = df_milano['day']

#把日期数据转换成 datetime 的格式
day_milano = [parser.parse(x) for x in x1]

# 调用 subplot 函数
fig, ax = plt.subplots()
plt.xticks(rotation=70)
hours = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(hours)
ax.plot(day_milano ,y1, 'r')
fig

# dist 是一个装城市距离海边距离的列表
dist = [df_ravenna['dist'][0],
	df_cesena['dist'][0],
	df_faenza['dist'][0],
	df_ferrara['dist'][0],
	df_bologna['dist'][0],
	df_mantova['dist'][0],
	df_piacenza['dist'][0],
	df_milano['dist'][0],
	df_asti['dist'][0],
	df_torino['dist'][0]
]

# temp_max 是一个存放每个城市最高温度的列表
temp_max = [df_ravenna['temp'].max(),
	df_cesena['temp'].max(),
	df_faenza['temp'].max(),
	df_ferrara['temp'].max(),
	df_bologna['temp'].max(),
	df_mantova['temp'].max(),
	df_piacenza['temp'].max(),
	df_milano['temp'].max(),
	df_asti['temp'].max(),
	df_torino['temp'].max()
]

# temp_min 是一个存放每个城市最低温度的列表
temp_min = [df_ravenna['temp'].min(),
	df_cesena['temp'].min(),
	df_faenza['temp'].min(),
	df_ferrara['temp'].min(),
	df_bologna['temp'].min(),
	df_mantova['temp'].min(),
	df_piacenza['temp'].min(),
	df_milano['temp'].min(),
	df_asti['temp'].min(),
	df_torino['temp'].min()
]

fig, ax = plt.subplots()
ax.plot(dist,temp_max,'ro')
fig


from sklearn.svm import SVR

# dist1是靠近海的城市集合，dist2是远离海洋的城市集合
dist1 = dist[0:5]
dist2 = dist[5:10]

# 改变列表的结构，dist1现在是5个列表的集合
# 之后我们会看到 numpy 中 reshape() 函数也有同样的作用
dist1 = [[x] for x in dist1]
dist2 = [[x] for x in dist2]

# temp_max1 是 dist1 中城市的对应最高温度
temp_max1 = temp_max[0:5]
# temp_max2 是 dist2 中城市的对应最高温度
temp_max2 = temp_max[5:10]

# 我们调用SVR函数，在参数中规定了使用线性的拟合函数
# 并且把 C 设为1000来尽量拟合数据（因为数据量不大不用担心过拟合）
svr_lin1 = SVR(kernel='linear', C=1e3)
svr_lin2 = SVR(kernel='linear', C=1e3)

# 加入数据，进行拟合（这一步可能会跑很久，大概10多分钟，休息一下:) ）
svr_lin1.fit(dist1, temp_max1)
svr_lin2.fit(dist2, temp_max2)

# 关于 reshape 函数请看代码后面的详细讨论
xp1 = np.arange(10,100,10).reshape((9,1))
xp2 = np.arange(50,400,50).reshape((7,1))
yp1 = svr_lin1.predict(xp1)
yp2 = svr_lin2.predict(xp2)

# 限制了 x 轴的取值范围
ax.set_xlim(0,400)

# 画出图像
ax.plot(xp1, yp1, c='b', label='Strong sea effect')
ax.plot(xp2, yp2, c='g', label='Light sea effect')
fig

# 定义了第一条拟合直线
def line1(x):
	a1 = svr_lin1.coef_[0][0]
	b1 = svr_lin1.intercept_[0]
	return a1*x + b1

# 定义了第二条拟合直线
def line2(x):
	a2 = svr_lin2.coef_[0][0]
	b2 = svr_lin2.intercept_[0]
	return a2*x + b2

# 定义了找到两条直线的交点的 x 坐标的函数
def findIntersection(fun1,fun2,x0):
	return fsolve(lambda x : fun1(x) - fun2(x),x0)


result = findIntersection(line1,line2,0.0)
print("[x,y] = [ %d , %d ]" % (result,line1(result)))

# x = [0,10,20, ..., 300]
x = np.linspace(0,300,31)
plt.plot(x,line1(x),x,line2(x),result,line1(result),'ro')

# axis 函数规定了 x 轴和 y 轴的取值范围
plt.axis((0,400,15,25))
plt.plot(dist,temp_min,'bo')
#plt.axis((0,400,15,25))
#plt.plot(dist,temp_min,'bo')

# 读取湿度数据
y1 = df_ravenna['humidity']
x1 = df_ravenna['day']
y2 = df_faenza['humidity']
x2 = df_faenza['day']
y3 = df_cesena['humidity']
x3 = df_cesena['day']
y4 = df_milano['humidity']
x4 = df_milano['day']
y5 = df_asti['humidity']
x5 = df_asti['day']
y6 = df_torino['humidity']
x6 = df_torino['day']

# 读取距离数据
dist = [df_ravenna['dist'][0],
    df_cesena['dist'][0],
    df_faenza['dist'][0],
    df_ferrara['dist'][0],
    df_bologna['dist'][0],
    df_mantova['dist'][0],
    df_piacenza['dist'][0],
    df_milano['dist'][0],
    df_asti['dist'][0],
    df_torino['dist'][0]
]

# 重新定义 fig 和 ax 变量
fig, ax = plt.subplots()
plt.xticks(rotation=70)

# 把时间从 string 类型转化为标准的 datetime 类型
day_ravenna = [parser.parse(x) for x in x1]
day_faenza = [parser.parse(x) for x in x2]
day_cesena = [parser.parse(x) for x in x3]
day_milano = [parser.parse(x) for x in x4]
day_asti = [parser.parse(x) for x in x5]
day_torino = [parser.parse(x) for x in x6]

# 规定时间的表示方式
hours = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(hours)

#表示在图上
ax.plot(day_ravenna,y1,'r',day_faenza,y2,'r',day_cesena,y3,'r')
ax.plot(day_milano,y4,'g',day_asti,y5,'g',day_torino,y6,'g')
fig


# 获取最大湿度数据
hum_max = [df_ravenna['humidity'].max(),
df_cesena['humidity'].max(),
df_faenza['humidity'].max(),
df_ferrara['humidity'].max(),
df_bologna['humidity'].max(),
df_mantova['humidity'].max(),
df_piacenza['humidity'].max(),
df_milano['humidity'].max(),
df_asti['humidity'].max(),
df_torino['humidity'].max()
]
plt.plot(dist,hum_max,'bo')



# 获取最小湿度
hum_min = [df_ravenna['humidity'].min(),
df_cesena['humidity'].min(),
df_faenza['humidity'].min(),
df_ferrara['humidity'].min(),
df_bologna['humidity'].min(),
df_mantova['humidity'].min(),
df_piacenza['humidity'].min(),
df_milano['humidity'].min(),
df_asti['humidity'].min(),
df_torino['humidity'].min()
]
plt.plot(dist,hum_min,'bo')

#风向频率玫瑰图
plt.plot(df_ravenna['wind_deg'],df_ravenna['wind_speed'],'ro')
hist, bins = np.histogram(df_ravenna['wind_deg'], 8, [0, 360])
#print(hist)
#print(bins)


def showRoseWind(values, city_name, max_value):
    N = 8

    # theta = [pi*1/4, pi*2/4, pi*3/4, ..., pi*2]
    theta = np.arange(0., 2 * np.pi, 2 * np.pi / N)
    radii = np.array(values)
    # 绘制极区图的坐标系
    plt.axes([0.025, 0.025, 0.95, 0.95], polar=True)

    # 列表中包含的是每一个扇区的 rgb 值，x越大，对应的color越接近蓝色
    colors = [(1 - x / max_value, 1 - x / max_value, 0.75) for x in radii]

    # 画出每个扇区
    plt.bar(theta, radii, width=(2 * np.pi / N), bottom=0.0, color=colors)

    # 设置极区图的标题
    plt.title(city_name, x=0.2, fontsize=20)


showRoseWind(hist, 'Ravenna', max(hist))
hist, bin = np.histogram(df_ferrara['wind_deg'],8,[0,360])
showRoseWind(hist,'Ferrara', max(hist))

def RoseWind_Speed(df_city):
    # degs = [45, 90, ..., 360]
	degs = np.arange(45,361,45)
	tmp = []
	for deg in degs:
	    # 获取 wind_deg 在指定范围的风速平均值数据
		tmp.append(df_city[(df_city['wind_deg']>(deg-46)) & (df_city['wind_deg']<deg)]
		['wind_speed'].mean())
	return np.array(tmp)

showRoseWind(RoseWind_Speed(df_ravenna),'Ravenna',max(hist))
