---
layout: post
title:  省赛
date:   2020-10-26 00:01:01 +0300
image:  2020-10-26-sunset.jpg
tags:   [ctf,省赛]
---

[TOC]

## Upx

Upx -d脱壳

Python exp：

```assembly
flag = ""
result = "cjfor~c=~?|v &ti"

for i in range(16):
   flag += chr(ord(result[i])^(i+5))

print(flag)
```

## special_apk

MainActivity中看到输入的字符串和nativa中的一个字符串比较

Ida打开.so文件在Java_com_example_easyapk_MainActivity_a函数中找到字符串：

"easyapk_is_great"

逆向算法，就是异或和字符的交换

C语言exp

```assembly
#include <stdio.h>

int main()
{
  char a[17] = "easyapk_is_great";
  char ee[17]={'@','\t',0x1,'\n','1',0x3,'\b',0x12,'\n',')',0x1A,0x1A,0x12,0x1E,0x3,'\r'}; 
  char b[16]={3,'\r', 18, 30, 26, 26, '\n', ')', '\x08', 18,  '1', 3,  1, '\n', '@', '\t'};

  for(int i=0;i<16;i++)
  {
      printf("%c",b[i]^a[i]);
  }
  printf("%s",ee);
  return 0;
}
```

## Log

用压缩后的readme.zip爆破明文攻击123.zip得到密码123.Com

将access.log用Unicode解码

在spl注入语句的最后一部分，

每行逐次判断字符串的ASCII码值，'>'和'<'都代表不是，只有!=后猜测是真正的字符串中的字符对应flag

102,108,97,103,32,105,115,32,102,108,97,103,123,53,56,52,52,101,99,57,53,101,51,57,101,48,102,51,49,52,48,55,99,51,52,53,98,48,56,97,54,51,56,49,50,125

![]({{site.baseurl}}/img/2020-10-26-sql.jpg)

## Easycaser

```assembly
from random import randint
 flag=""
 table = "xuwb52lj0md1qr43vayphf8enogz769kcsit"
 displacement = 26
 cipher = "kvzx{cslszzcw-rfos-nol4-rrf3-f5zrs54ywfr5}"
 for i in cipher:
   if i not in table:
     flag += i
   else:
     flag += table[(table.find(i)+26) % len(table)]
 print(flag)
 \# kvzx{cslszzcw-rfos-nol4-rrf3-f5zrs54ywfr5}

 for i in range(2**4-1,2**8):
   if (21+i)%36==31:
     if (6+i)%36==16:
       if (17+i)%36==27:
         if (26+i)%36==0:
           print(&apos;oh&apos;)
           print(i)
           break
```

