---
layout: post
title:  Principles of Communications
date:   2020-10-01 00:01:01 +0300
image:  2020-10-01-horses.jpg
tags:   [note]
---

### 指数信号

$$
f(t)=ke^{-αt}
$$

* α>0递减，α<0递增
* |α|越大，函数增长越快
* 指数信号的时间常数

$$
τ=\frac{1}{|α|}
$$

### 正弦(型)信号

$$
f(t)=ksin(ωt+θ)
$$

* $$
  T=\frac{1}{f}=\frac{2Π}{ω}
  $$

  

* $$
  e^{jωt}=cosωt+jsinωt\\
  e^{-jωt}=cosωt-jsinωt\\
  sinωt=\frac{1}{2j}(e^{jωt}-e^{-jωt})\\
  cosωt=\frac{1}{2}(e^{jωt}+e^{-jωt})
  $$

### 复指数信号

$$
s=α+jω\\
f(t)=ke^{st}\\
f(t)=ke^{αt}cosωt+jke^{αt}sinωt
$$

* α>0增幅，α<0减幅
* * α=0，ω=0，直流
  * α=0，ω≠0，等幅振荡(是指在电磁振荡中，如果没有能量损失，振荡应该永远持续下去，振幅应该保持不变，由意大利科学家伽利略发现)
  * α≠0，ω=0，指数信号

### Sa(t)信号(抽样信号)

$$
Sa(t)=\frac{sint}{t}
$$

![]({{site.baseurl}}/img/2020-10-01-sa.jpg)

* ±Π，±2Π，±3Π，……，±nΠ过零点

* Sa(0)=1

* 主要能量

* $$
  \int_{-∞}^{∞}Sa(t)dt=Π\\
  \int_{0}^{∞}Sa(t)dt=\frac{Π}{2}
  $$

  

### 钟形信号

### 单位斜变(升)(坡)

$$
\begin{eqnarray}
y =
\begin{cases}
0   & t < 0 \\
t   & t \geq 0
\end{cases}
\end{eqnarray}
$$

### 阶跃信号
$$
\begin{eqnarray}
μ =
\begin{cases}
0   & t < 0 \\
1   & t > 0
\end{cases}
\end{eqnarray}\\
t=0无定义或\frac{1}{2}
$$

* $$
  μ(t)=\frac{df(t)}{dt}
  $$

* $$
  \begin{eqnarray}
  μ(t-t_{0}) =
  \begin{cases}
  0   & t < t_0 \\
  1   & t > t_0
  \end{cases}
  \end{eqnarray}\\
  $$

* 单边特性
  $$
  f(t)=e^{-αt}[μ(t)-μ(t-1)]
  $$

* 符号信号
  $$
  \begin{eqnarray}
  sgn =
  \begin{cases}
  -1 &=μ(t)-μ(-t)  & t < 0 \\
  1  &=2μ(t)-1     & t > 0
  \end{cases}
  \end{eqnarray}\\
  $$
  

### 冲激信号

定义：矩形面积不变，宽趋于0时的极限
$$
{\lim_{τ \to 0}}\frac{1}{τ}[μ(t+\frac{τ}{2})-μ(t-\frac{τ}{2})]
$$
![]({{site.baseurl}}/img/2020-10-01-chongji.jpg)

* $$
  \int_{-∞}^{∞}σ(t)dt=1
  $$

  

--------------------------------

9月29日

## 傅里叶变换

$$
F(w)=\int_{-∞}^{∞}f(t)e^{-jωt}dt\\
f(t)=\frac{1}{2Π}\int_{-∞}^{∞}F(W)e^{jnωt}dω
$$

