---
layout: post
title:  Socal Computing
date:   2021-03-01 00:01:01 +0300
image:  2021-03-01-books.jpg
tags:   [note]
---

## 图

### 度

和该节点相关联的边的条数，又称关联度。

### 定义

- 加权图

- 完全图

- 子图

  节点集和边集分别是某一图的节点集的子集和边集的子集的图。

- 母图

- 生成子图

  若图G的一个子图**包含G的所有顶点**，则称该子图为G的一个生成子图。

### 区分

- walk
- trail
- path

### 性质

- 连通性(connectedness)

  - 强连通

    在有向图G中，如果对于每一对vi、vj，vi≠vj，从vi到vj和从vj到vi都存在路径，则称G是强连通图。

  - 弱连通

    将有向图的所有的有向边替换为无向边，所得到的图称为原图的基图。如果一个有向图的基图是连通图，则有向图是**弱连通图**。

  - k-connected

    minimum number of vertices (size of smallest cut set) whose removal disconnects the graph.

  - 连通分支(connected component)

    一个图被分成几个小块,每个小块是连通的,但小块之间不连通,那么每个小块称为连通分支.一个孤立点也是一个连通分支。

  - 强连通分支

  - 关节节点/割节点

  - edge-connectivity

    去掉最少边后使连通的图变得不连通了，这个去掉的最少的边的个数。

  - disjoint paths

  - edge-disjoint

  - 门杰定理(Menger's Theorem)

    设x和y为图G中两个不相邻的顶点，则G中内部不相交的(x，y)-路的最大数目=G中最小的xy-顶点分隔集的顶点数。

- 距离

  d<sub>G</sub>(u,v)

  u和v的最短路径的长度。

- 直径

  任意两个顶点间距离的最大值.

- 维纳指数(weiner index)

	- 图中所有可到达的两个点之间的最短距离之和。该指数反应了图中两点间距离的平均信息。

- k-spanner
  $$
  d_{G^{’}}(u,v)≤k*d_{G}(u,v)\\
  k=dilation\space factor
  $$

- 独立集(independent set)

  图G中两两互不相邻的顶点构成的集合。

- 边独立集(edge independent set)

  由一个图的两两互不相邻且不是环的一些边组成的集合称为该图的一个边独立集。

### centrality meatures

- 度中心性(degree centrality)

  一个节点的节点度越大就意味着这个节点的度中心性越高，该节点在网络中就越重要。
  $$
  C_D(v_i)=d_i=\sum_jA_{ij}
  $$
  Normalized Degree Centrality
  $$
  C_D(v_i)^{’}=\frac{d_i}{n-1}
  $$

- 介数中心性(betweenness centrality)

  每个节点的介数中心性即为最短路径穿过该节点的次数。 
  $$
  C_B(v)=∑_{s≠v≠t∈V}\frac{σ_{st}(v)}{σ_{st}}
  $$
  σ<sub>st</sub>(v)表示经过节点v的s→t的最短路径条数, σ<sub>st</sub>表示s→t的最短路径条数。

- 紧密中心性(closeness centrality)

  Average Distance
  $$
  D_{avg}(v_i)=\frac{\sum_{t∈V,t≠v}d_G(v,t)}{n-1}
  $$
  Closeness Centrality
  $$
  C_c(v_i)=[\frac{\sum_{t∈V,t≠v}d_G(v,t)}{n-1}]^{-1}=\frac{n-1}{\sum_{t∈V,t≠v}d_G(v,t)}
  $$

- 特征向量中心性(eigenvector centrality)

  特征向量中心性的基本思想是，一个节点的中心性是相邻节点中心性的函数。也就是说，与你连接的人越重要，你也就越重要。

  特征向量中心性和点度中心性不同，一个点度中心性高即拥有很多连接的节点特征向量中心性不一定高，因为所有的连接者有可能特征向量中心性很低。同理，特征向量中心性高并不意味着它的点度中心性高，它拥有很少但很重要的连接者也可以拥有高特征向量中心性。

## 树

* 树的重量

  树上所有边权之和。

### 最小生成树

#### 克鲁克儿算法

假设连通网N＝（V，{E}）。则令最小生成树的初始状态为只有n个顶点而无边的非连通图T＝（V，{}），图中每个顶点自成一个连通分量。在E中选择最小代价的边，若该边依附的顶点落在T中不同的连通分量中，则将该边加入到T中，否则舍去此边而选择下一条代价最小的边，依次类推，直到T中所有顶点都在同一连通分量上为止。

### Kirchhoff

对一个图构造两个矩阵，分别是这个图的邻接矩阵和度数矩阵。邻接矩阵S<sub>1</sub>的第i行第j列上的数字表示原无向图中编号为i和编号为j的两个点之间的边的条数。度数矩阵S<sub>2</sub>只有斜对角线上有数字，即只有第i行第i列上有数字，表示编号为i的点的度数是多少。我们将两个矩阵相减，即S<sub>2</sub>− S<sub>1</sub>，我们记得到的矩阵为T，我们将矩阵T去掉任意一行和一列（一般情况去掉最后一行和最后一列）得到T′ ，最后生成树的个数就是这个矩阵T′的行列式。

## Max-Flow Min-Cut

Capacity(S,T):离开S的边的权重之和。
$$
|f|=\sum_{v∈V}f(s,v)=\sum_{v∈V}f(v,t)
$$
**最小割问题**

定义：找到一个最小capacity的（S，T）cut

**最大流问题**

定义：找到到达sink节点t的最大化净流量。

#### Ford-Fulkerson算法

残存网络中没有从s到t的路径时，最大流等于最小割容量。

沿着增广路径增加**flow**。增广路径是一条从**s**到**t**的无向路径，但也有些条件，可以经过没有满容量的前向路径（s到t）或者是不为空的反向路径(t->s)

最大流=从s流出的流量，每个步骤依次相加。

### K-shell分解

K-shell方法递归地剥离网络中度数等于k的节点,我们让k值为1，不断地让节点的度数值与其相比较，如果等于那么我们就将该节点从网络中剥离出去，然后继续重复比较和剥离的过程，直到度数值都不等于k，这就意味着我们需要将k增大，然后再重复比较剥离和k值增大的过程。

### pagerank算法

转移矩阵

### hits 算法



### 问题

- 最短路径

	- Floyd-Warshell
	- Dijkstra's algorithm
- 图着色

## 网络

### 桥

对于无向图,如果删除了一条边,**整个图的联通分量数量变化,**则这条边称为桥.

### Neighborhood Overlap

$$
overlap(v_i,v_j)=\frac{|N_i∩N_j|}{|N_i∪N_j|-2}
$$

## 三元闭包(triadic closure)

### 聚类系数（Clustering Coefficient）

#### 全局

$$
\frac{number\space of\space triangles × 3}{number\space of\space connected\space triples}
$$

#### 局部

局部计算是面向节点的。
$$
\frac{number\space of\space pairs\space of\space neighbours\space of\space i\space that\space are\space connected}{number\space of\space pairs\space of\space neighbours\space of\space i}\\
=\frac{number\space of\space pairs\space of\space neighbours\space of\space i\space that\space are\space connected}{\frac{k_i(k_i-1)}{2}}
$$
k<sub>i</sub>是节点i的度

#### 平均

$$
C=\frac{1}{n}\sum_{i=1}^nC_i
$$

#### transitivity

$$
\frac{number\space of\space triangles × 6}{number\space of\space paths\space of\space length\space two}
$$

### 影响力模型

#### 线性域值模型(Linear threshold model(LTM))



#### 独立级联模型(Independent cascade model(ICM))

在𝑡=0时刻，一个预先选好的初始集合s<sub>0</sub>首先被激活，而其他节点都处于不活跃状态。这个初始节点集合被称作种子节点集合。
对任何时刻t≥1,用s<sub>t</sub>表示到这个时刻为止所有活跃点的集合。对任何一个在上一时刻刚被激活的节点𝑢∈s <sub>t−1</sub>\s<sub>t−2</sub>，节点𝑢会对它的每个尚未被激活的出邻居节点v∈N<sup>+</sup>(v)\s<sub>t−1</sub>，尝试激活一次，而这次尝试成功的概率为p(u,v)，且这次激活尝试与所有其他的激活尝试事件相互独立。如果尝试成功，则节点𝑣在时刻𝑡被激活，即v∈s<sub>t</sub>\s<sub>t−1</sub>；如果尝试不成功，且节点𝑣的其他入邻居也未在时刻𝑡成功激活节点𝑣，则节点𝑣在时刻 𝑡仍为不活跃状态，即v∈V\s<sub>t</sub> 。
当在某一时刻不再有新的节点被激活时，传播过程结束。

#### 影响力最大化

在给定的网络中给定初始活跃节点的个数，影响力最大化问题为找到固定个数的活跃节点集，经由特定的传播模型，使得最终活跃节点的数目达到最大。

### 相关

- 同质性(homophily)
- 混淆性(confounding)
- 影响性(influence)

### Activation likelihood

### Shuffle test

### network similarity

- structural equivalence（结构等价）

  - 相同邻居

  - 计算
    $$
    n_{i,j}=\sum_kA_{i,k}A_{k,j}
    $$

- regular equivalence（正则等价）

  * 相似邻居

### Cosine Similarity

$$
σ_{i,j}=\frac{共同相邻节点个数}{\sqrt{K_i}\sqrt{K_j}}
$$

### Pearson Coefficients

### 大网络

- 小世界效应

	- 若网络中任意两点间的平均距离L 随网络格点数N 的增加呈对数增长，即 L ~ l n N ， 且网络的局部结构上仍具有较明显的集团化特征。
	- log n

- 度分布Pk

	- 度序列

		- 集{k1,k2,k3...}所有顶点的度

- power laws
$$
	lnp_k=-αlnk+c\\
p_k=Ck^{-α}
$$

- 无标度网络（scale-free networks）

  大部分的连接都集中在少数的中心

- *

### 社区发现（Community Detection）

- group

	- 显式组（Explicit Group）
	- 隐式组（Implicit Group）

- 分类标准

  - Node

    - clique

    	- 最大完整的子图
    	
    	- 在k大小的小集团中，每个节点维护度>=k-1
    	
    	- Maximum Clique
    	
    	  In order to find a clique > n, remove all nodes with degree <= n-1.
    - **派系过滤算法（Clique Percolation Method（CPM））**
      * 概念
        * k-派系表示该全耦合网络的节点数目为k
        * k-派系相邻：两个不同的k-派系共享k-1个节点，认为他们相
      * 步骤
          * 找出给定网络中所有k大小的clique。
          * 如果两个clique共享k-1个节点，那么他们相邻。
          * clique图中的每一个component都形成一个社区。

  - k-clique

    * 最大子图，其中任意两点最大路径<=k

    * 在原图基础上

  - k-club

    * 直径<=k的子结构

    * 不在原图基础上

  - Group

    - quasi-clique

  	- $$
    	  \frac{|E_s|}{|V_s|(|V_s|-1)/2}≥γ
  	  $$
    	
  	  E<sub>s</sub>边数，V<sub>s</sub>结点数

  - Network

    - vertex similarity

      - Jaccard Similarity（杰卡德系数）
        $$
        Jaccard(v_i,v_j)=\frac{N_i∩N_j}{N_i∪N_j}
        $$

      - Cosine Similarity
      $$
        cosine(v_i,v_j)=\frac{Σ_{k}A_{ik}A_{jk}}{\sqrt{{A_{is}}^2·Σ_t{A_{jt}}^2}}
      $$

    - 隐式空间模型（Latent space models）

      - Multi-dimensional scaling（MDS）

      	- Solution
      	  $$
      	  S=Vλ^{\frac{1}{2}}\\
      	  V为\widetilde{P}的特征向量矩阵,λ为d个最大特征值所构成的对角矩阵
      	  $$
      	
      	- 特征值
      	
    	  设A是n阶方阵，如果存在数m和非零n维列向量x，使得**Ax=mx**成立，则称m是矩阵A的一个特征值(characteristic value)或本征值(eigenvalue)。
      	
      	计算方法
    	
      	对于矩阵A，由AX=λ<sub>0</sub>X，λ<sub>0</sub>EX=AX，得[λ<sub>0</sub>E-A]X=0即齐次线性方程组,说明特征根是特征多项式**|λ<sub>0</sub>E-A|=0**的根。

    - Block model approximation
    
  - 谱聚类（Spectral clustering）

    - cut

    - 最小割

    	- 找到一个图形划分，使这两组之间的边数最小化

      - 标准化

      - Ratio Cut

        $$
          Ratio Cut(Π)=\frac{1}{k}\sum_{i=1}^{k}\frac{cut(C_i,C_i)}{|C_i|}
        $$

      - Normalized Cut

        $$
          Normalized Cut(Π)=\frac{1}{k}\sum_{i=1}^{k}\frac{cut(C_i,C_i)}{|C_i|}
        $$

      C<sub>i</sub>：a community

      |C<sub>i</sub>|：number of nodes in Ci

      vol(C<sub>i</sub>)：sum of degrees in C<sub>i</sub>

      - Kernighan-Lin‘s Algorithm

      - spectral partitioning

      连接两个组的边的数量：
      $$
        R=\frac{1}{2}\sum_{i,j\space in\space different\space groups}A_{i,j}\\
        S_i=\begin{cases}
        +1&\mbox{if vertex i belongs to g1}\\
      -1&\mbox{if vertex i belongs to g2}
        \end{cases}\\
        \frac{1}{2}(1-s_is_j)=\begin{cases}
        1&\mbox{i and j are in different group}\\
        0&\mbox{i and j are in same group}
        \end{cases}\\
        R=\frac{1}{4}\sum_{ij}A_{i,j}(1-s_is_j)
      $$

    - 图拉普拉斯
        $$
      L=D-A
      $$
      D为图的度矩阵，A为图的邻接矩阵。

  - Modularity maximization

    - expected number of edges
        $$
      d_id_j/2m\\
        m:number\space of\space edges 
      $$

    - Strength of a community
        $$
      \sum_{i∈C,j∈C}A_{ij}-d_id_j/2m
      $$

      - Modularity
      $$
        Q=\frac{1}{2m}\sum_{ζ=1}^{k}\sum_{i∈C_ζ,j∈C_ζ}A_{ij}-d_id_j/2m
      $$
      
      - Louvain Method

        步骤：

        1）将图中的每个节点看成一个独立的社区，次数社区的数目与节点个数相同。

        2）对每个节点i，依次尝试把节点i分配到其每个邻居节点所在的社区，计算分配前与分配后的模块度变化Delta Q（新社区的Modularity减去前两个Modularity），并记录Delta Q最大的那个邻居节点，如果maxDelta Q>0，则把节点i分配Delta Q最大的那个邻居节点所在的社区，否则保持不变。

        3）重复2），直到所有节点的所属社区不再变化。

        4）对图进行压缩，将所有在同一个社区的节点压缩成一个新节点，社区内节点之间的边的权重转化为新节点的环的权重，社区间的边权重转化为新节点间的边权重。

        5）重复1）直到整个图的模块度不再发生变化。

  - Hierarchy

    - Divisive Hierarchical Clustering（分解层次聚类）

      先将所有样本当作一整个簇，然后找出簇中距离最远的两个簇进行分裂，不断重复到预期簇或者其他终止条件。

      Freeman (1975) 提出过一个叫betweenness的指标，它衡量的是网络里一个节点占据其他n-1节点间捷径的程度。具体而言，首先对每一对节点寻找最短路径，得到一个n * (n-1)/2的最短路径集合S，然后看这个集合中有多少最短路径需要通过某个具体的节点。Newman借鉴了这个标准，但不是用来分析节点而是分析连边。一个连边的**edge betweenness**就是S集合里的最短路径包含该连边的个数。 

      定义了连边的betweenness后，就可以通过迭代算法来进行社区划分了。具体做法是先计算所有连边的betweenness，然后去除最高值连边，再重新计算，再去除最高值连边，如此反复，直到网络中的所有连边都被移除。在这个过程中网络就逐渐被切成一个个越来越小的component。在这个过程中，我们同样可以用Q-modularity来衡量社区划分的结果。这种算法定义比较清晰，也不涉及矩阵数学等运算，但问题是计算复杂度比较大。

    - Agglomerative Hierarchical Clustering（聚合层次聚类）

      先将所有样本的每个点都看成一个簇，然后找出距离最小的两个簇进行合并，不断重复到预期簇或者其他终止条件。

* community evalition

  * Normalized mutal information
    $$
    NMI(Π^a,Π^b)=\frac{\sum_{h=1}^{k^{(a)}}\sum_{l=1}^{k^{(b)}}n_{h,l}log(\frac{n×n_{h,l}}{n_{h}^{(a)}×n_{l}^{(b)}})}{\sqrt{(\sum_{h=1}^{k^{(a)}}n_n^{(a)}log\frac{n_h^a}{n})(\sum_{l=1}^{k^{(b)}}n_l^{(b)}log\frac{n_l^{b}}{n})}}
    $$

  * Accuracy of pairwise community memberships
    $$
    accuracy=\frac{a+d}{a+b+c+d}=\frac{a+d}{n(n+1)/2}
    $$
    

### heterogeneous networks

* 多维网络

  * Networks integration

    average strength
    $$
    \overline{A}=\frac{1}{p}\sum_{i=1}^pA^{(i)}
    $$

  * Utility Integration

  * Frature Integration

    averge of structural fearutes
    $$
    \overline{S}=\frac{1}{p}\sum_{i=1}^SA^{(i)}
    $$

  * Partition Integration

    * CPSA
    * Partition Feature Integration

* multi-mode networks(多模网络)

  * Co-Clustering

    奇异值

    奇异值分解

    假设M是一个m×n阶矩阵，其中的元素全部属于域 K，也就是实数域或复数域。如此则存在一个分解使得
    $$
    M=U∑V*
    $$
    其中U是m×m阶酉矩阵；Σ是半正定m×n阶对角矩阵；而V*，即V的共轭转置，是n×n阶酉矩阵。这样的分解就称作M的奇异值分解。Σ对角线上的元素Σi，其中Σi即为M的奇异值。

    normalized adjacency matrix
    $$
    \widetilde{A}=D_u^{-\frac{1}{2}}AD_t^{-\frac{1}{2}}
    $$
    D<sub>u</sub>=diag(d<sub>u1</sub>,d<sub>u2</sub>,...,d<sub>u<sub>m</sub></sub>)

    D<sub>t</sub>=diag(d<sub>t1</sub>,d<sub>t2</sub>,...,d<sub>t<sub>n</sub></sub>)
    $$
    \widetilde{A}≈S^{(u)}Σ_kS^{(t)}\\
    \begin{bmatrix} D_{u}^{-\frac{1}{2}} & S^{(u)} \\ D_{t}^{-\frac{1}{2}} & S^{(t)} \end{bmatrix}
    \quad
    $$
    
