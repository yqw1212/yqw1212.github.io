# 无监督学习

## 降维

### PCA方法及其应用

#### 主成分分析（PCA）

* 主成分分析（ Principal Component Analysis PCA ）是最常用的一种降维方法，通常用于高维数据集的探索与可视化，还可以用作数据压缩和预处理等。
* PCA 可以把具有相关性的高维变量合成为线性无关的低维变量，称为主成分。主成分能够尽可能保留原始数据的信息。

#### 在介绍PCA 的原理之前需要回顾涉及到的相关术语

* 方差

  是各个样本和样本均值的差的平方和的均值，用来度量一组数据的分散程度。

* 协方差

  用于度量两个变量之间的线性相关性程度，若两个变量的协方差为0，则可认为二者线性无关。

* 协方差矩阵

  协方差矩阵是由变量的协方差值构成的矩阵（对称阵）。

* 特征向量和特征值

  矩阵的特征向量是描述数据集结构的非零向量，并满足如下公式：
  $$
  𝑨𝒗=𝝀𝒗
  $$
  A是方阵，𝒗是特征向量，𝝀是特征值。

#### 原理

矩阵的主成分就是其协方差矩阵对应的特征向量，按照对应的特征值大小进行排序，最大的特征值就是第一主成分，其次是第二主成分，以此类推。

#### sklearn中主成分分析

在sklearn 库中，可以使用 sklearn.decomposition.PCA 加载 PCA 进行降维，主要参数有：

* n_components ：指定主成分的个数，即降维后数据的维度
* svd_solver ：设置特征值分解的方法，默认为auto’,其他可选有‘full’, ‘arpack’, ‘randomized 。

#### 实例程序编写

* 建立工程，导入 sklearn 相关工具包

  ```python
  import matplotlib.pyplot as plot
  #加载 matplotlib 用于数据的可视化
  from sklearn.decomposition import PCA
  #加载 PCA 算法包
  from sklearn.datasets import load_iris
  #加载鸢尾花数据集导入函数
  ```

* 加载数据并进行降维

  ```python
  data = load_iris()
  #以字典形式加载鸢尾花数据集
  y = data.target#使用 y 表示数据集中的 标签
  x = data.data#使用 X 表示数据集中的 属性数据
  pca = PCA(n_components=2)
  #加载 PCA 算法，设置降维后主成分数目为2
  reduce_X = pca.fit_transform(x)
  #对原始数据进行降维，保存在 reduced_X中
  ```

  这里的y是

  ```
  [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
   0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
   1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2
   2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
   2 2]
  ```

* 按类别对降维后的数据进行保存

  ```python
  red_x, red_y = [], []
  #第一类数据点
  blue_x, blue_y = [], []
  #第二类数据点
  green_x, green_y = [], []
  #第三类数据点
  for i in range(len(reduce_X)):
      if y[i] == 0:
          red_x.append(reduce_X[i][0])
          red_y.append(reduce_X[i][1])
      elif y[i] == 1:
          blue_x.append(reduce_X[i][0])
          blue_y.append(reduce_X[i][1])
      else:
          green_x.append(reduce_X[i][0])
          green_y.append(reduce_X[i][1])
  ```

* 降维后数据点的可视化

  ```python
  plt.scatter(red_x, red_y, c='r', marker='x')
  #第一类数据点
  plt.scatter(blue_x, blue_y, c='b', marker='D')
  #第二类数据点
  plt.scatter(green_x, green_y, c='g',marker='.')
  #第三类数据点
  plt.show()
  #可视化
  ```

* 结果展示

  可以看出，降维后的数据仍能够清晰地分成三类。这样不仅能削减数据的维度，降低分类任务的工作量，还能保证分类的质量。

### NMF方法及实例

#### 非负矩阵分解（NMF）

非负矩阵分解（Non-negative Matrix Factorization，NMF）是在矩阵中所有元素均为非负数约束条件之下的矩阵分解方法。
基本思想：给定一个非负矩阵V，NMF 能够找到一个非负矩阵W和一个非负矩阵H，使得矩阵W和H的乘积近似等于矩阵V中的值。
$$
𝑽𝒏∗𝒎=𝑾𝒏∗𝒌∗𝑯𝒌∗𝒎
$$

* W矩阵：基础图像矩阵，相当于从原矩阵V中抽取出来的特征
* H 矩阵：系数矩阵。
* NMF能够广泛应用于图像分析、文本挖掘和语音处理等领域。

##### 矩阵分解优化目标

最小化W矩阵H矩阵的乘积和原始矩阵之间的差别。

 

在sklearn库中，可以使用sklearn.decomposition.NMF加载NMF算法，主要参数有：

* n_components ：用于指定分解后矩阵的单个维度 k
* init： W矩阵和H矩阵的初始化方式，默认为‘nndsvdar’。

#### 实例程序编写

* 建立工程，导入 sklearn 相关工具包

  ```python
  import matplotlib.pyplot as plt
  #加载 matplotlib 用于数据的可视化
  from sklearn import decomposition
  #加载PCA算法包
  from sklearn.datasets import fetch_olivetti_faces
  #加载Olivetti人脸数据集导入函数
  from numpy.random import RandomState
  #加载RandomState用于创建随机种子
  ```

* 设置基本参数并加载数据

  ```python
  n_row, n_col = 2, 3
  #设置图像展示时的排列情况
  n_components = n_row * n_col
  #设置提取的特征的数目
  image_shape = (64, 64)
  #设置人脸数据图片的大小
  dataset = fetch_olivetti_faces(shuffle=True,random_state=RandomState(0))
  #加载数据，并打乱顺序
  faces = dataset.data
  ```

* 设置图像的展示方式

  ```python
  def plot_gallery(title, images, n_col=n_col, n_row=n_row):
      plt.figure(figsize=(2. * n_col, 2.26 * n_row))
      #创建图片，并指定图片大小（英寸）
      plt.suptitle(title, size=16)
      #设置标题及字号大小
      for i, comp in enumerate(images):
          plt.subplot(n_row, n_col, i+1)
          #选择画制的子图
          vmax = max(comp.max(), -comp.min())
  
          plt.imshow(comp.reshape(image_shape),cmap=plt.cm.gray, interpolation='nearest',vmin=-vmax, vmax=vmax)
          #对数值归一化，并以灰度图形式显示
          plt.xticks(())
          plt.yticks(())#去除子图的坐标轴标签
      plt.subplots_adjust(0.01, 0.05, 0.99, 0.93, 0.04, 0.)
      #对子图位置及间隔调整
  ```

* 创建特征提取的对象 NMF ，使用PCA作为对比

  ```python
  estimators = [('Eigenfaces-PCA using randomized SVD', decomposition.PCA(n_components=6,whiten=True)),
                ('Non-negative components - NMF', decomposition.NMF(n_components=6, init='nndsvda',tol=5e-3))]
  #将它们存放在一个列表中
  ```

* 降维后数据点的可视化

  ```python
  for name, estimator in estimators:#分别调用 PCA 和 NMF
      estimator.fit(faces)#调用 PCA 或 NMF 提取特征
      components_ = estimator.components_
      #获取 提取的特征
      plot_gallery(name, components_[:n_components])
      #按照固定格式进行排列
  plt.show()
  ```

#### 结果

* PCA提取的特征

  ![image-20200330230316321](C:\Users\yqw\AppData\Roaming\Typora\typora-user-images\image-20200330230316321.png)

* NMF提取的特征

  ![image-20200330230328598](C:\Users\yqw\AppData\Roaming\Typora\typora-user-images\image-20200330230328598.png)

* 去掉random_state=RandomState(0)的结果相同

  ```python
  import matplotlib.pyplot as plt
  from sklearn import decomposition
  from sklearn.datasets import fetch_olivetti_faces
  
  n_row, n_col = 2, 3
  n_components = n_row * n_col
  image_shape = (64, 64)
  dataset = fetch_olivetti_faces(shuffle=True)
  faces = dataset.data
  
  
  def plot_gallery(title, images, n_col=n_col, n_row=n_row):
      plt.figure(figsize=(2. * n_col, 2.26 * n_row))
      plt.suptitle(title, size=16)
      for i, comp in enumerate(images):
          plt.subplot(n_row, n_col, i+1)
          vmax = max(comp.max(), -comp.min())
  
          plt.imshow(comp.reshape(image_shape), cmap=plt.cm.gray, interpolation='nearest',
                     vmin=-vmax, vmax=vmax)
          plt.xticks(())
          plt.yticks(())
      plt.subplots_adjust(0.01, 0.05, 0.99, 0.93, 0.04, 0.)
  
  
  estimators = [('Eigenfaces-PCA using randomized SVD', decomposition.PCA(n_components=6,whiten=True)),
                ('Non-negative components - NMF', decomposition.NMF(n_components=6, init='nndsvda',tol=5e-3))]
  
  for name, estimator in estimators:
      estimator.fit(faces)
      components_ = estimator.components_
      plot_gallery(name, components_[:n_components])
  plt.show()
  ```

### 基于聚类的“图像分割”实例编写

#### 图像分割

图像分割：利用图像的灰度、颜色、纹理、形状等特征，把图像分成若干个互不重叠的区域，并使这些特征在同一区域内呈现相似性，在不同的区域之间存在明显的差异性 。然后就可以将分割的图像中具有独特性质的区域提取出来用于不同的研究。
图像分割技术已在实际生活中得到广泛的应用。例如：在机车检验领域，可以应用到轮毂裂纹图像的分割，及时发现裂纹，保证行车安全；在生物医学工程方面，对肝脏CT图像进行分割，为临床治疗和病理学研究提供帮助。

#### 图像分割常用方法：

* 阈值分析：对图像灰度值进行度量，设置不同类别的阈值，达到分割的目的
* 边缘分割：对图像边缘进行检测，即检测图像中灰度值发生跳变的地方，则为一片区域的边缘。
* 直方图法：对图像的颜色建立直方图，而直方图的波峰波谷能够表示一块区域的颜色值的范围，来达到分割的目的。
* 特定理论：基于 聚类分析 、小波变换等理论完成图像分割。

#### 实例描述

* 目标：利用K-means 聚类算法对图像像素点颜色进行聚类实现简单的图像分割
* 输出：同一聚类中的点使用相同颜色标记，不同聚类颜色不同
* 技术路线：sklearn.cluster.KMeans
* 实例数据：本实例中的数据可以是任意大小的图片，为了使效果更佳直观，
  可以采用区分度比较明显的图片。

#### “kmeans 实现图片分割 ”实例编写

* 建立工程并导入sklearn包

  ```python
  import numpy as np
  import PIL.Image as image
  from sklearn.cluster import KMeans
  ```

* 加载图片并进行预处理

  ```python
  def loadData(filePath):
      f = open(filePath, 'rb')
      data = []
      img = image.open(f)
      m, n = img.size
      for i in range(m):
          for j in range(n):
              x, y, z = img.getpixel((i, j))
              data.append([x/256.0, y/256.0, z/256])
      f.close()
      return np.mat(data), m, n
  
  
  imgData, row, col = loadData('kmeans/horse.jpg')
  ```

* 加载 Kmeans 聚类算法

  ```python
  km = KMeans(n_clusters=3)
  ```

* 对像素点进行聚类并输出

  ```python
  km = KMeans(n_clusters=3)
  
  label = km.fit_predict(imgData)
  label = label.reshape([row, col])
  
  pic_new = image.new("L", (row, col))
  
  for i in range(row):
      for j in range(col):
          pic_new.putpixel((i, j), int(256/(label[i][j]+1)))
  
  pic_new.save("result-bull-4.jpg", "JPEG")
  ```

  #### 结果展示

  <img src="D:\文档\ps\rest-4933097.jpg" alt="rest-4933097" style="zoom:50%;" />

  

  <img src="D:\文档\新建文件夹 (2)\mach\result-bull-4.jpg" alt="result-bull-4" style="zoom: 25%;" />

  #### 实验分析

  通过设置不同的k值，能够得到不同的聚类结果。同时，k值的不确定也是 Kmeans算法的一个缺点。往往为了达到好的实验结果，需要进行多次尝试才能够选取最优的 k 值。而像层次聚类的算法，就无需指定 k 值，只要给定限制条件，就能自动地得到类别数k。