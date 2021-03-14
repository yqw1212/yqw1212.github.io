---
layout: post
title:  线性回归
date:   2020-10-12 00:01:01 +0300
image:  2020-10-12-typewriter.jpg
tags:   [MachineLearning]
---

## 线性回归

* 线性回归(Linear)是利用数理统计中回归分析，来确定两种或两种以上变量间相互依赖的定量关系的一种统计分析方法。
* 线性回归利用称为线性回归方程的最小平方函数对一个或多个自变量和因变量之间关系进行建模。这种函数是一个或多个称为回归系数的模型参数的线性组合。只有一个自变量的情况称为简单回归大于一个自变量情况的叫做多元回归。

## 线性回归的实际用途

* 如果目标是预测或者映射，线性回归可以用来对观测数据集的y和X的值拟合出一个预测模型。当完成这样一个模型以后，对于一个新增的X值，在没有给定与它相配对的y的情况下，可以用这个拟合过的模型预测出一个y值。
* 给定一个变量y和一些变量X1,⋯,𝑋𝑝,这些变量有可能与y相关，线性回归分析可以用来量化y与X𝑗之间相关性的强度，评估出与y不相关的X𝑗,并识别出哪些X𝑗的子集包含了关于y的冗余信息。

## 应用

### 背景

与房价密切相关的除了单位的房价，还有房屋的尺寸。我们可以根据已知的房屋成交价和房屋的尺寸进行线性回归，继而可以对已知房屋尺寸，而未知房屋成交价格的实例进行成交价格的预测。

### 目的

对房屋成交信息建立回归方程，并依据回归方程对房屋价格进行预测

### 技术路线

sklearn. linear_model.LinearRegression

### 实例数据

为了方便展示，成交信息只使用了房屋的面积以及对应的成交价格 。
其中：

* 房屋面积单位为平方英尺（ft2）房
* 屋成交价格单位为万

```assembly
1000,168
792,184
1260,197
1262,220
1240,228
1170,248
1230,305
1255,256
1194,240
1450,230
1481,202
1475,220
1482,232
1484,460
1512,320
1680,340
1620,240
1720,368
1800,280
4400,710
4212,552
3920,580
3212,585
3151,590
3100,560
2700,285
2612,292
2705,482
2570,462
2442,352
2387,440
2292,462
2308,325
2252,298
2202,352
2157,403
2140,308
4000,795
4200,765
3900,705
3544,420
2980,402
4355,762
3150,392
```

### 可行性分析

* 简单而直观的方式是通过数据的可视化直接观察房屋成交价格与房屋尺寸间是否存在线性关系。
* 对于本实验的数据来说，散点图就可以很好的将其在二维平面中进行可视化表示。

### 实验过程

```assembly
import matplotlib.pyplot as plt
from sklearn import linear_model
import numpy as np

datasets_X = []
datasets_Y = []
fr = open("prices.txt", "r")
lines = fr.readlines() # 一次读取整个文件
for line in lines:
    items = line.strip().split(",")
    datasets_X.append(int(items[0]))
    datasets_Y.append(int(items[1]))
length = len(datasets_X)
datasets_X = np.array(datasets_X).reshape([length, 1])
# 将datasets_X 转化为数组，并变为二维，以符合线性回归拟合函数输入参数要求。
datasets_Y = np.array(datasets_Y)

minX = min(datasets_X)
maxX = max(datasets_X)
X = np.arange(minX, maxX).reshape([-1, 1])
# 以数据datasets_X 的最大值和最小值为范围，建立等差数列，方便后续画图。

linear = linear_model.LinearRegression()
linear.fit(datasets_X, datasets_Y, sample_weight=None)
# sample_weight : 分配给各个样本的权重 数组 一般不需要使用，可省略。

# 调用sklearn.linear_model.LinearRegression() 所需参数：
# fit_intercept:布尔型参数，表示是否计算该模型截距。可选参数。
# normalize:布尔型参数，若为True，则X在回归前进行归一化。可选参数。默认值为 False 。
# copy_X:布尔型参数,若为True,则X将被复制；否则将被覆盖。可选参数。默认值为True 。
# n_jobs:整型参数，表示用于计算的作业数量；若为1，则用所有的CPU。可选参数。默认值为1。

# 查看回归方程系数
print("Coefficients:", linear.coef_)
# 查看回归方程截距
print("intercept:", linear.intercept_)

plt.scatter(datasets_X, datasets_Y, color="red")
plt.plot(X, linear.predict(X), color="blue")
plt.xlabel("Area")
plt.ylabel("Price")
plt.show()
```

show

![]({{site.baseurl}}/img/2020-10-12-show.jpg)

```assembly
Coefficients: [0.14839484]
intercept: 43.92337096187816
```

## 多项式回归

* 多项式回归(Polynomial Regression)是研究一个因变量与一个或多个自变量间多项式的回归分析方法。如果自变量只有一个时，称为一元多项式回归；如果自变量有多个时，称为多元多项式回归 。

* 一元 m 次多项式回归方程为
  $$
  y=b0+b1x+b2x^2+……+bmx^m
  $$

* 二元二次多项式回归方程为：
  $$
  y=b0+b1x1+b2x2+b3x1^2+b4x2^2+b5x1x2
  $$

* 在 一元回归分析中，如果依变量y与自变量x的关系为非线性的，但是又找不到适当的函数曲线来拟合，则可以采用一元多项式回归。
* 多项式回归的最大优点就是可以通过增加x的高次项对实测点进行逼近，直至满意为止。
* 事实上，多项式回归可以处理相当一类非线性问题，它在回归分析中占有重要的地位，因为任一函数都可以分段用多项式来逼近 。

## 多项式回归的应用

### 应用背景

我们在前面已经根据已知的房屋成交价和房屋的尺寸进行了线性回归，继而可以对已知房屋尺寸，而未知房屋成交价格的实例进行了成交价格的预测，但是在实际的应用中这样的拟合往往不够好，因此我们在此对该数据集进行多项式回归。

### 目的

对房屋成交信息建立多项式回归方程，并依据回归方程对房屋价格进行预测

### 技术路线

sklearn.preprocessing.PolynomialFeatures

### 实验过程

```assembly
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
# 导入线性模型和多项式特征构造模块

datasets_X = []
datasets_Y = []
fr = open("prices.txt", "r")
lines = fr.readlines()
for line in lines:
    items = line.strip().split(",")
    datasets_X.append(int(items[0]))
    datasets_Y.append(int(items[1]))
length = len(datasets_X)
datasets_X = np.array(datasets_X).reshape([length, 1])
datasets_Y = np.array(datasets_Y)

minX = min(datasets_X)
maxX = max(datasets_X)
X = np.arange(minX, maxX).reshape([-1, 1])

poly_reg = PolynomialFeatures(degree=2)
# degree=2表示建立datasets_X的二次多项式特征X_poly。
X_poly = poly_reg.fit_transform(datasets_X)

lin_reg_2 = linear_model.LinearRegression()
lin_reg_2.fit(X_poly, datasets_Y)
# 创建线性回归，使用线性模型学习X_poly和datasets_Y之间的映射关系（即参数）。

plt.scatter(datasets_X, datasets_Y, color="red")
plt.plot(X, lin_reg_2.predict(poly_reg.fit_transform(X)), color="blue")
plt.xlabel("Area")
plt.ylabel("Price")
plt.show()
```

![]({{site.baseurl}}/img/2020-10-12-poly.jpg)

## 岭回归

### 线性回归

对于一般地线性回归问题，参数的求解采用的是最小二乘法，其目标函数如下：
$$
argmin||Xw-y||^2
$$
参数w的求解，也可以使用如下矩阵方法进行
$$
w=(X^TX)^{-1}X^Ty
$$
对于矩阵X，若某些列线性相关性较大（即训练样本中某些属性线性相关），就会导致𝑿<sup>𝑻</sup>𝑿的值接近0，在计算 (𝑿<sup>𝑻</sup>𝑿)<sup>−𝟏</sup>时就会出现不稳定性

**结论：传统的基于最小二乘的线性回归法缺乏稳定性。**

### 岭回归

岭回归的优化目标：
$$
argmin||Xw-y||^2+α||w||^2
$$
对于矩阵求解方法为
$$
w=(X^TX+αI)^{-1}X^Ty
$$

* 岭回归(ridge regression)是一种专用于共线性数据分析的有偏估计回归方法
* 是一种改良的最小二乘估计法，对某些数据的拟合要强于最小二乘法 。

在sklearn库中，可以使用sklearn.linear_model.Ridge调用岭回归模型，其主要参数有：

* alpha：正则化因子，对应于损失函数中的𝜶
* fit_intercept：表示是否计算截距
* solver：设置计算参数的方法，可选参数‘auto’、’svd ’、‘sag ’等

### 交通流量预测实例

#### 数据介绍

数据为某路口的交通流量监测数据，记录全年小时级别的车流量。

#### 实验目的

根据已有的数据创建多项式特征，使用岭回归模型代替一般的线性模型，对车流量的信息进行多项式回归。

#### 数据实例

数据特征如下：

* HR：一天中的第几个小时(0~23)
* WEEK_DAY：一周中的第几天(0~6)
* DAY_OF_YEAR：一年中的第几天(1~365)
* WEEK_OF_YEAR：一年中的第几周(1~53)
* TRAFFIC_COUNT：交通流量

全部数据集包含2万条以上数据（21626）

#### 实例程序编写

```assembly
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures

data = pd.read_csv("data.csv", encoding="gbk")
data = np.array(data)

X = data[:, 1:5]
# X用于保存0~3维数据，即属性
y = data[:, 5]
# y用于保存第 4 维数据，即车流量
poly = PolynomialFeatures(6)
# 用于创建最高次数 6 次方的的多项式特征，多次试验后决定采用6次
X = poly.fit_transform(X)
# X为创建的多项式特征

train_set_X, test_set_X, train_set_y, test_set_y = train_test_split(X, y, test_size=0.3, random_state=0)
# test_size 表示测试集的比例,random_state 是随机数种子

clf = Ridge(alpha=1.0, fit_intercept=True) # 创建岭回归实例
clf.fit(train_set_X, train_set_y)
clf.score(test_set_X, test_set_y)
# 利用测试集计算回归曲线的拟合优度， clf.score 返回值为 0.7375
# 拟合优度，用于评价拟合好坏，最大为 1 ，无最小值，
# 当对所有输入都输出同一个值时，拟合优度为 0

start = 200
end = 300
y_pre = clf.predict(X) # 是调用 predict 函数的拟合值
time = np.arange(start, end)
plt.plot(time, y[start:end], "b", label="real")
plt.plot(time, y_pre[start:end], "r", label="predict")
# 展示真实数据（蓝色）以及拟合的曲线（红色）
plt.legend(loc="upper left") # 设置图例的位置
plt.show()
```

![]({{site.baseurl}}/img/2020-10-12-traffic.jpg)