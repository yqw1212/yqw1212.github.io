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
* 测试集：10,000个手写体图片及对应标签

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

#### 比较KNN的识别效果与多层感知机的识别效果

比较KNN的识别效果与多层感知机的识别效果。

KNN的输入为图片矩阵展开的一个1024维的向量。

##### KNN手写识别实体构建

```assembly
import numpy as np
from os import listdir
from sklearn import neighbors

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
    hwLabels = np.zeros([numFiles]) # 用于存放对应的标签,与神经网络不同
    for i in range(numFiles):
        filePath = fileList[i]
        hwLabels[i] = int(filePath.split("_")[0])
        dataSet[i] = img2vector(path + "/" + filePath)
    return dataSet, hwLabels

train_dataSet, train_hwLabels = readDataSet("D:/文档/新建文件夹 (2)/mach/trainingDigits")

knn = neighbors.KNeighborsRegressor(algorithm="kd_tree", n_neighbors=3)
knn.fit(train_dataSet, train_hwLabels)

dataSet, hwLabels = readDataSet("D:/文档/新建文件夹 (2)/mach/testDigits")

res = knn.predict(dataSet)
err_num = np.sum(res != hwLabels)
num = len(dataSet)
print("Total num:", num, ", Wrong num:", err_num, ", Wrong rate:", err_num/float(num))

```

实验效果

| 邻居数量 | 1      | 3      | 5      | 7      |
| -------- | ------ | ------ | ------ | ------ |
| 错误数量 | 12     | 10     | 19     | 24     |
| 正确率   | 0.9873 | 0.9894 | 0.9799 | 0.9746 |

K=3时正确率最高，当K>3时正确率开始下降，这是由于当样本为稀疏数据集时（本实例只有946个样本），其第 k个邻居点可能与测试点距离较远，因此投出了错误的一票进而影响了最终预测结果。

##### 对比实验——KNN分类器 vs. 多层感知机
我们取在上节对不同的隐藏层神经元个数、最大迭代次数、学习率进行的各个对比实验中准确率最高（H）与最差 （L）的MLP分类器来进行对比，其各个MLP的参数设置如下：

| MLP代号 | 隐藏层神经元个数 | 最大迭代次数 | 优化方法 | 初始学习率/学习率 |
| ------- | ---------------- | ------------ | -------- | ----------------- |
| MLP-YH  | 200              | 2000         | adam     | 0.0001            |
| MLP-YL  | 50               | 2000         | adam     | 0.0001            |
| MLP-DH  | 100              | 2000         | adam     | 0.0001            |
| MLP-DL  | 100              | 500          | adam     | 0.0001            |
| MLP-XH  | 100              | 2000         | sgd      | 0.1               |
| MLP-XL  | 100              | 2000         | sgd      | 0.0001            |

将效果最好的KNN分类器（K=3）和效果最差的KNN分类器（K=7）与各个MLP分类器作对比如下：

| 分类器   | MLP隐藏层神经元个数(MLP-Y) | MLP迭代次数(MLP-D) | MLP学习率(MLP-X) | KNN邻居数量 |
| -------- | -------------------------- | ------------------ | ---------------- | ----------- |
| 错误数量 | 37                         | 40                 | 35               | 10          |
| 正确率   | 0.9608                     | 0.9577             | 0.9630           | 0.9894      |
| 错误数量 | 47                         | 50                 | 222              | 24          |
| 正确率   | 0.9503                     | 0.9471             | 0.7653           | 0.9746      |

* KNN的准确率远高于MLP分类器，这是由于MLP在小数据集上容易过拟合的原因。
* MLP对于参数的调整比较敏感，若参数设置不合理，容易得到较差的分类效果，因此参数的设置对于MLP至关重要。

### RBF网络

1985年，Powell提出了多变量插值的径向基函数（RBF）方法。径向基函数是一个取值仅仅依赖于离原点距离的实值函数，也就是Φ(x)=Φ(‖x‖),或者还可以是到任意一点c的距离，c点称为中心点，也就是Φ(x，c)=Φ(‖x-c‖)。任意一个满足Φ(x)=Φ(‖x‖)特性的函数Φ都叫做径向基函数，标准的一般使用欧氏距离(也叫做欧式径向基函数)，尽管其他距离函数也是可以的。最常用的径向基函数是高斯核函数 ,形式为 k(||x-xc||)=exp{-||x-xc||<sup>2</sup>/(2*σ)<sup>2</sup>) } 其中x_c为核函数中心,σ为函数的宽度参数 , 控制了函数的径向作用范围。

RBF神将网络是一种三层神经网络，其包括输入层、隐层、输出层。从输入空间到隐层空间的变换是非线性的，而从隐层空间到输出层空间变换是线性的。

RBF网络的基本思想是：用RBF作为隐单元的“基”构成隐含层空间，这样就可以将输入矢量直接映射到隐空间，而不需要通过权连接。当RBF的中心点确定以后，这种映射关系也就确定了。而隐含层空间到输出空间的映射是线性的，即网络的输出是隐单元输出的线性加权和，此处的权即为网络可调参数。**其中，隐含层的作用是把向量从低维度的p映射到高维度的h，这样低维度线性不可分的情况到高维度就可以变得线性可分了，主要就是核函数的思想。**这样，网络由输入到输出的映射是非线性的，而网络输出对可调参数而言却又是线性的。网络的权就可由线性方程组直接解出，从而大大加快学习速度并避免局部极小问题。

#### RBF神经网络与BP神经网络之间的区别

* 局部逼近与全局逼近

  ​        BP神经网络的隐节点采用输入模式与权向量的内积作为激活函数的自变量，而激活函数采用Sigmoid函数。各调参数对BP网络的输出具有同等地位的影响，因此BP神经网络是对非线性映射的**全局逼近**。

  ​		RBF神经网络的隐节点采用输入模式与中心向量的距离（如欧式距离）作为函数的自变量，并使用径向基函数（如Gaussian函数）作为激活函数。神经元的输入离径向基函数中心越远，神经元的激活程度就越低（高斯函数）。RBF网络的输出与部分调参数有关，譬如，一个wij值只影响一个yi的输出（参考上面第二章网络输出），RBF神经网络因此具有**“局部映射”**特性。
  
* 中间层数的区别

  ​		BP神经网络可以有多个隐含层，但是RBF只有一个隐含层。

* 训练速度的区别

  　　使用RBF的训练速度快，一方面是因为隐含层较少，另一方面，局部逼近可以简化计算量。对于一个输入x，只有部分神经元会有响应，其他的都近似为0，对应的w就不用调参了。

* Poggio和Girosi已经证明，RBF网络是连续函数的最佳逼近，而BP网络不是。

#### RBF神经网络与SVM的区别

SVM等如果使用核函数的技巧的话，不太适应于大样本和大的特征数的情况，因此提出了RBF。

另外，SVM中的高斯核函数可以看作与每一个输入点的距离，而RBF神经网络对输入点做了一个聚类。RBF神经网络用高斯核函数时,其数据中心C可以是训练样本中的抽样，此时与svm的高斯核函数是完全等价的，也可以是训练样本集的多个聚类中心，所以他们都是需要选择数据中心的，只不过SVM使用高斯核函数时，这里的数据中心都是训练样本本身而已。

#### 前馈网络、递归网络和反馈网络

​		前馈网络一般指前馈神经网络或前馈型神经网络。它是一种最简单的神经网络，各神经元分层排列。每个神经元只与前一层的神经元相连。接收前一层的输出，并输出给下一层，各层间没有反馈。包括：BP神经网络、RBF神经网络等。

　　递归神经网络（RNN）是两种人工神经网络的总称。一种是时间递归神经网络（recurrent neural network），又名循环神经网络，包括RNN、LSTM、GRU等；另一种是结构递归神经网络（recursive neural network）。

　　反馈网络(Recurrent Network)，又称自联想记忆网络，其目的是为了设计一个网络，储存一组平衡点，使得当给网络一组初始值时，网络通过自行运行而最终收敛到这个设计的平衡点上。包括CHNN、DHNN等。