---
layout: post
title:  物联网设备渗透实战思路
date:   2021-01-13 00:01:01 +0300
image:  2021-01-13-books.jpg
tags:   [IoT]
---

## 物联网设备安全概述

物联网设备层次

* 物理感知层（固件提取、硬件攻击（强磁场等））

* 通信层（流量监听、中间人攻击）

* 管理控制层/应用层（web、rtsp、ssh……）

物联网通信模型

* 云端安全风险
* 客户端（APP）安全风险
* 设备自身安全风险

IoT设备信息收集

* 端口扫描
  * 直接进行命令执行
* 流量抓取、分析（外部嗅探/内部调试）
  * 交换机端口镜像
  * wireshark
  * tcpdump
* 功能点评估
  * 摄像头rtmp

端口扫描

* 常规扫描
* 指定UDP扫描

```assembly
nmap -sV -sU -Pn --open 192.168.0.1
```

![img]({{site.baseurl}}/img/IoTPenetrating/HNIDRUS81_UJ5`RA6@O4ZNX.png)

物联网设备渗透所需技能

* 渗透测试
* 二进制逆向分析
* 硬件拆焊

反汇编工具：IDA/Ghidra

流量分析：wireshark/tcpdump/Burp suite

固件分析工具：binwalk/qemu（固件模拟）

## 物联网设备漏洞点分析

输入

导出配置文件

### 基于Web安全的漏洞风险

**未授权访问**

* 认证绕过

  * 敏感路径不需要认证。认证可绕过，如直接访问view.html、system.html

  * Cookie伪造

  * 其他奇怪的姿势

    ![@U44CSRRRNSF~TD@N5FVU7]({{site.baseurl}}/img/IoTPenetrating/@U44CSRRRNSF~TD@N5FVU7.png)

    ![G~7~O23ZYPEEDJRFBT]({{site.baseurl}}/img/IoTPenetrating/G~7~O23ZYPEEDJRFBT.png)

    字符串提取查找路径

    ![SVQP6YTA42@GN%_Q0ROPC]({{site.baseurl}}/img/IoTPenetrating/SVQP6YTA42@GN%_Q0ROPC.png)

    ![53Z``9J@EGY`M92QGV`I8]({{site.baseurl}}/img/IoTPenetrating/53Z``9J@EGY`M92QGV`I8.png)

    ![JJ%CPU1TB3A4I1O1~SW4]({{site.baseurl}}/img/IoTPenetrating/JJ%CPU1TB3A4I1O1~SW4.png)

* 弱密码
  * 任意密码登录
  * 常见密码爆破

https://github.com/ihebski/DefaultCreds-cheat-sheet

门槛低

黑灰产/僵尸网络广泛利用

**命令注入**

开发者未对用户可控的输入参数（可控数据）进行验证或者过滤，导致攻击者可以构造恶意的payload，达到执行系统命令的效果。

### 逻辑漏洞风险

* 任意文件读取

  * 存在路径穿越，没有过滤../、/../

  * 符号链接漏洞

    ![JOLM7IM~3KOWY3XH@`D]({{site.baseurl}}/img/IoTPenetrating/JOLM7IM~3KOWY3XH@`D.png)

    ![K488_DLEELHPV~`SX2G]({{site.baseurl}}/img/IoTPenetrating/K488_DLEELHPV~`SX2G.png)

* 任意密码重置

### 基于固件二进制的漏洞风险

固件获取

固件解包

逆向分析

漏洞风险

* 堆/栈溢出

  程序对用户的可控输入验证不足，导致攻击者可以输入过长的数据到栈缓冲区上，非法覆盖栈上的内容。

  ![1@Z1FJRQ_@GFNSA~HYJWQ]({{site.baseurl}}/img/IoTPenetrating/1@Z1FJRQ_@GFNSA~HYJWQ.png)

  ![7OJRG9`HCLVCFIVQQ]({{site.baseurl}}/img/IoTPenetrating/7OJRG9`HCLVCFIVQQ.png)

* 拒绝服务

  固件代码逻辑验证不足造成指针异常，进而导致程序非正常崩溃，造成设备服务无法正常访问。

  ![YGF2GKQ$D4RF3GBWVAI1]({{site.baseurl}}/img/IoTPenetrating/YGF2GKQ$D4RF3GBWVAI1.png)

  ![MJ9Q`T%TJK``@B875UXC]({{site.baseurl}}/img/IoTPenetrating/MJ9Q`T%TJK``@B875UXC.png)

* 整数溢出

* 越界读写

* 命令注入

### 基于通信/私有协议的漏洞风险

### 云端安全风险

* 传统web安全风险（SQL注入、命令注入）

* 越权访问

  ![JN@BE~T0MJ8UQFZO24]({{site.baseurl}}/img/IoTPenetrating/JN@BE~T0MJ8UQFZO24.png)

### 后门漏洞风险

* 服务访问后门（Web服务/Rtsp服务/……）

  ![01`B6CXAFFX07_@E6C7`X5]({{site.baseurl}}/img/IoTPenetrating/01`B6CXAFFX07_@E6C7`X5.png)

  ![$W~Q639MDGEX0S7WMFTP]({{site.baseurl}}/img/IoTPenetrating/$W~Q639MDGEX0S7WMFTP.png)

  ![3958G9@9BGY$KP6803]({{site.baseurl}}/img/IoTPenetrating/3958G9@9BGY$KP6803.png)

* 调试后门（软/硬件）

  ![1384R%_5R5_VICS~UC]({{site.baseurl}}/img/IoTPenetrating/1384R%_5R5_VICS~UC.png)

## 物联网设备常见漏洞挖掘方法

### 固件逆向之分析输入点

寻找二进制中统一的cgi输入接口函数

getenv("HTTP_HOST")

get_cgi("device")

websGetvar(wp,"device_id","")

……

### 固件逆向之敏感函数/代码段回溯

合理借助反汇编工具（IDA/Ghidra）脚本

列出引用system的函数地址

```assembly
import ida
import idc
system_list = set()
for loc,name in Names():
    if "system" == name:
        for addr in XrefsTo(loc):
            system_list.add(addr.frm)
print(system_list)
```

### 模糊测试（通信协议/固件）

端口fuzz

```assembly
cat  /dev/urandom | nc 192.168.0.1 9898

cat /dev/random | nc 192.168.0.1 9898
```

Burp Suite

协议fuzz工具（boofuzz/peach）