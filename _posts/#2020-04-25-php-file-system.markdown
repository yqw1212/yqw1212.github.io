---
layout: post
title:  PHP学习(三)
date:   2020-04-25 14:02:00 +0300
image:  5-loveourplanet.jpg
tags:   [PHP]
---

### read file()

### file_get_contents()

### fopen()

### fread()

### fclose()

fopen模式

| 模式 | 说明 |
| ---- | ---- |
| r    |      |
| r+   |      |
| w    |      |
| w+   |      |
| a    |      |
| a+   |      |
| x    |      |
| x+   |      |

| 模式 | 说明                  |
| ---- | --------------------- |
| t    | windows下将\n转为\r\n |
| b    | 二进制打开模式        |

### file_put_contents

### fwrite()

### tmpfile()

--------------------------

### rename()

### copy()

### unlink()

---------------------------------

### file_exists()

### is_readable()

### is_writeable()

### is_executable()

### is_file()

### is_dir()

### clearstatcache(void)

---------------------------------------

### rewind()

### fseek()

| 函数名    | 功能                                       |
| --------- | ------------------------------------------ |
| file      | 把整个文件读入一个数组中                   |
| fgets     | 从文件指针中读取一行,读到最后返回false     |
| fgetc     | 从文件指针中读取一个字符,读到最后返回false |
| ftruncate | 将文件截断到给定的长度                     |

文件时间的函数

| 函数      | 功能说明         |
| --------- | ---------------- |
| filectime | 文件创建时间     |
| filemtime | 文件修改时间     |
| fileatime | 文件上次访问时间 |

锁类型

| 锁类型  | 说明                       |
| ------- | -------------------------- |
| LOCK_SH | 取得共享锁定(读取的程序)   |
| LOCK_EX | 取得独占锁定(写入的程序)   |
| LOCK_UN | 释放的程序(无论共享或独占) |

目录处理函数

| 函数名   | 功能                                            |
| -------- | ----------------------------------------------- |
| opendir  |                                                 |
| readdir  |                                                 |
| is_dir   |                                                 |
| closedir |                                                 |
| filetype | 显示是文件夹还是文件,文件显示file,文件夹显示dir |

权限设置

| 函数  | 功能说明     |
| ----- | ------------ |
| chmod | 修改读取模式 |
| chgrp | 修改用户组   |
| chown | 修改权限     |

文件路径函数

| 函数名           | 功能                   |
| ---------------- | ---------------------- |
| pathinfo         | 返回文件的各个组成部分 |
| basename         | 返回文件名             |
| dirname          | 文件目录部分           |
| parse_url        | 网址拆解成各部分       |
| http_build_query | 生成url中的query字符串 |
| http_build_url   | 生成一个url            |

* dirname
* basename
* extension
* filename