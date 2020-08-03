---
layout: post
title:  Transform(MRCTF2020)
date:   2020-08-02 00:01:01 +0300
image:  2020-08-02-moon.jpg
tags:   [ctf,reverse]
---

ida打开文件，进入主函数，F5反编译，查看代码。

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  	__int64 v3; // rdx
  	__int64 v4; // rdx
    char v6[104]; // [rsp+20h] [rbp-70h]
    int j; // [rsp+88h] [rbp-8h]
    int i; // [rsp+8Ch] [rbp-4h]

    sub_402230(argc, argv, envp);
    sub_40E640(argc, (__int64)argv, v3, (__int64)"Give me your code:\n");
    sub_40E5F0(argc, (__int64)argv, (__int64)v6, (unsigned __int64)"%s");
    if ( strlen(*(const char **)&argc) != 33 )
    {
        sub_40E640(argc, (__int64)argv, v4, (__int64)"Wrong!\n");
        system(*(const char **)&argc);
        exit(argc);
    }
    for ( i = 0; i <= 32; ++i )
    {
        byte_414040[i] = v6[dword_40F040[i]];
        v4 = i;
        byte_414040[i] ^= LOBYTE(dword_40F040[i]);
    }
    for ( j = 0; j <= 32; ++j )
    {
        v4 = j;
        if ( aGyURsywBFbLwya[j] != byte_414040[j] )
        {
            sub_40E640(argc, (__int64)argv, j, (__int64)"Wrong!\n");
            system(*(const char **)&argc);
            exit(argc);
        }
    }
    sub_40E640(argc, (__int64)argv, v4, (__int64)"Right!Good Job!\n");
    sub_40E640(argc, (__int64)argv, (__int64)v6, (__int64)"Here is your flag: %s\n");
    system(*(const char **)&argc);
    return 0;
}
```

通过分析代码看出先将输入的flag使用dword_40F040数组作为索引，打乱顺序，再将每个字符与dword_40F040[i]异或，最后与aGyURsywBFbLwya数组比较。

根据以上分析编写C语言脚本

```assembly
#include <stdio.h>
#include <stdlib.h>

int main()
{
    char byte_414040[34] = "gy{gu+<RSyW^]B{-*fB~LWyAk~e<\\EobM";
    char dword_40F040[] = {0x9,0x0A,0x0F,0x17,0x7,0x18,0x0C,0x6,0x1,0x10,0x3,0x11,0x20,0x1D,0x0B,0x1E,0x1B,0x16,0x4,0x0D,0x13,0x14,0x15,0x2,
                            0x19,0x5,0x1F,0x8,0x12,0x1A,0x1C,0x0E,0x0};
    char v6[34] = {0};
    for (int i = 0; i <= 32; ++i)
    {
        byte_414040[i] ^= dword_40F040[i];
        v6[dword_40F040[i]] = byte_414040[i];
    }
    printf("%s",v6);
    return 0;
}

```

得到flag

```
MRCTF{Tr4nsp0sltiON_Clpp3r_1s_3z}
```

