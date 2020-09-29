---
layout: post
title:  机器学习简介
date:   2020-09-09 00:01:01 +0300
image:  2020-09-09-heritage.jpg
tags:   [MachineLearning]
---

### 机器学习的目标

机器学习是实现人工智能的手段，其主要研究内容是如何利用数据或经验进行学习，改善具体算法的性能

* 多领域交叉，涉及概率论、统计学，算法复杂度理论等多门学科
* 广泛应用于 网络搜索、垃圾邮件过滤 、推荐 系统、广告投放、信用评价 、欺诈检测、股票交易 和医疗诊断等应用

### 机器学习分类

机器学习一般分为下面几种类别

* 监督学习（Supervised Learning）
* 无监督学习（Unsupervised Learning）
* 强化学习（ Reinforcement Learning ，增强学习）
* 半监督学习（ Semi supervised Learning）
* 深度学习 (Deep）

### Python Scikit learn

* http://scikitlearn.org/stable/
* Machine Leaning in Python
* 一组简单有效的工具集
* 依赖 Python 的 NumPy SciPy 和 matplotlib 库
* 开源、可复用

### Scikit learn 常用函数

|                           | 应用(Applications)   | 算法(Algorithm) |
| ------------------------- | -------------------- | --------------- |
| 分类(Classification)      | 异常检测、图像识别等 | KNN、SVM        |
| 聚类(Clustering)          | 图像分割、群体划分等 | K-Means、谱聚类 |
| 回归(Regression)          | 价格预测、趋势预测等 | 线性回归、SVR   |
| 降维(Dimension Reduction) | 可视化               | PCA、NMF        |

### 相关书籍及课程推荐

http:// t.cn/RwUWKMS

http:// t.cn/RqRNasR

http:// t.cn/RIAfRUt

## sklearn库的安装

### sklearn库的简介

sklearn是scikit learn的简称，是一个基于 Python 的第三方模块。
sklearn 库集成了一些常用的机器学习方法，在进行机器学习任务时，并不需要实现算法，只需要简单的调用 sklearn 库中提供的模块就能完成大多数的机器学习任务。sklearn库是在Numpy 、 Scipy和matplotlib的基础上开发而成的，因此在介绍 sklearn 的安装前，需要先安装这些依赖库。

* Numpy（Numerical Python 的缩写）是一个开源的 Python 科学计算库。在Python中虽然提供了list容器和 array模块，但这些结构并不适合于进行数值计算，因此需要借助于Numpy库创建常用的数据结构（如：多维数组，矩阵等）以及进行常用的科学计算（如：矩阵运算）。
* Scipy库是sklearn库的基础，它是基于Numpy的一个集成了多种数学算法和函数的Python模块。它的不同子模块有不同的应用，如：积分、插值、优化和信号处理等 。
* matplotlib是基于Numpy的一套Python工具包，它提供了大量的数据绘图工具，主要用于绘制一些统计图形，将大量的数据转换成更加容易被接受的图表。（注意要先安装 numpy 再安装 matplotlib 库

### 安装包的下载

下载地址：http://www.lfd.uci.edu/~gohlke/pythonlibs（官方下载链接）

### 安装顺序

安装顺序如下：

* Numpy库
* Scipy库
* matplotlib库
* sklearn库

## sklearn库中的标准数据集及基本功能

### sklearn库中的标准数据集

数据集总览

| 数据集名称             | 调用方式               | 适用算法   | 数据规模     |
| ---------------------- | ---------------------- | ---------- | ------------ |
| 波士顿房价数据集       | load_boston()          | 回归       | 506*13       |
| 鸢尾花数据集           | load_iris()            | 分类       | 150*4        |
| 糖尿病数据集           | load_diabetes()        | 回归       | 442*10       |
| 手写数字数据集         | load_digits()          | 分类       | 5620*64      |
| Olivetti脸部图像数据集 | fetch_olivetti_faces() | 降维       | 400 * 64*64  |
| 新闻分类数据集         | fetch_20newsgroups()   | 分类       | -            |
| 带标签的人脸数据集     | fetch_lfw_people()     | 分类；降维 | -            |
| 路透设新闻语料数据集   | fetch_rcv()            | 分类       | 804414*47236 |

注：小数据集可以直接使用，大数据集要在调用时程序自动下载（一次即可）

#### 波士顿房价数据集

波士顿房价数据集包含506组数据，每条数据包含房屋以及房屋周围的详细信息。其中包括城镇犯罪率、一氧化氮浓度、住宅平均房间数、到中心区域的加权距离以及自住房平均房价等。因此，波士顿房价数据集能够应用到回归问题上。

#### 波士顿房价数据集属性描述

* CRIM：城镇人均犯罪率 。
* ZN：住宅用地超过 25000 sq.ft . 的比例 。
* INDUS：城镇非零售商用土地的比例 。
* CHAS：查理斯河空变量（如果边界是河流，则为 1 ；否则为 0
* NOX：一氧化氮浓度 。
* RM：住宅平均房间数 。
* AGE：1940 年之前建成的自用房屋比例 。
* DIS：到波士顿五个中心区域的加权距离 。
* RAD：辐射性公路的接近指数 。
* TAX：每 10000 美元的全值财产税率 。
* PTRATIO：城镇师生比例 。
* B：1000 Bk 0.63 ））^ 2 ，其中 Bk 指代城镇中黑人的比例 。
* LSTAT：人口中地位低下者的比例 。
* MEDV：自住房的平均房价，以千美元计。

#### 波士顿房价数据集

使用sklearn.datasets.load_boston 即可加载相关数据集其重要参数为：

* return_X_y 表示是否返回 target （即价格），默认为 False只返回 data （即属性）。

#### 波士顿房价数据集加载示例

##### 示例1

```assembly
from sklearn.datasets import load_boston
boston = load_boston()
print(boston.data.shape)
```

(506,13)

##### 示例2

```assembly
from sklearn.datasets import load_boston
data,target = load_boston(return_X_y=True)
print(data.shape)
print(target.shape)
```

(506,13)

(506)

#### 鸢尾花数据集

鸢尾花数据集采集的是鸢尾花的测量数据以及其所属的类别。测量数据包括：萼片长度、萼片、宽度、花瓣长度、花瓣宽度。类别共分为三类：Iris Setosa,Iris Versicolour,Iris Virginica 。该数据集可用于多分类问题。

使用sklearn.datasets.load_iris 即可加载相关数据集其参数有：

* return_X_y 若为 True ，则以 data, target ）形式返回数据；默认为 False ，表示以字典形式返回数据全部信息（包括data 和 target ）。

##### 加载示例

```assembly
from sklearn.datasets import load_iris
iris = load_iris()
print(iris.data.shape)
print(iris.target.shape)
list(iris.target_names)
```

(150,4)

(150, )

['setosa','versicolor','virginica']

#### 手写数字数据集

手写数字数据集包括 1797 个0\~9的手写数字数据，每个数字由8*8大小的矩阵构成，矩阵中值的范围是0\~16 ，代表颜色的深度。

使用sklearn.datasets load_digits 即可加载相关数据集其参数包括：

* return_X_y :若为 True ，则以 data, target ）形式返回数据；默认为 False ，表示以字典形式返回数据全部信息（包括 data 和 target)
* n_class ：表示返回数据的类别数，如 n_class=5, 则返回 0 到 4 的数据样本。

##### 示例：

```assembly
from sklearn.datasets import load_digits
digits = load_digits()
print(digits.data.shape)
>>(1797,64)
print(digits.target.shape)
>>(1797, )
print(digits.images.shape)
>>(1797,8,8)
import matplotlib.pyplot as plt
plt.matshow(digits.images[0])
plt.show()
```

### sklearn库的基本功能

sklearn 库的共分为 6 大部分，分别用于完成分类任务、回归任务、聚类任务、降维任务、 模型选择以及数据的预处理 。

* #### 分类任务

  | 分类模型   | 加载模块                     |
  | ---------- | ---------------------------- |
  | 最近邻算法 | neighbors.NearesNeighbors    |
  | 支持向量机 | svm.SVC                      |
  | 朴素贝叶斯 | naive_bayes.GaussianNB       |
  | 决策树     | tree.DecisionTreeClassifier  |
  | 集成方法   | ensemble.BaggingClassifier   |
  | 神经网络   | neural_network.MLPClassifier |

* 回归任务

  | 回归模型   | 加载模块                        |
  | ---------- | ------------------------------- |
  | 岭回归     | linear_model.Ridge              |
  | Lasso回归  | linear_model.Lass0              |
  | 弹性回归   | linear_model.ElasticNet         |
  | 最小角回归 | linear_model.Lars               |
  | 贝叶斯回归 | linear_model.BayesianRidge      |
  | 逻辑回归   | linear_model.LogisticRegression |
  | 多项式回归 | preprocessing.PolynomiaFeatures |

* 聚类任务

  | 聚类方法 | 加载模块                        |
  | -------- | ------------------------------- |
  | K-means  | cluster.kMeans                  |
  | Ap聚类   | cluster.AffinityPropagation     |
  | 均值漂移 | cluster.MeanShift               |
  | 层次聚类 | cluster.AgglomerativeClustering |
  | DBSCAN   | cluster.DBSCAN                  |
  | BIRCH    | cluster.Birch                   |
  | 谱聚类   | cluster.SpectralClustering      |

* 降维任务

  | 降维任务     | 加载模块                                |
  | ------------ | --------------------------------------- |
  | 主成分分析   | decomposition.PCA                       |
  | 截断SVD和LSA | decomposition.TruncatedSVD              |
  | 字典学习     | decomposition.SparseCoder               |
  | 因子分析     | decomposition.FactorAnalysis            |
  | 独立成分分析 | decomposition.FastICA                   |
  | 非负矩阵分解 | decomposition.NMF                       |
  | LDA          | decomposition.LatentDirichletAllocation |