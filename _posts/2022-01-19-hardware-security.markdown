---
layout: post
title:  硬件安全技术
date:   2022-01-19 00:08:01 +0300
image:  2022-01-19-chess.jpg
tags:   [note,hardware]
---

## 硬件安全综述

### 硬件安全

#### 传统视角：

硬件安全=密码芯片安全，特别是智能卡、可信计算、Ukey等芯片的攻防技术

* 密码芯片的逻辑接口、物理接口安全
* 核心功能：具备放攻击能力，能有效保护密钥存储、进行安全密码运算

#### 智联时代

* 万物互联+智能化：端云协作、数字孪生、海量数据
* 网络攻击进入物理世界

#### 新视角

* 芯片和固件密不可分
* 系统信任根由硬件+底软保护
* 底层有漏洞，系统完破

除了保护芯片，还要保护软件

### 硬件安全无处不在

#### IoT主控

软件层

* 固件认证和加密
* 芯片唯一ID
* 数据加解密

硬件层

* ROM安全
* Key/ID存储安全
* 硬件加解密模块
* 随机数发生器

#### 智能手机应用处理器

软件层

* APP安全
* 数据存储安全
* 通信安全
* 固件安全
* 可信执行环境

硬件层

* ROM安全
* Key/ID存储安全
* 硬件加解密模块
* 随机数发生器

#### 云服务器处理器

软件层

* 应用安全
* 网络安全
* Guest OS安全
* 固件安全
* 可信执行环境
* 虚拟化

硬件层

* ROM安全
* Key/ID存储安全
* 硬件加解密模块
* 随机数发生器
* 硬件虚拟化

### 全生命周期安全设计

如何在开放供应链上构建信任根和信任链

* 密钥安全、固件安全、测试调试安全

### 硬件安全技术

* 硬件安全架构
  * 安全生命周期管理
  * 测试调试端口
  * 固件安全
  * 可信执行环境

* 物理攻击技术

  * 侧信道攻击技术（Side-Channel Analysis，SCA）

    * 使用**顺势功耗**、**电磁辐射**、**光子泄露**、**计算时间**等侧信道信息。
    * 不需破坏芯片或修改软件，攻击门槛低，威胁大。
    * 防侧信道攻击时安全芯片的主要技术难点之一

    **微架构侧信道（MASCA）**

    微架构侧信道分析：利用处理器架构特点，获取与敏感信息（如密钥）相关的信息泄露（如timing），破解系统安全防护。

    * Meltdown & Spectre：滥用CPU推演执行功能，构造攻击场景，对大量Intel CPU有效。
    * FORESHADOW：滥用CPU推演执行破解SGX。
    * NCC Qualcomm QSEE攻击：利用分支预测和cache的时许泄露，获取Trustzone之中的ECDSA私钥。

  * 故障注入攻击技术（FA）

  * 侵入式攻击技术（IA）

  * 组合攻击技术

* 硬件安全元和抗攻击设计
  * 侧信道攻击防护技术
  * 故障注入防护技术
  * 随机数发生器
  * 物理不可克隆函数
  * 安全版图设计

* 面向软件安全的硬件设计
  * 软件流程保护
  * 安全指令拓展
  * 远程代码认证
  * 虚拟化
  * 可信启动

### 安全设计的内在挑战

攻击者变得更强

产品设计考虑——产品实际面对

系统复杂度变大（网络拓朴、芯片架构、软件应用、算法演进）

## 5G时代IoT环境下芯片安全风险与挑战

### 5G时代下的IoT

随着5G技术的发展，大通量，低时延的通讯成为可能，这给物联网世界带来迅猛的发展，智慧交通，智慧医疗，智慧电网，这些年逐步走进生活成为现实。

爆炸式的终端互联，已经进入每一个家庭。到2019年，消费物联网终端数量已经达到60亿，工业物联网终端超过50亿。

按照终端使用情况，我们可以把终端分为三类

* 消费性物联网终端（扫地机器人、手机）
* 公共性物联网终端（路灯、电表）
* 生产性物联网终端

5G、AI、智能IOT的有机结合是物联网终端设备发展的趋势。

#### 5G时代下的IoT智慧应用分层

* 智慧应用层
* 数据与服务融合层
  * 数据融合
    * 数据采集
    * 数据挖掘分析
    * 数据处理
    * 数据管理
  * 服务融合
    * 服务采集
    * 服务整合
    * 服务处理
    * 服务管理
* 计算/存储层
  * 算力资源
  * 存储资源
  * 软件系统资源
  * 硬件资源
* 网络通信层
  * 公共网络
  * 私有网络
  * 专有网络
* 物联感知层
  * 感知设备
    * 环境感知
    * 安全感知
    * 身份感知
    * 位置感知
  * 执行设备
    * 环境控制
    * 安全执行
    * 通告警示
    * 环境感知

#### IoT智慧应用建设特点——复杂/管控难

复杂系统，技术/安全参数不齐，方案各异

* 安全系统集成安全
* 代码安全控制
* 设备可信管理
* 安全溯源机制
* 系统可信传递
* 数据可信共享

#### IoT云管端各处的安全防御要点

* 云（物理环境安全、主机安全、数据安全、应用安全）
  * 机房安全
  * 账号管理
  * WAF
  * 网络隔离
  * 反DDOS
  * 入侵检测
  * 访问控制
  * 漏洞扫描
  * 数据加密
  * 身份认证
  * 日志监控
  * 数据脱敏
* 管（应用层协议安全、设备接入与认证安全、应用层协议安全）
  * WIFI安全
  * 移动通信
  * HTTPS安全
  * BLE安全
  * 设备ID
  * MQTT安全
  * ZigBee安全
  * 双向认证
  * COAP安全
  * LoRaWAN安全
  * 通信加密
* 端（硬件安全（物理安全、PCB安全、传感器安全、芯片安全）、软件安全（系统安全、应用安全））
  * 物理防护
  * SE & TEE
  * 代码安全
  * PCB安全
  * 可信启动
  * 安全SDK
  * 传感器安全
  * 系统加固
  * 日志上报
  * 芯片安全
  * 安全OTA

IOT设备数量爆炸，不可能做到每一个设备都进行测试与管控，但是我们可以通过对设备使用芯片的安全管控来达到整体安全提升的自的。并且会有专门的第三方认证机构进行安全认证，国家在这块已经有相应的参考标准与实验室。

IOT的供应链极长，供应链安全的管理也是其中的重点部分，未来区块链的应用也许会大量落地。

### IoT产品面临的实际威胁

#### 海外物联网安全事件

从2019年3月7日傍晚（当地时间)开始，委内瑞拉国内，包括首都加拉加斯在内的大部分地区，持续停电超过24小时。电力系统遭遇了三阶段攻击。第一阶段是发动网络攻击，主要针对西蒙·玻利瓦尔水电站，即国家电力公司(CORPOELEC)位于玻利瓦尔州古里水电站的计算机系统中枢，以及连接到加拉加斯（首都)控制中枢发动网络攻击;第二阶段是发动电磁攻击，“通过移动设备中断和逆转恢复过程”;第三阶段是“通过燃烧和爆炸”对采兰达州Alto Prado变电站进行破坏，进一步瘫痪了加拉加斯的所有电力。

2019年7月24日，网络安全公司lmperva公司表示，他们一个娱乐行业的CDN客户在2019年四月至五月期间受到了大规模DDoS攻击。该攻击针对站点的身份验证组件，由一个僵尸网络领导，该僵尸网络协调了402000个不同的IP，发动了持续13天的DDoS攻击，并达到了29.2方RPS 1的峰值流量和每秒5亿个数据包的攻击峰值，这是lmperva迄今为止观察到最大的应用层DDoS攻击。

2019年7月24日，网络安全公司lmperva公司表示，他们一个娱乐行业的CDN客户在2019年四月至五月期间受到了大规模DDoS攻击。该攻击针对站点的身份验证组件，由一个僵尸网络领导，该僵尸网络协调了402000个不同的IP，发动了持续13天的DDoS攻击，并达到了29.2方RPS 1的峰值流量和每秒5亿个数据包的攻击峰值，这是lmperva迄今为止观察到最大的应用层DDoS攻击。

2019年1月25日，日本通过了一项法律修正案，允许政府工作人员入侵物联网设备。修正案的内容包括两点，一是允许日本国家信息和通信技术研究所(NICT）通过弱口令对物联网设备进行扫描从而发现脆弱的设备，二是NICT可以将这些信息作为威胁情报共享给电信运营商。与之相对应，日本从2019年2月20日起启动NOTiCE项目[32]，开始对互联网上的物联网设备进行调查，识别易受攻击的设备，并将这些设备的信息提供给电信运营商。

#### IoT终端设备安全需求

| 编号 | 安全需求         | 需求详细说明                                                 |
| ---- | ---------------- | ------------------------------------------------------------ |
| 1    | 设备身份认证安全 | 1.特指服务器能安全、唯一地识别终端设备身份。终端身份具有唯一、不可更改、不可抵赖的安全特性。 |
| 2    | 设备固件安全     | 1.特指固件生命周期中的完整性和保密性<br>2.固件存放在终端NVM上安全，不易被通过拆机、远程读取等方式获得。<br>3.固件下载和升级过程安全，系统能验证固件的完整性（Integrity and authenticity），系统具有防止版本回滚的功能。<br>4.固件下载和升级过程中，黑客无法获得固件明文 |
| 3    | 数据传输安全     | 1.特指特征值在传输过程中的安全，包括<br>   ·服务器→终端传输<br>   ·终端→服务器传输<br>   ·终端→终端传输 |
| 4    | 数据存储安全     | 1.特征值在终端存储安全，包括<br>   ·特征值的保密性<br>   ·特征值的完整性（Integrity and authenticity） |
| 5    | 生命周期安全     | 1.特指芯片从出厂到设备过程，生命周期安全<br>   ·生命周期标志<br>   ·测试和调试端口保护 |
| 6    | 密钥管理安全     | 1.特指使用了密码技术后，后台密钥管理系统的安全<br>2.服务器整合终端形成完整的密钥管理<br>3.利用密钥管理实现人员权限区分<br>4.密钥导入/导出/更新安全 |

### 如何做好芯片的核心防护

芯片服务于应用，芯片安全最终是为了防护应用信息安全。

#### 以密钥和密码算法来武装芯片系统

合理的密钥和密码算法的设计赋予安全基石，结合硬件隔离技术建立整个芯片安全系统。

* 安全应用
  * 结合证书，建立应用安全可信传输
  * 系统结合芯片设计提供应用可信隔离
* 系统安全
  * 基于安全启动构建可信OS
  * 结合固件构建数据安全存储
* 固件安全
  * 公钥、非公钥、hash算法构建安全启动
  * 对称密钥、对称算法构建固件的加密存储
  * 对称密钥、对称算法构建固件安全导入
* 密钥和密钥算法
  * 对称密钥、非对称密钥、证书
  * 对称算法、非对称算法、hash算法、自研算法

#### 以方案将应用与芯片串联

以AI芯片防护为例，使用安全方案将芯片的安全属性付给AI的敏感信息

* 密钥管理
  * 密钥/证书安全存储
  * 密钥/证书安全使用
  * 密钥/证书安全导入
  * 密钥安全管理与拓展
* 特征值存储
  * 片上唯一密钥加密存储
  * 访问权限控制
  * 特征值有效自毁
* AI算法模型
  * 片上唯一密钥加密存储
  * 访问权限控制
  * 安全更新机制
  * 算法模型有效自毁
* 固件管理
  * 固件安全存储
  * 固件安全启动
  * 固件安全隔离
  * 固件安全导入
* 特征值传输
  * 传输双向身份认证（TLS）
  * 传输加密
  * 特征值有效更新

#### 标准出发的安全设计

从应用领域出发引出相关标准/认证，从认证/标准出发设计定义安全芯片。

以安全芯片为核心安全能力模块，向上满足响应的标准与认证，从而满足各个应用层的安全。

* 安全保障体系

  * 安全认证

    * IFAA认证
    * 金融认证（POS/EMVco）
    * TEE认证（GP/TAF）
    * CC认证
    * CA认证
    * DRM认证
    * 国密认证
    * 车规认证
    * TCG认证
    * FIBS认证

  * 安全标准

    * GDPR隐私

    * 车规标准

    * CA标准（Nagra/Irdeto/NDS）

    * CC标准（国际/中国）

    * TCG标准（TPM/存储/TPMC）

    * 国密标准

      安全芯片检测内容

      * 密码算法
      * 安全芯片接口
      * 密钥管理
      * 敏感信息保护
      * 固件安全
      * 自检
      * 审计
      * 生命周期保证
      * 攻击的削弱与防护（一级可选）

    * 视频监控标准（35114）

    * DRM标准（china/微软/谷歌）

    * 金融支付标准（EMCco/POS）

    * TEE标准（GP/TAF）

    * FIBS标准

* 安全芯片

  * 系统方案
    * TEE安全
    * 车规设计
    * 固件安全
    * 安全视频路径
    * 自检方案
    * 密钥管理方案
    * 版图防护方案
    * 敏感信息防护方案
    * 生命周期管理方案
    * 安全启动方案
  * IP
    * 抗攻击密码IP
    * 主动防护层
    * Sensor
    * TRNG
    * 国密算法IP
    * 国际算法IP
    * MPU
    * NVM加扰
    * RDM/RAM加扰
    * BUS加扰

## 芯片安全设计技术

### 常见的对称算法

分组密码

* AES（Advanced Encryption Standard）

  密钥长度：128、192、256

  轮数：10、12、14

  加解密的SBOX不同

  加解密使用轮密钥的顺序不同

  ECB模式

  实际加密的数据往往大于8字节或16字节，最简单的方式就是将数据分割为若干个分组后将对这些分组分别加密，也就是ECB模式。

  缺点：明文块相同，得到的密文块也是相同的，并且位置一一对应，明文数据上结构信息泄露，对于图片的加密效果很差。

  加密模式：

  * ECB（Electronic Code Book mode）

  * CBC（Cipher Block Chaining mode）

  * CTR（CounTeR mode）

  * GCM（Galois/Counter Mode）

    网络通信加密的常用模式

    * NISP SP800-38D
    * 既可以对数据加密，也可以用于提供校验值（Auth Tag）
    * 处理速度可以比CBC快，因为加解密部分可以并行处理。

  * XTS（XEX-based Tweaked-codebook mode with ciphertext Stealing）

    数据存储的常用模式

    * NIST SP800-38E
    * 无需IV
    * i为sector number
    * 可随机访问
    * 如有需要，可并行处理，得到更高的性能。

* DES/TDES（Data Encryption Standard）

* SM4

流密码

* ZUC
* Chacha20

#### 常见的使用模式及场景

##### 数据存储

Android 7.0及更高版本支持文件级加密(FBE)。采用文件级加密时，可以使用不同的密钥对不同的文件进行加密，也可以对加密文件单独解密。

所有加密都基于采用XTS模式的AES-256算法。内核中的加密性能必须要在使用AES XTS时至少达到50MB/s，以确保良好的用户体验。

##### 网络通信

SSL/TLS(Secure SocketLayer 安全套接层)是基于HTTPS下的一个协议加密层。

TLS通信中数据都会使用对称密码算法进行加密，密码算法的种类在握手阶段进行确认。

TLS_AES_128_GCM_SHA256为TLS v1.3的必选算法

#### 常见的抗攻击设计

##### 侧信道攻击防护

* 对中间值进行随机化处理，往往通过对中间值异或掩码来达到随机化中间过程的目的
  * 线性操作往往使用布尔掩码
  * 非线性操作使用乘法掩码、随机掩码和固定值掩码
* 增加随机延迟或伪操作（无法确定是否真的在算）
  * 在功耗上无法区分延迟/伪操作，使得攻击者无法对齐功耗曲线

##### FI（错误注入）防护

* 多次操作校验是否计算结果相同
  * 可以使用加密后解密来判断明文是否一致，对运算前后几轮需要重点关注
* 关键参数保存CRC
  * 例如密钥的CRC值可以由硬件保存，不定时计算目前使用的密钥CRC值是否一致

##### SBOX的设计实现策略

* 硬件上有两种主要实现方式
  * 使用查找表
  * 二项式求逆
* SMIC，100MHz，查找表的频率比二项式求逆的频率大

##### 轮密钥的计算逻辑

使用两个寄存器来存储轮密钥，RegA存储第一轮或最后一轮轮密钥，RegB用于存储当前的轮密钥。

需要有标识标志RegA存储的为第一轮还是最后一轮轮密钥。

在一个时钟周期只进行一轮（或较少轮数）运算时，避免在一开始就将轮密钥全部扩展完成，占用大量寄存器。

避免将轮密钥全部展开。

##### 密钥的管理

* 关键密钥

  关键密钥由硬件管理，软件不可见或控制访问权限，例如根密钥

* 应用密钥

  应用密钥由软硬件协调管理，增加灵活性，例如会话密钥

##### 指令集加速

通过查看CPU信息确认是否支持

```assembly
grep aes -o -ml /proc/cpuinfo
```

openssl1.0.1版本后，运行时期自动检测是否支持AES-NL，只有使用openssl EVP的接口定义函数才能够使用AES-NI。

#### 总结

根据应用场景选择合适的算法和模式，根据标准规范使用。

大多数算法还是可以使用空间换时间的方式进行加速。

物理安全设计包含前端、后端整个IC设计流程，安全性措施在设计完成后还需要经过实验室的测试。

常用的硬件对密码算法往往有加速支持。

### 常见的公钥密码算法

公钥密码学于1976年由Whitfield Diffe、Martin Hellman和Ralph Merkle公开介绍。

公钥密码技术是20世纪最伟大的思想之一改变了密钥分发的方式。可以广泛应用于数字签名和身份认证服务。

1977年提出的RSA成为以后使用最广泛的一种非对称密码算法

##### RSA算法

1977年由Ronald Rivest、Adi Shamir和Leonard Adleman发明，1978年公布。算法名称取自于作者的名字首字母。

1993年发布了PKCS#1标准来说明RSA的使用规范。2000年RSA专利到期（当时ECC专利还未到期)。

如今，只有短的RSA密钥才可能被强力方式解破。到2019年为止，还没有任何可靠的攻击RSA算法的方式。RSA-2048至今还是安全的。

##### 椭圆曲线密码

点乘运算可以转换为点加和倍点运算。主要运算为点乘，P和Q为椭圆曲线上的点，k为标量，Q=kP，知道P和Q，很难得到k。

点乘运算类似模幂运算

9(0b1001)P = (2(2(2P))) + P

#### 不同公钥算法安全级别对比

| 算法家族 | 密码体制         | 安     | 全     | 级     | 别      |
| -------- | ---------------- | ------ | ------ | ------ | ------- |
|          |                  | 80     | 128    | 192    | 256     |
| 因数分解 | RSA              | 1024位 | 3072位 | 7680位 | 15360位 |
| 离散对数 | DSA、DH          | 1024位 | 3072位 | 7680位 | 15360位 |
| 椭圆曲线 | ECDSA、ECDH、SM2 | 160位  | 256位  | 384位  | 512位   |
| 对称密钥 | AES、SM4         | 80位   | 128位  | 192位  | 256位   |

#### 常见的使用场景

##### 非对称算法应用

* 签名、验签

  私钥用于签名，公钥用于验签，确认签名者的身份

* 密钥协商

  双方协商出一个共同的密钥

* 加密、解密

  公钥用于加密、私钥用于解密，该方式加解密代价较大

##### 网络认证

客户端需要验证服务端的身份或者服务端验证客户端的身份，在双方验证完身份后，通过协商的密钥。

在握手阶段需要进行验签、密钥交换操作。

##### 安全启动

目前越来越多的设备使用了安全启动来保证安全，防止固件等被第三方篡改。

验证固件/应用的签名，但验证失败，无法进入下一阶段。

##### 新兴应用V2X

频繁对周围设备发来的位置信息进行验签。

验签速度远远大于签名速度，验签速度大约在2000次/秒左右。

目前的规范大多使用了ECDSA。

##### 嵌入式设备的实际应用

嵌入式设备往往都有mbedtls

mbedTLS(前身PolarSSL)是一个由ARM公司开源和维护的SSL/TLS算法库。其使用C编程语言以最小的编码占用空间实现了SSL/TLS 功能及各种加密算法。

mbedTLS 软件包提供了如下的能力

* 完整的SSL v3、TLSv1.0、TLS v1.1和TLS v1.2协议实现
* X.509证书处理
* 基于TCP的TLS传输加密
* 基于UDP的DTLS（Datagram TLS）传输加密-其它加解密库实现

##### RSA、ECC的选择

* RSA的验签速度可以做到很快

  在例如安全启动的场景下，如果对启动速度很敏感则有优势

* ECC的验签速度一般比签名速度慢

  如果使用ECDSA且未经过优化，签名速度一般是验签速度的两倍

* RSA的存储占用远远大于ECC

  对SRAM敏感的场景下，建议使用ECC算法

* RSA的密钥生成速度远远小于ECC。

#### 常见的抗攻击设计

##### 点乘/横幂的防侧信道保护

点乘

* 固定时间：蒙哥马利阶梯
* 标量掩码：标量加上阶的随机倍数
* 随机坐标：对投影坐标进行随机化处理

横幂

* 固定时间：蒙哥马利阶梯
* 指数掩码：对幂指数进行拆分
* 底数掩码：对底数乘上随机数，在得到最终结果前脱掩

##### 验签的防FI保护

* 硬件多次校验
* 多次校验之间使用随即延迟
* 如果使用了蒙哥马利阶梯，可以利用两数之间的关系进行校验
* 参数进行CRC校验

##### 层次化设计

根据运算调用关系进行分层

* 底层的运算被调用频率高，使用硬件有利于增加运算效率。
* 顶层协议级运算考虑使用软件设计以增加灵活性，但需要考虑硬件的中断设计，在硬件运算时可以释放CPU资源。

金字塔

* SM2、ECDSA
* 横幂、点加、倍点、点乘
* 横乘、模加减、模逆

##### 选取合适的坐标系

* 标准射影坐标系

  当P是大于3的素数时，Fp上椭圆曲线方程在标准射影坐标系下可以简化为`y2z=x3+axz2+bz3`，其中a，b∈Fp

* 雅可比（Jacobian）坐标系

  Fp上椭圆曲线方程在Jacobian射影坐标系下可以简化为`y2=x3+axz4+bz6`。其中a，b∈Fp。

##### 预计算加速（软件实现中较多）

* 对基点进行预计算
  * 提前计算如3P、5P等数值（P为基点）
  * 25（0b1 10 01）P = （（P\*2\*2 + 2P）* 2 * 2）+ P = 6P * 2 * 2 + P = 25P 
* OpenSSL的预计算优化
  * OpenSSL对secp256r1曲线进行了大量预计算，所以使用secp256r1进行运算的性能远远大于其他曲线。
  * 使用存储空间来换时间。

##### 使用SIMD指令进行加速

各家都有自己的SIMD指令

* Intel：AVX2/SSE
* ARM：NEON

利用SIMD特性，能够使运算提升数倍。

#### 总结

公钥算法用于身份识别，主要应用为签名/验签。

ECDSA/ECDH和RSA是主流的公钥密码体系中的算法，SM2是国内主要的公钥密码算法。

公钥密码算法往往有吞吐数据量小、运算时间长的特性。

口由于公钥算法比较复杂，可以优先考虑已有实现，避免反复造轮子。但要有优势，软硬件结合是最好的方式。

### 硬件安全解决方案

#### 为什么需要硬件安全

安全是系统级的，如果只是用软件进行安全防护，那么无法建立强有力的信任根。

Crypto Engine只是解决了密码计算问题，只是单纯的拼凑组合是无法组成安全系统的。

各种高等级的认证要求底层的核心安全/密码实现需要由硬件完成或参与完成。

#### 传统安全解决方案对比

|              | MCU      | TEE      | SE       |
| ------------ | -------- | -------- | -------- |
| 敏感信息存放 | 通用区域 | 可信区域 | 安全区域 |
| 密码算法     | 软件     | 软件     | 硬件     |
| 运算时间     | 长       | 长       | 短       |
| 身份识别     | 弱       | 中       | 强       |
| 物理安全     | 弱       | 弱       | 强       |
| BOM成本      | 低       | 中       | 高       |
| 使用成本     | 低       | 中       | 高       |

#### SoC安全解决方案

* 将传统SE的功能集成到SoC中，避免了板级走线带来的安全风险。
* 避免了外部的数据传输性能瓶颈，可以作为加速器使用
* 无需额外芯片，降低了整体成本。
* 目前手机AP厂商大多数使用该解决方案。

### Root of Trust（信任根）

Root of Trust（RoT）是建立信任链（chain of trust）的来源，也是SoC中的安全根基。

* 安全启动

  硬件负责初始化安全启动过程中需要使用的模块，例如随机数发生器、安全传感器、NVM控制器等。

  CPU从自身ROM中读取一级启动代码，对外部的二级Bootloader进行解密和验签，确保二级Bootloader的完整性和认证性。

* 密钥管理

  * 保护密钥的机密性
  * 确认密钥的完整性
  * 提前考虑各种角色，确保在实际场景中的可用性
  * 结合芯片生命周期管控烧写、使用、Debug相关权限

### 关键安全模块

**MPU**

* 访问地址、权限隔离

**Crypto Engine**

* 提供各种密钥运算的支持
* 提升密钥运算的性能和安全性
* 避免软件可以访问关键密钥

**Detector**

* 探测环境的异常变化

**Storage Protection Unit**

* 保护存储单元内的数据，地址总线和数据总线都需要加密/加扰

**Bus Protection Unit**

* 保护总线上传输的信息，地址和数据都需要加扰

**Secure Processor**

* 利用Memory Tagging等技术防止关于Memory的攻击
* 利用Time constant技术防止Timing Attack

### 安全系统的应用

智能电表是loT的典型安全敏感应用。

智能电表处于一个开放的不可控环境下。

智能电表覆盖量极大且与基础民生相关，有着很高的价值。

智能电表是一个典型的基于MCU的SoC芯片，SoC中有着多种防护措施保护RoT和运行环境。

### 总结

安全系统方案多种多样，根据实际业务场景进行选择。

单一模块无法保证系统安全，系统安全需要从硬件、软件、生产和使用统筹考虑。

RoT需要由硬件来实现从而达到不可篡改的特性。

随着新兴行业(loT、5G)的发展，硬件安全的重视程度逐渐提升。

## 物理不可克隆函数PUF及其应用

### 什么是PUF

A function module that uses the process uncertainty in the production process to generate unique chip characteristics.

Enhance the chip's ability to resist reverse attack.

A kind of "chip fingerprint".（芯片指纹）

* Uniqueness
* Anti cloning
* Unpredictability（芯片制造出之前无法预测）
* Tamper proofing
* No storage required（每次上电时从芯片中提取）

#### PUF Architecture

* SRAM PUF
* Arbiter PUF（利用延迟）
* RO PUF
* VIA PUF

### SRAM PUF的特征

Use standard SRAM

Unclonable and immutable

Device-unique high-quality keys

No secrets when power is off

No root key programming

Flexible and scalable

1. Process Variation

   Deep sub-micron variations in the production process give every transistor slightly random electric properties.

2. SRAM Start-up Values

   When the SRAM is powered on this randomness is expressed in the start-up values（0 or 1）of SRAM cells.

3. Silicon Fingerprint

   The start-up values create a highly random and repeatable pattern that is unique to each chip.

4. SRAM PUF Key

   The silicon fingerprint is turned into a secret key that builds the foundation of a security subsystem.

#### Key Storage with SRAM PUF

* Enrollment（注册过程）——One-Time Process

  SRAM PUF→PUF-IP→Activation Code（AC）（用于纠错）

* Key Reconstruction（重构）——in the Field

  SRAM→PUF-IP→SRAM PUF Key

  ​                   ↑

  ​    Activation Code（AC）

I（AC，Key）< ε，P[Key not Correct] < σ

#### BROADKEY

* software IP
* Delivered as Libraries
* 3 configurations
  * 8/10/21KB Code Size
* 128/256 bit strength
  * 0.7/1KB SRAM
* Portable Across MCUs
* In-field Retrofitting

#### QUIDDIKEY

* Hardware IP
* Delivered as RTL
* 2 configurations
  * 22/39K Gates
* 256 bit Strengh
  * 2KB SRAM
* Embedded as Fab
* APB interface

#### Foundational Security at Any Stage of Product Lifecycle

##### BROADKEY

Software IP，deployable greenfield to brownfield，for semiconductors/modules/OEMs

* Time to market
* Remote brownfield fix possible
* Risk mitigation for IC GTM challenges
* Portable across MCUs

##### QUIDDIKEY

Hardware IP for semiconductors

#### Proven Resilience，Guaranteed 25++ years Life

* Reliability
  * Temperature -55℃ to 150℃
  * Voltage +/- 20%
  * Radiation，EMC，humidity
  * <10<sup>-12</sup> Worst case error rate
* Manufacturability（可制造性）
  * 350nm~7nm Process Nodes
  * 认证
    * SMIC
    * Samsung
    * Intel
    * UMC
    * Cypress
    * IBM
    * TSMC
    * Renesas
    * ST
* Certifications
  * EMVCo Visa
  * cc/EAL6+
  * EU Government
  * U.S. Government
  * Indeoendent Labs

### SRAM PUF的应用

#### GetKey Operation Flow

Enrollment

* One-time procedure
* Read out SRAM PUF（1）
* Generate Activation Code（2）
* Activation code is non-sensitive and can be stored in unsecured NVM

Key Reconstruction

* Executed on the fly when key is needed
* Read SRAM PUF（3）and Activation code（4）to compute PUF root key
* Output key derived from PUF root key and "index"（5，6）

|--------|←（1）→|BROADKEY|→（2）→|---------------------------------|

|SRAM|                 |        or        |                  |Activation Code（AC）| 

|--------|←（3）→|QUIDDIKEY|←（4）←|---------------------------------|

​                                                   ↓   ←（5）←“index”

​                                               （6）

​                                                   ↓

​                                                K1🔑

#### Wrap Operation Flow

Enrollment

* Read out SRAM PUF（1）
* Generate Activation Code（2）

Key Programming

* Reconstruct internal device-unique PUF key from SRAM PUF and AC（3，4）
* Generate random key or input user key（5）
* Output wrapped key in the form of Key Code（6）

Key Reconstruction

* Reconstruct internal device-unique PUF key from SRAM PUF and AC（3，4）
* Unwrap Key Code（7）and output Key（8）

|--------|←（1）→|BROADKEY|→（2）→|---------------------------------|

|SRAM|                 |        or        |                  |Activation Code（AC）| 

|--------|←（3）→|QUIDDIKEY|←（4）←|---------------------------------|

​                                |                    |←（5）←🔑K2

​                                |                    |→（6）→|----------------|

​                                |----------------|←（7）←|Key Code 2|

​                                          ↓

​                                      （8）

​                                          ↓

​                                        K2🔑

#### BroadKey Anti-Cloning（Installation）

1. BROADKEY is integrated in bootloader
2. @first boot（in factory?）BROADKEY is enrolled and Activation Code is stored in data Flash
3. BROADKEY wraps Library Encryption Key into protected Key Code
4. Bootloader decrypts Library with Library Encryption Key and puts it in Flash. Enc. Library is cleared
5. Library Encryption Key is deleted from bootloader firmware
6. BROADKEY generates a device-unique Library Authentication Key🔑 and computes a binding MAC over the Library

#### BroadKeyAnti-Cloning（In-the-field）

1. Product Flash in-the-field does not contain any（unprotected）secret data
2. @boot in the field，BroadKey is started with Activation Code
3. BroadKey regenerates Library Authentication Key🔑 and recomputes Library Binding MAC，then checks it against MAC stored in Flash
4. if MAC verification succeeds，Library is run from Flash

#### BroadKeyAnti-Cloning（Updates）

1. @boot in the field，BROADKEY is started with Activation Code. Product receives OTA encrypted Lib update and puts it in Scratchpad，sends out ACK
2. When Product receives ENABLE，BROADKEY reconstructs（volatile）Lib Encryption Key from protected Key Code and decrypts Lib. Clears encrypted Lib from Flash.
3. BROADKEY regenerates device-unique Library Authentication Key🔑 and computes the new binding MAC over the new Library，stores it in Flash

#### BroadKeyAnti-Cloning（Product Cloning）

1. Extract Flash image of an in-the-field product instance（A）

2. Program Flash image on a clean product target platform

3. @boot of Clone，BROADKEY fails to start because Activation Code does not match physical device（A≠A’）

   →unable to retrieve Library Authentication Key

   →unable to match Library Binding MAC

   →non-function Clone

4. @OTA update of Clone

   →unable to retrieve Library Encryption Key

   →unable to decrypt new library

   →non-updateable Clone！

### 总结

* Easy to Implementation
* High Reliability
* Flexible Manufacture
* Security Proven

## 侧信道攻击技术——从理论到实践

设备需求

* Pico 3206D
* OSR-2560

### 侧信道基础

#### 侧信道概念

什么是侧信道

监听侧信道信息→推测设备行为

CRYPTO 2008，Eisenbarth等人成功基于KeeLoq算法的汽车远程无钥匙进入系统

CHES 2011，Oswald等人公布了对NXP公司RFID卡芯片主打产品Mifare DESFire MF3ICD40的攻击

2017，Ronen等人利用侧信道攻击，破解Philips智能灯泡Hue的Bootloader加密认证

##### 侧信道与安全标准

安全测评标准

* ISO/IEC 15408 CC标准
* EMVCo
* PCI DSS
* 密码模块安全检测要求
* 安全芯片密码检测要求
* 安全芯片密码检测准则
* 中国金融集成电路（IC）卡规范（PBOC 2.0）
* 信息技术安全性评估准则

#### 示波器原理

采样

* Nyquist采样定理

量化（示波器量化范围（垂直分辨率）有限）

* 量化噪声
* 避免
  * 垂直范围过大（很多范围没有用上）
  * 垂直范围过小（有效信号超出垂直范围）
* 触发
  * 上升沿触发
  * 下降沿触发
* 存储深度

##### 搭建采集环境

方案一

无源高阻探头×

有源差分探头√

方案二

无源高阻探头可以使用，但是记录信号不能真实反映情况

方案三

电流探头用法

方案四

电磁探头（操作空间更好）

#### 功耗曲线采集原理

### 波形采集记录

#### 功耗曲线采集实践

#### 泄露模型

### 密钥恢复原理和实践

#### CPA攻击方法

#### AES密钥恢复

## 故障注入攻击技术——从理论到实践

## 产品安全认证介绍

## TLS协议安全和测试