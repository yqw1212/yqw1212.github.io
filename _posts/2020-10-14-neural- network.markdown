---
layout: post
title:  神经网络
date:   2020-10-14 00:01:01 +0300
image:  2020-09-16-sheet.jpg
tags:   [MachineLearning]
---

# 图像识别

图像识别（Image Recognition）是指利用计算机对图像进行处理、分析和理解，以识别各种不同模式的目标和对像的技术 。
图像识别的发展经历了三个阶段：文字识别、数字图像处理与识别、物体识别 。机器学习领域一般将此类识别问题转化为分类问题。

# 手写数字识别

数字手写体识别由于其有限的类别（0~9共10个数字）成为了相对简单的手写识别任务。DBRHD和MNIST是常用的两个数字手写识别数据集。

### MNIST数据集

MNIST的下载链接：http://yann.lecun.com/exdb/mnist。
MNIST是一个包含数字0~9的手写体图片数据集，图片已归一化为以手写数字为中心的28×28规格的图片。MNIST 由训练集与测试集两个部分组成，各部分规模如下：

* 训练集：60,000个手写体图片及对应标签
* 测试集： 10,000 个手写体图片及对应标签

MNIST 数据集中的每一个图片由28×28个像素点组成，每个像素点的值区间为0~255，0表示白色，255表示黑色。

### DBRHD数据集

DBRHD（Pen Based Recognition of Handwritten Digits Data Set）是UCI的机器学习中心提供的数字手写体数据库：https archive.ics.uci.edu/ml/datasets/Pen-Based+Recognition+of+Handwritten+Digits。
DBRHD数据集包含大量的数字0~9的手写体图片，这些图片来源于44位不同的人的手写数字，图片已归一化为以手写数字为中心的32×32规格的图片。DBRHD的训练集与测试集组成如下：

* 训练集：7,494个手写体图片及对应标签，来源于40位手写者
* 测试集：3,498个手写体图片及对应标签，来源于14位手写者

DBRHD数据集特点：

* 去掉了图片颜色等复杂因素，将手写体数字图片转化为训练数据为大小32×32的文本矩阵。
* 空白区域使用0代表，字迹区域使用1表示。

## “手写识别”实例

已有许多模型在MNIST或DBRHD数据集上进行了实验，有些模型对数据集进行了偏斜矫正，甚至在数据集上进行了人为的扭曲、偏移、缩放及失真等操作以获取更加多样性的样本，使得模型更具有泛化性。

常用于数字手写体的分类器：

* 线性分类器
* K最近邻分类器
* Boosted Stumps
* 非线性分类器
* SVM
* 多层感知器
* 卷积神经网络

## 任务介绍

手写数字识别是一个多分类问题，共有10个分类，每个手写数字图像的类别标签是 0~9 中的其中一个数。例如下面这三张图片的标签分别是0，1，2。

任务：利用sklearn来训练一个简单的全连接神经网络，即多层感知机（Multilayer perceptron MLP）用于识别数据集DBRHD的手写数字。

#### MLP的输入

DBRHD数据集的每个图片是一个由0或1组成的32*32的文本矩阵；
多层感知机的输入为图片矩阵展开的1\*1024个神经元 。

#### MLP的输出

MLP输出：one hot vectors
一个one-hot向量除了某一位的数字是1以外其余各维度数字都是0。
图片标签将表示成一个只有在第n维度（从0开始）数字为1的10维向量。比如，标签0将表示成1,0,0,0,0,0,0,0,0,0,0 。即MLP输出层具有10个神经元。

### MLP结构

MLP的输入与输出层，中间隐藏层的层数和神经元的个数设置都将影响该MLP模型的准确率。
在本实例中，我们只设置一层隐藏层，在后续实验中比较该隐藏层神经元个数为 50、100、200时的 MLP 效果。

### MLP手写识别实例构建

```assembly
import numpy as np
from os import listdir # listdir模块用于访问本地文件
from sklearn.neural_network import MLPClassifier


def img2vector(fileName):
    retMat = np.zeros([1024], int) # 定义返回的矩阵，大小为1*1024
    fr = open(fileName) # 打开包含32*32大小的数字文件
    lines = fr.readlines()
    for i in range(32):
        for j in range(32):
            retMat[i*32+j] = lines[i][j]
    return retMat


def readDataSet(path):
    fileList = listdir(path)
    numFiles = len(fileList)
    dataSet = np.zeros([numFiles, 1024], int)
    hwLabels = np.zeros([numFiles, 10]) # 用于存放对应的标签one-hot
    for i in range(numFiles):
        filePath = fileList[i]
        digit = int(filePath.split("_")[0])
        hwLabels[i][digit] = 1.0
        dataSet[i] = img2vector(path + "/" + filePath)
    return dataSet, hwLabels


train_dataSet, train_hwLabels = readDataSet("trainingDigits")
clf = MLPClassifier(hidden_layer_sizes=(50,), activation="logistic",
                    solver="adam", learning_rate_init=0.0001, max_iter=2000)
# 构建神经网络：设置网络的隐藏层数、各隐藏层神经元个数、激活函数、学习率、优化方法、最大迭代次数。
# 设置含 100 个神经元的隐藏层。
# hidden_layer_sizes存放的是一个元组，表示第i层隐藏层里神经元的个数
# 使用 logistic 激活函数和 adam 优化方法，并令初始学习率为0.0001
clf.fit(train_dataSet, train_hwLabels)
# fit 函数能够根据训练集及对应标签集自动设置多层感知机的输入与输出层的神经元个数。
# 例如train_dataSet为 n*1024 的矩阵，train_hwLabels为 n*10 的矩阵，
# 则fit 函数将 MLP 的输入层神经元个数设为 1024 ，输出层神经元个数为10

dataSet, hwLabels = readDataSet("testDigits")
res = clf.predict(dataSet)
err_num = 0 # 统计预测错误的数目
num = len(dataSet)
for i in range(num):
    # 若预测结果和真实结果全相同，则np.sum()==10
    if np.sum(res[i] == hwLabels[i]) < 10:
        err_num += 1
print("Total num:", num, ", Wrong num:", err_num, ", Wrong rate:", err_num/float(num))

```

### 实验效果

```assembly
Total num: 946 , Wrong num: 0 , Wrong rate: 0.0
```

#### 隐藏层神经元个数影响：

| 神经元个数 | 50     | 100    | 200    |
| ---------- | ------ | ------ | ------ |
| 错误数量   | 47     | 40     | 37     |
| 正确率     | 0.9503 | 0.9577 | 0.9608 |

* 随着隐藏层神经元个数的增加， MLP的正确率持上升趋势
* 大量的隐藏层神经元带来的计算负担与对结果的提升并不对等，因此，如何选取合适的隐藏神经元个数是一个值得探讨的问题。

#### 迭代次数影响分析:

我们设隐藏层神经元个数为100，初始学习率为0.0001，最大迭代次数分别为500、1000、1500、2000, 结果如下：

| 学习率   | 500    | 1000   | 1500   | 2000   |
| -------- | ------ | ------ | ------ | ------ |
| 错误数量 | 50     | 41     | 41     | 40     |
| 正确率   | 0.9471 | 0.9567 | 0.9567 | 0.9577 |

* 过小的迭代次数可能使得MLP早停，造成较低的正确率。
* 当最大迭代次数>1000时，正确率基本保持不变，这说明MLP在第1000迭代时已收敛，剩余的迭代次数不再进行。
* 一般设置较大的最大迭代次数来保证多层感知机能够收敛，达到较高的正确率。

#### 学习率影响分析：

改用随机梯度下降优化算法即将MLPclassifer的参数（solver='sgd'）,设隐藏层神经元个数为100，最大迭代次数为2000，学习率分别为0.1、0.01、0.001、0.0001，结果如下：

| 学习率   | 0.1    | 0.01   | 0.001  | 0.0001 |
| -------- | ------ | ------ | ------ | ------ |
| 错误数量 | 35     | 41     | 49     | 222    |
| 正确率   | 0.9630 | 0.9567 | 0.9482 | 0.7653 |

* 较小的学习率带来了更低的正确率，这是因为较小学习率无法在2000次迭代内完成收敛，而步长较大的学习率使得MLP在2000次迭代内快速收敛到最优解。因此，较小的学习率一般要配备较大的迭代次数以保证其收敛。