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
\begin{equation*}
f(t)=\sum_{n=-∞}^∞F(nω_1)e^{jnω_1t}\\
\end{equation*}
F(n)=\frac{1}{T}\int_{-\frac{T}{2}}^{\frac{T}{2}}f(t)e^{-jnωt}dt\\
F(w)=\int_{-∞}^{∞}f(t)e^{-jωt}dt\\
f(t)=\frac{1}{2Π}\int_{-∞}^{∞}F(W)e^{jnωt}dω
$$

10.13
$$
\mathscr{F}[f_0(t)]=F_0(ω)=\int_{-\frac{T}{2}}^{\frac{T}{2}}f(t)e^{-jωt}\\
F_n=\frac{1}{T_1}F_0(ω)|_{ω=nω}\\
\mathscr{F}[f(t)]=2Π\sum_{n=-∞}^∞F_nσ(ω-nω_1)
$$

![]({{site.baseurl}}/img/2020-10-18-1.jpg)

* 注意T和ω之间的关系和化简

![]({{site.baseurl}}/img/2020-10-18-2.jpg)

![]({{site.baseurl}}/img/2020-10-18-3.jpg)

* ×1/2

![]({{site.baseurl}}/img/2020-10-18-4.jpg)

* 频率分量

![]({{site.baseurl}}/img/2020-10-18-5.jpg)

![]({{site.baseurl}}/img/2020-10-18-6.jpg)

![]({{site.baseurl}}/img/2020-10-18-7.jpg)

![]({{site.baseurl}}/img/2020-10-18-8.jpg)

* f(t)中的ω和e<sup>-jωt</sup>中的ω不是同一个ω，不要弄混了
* sin()，cos()利用欧拉公式变指数形式

![]({{site.baseurl}}/img/2020-10-18-9.jpg)

* 傅里叶变换的性质

![]({{site.baseurl}}/img/2020-10-18-10.jpg)

![]({{site.baseurl}}/img/2020-10-18-11.jpg)

![]({{site.baseurl}}/img/2020-10-18-12.jpg)

##### 傅里叶变换的对称性

![]({{site.baseurl}}/img/2020-10-18-13.jpg)

![]({{site.baseurl}}/img/2020-10-18-14.jpg)

![]({{site.baseurl}}/img/2020-10-18-15.jpg)

* 傅里叶变换微积分性质

![]({{site.baseurl}}/img/2020-10-18-16.jpg)

![]({{site.baseurl}}/img/2020-10-18-17.jpg)

![]({{site.baseurl}}/img/2020-10-18-18.jpg)

* 傅里叶逆变换

![]({{site.baseurl}}/img/2020-10-18-19.jpg)

![]({{site.baseurl}}/img/2020-10-18-20.jpg)

![]({{site.baseurl}}/img/2020-10-18-21.jpg)

![]({{site.baseurl}}/img/2020-10-18-22.jpg)

![]({{site.baseurl}}/img/2020-10-18-23.jpg)

![]({{site.baseurl}}/img/2020-10-18-24.jpg)

![]({{site.baseurl}}/img/2020-10-18-25.jpg)

![]({{site.baseurl}}/img/2020-10-18-26.jpg)

![]({{site.baseurl}}/img/2020-10-18-27.jpg)

11-13

某一特殊传输的图片，含2.25×10<sup>6</sup>个像素，为了很好的重现图片，每个像素需要16个亮度电平。假如所有这些亮度电平等概率出现，试计算用3min传输一张图片所需要的传递最小带宽（信道中信噪比为1023）.
$$
\begin{align*}
&log_216=4bit/Pix\\
&2.25×10^6×4=9×10^6bit/Picture\\
&C=\frac{9×10^6}{3×60}=5×10^4b/s=Blog_2(1+1023)\\
&B=5000Hz
\end{align*}
$$
