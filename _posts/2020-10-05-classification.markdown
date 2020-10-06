---
layout: post
title:  分类
date:   2020-10-05 00:01:01 +0300
image:  2020-10-05-girl.jpg
tags:   [MachineLearning]
---

# 人体运动状态预测实例分析

## 背景介绍

* 可穿戴式设备的流行，让我们可以更便利地使用传感器获取人体的各项数据，甚至生理数据。
* 当传感器采集到大量数据后，我们就可以通过对数据进行分析和建模，通过各项特征的数值进行用户状态的判断，根据用户所处的状态提供给用户更加精准、便利的服务。

## 数据介绍

我们现在收集了来自 A,B,C,D,E 5 位用户的可穿戴设备上的传感器数据，每位用户的数据集包含一个特征文件（a.feature）和一个标签文件（a.label ）。
特征文件中每一行对应一个时刻的所有传感器数值，标签文件中每行记录了和特征文件中对应时刻的标记过的用户姿态，两个文件的行数相同，相同行之间互相对应。

**特征文件的各项特征具体如下表所示**

| 1      | 2    | 3~15    | 16~28   | 29~41   |
| ------ | ---- | ------- | ------- | ------- |
| 时间戳 | 心率 | 传感器1 | 传感器2 | 传感器3 |

**在传感器1对应的13列数据特征中，包含：1项温度数据、3项一型三轴加速度数据、3项二型三轴加速度数据、3项三轴陀螺仪数据和3项三轴磁场数据。**

| 3    | 4~6            | 7~9            | 10~12      | 13~15    |
| ---- | -------------- | -------------- | ---------- | -------- |
| 温度 | 一型三轴加速度 | 二型三轴加速度 | 三轴陀螺仪 | 三轴磁场 |

* 人体的温度数据可以反映当前活动的剧烈程度，一般在静止状态时，体温趋于稳定在36.5度上下；当温度高于 37 度时，可能是进行短时间的剧烈运动，比如跑步和骑行。
* 在数据中有两个型号的加速度传感器，可以通过互相印证的方式，保证数据的完整性和准确性。通过加速度传感器对应的三个数值，可以知道空间中x、y、z三个轴上对应的加速度，而空间上的加速度和用户的姿态有密切的关系，比如用户向上起跳时， z 轴上的加速度会激增。
* 陀螺仪是角运动检测的常用仪器，可以判断出用户佩戴传感器时的身体角度是水平、倾斜还是垂直。直观地，通过这些数值都是推断姿态的重要指标。
* 磁场传感器可以检测用户周围的磁场强度和数值大小，这些数据可以帮助我们理解用户所处的环境。比如在一个办公场所，用户座位附近的磁场是大体上固定的，当磁场发生改变时，我们可以推断用户的位置和场景发生了变化。

### label

标签文件内容如图所示，每一行代表与特征文件中对应行的用户姿态类别。
总共有0~24共 25 种身体姿态，如：无活动状态，坐态、跑态等。标签文件作为训练集的标准参考准则，可以进行特征的监督学习。

## 任务介绍

* 假设现在出现了一个新用户，但我们只有传感器采集的数据，那么该如何得到这个新用户的姿态呢？
* 又或者对同一用户如果传感器采集了新的数据，怎么样根据新的数据判断当前用户处于什么样的姿态呢？

在明确这是一个分类问题的情况下，我们可以选定某种分类模型（或者说是算法），通过使用训练数据进行模型学习，然后对每个测试样本给出对应的分类结果。
机器学习的分类算法众多，在接下来的学习中我们将会详细介绍经典的分类算法，如：K近邻、决策树和朴素贝叶斯的原理和实现。

# 基本分类模型

## K近邻分类器 (KNN)

KNN：通过计算待分类数据点，与已有数据集中的所有数据点的距离。取距离最小的前K个点，**这K个实例的多数属于某个类**，根据“少数服从多数“的原则，就将这个数据点划分为出现次数最多的那个类别。

在sklearn 库中，可以使用 sklearn.neighbors.KNeighborsClassifier创建一个K近邻分类器，主要参数有：

* n_neighbors ：用于指定分类器中K的大小默认值为5，注意与kmeans的区别
* weights ：设置选中的K个点对分类结果影响的权重（默认值为平均权重“uniform”，可以选择“distance”代表越近的点权重越高或者传入自己编写的以距离为参数的权重计算函数）

它的主要参数还有：

* algorithm：设置用于计算临近点的方法，因为当数据量很大的情况下计算当前点和所有点的距离再选出最近的k各点，这个计算量是很费时的，所以（选项中有 ball_tree、kd_tree和brute，分别代表不同的寻找邻居的优化算法， 默认值为auto，根据训练数据自动选择）

### K近邻分类器的使用

创建一组数据X和它对应的标签y

```assembly
X = [[0],[1],[2],[3]]
y = [0,0,1,1]
```

使用import 语句导入 K 近邻分类器。

```assembly
from sklearn.neighbors import KNeighborsClassifier
```

参数n_neighbors设置为3，即使用最近的3个邻居作为分类的依据，其他参数保持默认值，并将创建好的实例赋给变量neigh 。

```assembly
neigh = KNeighborsClassifier(n_neighbors=3)
```

调用fit() 函数，将训练数据X和标签y送入分类器进行学习。

```assembly
neigh.fit(x,y)
```

调用predict() 函数，对未知分类样本[1.1]分类，可以直接并将需要分类的数据构造为数组形式作为参数传入，得到分类标签作为返回值。

```assembly
>>>print(neigh.predict([[1.1]]))
[0]
```

样例输出值是0，表示K近邻分类器通过计算样本[1.1]与训练数据的距离，取0,1,2这 3 个邻居作为依据，根据“投票法”最终将样本分为类别0。

### KNN的使用经验

在实际使用时，我们可以使用所有训练数据构成特征X和标签y，使用fit()函数进行训练。在正式分类时，通过一次性构造测试集或者一个一个输入样本的方式，得到样本对应的分类结果。有关K的取值

* 如果较大，相当于使用较大邻域中的训练实例进行预测，可以减小估计误差，但是距离较远的样本也会对预测起作用，导致预测错误。
* 相反地，如果K较小，相当于使用较小的邻域进行预测，如果邻居恰好是噪声点，会导致过拟合。
* 一般情况下，K会倾向选取较小的值，并使用交叉验证法选取最优K值。

----------------------------------------

## 决策树

决策树是一种树形结构的分类器，通过顺序询问分类点的属性决定分类点最终的类别。通常根据特征的信息增益或其他指标，构建一颗决策树。在分类时，只需要按照决策树中的结点依次进行判断，即可得到样本所属类别。
例如，根据一个构造好的分类决策树，一个无房产单身年收入55K的人的会被归入无法偿还信用卡这个类别。

在sklearn库中，可以使用 sklearn.tree.DecisionTreeClassifier创建一个决策树用于分类，其主要参数有：

* criterion：用于选择属性的准则，可以传入”gini ”代表基尼系数，或者“entropy”代表信息增益。
* max_features：表示在决策树结点进行分裂时，从多少个特征中选择最优特征。可以设定固定数目、百分比或其他标准。它的默认值是使用所有特征个数。

### 决策树的使用

首先，我们导入sklearn内嵌的鸢尾花数据集：

```assembly
from sklearn.datasets import load_iris
```

接下来，我们使用import语句导入决策树分类器，同时导入计算交叉验证值的函数cross_val_score。

```assembly
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
```

我们使用默认参数，创建一颗基于基尼系数的决策树，并将该决策树分类器赋值给变量clf。

```assembly
clf = DecisionTreeClassifier()
```

将鸢尾花数据赋值给变量iris 。

```assembly
iris = load_iris()
```

这里我们将决策树分类器做为待评估的模型，iris.data鸢尾花数据做为特征，iris.target鸢尾花分类标签做为目标结果，通过设定cv为10，使用10折交叉验证。得到最终的交叉验证得分。

```assembly
>>>cross_val_score(clf,iris.data,iris.target,cv=10)
...
array([1., 0.93..., 0.86..., 0.93..., 0.93..., 0.93...,0.93..., 1., 0.93..., 1.])
```

以仿照之前K近邻分类器的使用方法，利用fit()函数训练模型并使用predict()函数预测：

```assembly
clf.fit(X,y)
clf.predict(x)
```

### 决策树

* 决策树本质上是寻找一种对特征空间上的划分，旨在构建一个训练数据拟合的好，并且复杂度小的决策树。
* 在实际使用中，需要根据数据情况，调整DecisionTreeClassifier类中传入的参数，比如选择合适的criterion，设置随机变量等。

-----------------------------------------------

## 朴素贝叶斯

朴素贝叶斯分类器是一个以贝叶斯定理为基础的多分类的分类器。
对于给定数据，首先基于特征的条件独立性假设，学习输入输出的联合概率分布，然后基于此模型，对给定的输入x，利用贝叶斯定理求出后验概率最大的输出 y 。
$$
p(A|B)=\frac{p(B|A)*p(A)}{p(B)}
$$
在sklearn 库中，实现了三个朴素贝叶斯分类器，如下表所示：

| 分类器                    | 描述                                 |
| ------------------------- | ------------------------------------ |
| naive_bayes.GussianNB     | 高斯朴素贝叶斯                       |
| naive_bayes.MultinomialNB | 针对多项式模型的朴素贝叶斯分类器     |
| naive_bayes.BernoulliNB   | 针对多元伯努利模型的朴素贝叶斯分类器 |

区别在于假设某一特征的所有属于某个类别的观测值符合特定分布，如：分类问题的特征包括人的身高，身高符合高斯分布，这类问题适合高斯朴素贝叶斯。

在sklearn 库中，可以使用sklearn.naive_bayes.GaussianNB创建一个高斯朴素贝叶斯分类器，其参数有：

* priors：给定各个类别的先验概率。如果为空，则按训练数据的实际情况进行统计；如果给定先验概率，则在训练过程中不能更改。

### 朴素贝叶斯的使用

导入numpy库，并构造训练数据X和y。

```assembly
import numpy as np
X = np.array([[-1,-1],[-2,-1],[-3,-2],[1,1],[2,1],[3,2]])
Y = np.array([ 1,      1,      1 ,     2 ,   2 ,   2 ])
```

使用import 语句导入朴素贝叶斯分类器。

```assembly
from sklearn.naive_bayes import GaussianNB
```

使用默认参数，创建一个高斯朴素贝叶斯分类器，并将该分类器赋给变量clf。

```assembly
clf = GaussianNB(priors=None)
```

类似的，使用fit()函数进行训练，并使用predict()函数进行预测，得到预测结果为1。（测试时可以构造二维数组达到同时预测多个样本的目的）

```assembly
>>>clf.fit(X,Y)
>>>print(clf.predict([[-0.8,-1]]))
[1]
```

### 总结

朴素贝叶斯是典型的生成学习方法，由训练数据学习联合概率分布，并求得后验概率分布。
朴素贝叶斯一般在小规模数据上的表现很好，适合进行多分类任务。

## 运动状态-程序编写

### 算法流程

* 需要从特征文件和标签文件中将所有数据加载到内存中，由于存在缺失值，此步骤还需要进行简单的数据预处理。
* 创建对应的分类器，并使用训练数据进行训练。
* 利用测试集预测，通过使用真实值和预测值的比对，计算模型整体的准确率和召回率，来评测模型。

### 模块导入

SimpleImputer，这个类是用来填充数据里面的缺失值的。

```assembly
def __init__(self, missing_values=np.nan, strategy="mean",
                 fill_value=None, verbose=0, copy=True, add_indicator=False):
```

* missing_values,也就是缺失值是什么，一般情况下缺失值当然就是空值啦，也就是np.nan

* strategy:也就是你采取什么样的策略去填充空值，总共有4种选择。分别是mean,median, most_frequent,以及constant，这是对于每一列来说的，如果是mean，则该列则由该列的均值填充。而median,则是中位数，most_frequent则是众数。需要注意的是，如果是constant,则可以将空值填充为自定义的值，这就要涉及到后面一个参数了，也就是fill_value。如果strategy='constant',则填充fill_value的值。

* copy:则表示对原来没有填充的数据的拷贝。

* add_indicator:如果该参数为True，则会在数据后面加入n列由0和1构成的同样大小的数据，0表示所在位置非空，1表示所在位置为空。相当于一种判断是否为空的索引。

```assembly
import numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from sklearn.neighbors import KNeighborsClassifier #K 近邻分类器
from sklearn.tree import DecisionTreeClassifier #决策树分类器
from sklearn.naive_bayes import GaussianNB #和高斯朴素贝叶斯函数


def load_dataset(feature_paths, label_paths):
    '''
    读取特征文件列表和标签列表中的内容，归并后返回
    '''
    feature = np.ndarray(shape=(0, 41))
    label = np.ndarray(shape=(0, 1))
    # 编写数据导入函数，设置传入两个参数，分别是特征文件的列表feature_paths和标签
    # 文件的列表label_paths 。
    # 定义feature数组变量，列数量和特征维度一致为41定义空的标签变量，列数量与标签维度一致为1。
    for file in feature_paths:
        # 使用逗号分隔符读取特征数据，将问号替换标记为缺失值，文件中不包含表头
        df = pd.read_table(file, delimiter=',', na_values='?', header=None)
        # 使用平均值补全缺失值，然后将数据进行补全
        imp = SimpleImputer(missing_values=np.NaN, strategy='mean', fill_value=None, verbose=0)
        imp.fit(df)
        # fit()函数用于训练预处理器
        df = imp.transform(df)
        # transform()函数用于生成预处理结果。

        # 将新读入的数据合并到特征集合中
        feature = np.concatenate((feature, df))

    for file in label_paths:
        df = pd.read_table(file, header=None)
        label = np.concatenate((label, df))
    label = np.ravel(label)
    # 将标签归整为一维向量
    return feature, label


if __name__ == '__main__':
    feature_paths = ['A/A.feature', 'B/B.feature', 'C/C.feature',
                     'D/D.feature', 'E/E.feature']
    label_paths = ['A/A.label', 'B/B.label', 'C/C.label', 'D/D.label', 'E/E.label']

    x_train, y_train = load_dataset(feature_paths[:4], label_paths[:4])
    # 将前4个数据作为训练集读入
    x_test, y_test = load_dataset(feature_paths[4:], label_paths[4:])
    # 将最后一个数据集作为测试集读入
    x_train, x_, y_train, y_ = train_test_split(x_train, y_train, test_size=None)
    # 使用全局数据作为训练集，借助train_test_split函数将训练数据打乱，
    # 通过设置测试集比例test_size为0 ，将数据随机打乱，便于后续分类

    print("Start training knn")
    knn = KNeighborsClassifier().fit(x_train, y_train)
    print("Training done!")
    answer_knn = knn.predict(x_test)
    print("Prediction done")

    print("Start training DT")
    dt = DecisionTreeClassifier().fit(x_train, y_train)
    print("Training done")
    answer_dt = dt.predict(x_test)
    print("Prediction done")

    print("Start train Bayes")
    gnb = GaussianNB().fit(x_train, y_train)
    print("Training done")
    answer_gnb = gnb.predict(x_test)
    print("Prediction done")

    print("\n\nThe classification report for knn:")
    # print(y_test.shape)
    # print(type(answer_knn))
    # print(answer_knn.shape)
    print(classification_report(y_test, answer_knn))

    print("\n\nThe classification report for dt:")
    print(classification_report(y_test, answer_dt))

    print("\n\nThe classification report for gnb:")
    print(classification_report(y_test, answer_gnb))
    # 使用classification_report函数对分类结果，从精确率precision、召回率recall、f1值f1-score
    # 和支持度support四个维度进行衡量。
    # 分别对三个分类器的分类结果进行输出

```

#### 结果输出

```assembly
The classification report for knn:
              precision    recall  f1-score   support

         0.0       0.56      0.60      0.58    102341
         1.0       0.92      0.93      0.93     23699
         2.0       0.94      0.78      0.85     26864
         3.0       0.82      0.82      0.82     22132
         4.0       0.85      0.89      0.87     32033
         5.0       0.39      0.20      0.27     24646
         6.0       0.77      0.89      0.82     24577
         7.0       0.80      0.95      0.87     26271
        12.0       0.32      0.32      0.32     14281
        13.0       0.16      0.22      0.18     12727
        16.0       0.90      0.67      0.77     24445
        17.0       0.89      0.96      0.92     33034
        24.0       0.00      0.00      0.00      7733

    accuracy                           0.69    374783
   macro avg       0.64      0.63      0.63    374783
weighted avg       0.69      0.69      0.68    374783



The classification report for dt:
              precision    recall  f1-score   support

         0.0       0.46      0.68      0.55    102341
         1.0       0.66      0.96      0.78     23699
         2.0       0.84      0.86      0.85     26864
         3.0       0.91      0.73      0.81     22132
         4.0       0.24      0.16      0.19     32033
         5.0       0.63      0.52      0.57     24646
         6.0       0.56      0.65      0.60     24577
         7.0       0.68      0.15      0.24     26271
        12.0       0.64      0.63      0.64     14281
        13.0       0.64      0.57      0.60     12727
        16.0       0.83      0.07      0.14     24445
        17.0       0.86      0.85      0.86     33034
        24.0       0.34      0.29      0.31      7733

    accuracy                           0.58    374783
   macro avg       0.64      0.55      0.55    374783
weighted avg       0.61      0.58      0.55    374783



The classification report for gnb:
              precision    recall  f1-score   support

         0.0       0.62      0.81      0.70    102341
         1.0       0.97      0.91      0.94     23699
         2.0       1.00      0.66      0.79     26864
         3.0       0.61      0.66      0.63     22132
         4.0       0.91      0.77      0.83     32033
         5.0       1.00      0.00      0.00     24646
         6.0       0.87      0.72      0.78     24577
         7.0       0.31      0.47      0.37     26271
        12.0       0.52      0.59      0.55     14281
        13.0       0.61      0.50      0.55     12727
        16.0       0.88      0.72      0.79     24445
        17.0       0.75      0.91      0.82     33034
        24.0       0.59      0.24      0.34      7733

    accuracy                           0.68    374783
   macro avg       0.74      0.61      0.62    374783
weighted avg       0.74      0.68      0.67    374783

```

### 结果对比

| 模型   | K邻近 | 决策树 | 贝叶斯 |
| ------ | ----- | ------ | ------ |
| 准确率 | 0.69  | 0.61   | 0.74   |
| 召回率 | 0.69  | 0.64   | 0.68   |
| F1值   | 0.68  | 0.60   | 0.67   |

结论：

* 从准确度的角度衡量，贝叶斯分类器的效果最好
* 从召回率和F1值的角度衡量， k近邻效果最好
* 贝叶斯分类器和k近邻的效果好于决策树

### 课后思考

* 在所有的特征数据中，可能存在缺失值或者冗余特征。如果将这些特征不加处理地送入后续的计算，可能会导致模型准确度下降并且增大计算量。
* 在特征选择阶段，通常需要借助辅助软件（例如Weka）将数据进行可视化并进行统计。
* 请大家可以通过课外学习思考如何筛选冗余特征，提高模型训练效率，也可以尝试调用sklearn提供的其他分类器进行数据预测。