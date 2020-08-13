---
layout: post
title:  open-source
date:   2020-08-06 00:01:01 +0300
image:  2020-08-06-church.jpg
tags:   [ctf,reverse,adworld,HackYouCTF]
---

下载文件是.c文件，打开文件，查看源码

```assembly
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 4) {
    	printf("what?\n");
    	exit(1);
    }

    unsigned int first = atoi(argv[1]);
    if (first != 0xcafe) {
    	printf("you are wrong, sorry.\n");
    	exit(2);
    }

    unsigned int second = atoi(argv[2]);
    if (second % 5 == 3 || second % 17 != 8) {
    	printf("ha, you won't get it!\n");
    	exit(3);
    }

    if (strcmp("h4cky0u", argv[3])) {
    	printf("so close, dude!\n");
    	exit(4);
    }

    printf("Brr wrrr grr\n");

    unsigned int hash = first * 31337 + (second % 17) * 11 + strlen(argv[3]) - 1615810207;

    printf("Get your key: ");
    printf("%x\n", hash);
    return 0;
}
```

显然first == 0xcafe

然后分析second，因为argv是字符串，所以爆破看看second可能的值

```assembly
#include <stdio.h>

int main()
{
    for(int i=0;i<=126;i++)
    {
        if(i % 5 != 3 && i % 17 == 8)
            printf("%d\n",i);
    }
    return 0;
}
```

输出为

```assembly
25-->
42-->*
59-->;
76-->L
110->n
```

显然argv[3]=="h4cky0u"

接着看代码

```assembly
unsigned int hash = first * 31337 + (second % 17) * 11 + strlen(argv[3]) - 1615810207;
```

这里first和argv[3]已经确定，second虽然不确定，但是second % 17在之前的判断语句中我们已经知道等于8（看来之前的爆破second完全是白费）

```assembly
print(0xcafe * 31337 + 8 * 11 + 7 - 1615810207)
```

得到结果

12648430

而题目要求的是16进制形式

转换一下得到结果

C0FFEE

提交gg

卡了很久才想到可能是字母要小写~~我艹~~

换成c0ffee,正确