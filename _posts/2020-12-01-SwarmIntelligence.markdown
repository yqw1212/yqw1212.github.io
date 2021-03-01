---
layout: post
title:  Swarm Intelligence Algorithm
date:   2020-12-01 00:01:01 +0300
image:  2020-12-01-alley.jpg
tags:   [AI,algorithm]
---

自然界有许多令人惊奇的现象，如蚂蚁搬家，鸟群觅食等。受自然界和生物界规律的启迪，人们根据其原理设计了许多求解问题的算法。如：**遗传算法**，**粒子群算法**，**蚁群算法等**。

##### 遗传算法

遗传算法的概念是在 1975 年由密切根大学的J.Holland提出的，这是一种通过**模拟自然进化过程寻找最优解**的方法。它遵循达尔文的**物竞天择，适者生存**的进化准则。基本思想：

初始一个种群，选择种群中适应度高的个体进行交叉变异。然后再将适应度低的个体淘汰，留下适应度高的个体进行繁殖，这样不断的进化，最终留下的都是优秀的个体。

###### 基因和染色体

在遗传算法中，我们首先需要将要解决的问题映射成一个数学问题，也就是所谓的**数学建模**，那么这个问题的一个可行解即被称为一条**染色体或个体**。如：
$$
3x+4y+5z<100
$$
[1,2,3]，[2,3,4]，[3,2,1]均为这个函数的可行解，这些可行解在遗传算法中均被称为染色体，每一个元素就被称为染色体上的一个基因。

###### 染色体编码与解码

遗传算法的运算对象是表示染色体的符号串，所以必须把变量x，y，z编码为一种符号串。常见的编码方式如用无符号**二进制整数**来表示。解码即将二进制整数转换回最初的表现型。

编码： 5 –> 0101。

解码： 0101 –> 5。 

###### 初始群体的产生

遗传算法是对群体进行的进化操作，需要给其准备一些表示起始搜索点的初始群体数据。假如群体规模的大小取为 4，即群体由 4 个染色体组成，每个染色体可通过随机方法产生。

如：011101，101011，011100，111001。 

###### 物竞天择

适应度函数：遗传算法中以染色体适应度的大小来评定各个染色体的优劣程度，从而决定其遗传机会的大小。
选择函数：自然界中，越适应的个体就越有可能繁殖后代。但是也不能说适应度越高的就肯定后代越多，只能是从概率上来说更多。常用的选择方法有轮盘赌选择法。

若*f*<sub>i</sub>表示每个染色体的适应度，则每个个体遗传下来的概率为：
$$
p(i)=\frac{f_i}{\sum_if_i}
$$
由公式可以看出，适应度越高，则遗传下来的概率就越大，好比赌轮盘，轮盘上所占面积越大，则被小球滚到的概率就越大。

###### 交叉与变异

**交叉**是遗传算法中产生新的个体的主要操作过程，以一定的概率决定个体间是否进行交叉操作。

**变异**为另一种产生新个体的操作，它可以为种群带来多样性。

###### 遗传算法流程

遗传算法流程：

* 初始化种群
* 计算适应度
* 选择适应度高的个体
* 通过交叉变异选择新的染色体
* 终止进化

```assembly
#encoding=utf8
import numpy as np

# 染色体长度
DNA_SIZE = 10
# 解的个数，即染色体个数
POP_SIZE = 100

CROSS_RATE = 0.8 
MUTATION_RATE = 0.003    
N_GENERATIONS = 500

# 函数定义域
X_BOUND = [0, 5]

# 获取染色体适应度
# 如果是求解最大值，则函数值越大越应该被选择，所以，将每个染色体对应的函数值减去最小值作为适应度：
def get_fitness(pred): 
    return pred + 1e-3 - np.min(pred)
    
# 由于染色体为二进制编码，所以需要将二进制转换为浮点数的解码方法。
# 将二进制染色体先转为十进制，再缩放到一定的范围内。
# 如将 10101 转换到 0 到 5 之间：
# x= (2^4+2^2+2^0)/(2^5-1)*5
def translateDNA(pop):
    return pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2**DNA_SIZE-1) * X_BOUND[1]
    '''
    numpy.dot(a, b, out=None)
    计算两个数组的乘积。
    对于二维数组来说，dot()计算的结果就相当于矩阵乘法。
    对于一维数组，它计算的是两个向量的点积。
    对于N维数组，它是a的最后一维和b的倒数第二维积的和：dot(a, b)[i,j,k,m] = sum(a[i,j,:] * b[k,:,m])
    参数：
    a : array_like
    b : array_like
    out : ndarray, optional，用来保存dot()的计算结果
    '''

# 选择适应度高的染色体
def select(pop, fitness):
    idx = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True,
                           p=fitness/fitness.sum())
    '''
    numpy.random.choice(a, size=None, replace=True, p=None)
    从a(只要是ndarray都可以，但必须是一维的)中随机抽取数字，并组成指定大小(size)的数组
    replace:True表示可以取相同数字，False表示不可以取相同数字.
    数组p：与数组a相对应，表示取数组a中每个元素的概率，默认为选取每个元素的概率相同。
    '''
    return pop[idx]

#交叉
def crossover(parent, pop):
    if np.random.rand() < CROSS_RATE:
        # 随机选取一个pop的index
        i_ = np.random.randint(0, POP_SIZE, size=1)
        cross_points = np.random.randint(0, 2, size=DNA_SIZE).astype(np.bool)
        # 将pop[i_]一维数组数组中true的数据赋值到parent中的相同位置。
        parent[cross_points] = pop[i_, cross_points]                            
    return parent

# 变异
# child:一维数组(一个染色体)
def mutate(child):
    for point in range(DNA_SIZE):
        if np.random.rand() < MUTATION_RATE:
            child[point] = 1 if child[point] == 0 else 0
    return child
    
def ga(F):
    '''
    F:需要求解的函数
    x:最优解
    '''
    
    #初始化种群
    pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))
    '''
    numpy.random.randint(low, high=None, size=None, dtype='l')
    Return random integers from the "discrete uniform" distribution of
    the specified dtype in the "half-open" interval [`low`, `high`).
    If `high` is None (the default), then results are from [0, `low`).
    low : int        #产生随机数的最小值
    high : int, optional    #给随机数设置个上限，即产生的随机数必须小于high
    size : int or tuple of ints, optional    #整数，生成随机元素的个数或者元组，数组的行和列
    dtype : dtype, optional    #期望结果的类型
    '''
    
    #开始进化
    for _ in range(N_GENERATIONS):
        #计算函数值
        F_values = F(translateDNA(pop))
        #计算适应度
        fitness = get_fitness(F_values)
        #选择适应度高的个体
        pop = select(pop, fitness)
        pop_copy = pop.copy()
        #通过交叉变异选择新的染色体
        for parent in pop:
            #交叉产生子代
            child = crossover(parent, pop_copy)
            #变异产生子代
            child = mutate(child)
            #子代代替父代
            parent[:] = child
    #获取最优解
    x = translateDNA(pop)[-1]
    return x
```

##### 粒子群算法

粒子群算法 (particle swarm optimization，PSO) 由 Kennedy 和 Eberhart 在 1995 年提出，该算法模拟鸟群觅食的方法进行**寻找最优解**。基本思想：

人们发现，鸟群觅食的方向由两个因素决定。第一个是自己当初飞过离食物最近的位置，第二个因素是鸟群中离食物最近的鸟的位置。根据这个两个因素不断的改变自己的位置。最终，整个鸟群都能寻找到食物。

###### 编码与适应度函数

在粒子群算法中也需要进行编码，不过相对于遗传算法粒子群算法编码非常简单。例如，函数：
$$
f(x_1,x_2)={x_1}^2+{x_2}^2
$$
可直接将函数解(*x*1,*x*2)作为编码。而函数的值*f*(*x*1,*x*2)即可作为适应度，若求解函数最小值则适应度越小越好，若求解函数最大值则适应度越大越好。
$$
v=wv+c_1r_1(p−x)+c_2r_2(p_g−x)...(1)\\
x=v+x...(2)
$$
其中，*x*=(*x*<sub>1</sub>,*x*<sub>2</sub>,..,*x*<sub>n</sub>)为鸟群的位置，*v*=(*v*<sub>1</sub>,*v*<sub>2</sub>,..,*v*<sub>n</sub>)为鸟飞行的速度，即鸟群更新位置的因素。而公式(2)就是决定速度的因素：

* p:个体最佳位置
* pg:全局最佳位置
* w:惯性权重因子，用来控制速度的更新
* c1,c2:加速度常数，通常设为2
* r1,r2:0到1之间的随机数

###### 粒子群算法流程

* 随机初始粒子群位置与速度
* 计算粒子群适应度
* 根据公式更新粒子群位置与速度
* 重复2,3直到满足停止条件

```assembly
#encoding=utf8
import numpy as np

pop_size =10 # 粒子群大小(鸟的数量)
n_iters = 1000 # 训练轮数
dim = 2 # 搜索空间维度

w = 0.6 # 惯性权重因子
c1 = 2 # 加速度常数，通常设为2
c2 = 2 # 加速度常数，通常设为2
x_bound = [-10,10] # 函数定义域

def pso(f):
    '''
    f:目标函数
    pg:最优解坐标
    '''
    
    #初始化粒子群位置
    x = np.random.uniform(x_bound[0], x_bound[1],(pop_size, dim))
    '''
    numpy.random.uniform(low,high,size)
    功能：从一个均匀分布[low,high)中随机采样，注意定义域是左闭右开，即包含low，不包含high.
    low: 采样下界，float类型，默认值为0；
    high: 采样上界，float类型，默认值为1；
    size: 输出样本数目，为int或元组(tuple)类型，例如，size=(m,n,k), 则输出m*n*k个样本，缺省时输出1个值。
    '''
    #初始化粒子群速度
    v = np.random.rand(pop_size,dim)
    #初始个体最佳位置
    p = x
    
    #计算适应度
    fitness = f(x)
    
    #全局最优位置
    pg = x[np.argmin(fitness)]
    # argmin(a, axis=None, out=None)
    # Returns the indices of the minimum values along an axis.
    
    #个体最优适应度
    individual_best_fitness = fitness
    #全局最优适应度
    global_best_fitness = np.min(individual_best_fitness)
    
    #开始进化
    for i in range(n_iters):
        #产生随机数r1,r2
        r1 = np.random.rand(pop_size,dim)
        r2 = np.random.rand(pop_size,dim)
        
        #计算粒子群速度
        v = w*v+c1*r1*(p-x)+c2*r2*(pg-x)
        #更新粒子群位置
        x = v + x
        #计算更新后的适应度
        fitness = f(x)
        
        #需更新的个体
        update_id = np.greater(individual_best_fitness, fitness)
        '''
        numpy.greater(x1，x2 [，out])：检查x1是否大于x2。
        return:
        Boolean array indicating results, whether x1 is greater than x2 or not.
        '''
        #更新p
        p[update_id] = x[update_id]
        #更新个体最优适应度
        individual_best_fitness[update_id] = fitness[update_id]
        
        #更新全局最优位置与全局最优适应度
        if np.min(fitness) < global_best_fitness:
                    pg = x[np.argmin(fitness)]
                    global_best_fitness = np.min(fitness)
    return pg
```

##### 蚁群算法

蚁群算法是一种用来**寻找优化路径**的概率型算法。它由 Marco Dorigo 于 1992 年在他的博士论文中提出，其灵感来源于蚂蚁在寻找食物过程中发现路径的行为。基本思想：

蚂蚁在行走过程中会释放一种称为**信息素**的物质，用来标识自己的行走路径。蚂蚁会根据信息素的浓度选择寻找食物的方向。**信息素会随着时间的推移而逐渐挥发。**刚开始，地面上没有信息素，蚂蚁的行走路径是随机的。蚂蚁在寻找食物的过程中会不断释放信息素，标识自己的行走路径。随着时间的推移，有若干只蚂蚁找到了食物，此时便存在若干条从洞穴到食物的路径。由于蚂蚁的行为轨迹是随机分布的，因此在单位时间内，短路径上的蚂蚁数量比长路径上的蚂蚁数量要多，从而蚂蚁留下的信息素浓度也就越高。这为后面的蚂蚁们提供了强有力的方向指引，越来越多的蚂蚁聚集到最短的路径上去。

蚂蚁是根据信息素浓度来选择下一步行走的路线，信息素越浓，蚂蚁选择的概率越大，公式如下：
$$
p_{ij}^{k(t)}=\frac{[τ_{ij}(t)^α][η_{ij}(t)^β]}{\sum_{s\in J_k(i)}[τ_{ij}(t)^α][η_{ij}(t)^β]}
$$
*p*<sub>ij</sub><sup>k(*t*)</sup>：第 k 只蚂蚁 t 时刻，从城市 i 到 j 的概率。

*τ*<sub>ij</sub>(*t*): t 时刻蚂蚁走完一周后，城市 i 到 j 的信息素浓度。

*η*<sub>*ij*</sub>：启发式因子。
$$
η_{ij}=\frac{1}{d_{ij}}\\
τ_{ij}(t+n)=(1-ρ)τ_{ij}(t)+Δτ_{ij}\\
Δτ_{ij}=\sum_{k=1}^{m}Δτ_{ij}^k(t+n)\\
Δτ_{ij}^k=\frac{Q}{L_k}
$$
*α*：信息素重要程度。

*β*：启发式因子重要程度。

*ρ*:信息素挥发速度。

*Lk*:蚂蚁 k 在本次周游中所走路径长度。

*m*:蚂蚁个数。

*n*:城市个数。

*d*:城市之间距离。

###### 蚁群算法流程

* 初始化各个参数
* 随机放置蚂蚁到各个城市
* 对每一只蚂蚁选择下一个城市
* 走遍所有城市时，计算当前最佳路径并更新信息素浓度
* 重复2,3,4直到达到最大迭代次数
* 输出最短路径

###### 使用蚁群算法解决商队旅行问题

旅行商 (TSP) 问题：

有一队商客，他们想要去n个城市进行旅游。每个城市只能去一次。从某城市出发，最终得回到这个城市。选择出最短的路线。

```assembly
#encoding=utf8
import numpy as np

#计算距离矩阵
def getdistmat(city):
    num = city.shape[0] 
    distmat = np.zeros((num,num))
    for i in range(num):
        for j in range(i,num):
            distmat[i][j] = distmat[j][i] = np.linalg.norm(city[i]-city[j])
    return distmat
    
def aco(city):
    '''
    city(ndarray):城市位置坐标
    '''
    numant = 15  #蚂蚁个数，通常为城市数目1.5倍
    numcity = city.shape[0] #城市个数
    alpha = 1   #信息素重要程度因子
    beta = 4    #启发函数重要程度因子
    rho = 0.05   #信息素的挥发速度
    Q = 1   #信息素常数
    n_iters = 50  #迭代次数
    distmat = getdistmat(city)   #城市的距离矩阵
    etatable = 1.0/(distmat+np.diag([1e10]*numcity)) #启发函数矩阵，表示蚂蚁从城市i转移到矩阵j的期望程度
    pheromonetable  = np.ones((numcity, numcity)) # 信息素矩阵
    pathtable = np.zeros((numant, numcity)).astype(int) #路径记录表
    lengthaver = np.zeros(n_iters) #各代路径的平均长度
    lengthbest = np.zeros(n_iters) #各代及其之前遇到的最佳路径长度
    pathbest = np.zeros((n_iters, numcity),dtype=int) # 各代及其之前遇到的最佳路径长度
    
    for iters in range(n_iters):
        #随机产生各个蚂蚁的起点城市
        pathtable[:numcity, 0] = np.random.permutation(range(0, numcity))[:]
        pathtable[numcity:, 0] = np.random.permutation(range(0, numcity))[:numant-numcity]
        
        #计算各个蚂蚁的路径距离    
        length = np.zeros(numant)    
        for i in range(numant):
            # 当前所在的城市
            visiting = pathtable[i, 0]
            #未访问的城市
            unvisited = set(range(numcity))
            #删除元素
            unvisited.remove(visiting)
            #访问剩余的numcity-1个城市
            for j in range(1,numcity):    
                #每次用轮盘法选择下一个要访问的城市
                listunvisited = list(unvisited)  
                probtrans = np.zeros(len(listunvisited))
                for k in range(len(listunvisited)):
                    probtrans[k] = np.power(pheromonetable[visiting][listunvisited[k]], alpha)\
                            *np.power(etatable[visiting][listunvisited[k]], alpha)
                cumsumprobtrans = (probtrans/sum(probtrans)).cumsum()
                cumsumprobtrans -= np.random.rand()
                for n in range(len(cumsumprobtrans)):
                    if cumsumprobtrans[n] > 0:
                        break
                #下一个要访问的城市     
                k = listunvisited[n]   
                pathtable[i, j] = k   
                unvisited.remove(k)    
                length[i] += distmat[visiting][k]    
                visiting = k
            #蚂蚁的路径距离包括最后一个城市和第一个城市的距离    
            length[i] += distmat[visiting][pathtable[i,0]]
        #计算最佳路径
        lengthaver[iters] = length.mean()    
        if iters == 0:
            lengthbest[iters] = length.min()
            pathbest[iters] = pathtable[length.argmin()].copy()
        else:
            if length.min() > lengthbest[iters-1]:
                lengthbest[iters] = lengthbest[iters-1]
                pathbest[iters] = pathbest[iters-1].copy()    
            else:
                lengthbest[iters] = length.min()
                pathbest[iters] = pathtable[length.argmin()].copy()
        # 更新信息素
        changepheromonetable = np.zeros((numcity, numcity))
        for i in range(numant):
            for j in range(numcity-1):
                changepheromonetable[pathtable[i, j]][pathtable[i, j+1]] += Q/distmat[pathtable[i, j]][pathtable[i, j+1]]   
            changepheromonetable[pathtable[i, j+1]][pathtable[i, 0]] += Q/distmat[pathtable[i, j+1]][pathtable[i, 0]]    
        pheromonetable = (1-rho)*pheromonetable + changepheromonetable
    #记录历史最短路径距离    
    dist = []
    for i in pathbest:
        x = city[i][:,0]
        y = city[i][:,1]
        dist.append(np.sum(np.sqrt(np.square(np.diff(x)) + np.square(np.diff(y)))))
    #获取最短路径距离
    min_dist = min(dist)
    return min_dist
```

