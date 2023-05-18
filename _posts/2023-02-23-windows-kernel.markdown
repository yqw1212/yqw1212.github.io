---
layout: post
title:  Windows内核调试
date:   2023-02-23 00:08:01 +0300
image:  2023-02-23-cat.jpg
tags:   [note]
---

# 环境配置

安装Visual studio，选择安装C++桌面开发（win10 SDK），Windows Kits\10\Vsix\VS2019，找到WDK.vsix，安装WDK。

在win10 SDK安装目录下中找到x64/windbg.exe程序对应的位置，右击发送快捷方式到桌面，在目标框后添加`-b -k com:port=\\.\pipe\com2,baud=115200,pipe`

Path环境变量中添加`C:\Program Files (x86)\Windows Kits\10\Debuggers\x64`

添加``_NT_SYMBOL_PATH``环境变量，内容为``SRV\*D:\Windows_soft\symbols\* http://msdl.microsoft.com/download/symbols ``

### 系统调试端口设置

winXP

C盘下，取消隐藏受保护的操作系统文件，显示所有文件和文件夹，取消隐藏已知文件类型的拓展名

修改boot.ini文件，添加代码

```assembly
multi(0)disk(0)rdisk(0)partition(1)\WINDOWS="Microsoft Windows XP Professional" /noexecute=optin /fastdetect /debug /debugport=com2 /baudrate=115200
```

win+R，msconfig查看启动项目设置，使用修改过的BOOT.INT

win7

管理员身份运行cmd

```assembly
bcdedit /dbgsettings serial baudrate:115200 debugport:1
bcdedit /copy {current} /d sunn
bcdedit /displayorder {current} {73044f87-5f63-11e9-a7fe-af2693623221}
bcdedit /debug {73044f87-5f63-11e9-a7fe-af2693623221} ON
```

# 中断提权

idtr寄存器保存中断表的位置

```assembly
kd> r idtr
idtr=8003f400
kd> dd 8003f400
8003f400  0008e36c 80538e00 0008e4e4 80538e00
8003f410  0058112e 00008500 0008e8b4 8053ee00
8003f420  0008ea34 8053ee00 0008eb90 80538e00
8003f430  0008ed04 80538e00 0008f36c 80538e00
8003f440  00501188 00008500 0008f790 80538e00
8003f450  0008f8b0 80538e00 0008f9f0 80538e00
8003f460  0008fc4c 80538e00 0008ff30 80538e00
8003f470  00080620 80548e00 00080950 80548e00
kd> dq 8003f400 l40
8003f400  80538e00`0008e36c 80538e00`0008e4e4
8003f410  00008500`0058112e 8053ee00`0008e8b4
8003f420  8053ee00`0008ea34 80538e00`0008eb90
8003f430  80538e00`0008ed04 80538e00`0008f36c
8003f440  00008500`00501188 80538e00`0008f790
8003f450  80538e00`0008f8b0 80538e00`0008f9f0
8003f460  80538e00`0008fc4c 80538e00`0008ff30
8003f470  80548e00`00080620 80548e00`00080950
8003f480  80548e00`00080a70 80548e00`00080ba8
8003f490  80548500`00a00950 80548e00`00080d10
8003f4a0  80548e00`00080950 80548e00`00080950
8003f4b0  80548e00`00080950 80548e00`00080950
8003f4c0  80548e00`00080950 80548e00`00080950
8003f4d0  80548e00`00080950 80548e00`00080950
8003f4e0  80548e00`00080950 80548e00`00080950
8003f4f0  80548e00`00080950 806d8e00`00080fd0
8003f500  00000000`00080000 00000000`00080000
8003f510  00000000`00080000 00000000`00080000
8003f520  00000000`00080000 00000000`00080000
8003f530  00000000`00080000 00000000`00080000
8003f540  00000000`00080000 00000000`00080000
8003f550  8053ee00`0008dbae 8053ee00`0008dcb0
8003f560  8053ee00`0008de50 8053ee00`0008e790
8003f570  8053ee00`0008d651 80548e00`00080950
8003f580  80538e00`0008cd10 80538e00`0008cd1a
8003f590  80538e00`0008cd24 80538e00`0008cd2e
8003f5a0  80538e00`0008cd38 80538e00`0008cd42
8003f5b0  80538e00`0008cd4c 806d8e00`00080728
8003f5c0  80538e00`0008cd60 80538e00`0008cd6a
8003f5d0  80538e00`0008cd74 80538e00`0008cd7e
8003f5e0  80538e00`0008cd88 806d8e00`00081b70
8003f5f0  80538e00`0008cd9c 80538e00`0008cda6
```

编写代码

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

void __declspec(naked) IdtEntry(){
	__asm {
		iretd
	}
}

int main() {
	if ((DWORD)IdtEntry != 0x401040) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	//printf("%p\n", IdtEntry);
	system("pause");
}
```

将函数写到中断表空位置

```assembly
kd> eq 8003f500 00408e00`00081000
kd> dq 8003f400 l40
8003f400  80538e00`0008e36c 80538e00`0008e4e4
8003f410  00008500`0058112e 8053ee00`0008e8b4
8003f420  8053ee00`0008ea34 80538e00`0008eb90
8003f430  80538e00`0008ed04 80538e00`0008f36c
8003f440  00008500`00501188 80538e00`0008f790
8003f450  80538e00`0008f8b0 80538e00`0008f9f0
8003f460  80538e00`0008fc4c 80538e00`0008ff30
8003f470  80548e00`00080620 80548e00`00080950
8003f480  80548e00`00080a70 80548e00`00080ba8
8003f490  80548500`00a00950 80548e00`00080d10
8003f4a0  80548e00`00080950 80548e00`00080950
8003f4b0  80548e00`00080950 80548e00`00080950
8003f4c0  80548e00`00080950 80548e00`00080950
8003f4d0  80548e00`00080950 80548e00`00080950
8003f4e0  80548e00`00080950 80548e00`00080950
8003f4f0  80548e00`00080950 806d8e00`00080fd0
8003f500  00408e00`00081000 00000000`00080000
8003f510  00000000`00080000 00000000`00080000
8003f520  00000000`00080000 00000000`00080000
8003f530  00000000`00080000 00000000`00080000
8003f540  00000000`00080000 00000000`00080000
8003f550  8053ee00`0008dbae 8053ee00`0008dcb0
8003f560  8053ee00`0008de50 8053ee00`0008e790
8003f570  8053ee00`0008d651 80548e00`00080950
8003f580  80538e00`0008cd10 80538e00`0008cd1a
8003f590  80538e00`0008cd24 80538e00`0008cd2e
8003f5a0  80538e00`0008cd38 80538e00`0008cd42
8003f5b0  80538e00`0008cd4c 806d8e00`00080728
8003f5c0  80538e00`0008cd60 80538e00`0008cd6a
8003f5d0  80538e00`0008cd74 80538e00`0008cd7e
8003f5e0  80538e00`0008cd88 806d8e00`00081b70
8003f5f0  80538e00`0008cd9c 80538e00`0008cda6
```

这个中断号为0x20，所以我们要产生一个0x20的中断

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

void __declspec(naked) IdtEntry() {
	__asm {
		iretd
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	//printf("%p\n", IdtEntry);
	system("pause");
}
```

直接执行发现会报错，因为0x20中段的权限不够，修改属性

```assembly
kd> eq 8003f500 0040ee00`00081000
```

为了验证确实实现了中断提权，修改代码

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

DWORD g_tmp;

void __declspec(naked) IdtEntry() {
	__asm {
		mov eax, dword ptr ds:[0x8003f500]
		mov g_tmp, eax
		iretd
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("%p\n", g_tmp);
	system("pause");
}
```

# 多核复杂性

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

DWORD g_flags;

void __declspec(naked) IdtEntry() {
	__asm {
		pushfd
		pop eax
		mov g_flags, eax
		iretd
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("%p\n", g_flags);
	system("pause");
}
```

在中断表写入函数地址

可以看到输出的值为0x46（01000110）

Interrupt Fnable Flag（IF）寄存器在从右数的第9位（开头为0），所以IF寄存器的值为0，关中断，表示不可被系统打断，防止中断嵌套。

开中断

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

DWORD g_flags;

void __declspec(naked) IdtEntry() {
	__asm {
		sti
Label:
		jmp Label
		iretd
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("%p\n", g_flags);
	system("pause");
}
```

多核

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

DWORD g_id;

void __declspec(naked) IdtEntry1() {
	__asm {
		mov eax, 1
		mov g_id, eax
		iretd
	}
}

void __declspec(naked) IdtEntry2() {
	__asm {
		mov eax, 2
		mov g_id, eax
		iretd
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry2 != 0x401010 || (DWORD)IdtEntry1 != 0x401000) {
		printf("wrong addr:%p", IdtEntry1);
		printf("wrong addr:%p", IdtEntry2);
		exit(-1);
	}
	go();
	printf("%p\n", g_id);
	system("pause");
}
```

查看内存权限

```assembly
kd> !pte 8003f500
                    VA 8003f500
PDE at C0602000            PTE at C04001F8
contains 0000000000312163  contains 000000000003F163
pfn 312       -G-DA--KWEV  pfn 3f        -G-DA--KWEV
```

分别为页目录表，页表

cr0寄存器第16位是WP位，只要将这一位置0就可以禁用写保护，置1则可将其恢复。

```assembly
// 关闭写保护
__asm{
    cli ;//将处理器标志寄存器的中断标志位清0，不允许中断
    mov eax, cr0
    and  eax, ~0x10000
    mov cr0, eax
}

// 恢复写保护
__asm{
    mov  eax, cr0
    or     eax, 0x10000
    mov  cr0, eax
    sti ;//将处理器标志寄存器的中断标志置1，允许中断
}
```

给一个不可写的内存写值

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>


void __declspec(naked) IdtEntry1() {
	__asm {
		mov eax, cr0
		and eax, not 10000h
		mov cr0, eax
		
		mov eax, 0xFFFFFFFF
		mov ds:[0x80542520], eax
L:
		jmp L
		iretd
	}
}


void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry0);
		exit(-1);
	}
	go();
	system("pause");
}
```

# 中断现场

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

DWORD g_eax[2], g_ecx[2], g_edx[2], g_ebx[2];
DWORD g_esp[2], g_ebp[2], g_esi[2], g_edi[2];
WORD  g_cs[2], g_ds[2], g_ss[2], g_es[2], g_fs[2], g_gs[2];

void __declspec(naked) IdtEntry() {
	__asm {
		mov [g_eax+4], eax
		mov [g_ecx+4], ecx
		mov [g_edx+4], edx
		mov [g_ebx+4], ebx
		mov [g_esp+4], esp
		mov [g_ebp+4], ebp
		mov [g_esi+4], esi
		mov [g_edi+4], edi

		push eax
		mov ax, cs
		mov [g_cs+2], ax
		mov ax, ds
		mov [g_ds+2], ax
		mov ax, ss
		mov [g_ss+2], ax
		mov ax, es
		mov [g_es+2], ax
		mov ax, fs
		mov [g_fs+2], ax
		mov ax, gs
		mov [g_gs+2], ax


		pop eax

		iretd
	}
}

void go() {
	__asm{
		mov [g_eax], eax
		mov [g_ecx], ecx
		mov [g_edx], edx
		mov [g_ebx], ebx
		mov [g_esp], esp
		mov [g_ebp], ebp
		mov [g_esi], esi
		mov [g_edi], edi

		push eax
		mov ax, cs
		mov [g_cs], ax
		mov ax, ds
		mov [g_ds], ax
		mov ax, ss
		mov [g_ss], ax
		mov ax, es
		mov [g_es], ax
		mov ax, fs
		mov [g_fs], ax
		mov ax, gs
		mov [g_gs], ax
		pop eax
	}
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("eax:%p\tecx:%p\tedx:%p\tebx:%p\n", g_eax[0], g_ecx[0], g_edx[0], g_ebx[0]);
	printf("esp:%p\tebp:%p\tesi:%p\tedi:%p\n", g_esp[0], g_ebp[0], g_esi[0], g_edi[0]);
	printf("cs:%p\tds:%p\tss:%p\tes:%p\tfs:%p\tgs:%p\n", g_cs[0], g_ds[0], g_ss[0], g_es[0], g_fs[0], g_gs[0]);
	printf("eax:%p\tecx:%p\tedx:%p\tebx:%p\n", g_eax[1], g_ecx[1], g_edx[1], g_ebx[1]);
	printf("esp:%p\tebp:%p\tesi:%p\tedi:%p\n", g_esp[1], g_ebp[1], g_esi[1], g_edi[1]);
	printf("cs:%p\tds:%p\tss:%p\tes:%p\tfs:%p\tgs:%p\n", g_cs[1], g_ds[1], g_ss[1], g_es[1], g_fs[1], g_gs[1]);
	system("pause");
}
```

输出

```assembly
eax:00401000    ecx:78B53714    edx:00000000    ebx:00000000
esp:0012FF78    ebp:0012FFC0    esi:00000001    edi:004033C8
cs:0000001B     ds:00000023     ss:00000023     es:00000023     fs:0000003B
gs:00000000
eax:00401000    ecx:78B53714    edx:00000000    ebx:00000000
esp:F0504DCC    ebp:0012FFC0    esi:00000001    edi:004033C8
cs:00000008     ds:00000023     ss:00000010     es:00000023     fs:0000003B
gs:00000000
```

cs，ss，esp改变

描述符根据逻辑用途分类：

* 内存区域类：基址，界限，用途

  代码段，数据段，TSS段，LDT段

* 门类：权限变化，跳转目标

  中断门，陷阱门，调用门，任务门

IDT表项是门，保护内核数据不被随意读写

GDT

- GDT：全局描述符表
- LDT ：局部描述符表

有 3 个重要的寄存器用来定位这两张表：

- gdtr：GDT 表基址
- gdtl：GDT 表的大小
- ldtr：LDT 表基址， Windows 不使用 LDT

栈数据是线程的核心资源，应受到保护，所以特权切换必须伴随栈切换，切换应由CPU硬件支持

ss是和tss段有关

利用int3断到windbg

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

DWORD g_eax[2], g_ecx[2], g_edx[2], g_ebx[2];
DWORD g_esp[2], g_ebp[2], g_esi[2], g_edi[2];
WORD  g_cs[2], g_ds[2], g_ss[2], g_es[2], g_fs[2], g_gs[2];
WORD g_tr;

void __declspec(naked) IdtEntry() {
	__asm {
		mov [g_eax+4], eax
		mov [g_ecx+4], ecx
		mov [g_edx+4], edx
		mov [g_ebx+4], ebx
		mov [g_esp+4], esp
		mov [g_ebp+4], ebp
		mov [g_esi+4], esi
		mov [g_edi+4], edi

		push eax
		mov ax, cs
		mov [g_cs+2], ax
		mov ax, ds
		mov [g_ds+2], ax
		mov ax, ss
		mov [g_ss+2], ax
		mov ax, es
		mov [g_es+2], ax
		mov ax, fs
		mov [g_fs+2], ax
		mov ax, gs
		mov [g_gs+2], ax

		str ax
		mov g_tr, ax

		pop eax
		
		int 3

		iretd
	}
}

void go() {
	__asm{
		mov [g_eax], eax
		mov [g_ecx], ecx
		mov [g_edx], edx
		mov [g_ebx], ebx
		mov [g_esp], esp
		mov [g_ebp], ebp
		mov [g_esi], esi
		mov [g_edi], edi

		push eax
		mov ax, cs
		mov [g_cs], ax
		mov ax, ds
		mov [g_ds], ax
		mov ax, ss
		mov [g_ss], ax
		mov ax, es
		mov [g_es], ax
		mov ax, fs
		mov [g_fs], ax
		mov ax, gs
		mov [g_gs], ax
		pop eax
	}
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("eax:%p\tecx:%p\tedx:%p\tebx:%p\n", g_eax[0], g_ecx[0], g_edx[0], g_ebx[0]);
	printf("esp:%p\tebp:%p\tesi:%p\tedi:%p\n", g_esp[0], g_ebp[0], g_esi[0], g_edi[0]);
	printf("cs:%p\tds:%p\tss:%p\tes:%p\tfs:%p\tgs:%p\n", g_cs[0], g_ds[0], g_ss[0], g_es[0], g_fs[0], g_gs[0]);
	printf("eax:%p\tecx:%p\tedx:%p\tebx:%p\n", g_eax[1], g_ecx[1], g_edx[1], g_ebx[1]);
	printf("esp:%p\tebp:%p\tesi:%p\tedi:%p\n", g_esp[1], g_ebp[1], g_esi[1], g_edi[1]);
	printf("cs:%p\tds:%p\tss:%p\tes:%p\tfs:%p\tgs:%p\n", g_cs[1], g_ds[1], g_ss[1], g_es[1], g_fs[1], g_gs[1]);
	system("pause");
}
```

查看栈内容

```assembly
kd> r esp
esp=f0dd7dcc
kd> dps esp
f0dd7dcc  004010e9  // 中断返回到的eip
f0dd7dd0  0000001b  // 进来之前的cs
f0dd7dd4  00000246  // ring3 eflags
f0dd7dd8  0012ff78  // ring3 esp
f0dd7ddc  00000023  // ring3 ss
f0dd7de0  0a0d2f2f
f0dd7de4  4d202f2f
f0dd7de8  61737365
```

验证

```assembly
kd> u 004010e9
004010e9 c3              ret
004010ea cc              int     3
004010eb cc              int     3
004010ec cc              int     3
004010ed cc              int     3
004010ee cc              int     3
004010ef cc              int     3
004010f0 b800104000      mov     eax,401000h
kd> ub 004010e9
004010cb 668cc0          mov     ax,es
004010ce 66a3a4334000    mov     word ptr ds:[004033A4h],ax
004010d4 668ce0          mov     ax,fs
004010d7 66a390334000    mov     word ptr ds:[00403390h],ax
004010dd 668ce8          mov     ax,gs
004010e0 66a3b4334000    mov     word ptr ds:[004033B4h],ax
004010e6 58              pop     eax
004010e7 cd20            int     20h
```

# 再次开中断

KPCR介绍：

1 .当线程进入0环时，FS：[0]指向KPCR（3环FS:[0]–>TEB）

2 .每个CPU都有一个KPCR结构体（一个核一个）

3 .KPCR 存储了CPU本身要用的一些重要数据：GDT，IDT以及线程相关的一些信息 （IDT和GDT并非通用，而是一个CPU有一组）

_NT_TIB主要成员介绍

1) +0x000 ExceptionList : Ptr32_EXCEPTION_REGISTRATION_RECORD

当前线程内核异常链表(SEH)

2) +0x004 StackBase : Ptr32 Void

+0x008 StackLimit : Ptr32 Void

当前线程内核栈的基址和大小

3) +0x018 Self : Ptr32 _NT_TIB

指向自己(也就是指向KPCR结构) 这样设计的目的是为了查找方便

KPCR的其他成员介绍

1) +0x01c SelfPcr : Ptr32 _KPCR

指向自己，方便寻址

2) +0x020 Prcb : Ptr32 _KPRCB

指向拓展结构体PRCB

3) +0x038 IDT : Ptr32 _KIDTENTRY

IDT表基址

4) +0x03c GDT : Ptr32 _KGDTENTRY

GDT表基址

5) +0x040 TSS : Ptr32 _KTSS

指针，指向TSS，每个CPU都有一个TSS.都是指向当前线程的

6) +0x051 Number : UChar

CPU编号：0 1 2 3 4 5。。。

7) +0x120 PrcbData : _KPRCB

拓展结构体

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

void __declspec(naked) IdtEntry() {
	__asm {

		push 0x30
		pop fs
		sti
L:
		jmp L
		iretd
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	system("pause");
}
```

用windbg修改死循环

```assembly
kd> u 401000
00401000 6a30            push    30h
00401002 6a30            push    30h
00401004 fb              sti
00401005 ebfe            jmp     00401005
00401007 cf              iretd
00401008 cc              int     3
00401009 cc              int     3
0040100a cc              int     3
kd> ew 00401005 9090
```

# API调用

进内核出内核——安全的内核环境

内核空间分配内存

ExAllocatePool function (wdm.h)

**ExAllocatePool** allocates pool memory of the specified type and returns a pointer to the allocated block.

Syntax

```assembly
PVOID ExAllocatePool(
  [in] __drv_strictTypeMatch(__drv_typeExpr)POOL_TYPE PoolType,
  [in] SIZE_T                                         NumberOfBytes
);
```

Parameters

```assembly
[in] PoolType
```

Specifies the type of pool memory to allocate. For a description of the available pool memory types, see [POOL_TYPE](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/ne-wdm-_pool_type).

You can modify *PoolType* by using a bitwise OR with the POOL_COLD_ALLOCATION flag as a hint to the kernel to allocate the memory from pages that are likely to be paged out quickly. To reduce the amount of resident pool memory as much as possible, you should not reference these allocations frequently. The POOL_COLD_ALLOCATION flag is only advisory and is available for Windows XP and later versions of the Windows operating system.

```
[in] NumberOfBytes
```

Specifies the number of bytes to allocate.

Return value

**ExAllocatePool** returns **NULL** if there is insufficient memory in the free pool to satisfy the request. Otherwise the routine returns a pointer to the allocated memory.

在ntkrnlpa.exe中可以找到该函数

```assembly
.text:8053454C ; =============== S U B R O U T I N E =======================================
.text:8053454C
.text:8053454C ; Attributes: bp-based frame
.text:8053454C
.text:8053454C ; PVOID __stdcall ExAllocatePool(POOL_TYPE PoolType, SIZE_T NumberOfBytes)
.text:8053454C                 public _ExAllocatePool@8
.text:8053454C _ExAllocatePool@8 proc near             ; CODE XREF: IopComputeHarddiskDerangements(x)+2E↓p
.text:8053454C                                         ; KeQueryLogicalProcessorInformation(x,x,x)+1E↓p ...
.text:8053454C
.text:8053454C PoolType        = dword ptr  8
.text:8053454C NumberOfBytes   = dword ptr  0Ch
.text:8053454C
.text:8053454C                 mov     edi, edi
.text:8053454E                 push    ebp
.text:8053454F                 mov     ebp, esp
.text:80534551                 push    656E6F4Eh       ; Tag
.text:80534556                 push    [ebp+NumberOfBytes] ; NumberOfBytes
.text:80534559                 push    [ebp+PoolType]  ; PoolType
.text:8053455C                 call    _ExAllocatePoolWithTag@12 ; ExAllocatePoolWithTag(x,x,x)
.text:80534561                 pop     ebp
.text:80534562                 retn    8
.text:80534562 _ExAllocatePool@8 endp
```

_DbgPrint

```assembly
.text:80528E62 ; Attributes: bp-based frame
.text:80528E62
.text:80528E62 ; ULONG DbgPrint(PCSTR Format, ...)
.text:80528E62                 public _DbgPrint
.text:80528E62 _DbgPrint       proc near               ; CODE XREF: KeBugCheck2(x,x,x,x,x,x)+513↑p
.text:80528E62                                         ; KeBugCheck2(x,x,x,x,x,x)+535↑p ...
.text:80528E62
.text:80528E62 Format          = dword ptr  8
.text:80528E62 arglist         = byte ptr  0Ch
.text:80528E62
.text:80528E62                 mov     edi, edi
.text:80528E64                 push    ebp
.text:80528E65                 mov     ebp, esp
.text:80528E67                 lea     eax, [ebp+arglist]
.text:80528E6A                 push    eax             ; arglist
.text:80528E6B                 push    [ebp+Format]    ; Format
.text:80528E6E                 push    0               ; Level
.text:80528E70                 push    0FFFFFFFFh      ; ComponentId
.text:80528E72                 push    offset Prefix   ; Prefix
.text:80528E77                 call    _vDbgPrintExWithPrefix@20 ; vDbgPrintExWithPrefix(x,x,x,x,x)
.text:80528E7C                 pop     ebp
.text:80528E7D                 retn
.text:80528E7D _DbgPrint       endp
```

代码

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

typedef enum _POOL_TYPE {
    NonPagedPool,
    NonPagedPoolExecute = NonPagedPool,
    PagedPool,
    NonPagedPoolMustSucceed = NonPagedPool + 2,
    DontUseThisType,
    NonPagedPoolCacheAligned = NonPagedPool + 4,
    PagedPoolCacheAligned,
    NonPagedPoolCacheAlignedMustS = NonPagedPool + 6,
    MaxPoolType,
    NonPagedPoolBase = 0,
    NonPagedPoolBaseMustSucceed = NonPagedPoolBase + 2,
    NonPagedPoolBaseCacheAligned = NonPagedPoolBase + 4,
    NonPagedPoolBaseCacheAlignedMustS = NonPagedPoolBase + 6,
    NonPagedPoolSession = 32,
    PagedPoolSession = NonPagedPoolSession + 1,
    NonPagedPoolMustSucceedSession = PagedPoolSession + 1,
    DontUseThisTypeSession = NonPagedPoolMustSucceedSession + 1,
    NonPagedPoolCacheAlignedSession = DontUseThisTypeSession + 1,
    PagedPoolCacheAlignedSession = NonPagedPoolCacheAlignedSession + 1,
    NonPagedPoolCacheAlignedMustSSession = PagedPoolCacheAlignedSession + 1,
    NonPagedPoolNx = 512,
    NonPagedPoolNxCacheAligned = NonPagedPoolNx + 4,
    NonPagedPoolSessionNx = NonPagedPoolNx + 32,

} POOL_TYPE;

typedef DWORD (__stdcall *EX_ALLOCATE)(DWORD PoolType, DWORD NumberOfBytes);
EX_ALLOCATE ExAllocatePool = (EX_ALLOCATE)0x8053454C;
DWORD g_pool;

typedef DWORD (*DBG_PRINT)(char* Format, ...);
DBG_PRINT DbgPrint = (DBG_PRINT)0x80528E62;
char str[] = "Hello Driver";

void __declspec(naked) IdtEntry() {
	__asm {
		push 0x30
		pop fs
		sti
	}

	//g_pool = ExAllocatePool(POOL_TYPE::NonPagedPool, 4096);
	DbgPrint(str);

	__asm{	
		push 0x3B
		pop fs
		iretd
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	//printf("%p\n", g_pool);
	system("pause");
}
```

# InlineHook

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>


typedef DWORD (__stdcall *EX_ALLOCATE)(DWORD PoolType, DWORD NumberOfBytes);
EX_ALLOCATE ExAllocatePool = (EX_ALLOCATE)0x8053454C;
DWORD g_pool;


void __declspec(naked) IdtEntry() {
	__asm {
		push 0x30
		pop fs
		sti
	}

	// g_pool = ExAllocatePool(0, 4096);

	__asm{
		cli
		push 0x3B
		pop fs
		iretd
	}
}

void go() {
	while(1)
		__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	//printf("%p\n", g_pool);
	system("pause");
}
```

free

```assembly
POOLCODE:80545E68 ; Attributes: bp-based frame
POOLCODE:80545E68
POOLCODE:80545E68 ; void __stdcall ExFreePool(PVOID P)
POOLCODE:80545E68                 public _ExFreePool@4
POOLCODE:80545E68 _ExFreePool@4   proc near               ; CODE XREF: RtlFreeAnsiString(x)+11↓p
POOLCODE:80545E68                                         ; RtlFreeOemString(x)+10↓p ...
POOLCODE:80545E68
POOLCODE:80545E68 P               = dword ptr  8
POOLCODE:80545E68
POOLCODE:80545E68                 mov     edi, edi
POOLCODE:80545E6A                 push    ebp
POOLCODE:80545E6B                 mov     ebp, esp
POOLCODE:80545E6D                 push    0               ; Tag
POOLCODE:80545E6F                 push    [ebp+P]         ; P
POOLCODE:80545E72                 call    _ExFreePoolWithTag@8 ; ExFreePoolWithTag(x,x)
POOLCODE:80545E77                 pop     ebp
POOLCODE:80545E78                 retn    4
POOLCODE:80545E78 _ExFreePool@4   endp
```

free在内核分配的内存

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>


typedef DWORD (__stdcall *EX_ALLOCATE)(DWORD PoolType, DWORD NumberOfBytes);
EX_ALLOCATE ExAllocatePool = (EX_ALLOCATE)0x8053454C;
typedef void (__stdcall *EX_FREE)(DWORD P);
EX_FREE ExFreePool = (EX_FREE)0x80545E68;

DWORD g_pool;


void __declspec(naked) IdtEntry() {
	__asm {
		push 0x30
		pop fs
		sti
	}

	// g_pool = ExAllocatePool(0, 4096);

	__asm{
		cli
		push 0x3B
		pop fs
		iretd
	}
}

void go() {
	while(1)
		__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	//printf("%p\n", g_pool);
	system("pause");
}
```

内核代码

```assembly
.text:8053E540
.text:8053E540 ; =============== S U B R O U T I N E =======================================
.text:8053E540
.text:8053E540
.text:8053E540 _KiFastCallEntry proc near              ; DATA XREF: KiLoadFastSyscallMachineSpecificRegisters(x)+24↑o
.text:8053E540                                         ; _KiTrap01+72↓o
.text:8053E540
.text:8053E540 var_B           = byte ptr -0Bh
.text:8053E540
.text:8053E540 ; FUNCTION CHUNK AT .text:8053E519 SIZE 00000025 BYTES
.text:8053E540 ; FUNCTION CHUNK AT .text:8053E7DC SIZE 00000014 BYTES
.text:8053E540
.text:8053E540                 mov     ecx, 23h ; '#'
.text:8053E545                 push    30h ; '0'
.text:8053E547                 pop     fs
.text:8053E549                 mov     ds, ecx
.text:8053E54B                 mov     es, ecx
.text:8053E54D                 mov     ecx, ds:0FFDFF040h
.text:8053E553                 mov     esp, [ecx+4]
.text:8053E556                 push    23h ; '#'
.text:8053E558                 push    edx
.text:8053E559                 pushf
.text:8053E55A
.text:8053E55A loc_8053E55A:                           ; CODE XREF: _KiFastCallEntry2+22↑j
.text:8053E55A                 push    2
.text:8053E55C                 add     edx, 8
.text:8053E55F                 popf
.text:8053E560                 or      [esp+0Ch+var_B], 2
.text:8053E565                 push    1Bh
.text:8053E567                 push    dword ptr ds:0FFDF0304h
.text:8053E56D                 push    0
.text:8053E56F                 push    ebp
.text:8053E570                 push    ebx
.text:8053E571                 push    esi
.text:8053E572                 push    edi
.text:8053E573                 mov     ebx, ds:0FFDFF01Ch
.text:8053E579                 push    3Bh ; ';'
.text:8053E57B                 mov     esi, [ebx+124h]
.text:8053E581                 push    dword ptr [ebx]
.text:8053E583                 mov     dword ptr [ebx], 0FFFFFFFFh
.text:8053E589                 mov     ebp, [esi+18h]
.text:8053E58C                 push    1
.text:8053E58E                 sub     esp, 48h
.text:8053E591                 sub     ebp, 29Ch
.text:8053E597                 mov     byte ptr [esi+140h], 1
.text:8053E59E                 cmp     ebp, esp
.text:8053E5A0                 jnz     short loc_8053E53C
.text:8053E5A2                 and     dword ptr [ebp+2Ch], 0
.text:8053E5A6                 test    byte ptr [esi+2Ch], 0FFh
.text:8053E5AA                 mov     [esi+134h], ebp
.text:8053E5B0                 jnz     Dr_FastCallDrSave
.text:8053E5B6
.text:8053E5B6 loc_8053E5B6:                           ; CODE XREF: Dr_FastCallDrSave+10↑j
.text:8053E5B6                                         ; Dr_FastCallDrSave+7C↑j
.text:8053E5B6                 mov     ebx, [ebp+60h]
.text:8053E5B9                 mov     edi, [ebp+68h]
.text:8053E5BC                 mov     [ebp+0Ch], edx
.text:8053E5BF                 mov     dword ptr [ebp+8], 0BADB0D00h
.text:8053E5C6                 mov     [ebp+0], ebx
.text:8053E5C9                 mov     [ebp+4], edi
.text:8053E5CC                 sti
.text:8053E5CD
.text:8053E5CD loc_8053E5CD:                           ; CODE XREF: _KiBBTUnexpectedRange+18↑j
.text:8053E5CD                                         ; _KiSystemService+6F↑j
.text:8053E5CD                 mov     edi, eax
.text:8053E5CF                 shr     edi, 8
.text:8053E5D2                 and     edi, 30h
.text:8053E5D5                 mov     ecx, edi
.text:8053E5D7                 add     edi, [esi+0E0h]
.text:8053E5DD                 mov     ebx, eax
.text:8053E5DF                 and     eax, 0FFFh
.text:8053E5E4                 cmp     eax, [edi+8]
.text:8053E5E7                 jnb     _KiBBTUnexpectedRange
.text:8053E5ED                 cmp     ecx, 10h
.text:8053E5F0                 jnz     short loc_8053E60C
.text:8053E5F2                 mov     ecx, ds:0FFDFF018h
.text:8053E5F8                 xor     ebx, ebx
.text:8053E5FA
.text:8053E5FA loc_8053E5FA:                           ; DATA XREF: _KiTrap0E+113↓o
.text:8053E5FA                 or      ebx, [ecx+0F70h]
.text:8053E600                 jz      short loc_8053E60C
.text:8053E602                 push    edx
.text:8053E603                 push    eax
.text:8053E604                 call    ds:_KeGdiFlushUserBatch
.text:8053E60A                 pop     eax
.text:8053E60B                 pop     edx
.text:8053E60C
.text:8053E60C loc_8053E60C:                           ; CODE XREF: _KiFastCallEntry+B0↑j
.text:8053E60C                                         ; _KiFastCallEntry+C0↑j
.text:8053E60C                 inc     dword ptr ds:0FFDFF638h
.text:8053E612                 mov     esi, edx
.text:8053E614                 mov     ebx, [edi+0Ch]
.text:8053E617                 xor     ecx, ecx
.text:8053E619                 mov     cl, [eax+ebx]
.text:8053E61C                 mov     edi, [edi]
.text:8053E61E                 mov     ebx, [edi+eax*4]
.text:8053E621                 sub     esp, ecx
.text:8053E623                 shr     ecx, 2
.text:8053E626                 mov     edi, esp
.text:8053E628                 cmp     esi, ds:_MmUserProbeAddress
.text:8053E62E                 jnb     loc_8053E7DC
.text:8053E634
.text:8053E634 loc_8053E634:                           ; CODE XREF: _KiFastCallEntry+2A0↓j
.text:8053E634                                         ; DATA XREF: _KiTrap0E+109↓o
.text:8053E634                 rep movsd
.text:8053E636                 call    ebx
.text:8053E638
.text:8053E638 loc_8053E638:                           ; CODE XREF: _KiFastCallEntry+2AB↓j
.text:8053E638                                         ; DATA XREF: _KiTrap0E+129↓o ...
.text:8053E638                 mov     esp, ebp
.text:8053E63A
.text:8053E63A loc_8053E63A:                           ; CODE XREF: _KiBBTUnexpectedRange+38↑j
.text:8053E63A                                         ; _KiBBTUnexpectedRange+43↑j
.text:8053E63A                 mov     ecx, ds:0FFDFF124h
.text:8053E640                 mov     edx, [ebp+3Ch]
.text:8053E643                 mov     [ecx+134h], edx
.text:8053E643 _KiFastCallEntry endp
```

挂钩

cpyfunc

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>


// target 8003f120
// 8053E545
// 0x4ff420

void JmpTarget();


int i;
char* p;
void __declspec(naked) IdtEntry() {
	
	p = (char*)0x8003f120;
	for(i=0; i<64; i++){
		*p = ((char*)JmpTarget)[i];
		p++;
	}
	__asm {
		iretd
	}
}

void __declspec(naked) JmpTarget() {
	
	__asm {
		pushad
		pushfd

		mov eax, ds:[0x8003f3f0]
		inc eax
		mov ds:[0x8003f3f0], eax

		popfd
		popad

		mov  ecx, 0x23
		push 30h
		pop  fs
		mov  ds, cx
		mov  es, cx

		mov ecx, 0x8053E54D
		jmp ecx
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	system("pause");
}
```

修改kifastcall

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>



void __declspec(naked) IdtEntry() {
	__asm {
		mov eax, cr0
		and eax, not 10000h
		mov cr0, eax

		mov al, 0xe9
		mov ds:[0x8053E540], al
		mov eax, 0xFFB00BDB
		mov ds:[0x8053E541], eax

		mov eax, cr0
		or  eax, 10000h
		mov cr0, eax
		iretd
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	system("pause");
}
```

## 通过hook查看系统调用次数

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

DWORD g_num;

void __declspec(naked) IdtEntry() {
	__asm {
		test eax, eax
		jnz L
		mov ds:[0x8003f3f0], eax
		mov g_num, eax
		jmp End
L:
		mov eax, ds:[0x8003f3f0]
		mov g_num, eax
End:
		iretd
	}
}

void reset() {
	__asm{
		xor eax, eax
		int 0x20;
	}
}


void go() {
	__asm{
		mov eax, 1
		int 0x20;
	}
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	reset();
	while(1){
		go();
		Sleep(1000);
		printf("%d\n", g_num);
	}
	system("pause");
}
```

## 单步异常挂钩

使用kitrap01

```assembly
.text:8053F314 ; =============== S U B R O U T I N E =======================================
.text:8053F314
.text:8053F314
.text:8053F314 _KiTrap01       proc near               ; DATA XREF: INIT:80690B04↓o
.text:8053F314
.text:8053F314 var_2           = word ptr -2
.text:8053F314 arg_4           = dword ptr  8
.text:8053F314
.text:8053F314 ; FUNCTION CHUNK AT .text:8053F013 SIZE 00000021 BYTES
.text:8053F314 ; FUNCTION CHUNK AT .text:8053F258 SIZE 00000010 BYTES
.text:8053F314
.text:8053F314                 push    0
.text:8053F316                 mov     [esp+4+var_2], 0
.text:8053F31D                 push    ebp
.text:8053F31E                 push    ebx
.text:8053F31F                 push    esi
.text:8053F320                 push    edi
.text:8053F321                 push    fs
.text:8053F323                 mov     ebx, 30h ; '0'
.text:8053F328                 mov     fs, bx
.text:8053F32B                 mov     ebx, large fs:0
.text:8053F332                 push    ebx
.text:8053F333                 sub     esp, 4
.text:8053F336                 push    eax
.text:8053F337                 push    ecx
.text:8053F338                 push    edx
.text:8053F339                 push    ds
.text:8053F33A                 push    es
.text:8053F33B                 push    gs
.text:8053F33D                 mov     ax, 23h ; '#'
.text:8053F341                 sub     esp, 30h
.text:8053F344                 mov     ds, ax
.text:8053F347                 mov     es, ax
.text:8053F34A                 mov     ebp, esp
.text:8053F34C                 test    [esp+68h+arg_4], 20000h
.text:8053F354                 jnz     short V86_kit1_a
.text:8053F356
.text:8053F356 loc_8053F356:                           ; CODE XREF: V86_kit1_a+25↑j
.text:8053F356                 cld
.text:8053F357                 mov     ebx, [ebp+60h]
.text:8053F35A                 mov     edi, [ebp+68h]
.text:8053F35D                 mov     [ebp+0Ch], edx
.text:8053F360                 mov     dword ptr [ebp+8], 0BADB0D00h
.text:8053F367                 mov     [ebp+0], ebx
.text:8053F36A                 mov     [ebp+4], edi
.text:8053F36D                 test    byte ptr ds:0FFDFF050h, 0FFh
.text:8053F374                 jnz     Dr_kit1_a
.text:8053F37A
.text:8053F37A loc_8053F37A:                           ; CODE XREF: Dr_kit1_a+10↑j
.text:8053F37A                                         ; Dr_kit1_a+7C↑j
.text:8053F37A                 cmp     dword ptr ds:0FFDFF054h, 0
.text:8053F381                 jnz     short loc_8053F3E3
.text:8053F383                 mov     ecx, [ebp+68h]
.text:8053F386                 cmp     ecx, offset _KiFastCallEntry
.text:8053F38C                 jz      loc_8053F258
.text:8053F392                 test    dword ptr [ebp+70h], 20000h
.text:8053F399                 jnz     short loc_8053F3BF
.text:8053F39B                 test    word ptr [ebp+6Ch], 1
.text:8053F3A1                 jz      short loc_8053F3AB
.text:8053F3A3                 cmp     word ptr [ebp+6Ch], 1Bh
.text:8053F3A8                 jnz     short loc_8053F3BF
.text:8053F3AA
.text:8053F3AA loc_8053F3AA:                           ; CODE XREF: _KiTrap01+BB↓j
.text:8053F3AA                 sti
.text:8053F3AB
.text:8053F3AB loc_8053F3AB:                           ; CODE XREF: _KiTrap01+8D↑j
.text:8053F3AB                                         ; _KiTrap01+C8↓j
.text:8053F3AB                 and     dword ptr [ebp+70h], 0FFFFFEFFh
.text:8053F3B2                 mov     ebx, [ebp+68h]
.text:8053F3B5                 mov     eax, 80000004h
.text:8053F3BA                 jmp     loc_8053F013
.text:8053F3BF ; ---------------------------------------------------------------------------
.text:8053F3BF
.text:8053F3BF loc_8053F3BF:                           ; CODE XREF: _KiTrap01+85↑j
.text:8053F3BF                                         ; _KiTrap01+94↑j
.text:8053F3BF                 mov     ebx, ds:0FFDFF124h
.text:8053F3C5                 mov     ebx, [ebx+44h]
.text:8053F3C8                 cmp     dword ptr [ebx+158h], 0
.text:8053F3CF                 jz      short loc_8053F3AA
.text:8053F3D1                 push    1
.text:8053F3D3                 call    _Ki386VdmReflectException_A@4 ; Ki386VdmReflectException_A(x)
.text:8053F3D8                 test    ax, 0FFFFh
.text:8053F3DC                 jz      short loc_8053F3AB
.text:8053F3DE                 jmp     Kei386EoiHelper@0 ; Kei386EoiHelper()
.text:8053F3E3 ; ---------------------------------------------------------------------------
.text:8053F3E3
.text:8053F3E3 loc_8053F3E3:                           ; CODE XREF: _KiTrap01+6D↑j
.text:8053F3E3                 mov     eax, ds:0FFDFF054h
.text:8053F3E8                 mov     dword ptr ds:0FFDFF054h, 0
.text:8053F3F2                 mov     [ebp+68h], eax
.text:8053F3F5                 mov     esp, ebp
.text:8053F3F7                 jmp     Kei386EoiHelper@0 ; Kei386EoiHelper()
.text:8053F3F7 _KiTrap01       endp
```

push ret跳转地址需要6字节

cpy to ker

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>


// target 8003f120
// 8053E545
// 0x4ff420

void JmpTarget();


int i;
char* p;
void __declspec(naked) IdtEntry() {
	
	p = (char*)0x8003f120;
	for(i=0; i<64; i++){
		*p = ((char*)JmpTarget)[i];
		p++;
	}
	__asm {
		iretd
	}
}

void __declspec(naked) JmpTarget() {
	
	__asm {
		push eax
		mov eax, ss:[esp+4]
		mov ds:[0x8003f3f0], eax
		pop eax

		push 0
		mov word ptr [esp+2], 0

		push 0x8053F31D
		ret
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	system("pause");
}
```

修改trap01函数

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

DWORD g_num;

void __declspec(naked) IdtEntry() {
	__asm {
		mov eax, cr0
		and eax, not 10000h
		mov cr0, eax
		
		// push 0x8003f120
		mov eax, 0x03f12068
		mov ds:[0x8053F314], eax
		mov ax, 0xc380
		mov ds:[0x8053F318], ax

		mov eax, cr0
		or  eax, 10000h
		mov cr0, eax
		iretd
	}
}


void go() {
	__asm{
		int 0x20;
	}
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	while(1){
		go();
		Sleep(1000);
		printf("%d\n", g_num);
	}
	system("pause");
}
```

读出01断点断的位置

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

DWORD g_num;

void __declspec(naked) IdtEntry() {
	__asm {
		mov eax, ds:[0x8003f3f0]
		mov g_num, eax
		iretd
	}
}


void go() {
	__asm{
		int 0x20;
	}
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	while(1){
		go();
		Sleep(1000);
		printf("%x\n", g_num);
	}
	system("pause");
}
```

## 优化

cpy

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>


// target 8003f120
// 8053E545
// 0x4ff420

void JmpTarget();


int i;
char* p;
void __declspec(naked) IdtEntry() {
	
	p = (char*)0x8003f120;
	for(i=0; i<64; i++){
		*p = ((char*)JmpTarget)[i];
		p++;
	}
	__asm {
		iretd
	}
}

void __declspec(naked) JmpTarget() {
	
	__asm {
		push eax
		mov eax, ss:[esp+4]
		mov ds:[0x8003f3f0], eax
		mov eax, 1
		mov ds:[0x8003f3f4], eax
		pop eax

		push 0
		mov word ptr [esp+2], 0

		push 0x8053F31D
		ret
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	system("pause");
}
```

output

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

DWORD g_num;
DWORD g_enalbed;

void __declspec(naked) IdtEntry() {
	__asm {
		mov eax, ds:[0x8003f3f0]
		mov g_num, eax
		mov eax, ds:[0x8003f3f4]
		mov g_enalbed, eax
		xor eax, eax
		mov ds:[0x8003f3f4], eax
		iretd
	}
}


void go() {
	__asm{
		int 0x20;
	}
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	while(1){
		go();
		Sleep(1000);
		if(g_enalbed){
			printf("%x\n", g_num);
		}
	}
	system("pause");
}
```

# 系统调用

cpy

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>


// target 8003f120
// 8053E545
// 0x4ff420

DWORD Target[3] = {0x8003f120, 0x8003f1c0, 0x8003f200};
DWORD *ServiceTable = (DWORD *)0x8003f3c0;

void SystemCallEntry();
void ReadMem();
void AllocMem();


int i;
char* p;
void __declspec(naked) IdtEntry() {
	
	p = (char*)Target[0];
	for(i=0; i<128; i++){
		*p = ((char*)SystemCallEntry)[i];
		p++;
	}

	p = (char*)Target[1];
	for(i=0; i<64; i++){
		*p = ((char*)ReadMem)[i];
		p++;
	}

	p = (char*)Target[2];
	for(i=0; i<64; i++){
		*p = ((char*)AllocMem)[i];
		p++;
	}
	ServiceTable[0] = 0x8003f1c0;
	ServiceTable[1] = 0x8003f200;
	__asm {
		mov eax, 0x0008f120
		mov ds:[0x8003f508], eax
		mov eax, 0x8003ee00
		mov ds:[0x8003f50c], eax
		iretd
	}
}

void __declspec(naked) SystemCallEntry() {
	
	__asm {
		push 0x30
		pop fs
		sti

		mov ebx, ss:[esp + 0xc]
		mov ecx, ds:[ebx + 4]
		mov ebx, 0x8003f3c0
		mov edx, ds:[ebx + eax*4]
		call edx

		cli
		push 0x3b
		pop fs
		iretd
	}
}

void __declspec(naked) ReadMem(){
	__asm{
		mov eax, ds:[ecx]
		ret
	}
}

void __declspec(naked) AllocMem(){
	__asm{
		push ecx
		push 0
		mov eax, 0x8053454C
		call eax
		ret
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	system("pause");
}
```

call

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

DWORD ReadMem(DWORD addr);
DWORD AllocMem(DWORD size);

DWORD __declspec(naked) ReadMem(DWORD addr) {
	__asm {
		mov eax, 0
		int 0x21
		ret
	}
}


DWORD __declspec(naked) AllocMem(DWORD size) {
	__asm {
		mov eax, 1
		int 0x21
		ret
	}
}


int main() {
	printf("%p\n", ReadMem(0x8003f3c0));
	printf("%p\n", AllocMem(16));
	system("pause");
}
```

# 非PAE分页

内核文件改变，很多函数地址都换了

!db查看物理内存

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

DWORD g_num = 0x12345678;
DWORD g_cr3;


DWORD __declspec(naked) IdtEntry() {
	__asm {
		mov eax, cr3
		mov g_cr3, eax
		iretd
	}
}


void go() {
	__asm int 0x20;
}


int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("addr:%p\n", &g_num);
	printf("cr3:%p\n", g_cr3);
	system("pause");
}
```

输出

```assembly
addr:00403018
cr3:06DFC000
```

调试

```assembly
kd> !process 0 0
**** NT ACTIVE PROCESS DUMP ****
Failed to get VadRoot
PROCESS 81bbda00  SessionId: none  Cid: 0004    Peb: 00000000  ParentCid: 0000
    DirBase: 00039000  ObjectTable: e1000d20  HandleCount: 255.
    Image: System

Failed to get VadRoot
PROCESS 81b1eda0  SessionId: none  Cid: 015c    Peb: 7ffdf000  ParentCid: 0004
    DirBase: 0d686000  ObjectTable: e14de5c8  HandleCount:  19.
    Image: smss.exe

Failed to get VadRoot
PROCESS 816d9da0  SessionId: 0  Cid: 0244    Peb: 7ffda000  ParentCid: 015c
    DirBase: 0fbb0000  ObjectTable: e17115c8  HandleCount: 469.
    Image: csrss.exe

Failed to get VadRoot
PROCESS 819ef460  SessionId: 0  Cid: 025c    Peb: 7ffd3000  ParentCid: 015c
    DirBase: 02c35000  ObjectTable: e1708500  HandleCount: 433.
    Image: winlogon.exe

Failed to get VadRoot
PROCESS 81671da0  SessionId: 0  Cid: 0288    Peb: 7ffdb000  ParentCid: 025c
    DirBase: 02f76000  ObjectTable: e1b5c790  HandleCount: 283.
    Image: services.exe

Failed to get VadRoot
PROCESS 81879da0  SessionId: 0  Cid: 0294    Peb: 7ffd9000  ParentCid: 025c
    DirBase: 030c1000  ObjectTable: e16b7680  HandleCount: 447.
    Image: lsass.exe

Failed to get VadRoot
PROCESS 817b7428  SessionId: 0  Cid: 0364    Peb: 7ffdd000  ParentCid: 0288
    DirBase: 0322c000  ObjectTable: e1bca0e8  HandleCount:  25.
    Image: vmacthlp.exe

Failed to get VadRoot
PROCESS 8189f3e8  SessionId: 0  Cid: 0370    Peb: 7ffdb000  ParentCid: 0288
    DirBase: 034b7000  ObjectTable: e1bd3b18  HandleCount: 193.
    Image: svchost.exe

Failed to get VadRoot
PROCESS 8162f710  SessionId: 0  Cid: 03c4    Peb: 7ffdf000  ParentCid: 0288
    DirBase: 0d1a7000  ObjectTable: e1bffac0  HandleCount: 275.
    Image: svchost.exe

Failed to get VadRoot
PROCESS 816715c0  SessionId: 0  Cid: 0454    Peb: 7ffdd000  ParentCid: 0288
    DirBase: 0356e000  ObjectTable: e1e167f8  HandleCount: 1173.
    Image: svchost.exe

Failed to get VadRoot
PROCESS 81b007e0  SessionId: 0  Cid: 0480    Peb: 7ffd6000  ParentCid: 0288
    DirBase: 00a40000  ObjectTable: e1e1f3a8  HandleCount:  77.
    Image: svchost.exe

Failed to get VadRoot
PROCESS 81a25698  SessionId: 0  Cid: 04ac    Peb: 7ffd3000  ParentCid: 0288
    DirBase: 0d24b000  ObjectTable: e1e284b8  HandleCount: 188.
    Image: svchost.exe

Failed to get VadRoot
PROCESS 81871b68  SessionId: 0  Cid: 0608    Peb: 7ffd8000  ParentCid: 0288
    DirBase: 0c730000  ObjectTable: e27fa6b8  HandleCount: 130.
    Image: spoolsv.exe

Failed to get VadRoot
PROCESS 8162d5c8  SessionId: 0  Cid: 0684    Peb: 7ffde000  ParentCid: 0668
    DirBase: 0c530000  ObjectTable: e1b54748  HandleCount: 308.
    Image: explorer.exe

Failed to get VadRoot
PROCESS 81a8f978  SessionId: 0  Cid: 06f4    Peb: 7ffdb000  ParentCid: 0684
    DirBase: 0ce5d000  ObjectTable: e170a590  HandleCount:  78.
    Image: rundll32.exe

Failed to get VadRoot
PROCESS 818714d8  SessionId: 0  Cid: 06fc    Peb: 7ffd9000  ParentCid: 0684
    DirBase: 00122000  ObjectTable: e29db0f8  HandleCount: 148.
    Image: vmtoolsd.exe

Failed to get VadRoot
PROCESS 81b01460  SessionId: 0  Cid: 0740    Peb: 7ffde000  ParentCid: 0684
    DirBase: 077f1000  ObjectTable: e2b575c0  HandleCount:  92.
    Image: ctfmon.exe

Failed to get VadRoot
PROCESS 81aaa4f8  SessionId: 0  Cid: 0080    Peb: 7ffdf000  ParentCid: 0288
    DirBase: 0677e000  ObjectTable: e29f3ed8  HandleCount:  85.
    Image: svchost.exe

Failed to get VadRoot
PROCESS 81983b28  SessionId: 0  Cid: 00d8    Peb: 7ffde000  ParentCid: 0288
    DirBase: 0bd61000  ObjectTable: e29b4328  HandleCount: 252.
    Image: sqlservr.exe

Failed to get VadRoot
PROCESS 81a03a10  SessionId: 0  Cid: 0180    Peb: 7ffdf000  ParentCid: 0288
    DirBase: 0baf4000  ObjectTable: e2b931f0  HandleCount:  85.
    Image: sqlwriter.exe

Failed to get VadRoot
PROCESS 81aa3598  SessionId: 0  Cid: 01ac    Peb: 7ffde000  ParentCid: 0288
    DirBase: 0ba60000  ObjectTable: e2b82828  HandleCount:  60.
    Image: VGAuthService.exe

Failed to get VadRoot
PROCESS 81aacb28  SessionId: 0  Cid: 0220    Peb: 7ffdf000  ParentCid: 0288
    DirBase: 09e29000  ObjectTable: e19e5cc0  HandleCount: 267.
    Image: vmtoolsd.exe

Failed to get VadRoot
PROCESS 81789440  SessionId: 0  Cid: 0678    Peb: 7ffdb000  ParentCid: 0454
    DirBase: 02027000  ObjectTable: e181d788  HandleCount:  39.
    Image: wscntfy.exe

Failed to get VadRoot
PROCESS 81a13da0  SessionId: 0  Cid: 0630    Peb: 7ffdf000  ParentCid: 0370
    DirBase: 02238000  ObjectTable: e19c48e8  HandleCount: 228.
    Image: wmiprvse.exe

Failed to get VadRoot
PROCESS 81809da0  SessionId: 0  Cid: 0334    Peb: 7ffd8000  ParentCid: 0288
    DirBase: 05c5f000  ObjectTable: e2b7a280  HandleCount: 105.
    Image: alg.exe

Failed to get VadRoot
PROCESS 817f22e8  SessionId: 0  Cid: 06c4    Peb: 7ffdc000  ParentCid: 0684
    DirBase: 09a62000  ObjectTable: e18f6858  HandleCount: 787.
    Image: devenv.exe

Failed to get VadRoot
PROCESS 81623da0  SessionId: 0  Cid: 0724    Peb: 7ffde000  ParentCid: 0288
    DirBase: 0655a000  ObjectTable: e173c730  HandleCount: 233.
    Image: WPFFontCache_v0400.exe

Failed to get VadRoot
PROCESS 81979da0  SessionId: 0  Cid: 0830    Peb: 7ffdf000  ParentCid: 0454
    DirBase: 0e5be000  ObjectTable: e112f0b8  HandleCount: 139.
    Image: wuauclt.exe

Failed to get VadRoot
PROCESS 81a15da0  SessionId: 0  Cid: 08b8    Peb: 7ffd8000  ParentCid: 06c4
    DirBase: 0ca15000  ObjectTable: e18a8e08  HandleCount:  92.
    Image: vcpkgsrv.exe

Failed to get VadRoot
PROCESS 819ee530  SessionId: 0  Cid: 09fc    Peb: 7ffd6000  ParentCid: 09f0
    DirBase: 06dc9000  ObjectTable: 00000000  HandleCount:   0.
    Image: cheatengine-i386.exe

Failed to get VadRoot
PROCESS 818bd378  SessionId: 0  Cid: 0b4c    Peb: 7ffde000  ParentCid: 0684
    DirBase: 0201b000  ObjectTable: e29cf2d0  HandleCount: 171.
    Image: PCHunter32.exe

Failed to get VadRoot
PROCESS 817c6110  SessionId: 0  Cid: 0c2c    Peb: 7ffdb000  ParentCid: 0c18
    DirBase: 0dc01000  ObjectTable: e2b883d0  HandleCount:  38.
    Image: conime.exe

Failed to get VadRoot
PROCESS 815fc2a0  SessionId: 0  Cid: 0f50    Peb: 7ffde000  ParentCid: 0370
    DirBase: 0a68e000  ObjectTable: e110f4f8  HandleCount: 133.
    Image: wmiprvse.exe

Failed to get VadRoot
PROCESS 819968d0  SessionId: 0  Cid: 0970    Peb: 7ffde000  ParentCid: 06c4
    DirBase: 06dfc000  ObjectTable: e11310f0  HandleCount:  20.
    Image: IdtEntry.exe

Failed to get VadRoot
PROCESS 81628620  SessionId: 0  Cid: 0980    Peb: 7ffda000  ParentCid: 0970
    DirBase: 0d0ee000  ObjectTable: e17be308  HandleCount:  35.
    Image: cmd.exe
```

DirBase就是进程的cr3

```assembly
kd> .formats 403018
Evaluate expression:
  Hex:     00403018
  Decimal: 4206616
  Octal:   00020030030
  Binary:  00000000 01000000 00110000 00011000
  Chars:   .@0.
  Time:    Thu Feb 19 00:30:16 1970
  Float:   low 5.89472e-039 high 0
  Double:  2.07834e-317
```

00000000 01→1

000000 0011→3

0000 00011000→18

|               |      |        |
| ------------- | ---- | ------ |
| 00000000 01   | 1    | pdi    |
| 000000 0011   | 3    | pti    |
| 0000 00011000 | 18   | offset |

```assembly
kd> !dd 06dfc000
# 6dfc000 0a86a067 0ba63067 00000000 00000000
# 6dfc010 00000000 00000000 00000000 00000000
# 6dfc020 00000000 00000000 00000000 00000000
# 6dfc030 00000000 00000000 00000000 00000000
# 6dfc040 00000000 00000000 00000000 00000000
# 6dfc050 00000000 00000000 00000000 00000000
# 6dfc060 00000000 00000000 00000000 00000000
# 6dfc070 00000000 00000000 00000000 00000000
kd> !dd 0ba63000 + 3*4
# ba6300c 0ee41047 04ce1005 00000000 00000000
# ba6301c 00000000 00000000 00000000 00000000
# ba6302c 00000000 00000000 00000000 00000000
# ba6303c 00000000 00000000 00000000 00000000
# ba6304c 00000000 00000000 00000000 00000000
# ba6305c 00000000 00000000 00000000 00000000
# ba6306c 00000000 00000000 00000000 00000000
# ba6307c 00000000 00000000 00000000 00000000
kd> !dd 0ee41000 + 18
# ee41018 12345678 00000000 00000001 00393070
# ee41028 00392a48 00000000 00000000 00000000
# ee41038 00000000 00000000 00000000 00000000
# ee41048 00000000 00000000 00000000 00000000
# ee41058 00000000 00000000 00000000 00000000
# ee41068 00000000 00000000 00000000 00000000
# ee41078 00000000 00000000 00000000 00000000
# ee41088 00000000 00000000 00000000 00000000
```

cr3→PDE→PTE→物理地址

va of pte = ((addr >> 12) << 2) + 0xc0000000

# PAE分页

```assembly
addr:00403018
cr3:00200400
```

调试

```assembly
kd> .formats 403018
Evaluate expression:
  Hex:     00403018
  Decimal: 4206616
  Octal:   00020030030
  Binary:  00000000 01000000 00110000 00011000
  Chars:   .@0.
  Time:    Thu Feb 19 00:30:16 1970
  Float:   low 5.89472e-039 high 0
  Double:  2.07834e-317
```

00→0

000000 010→2

00000 0011→3

0000 00011000→0x18

|               |      |        |
| ------------- | ---- | ------ |
| 00            | 0    | pdpti  |
| 000000 010    | 2    | pdi    |
| 00000 0011    | 3    | pti    |
| 0000 00011000 | 0x18 | offset |

```assembly
kd> !dq 00200400
#  200400 00000000`0674d001 00000000`03eea001
#  200410 00000000`05941001 00000000`0974c001
#  200420 00000000`0d5b9001 00000000`0e9f6001
#  200430 00000000`0a3f7001 00000000`05063001
#  200440 00000000`00c38001 00000000`0dee6001
#  200450 00000000`07e15001 00000000`08060001
#  200460 00000000`fa0f2480 00000000`00000000
#  200470 00000000`00000000 00000000`00000000
kd> !dq 0674d000
# 674d000 00000000`09bcd067 00000000`0dadf067
# 674d010 00000000`02a36067 00000000`00000000
# 674d020 00000000`00000000 00000000`00000000
# 674d030 00000000`00000000 00000000`00000000
# 674d040 00000000`00000000 00000000`00000000
# 674d050 00000000`00000000 00000000`00000000
# 674d060 00000000`00000000 00000000`00000000
# 674d070 00000000`00000000 00000000`00000000
kd> !dq 02a36000
```

以此类推

va of pte = 0xc0000000 + ((addr >> 12) << 3)

va of pde = 0xc0600000 + ((addr >> 21) << 3)

# 零地址读写

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

DWORD g_tmp;

void __declspec(naked) IdtEntry() {
	__asm {
		iretd
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	system("pause");
}
```

windbg

```assembly
kd> !process 0 0
**** NT ACTIVE PROCESS DUMP ****
Failed to get VadRoot
PROCESS 81bbda00  SessionId: none  Cid: 0004    Peb: 00000000  ParentCid: 0000
    DirBase: 00305000  ObjectTable: e1000d20  HandleCount: 245.
    Image: System

Failed to get VadRoot
PROCESS 8187eaf0  SessionId: 0  Cid: 0f10    Peb: 7ffd9000  ParentCid: 0efc
    DirBase: 003c04a0  ObjectTable: e13ec370  HandleCount:  30.
    Image: mspdbsrv.exe

Failed to get VadRoot
PROCESS 81aab720  SessionId: 0  Cid: 0ff8    Peb: 7ffd8000  ParentCid: 0080
    DirBase: 003c0480  ObjectTable: e10b99f8  HandleCount:  22.
    Image: IdtEntry.exe

Failed to get VadRoot
PROCESS 81ac9c08  SessionId: 0  Cid: 012c    Peb: 7ffde000  ParentCid: 0ff8
    DirBase: 003c0460  ObjectTable: e106b8d8  HandleCount:  35.
    Image: cmd.exe

Failed to get VadRoot
PROCESS 81b07c08  SessionId: 0  Cid: 0174    Peb: 7ffde000  ParentCid: 0ff8
    DirBase: 003c04c0  ObjectTable: e12036f8  HandleCount:  38.
    Image: conime.exe

kd> .process /i 81aab720
You need to continue execution (press 'g' <enter>) for the context
to be switched. When the debugger breaks in again, you will be in
the new process context.
kd> g
Break instruction exception - code 80000003 (first chance)
nt!RtlpBreakWithStatusInstruction:
80528bdc cc              int     3
kd> !pte 401000
                    VA 00401000
PDE at C0600010            PTE at C0002008
contains 000000000EF42067  contains 0000000007F51005
pfn ef42      ---DA--UWEV  pfn 7f51      -------UREV

kd> !pte 0
                    VA 00000000
PDE at C0600000            PTE at C0000000
contains 000000000DCC2067  contains 0000000000000000
pfn dcc2      ---DA--UWEV  not valid
```

读

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define PDE(x) ((DWORD *)(0xc0600000 + ((x >> 21) << 3)))

// 0x403018
DWORD g_var = 0x12345678;
DWORD g_out;

void __declspec(naked) IdtEntry() {
	PTE(0)[0] = PTE(0x403018)[0];
	PTE(0)[1] = PTE(0x403018)[1];
	g_out = *(DWORD*)0;
	__asm {
		iretd
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("out:%p\n", *(DWORD*)0x403000);
	printf("out:%p\n", g_out);
	system("pause");
}
```

写

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define PDE(x) ((DWORD *)(0xc0600000 + ((x >> 21) << 3)))

// 0x403018
DWORD g_var = 0x12345678;
DWORD g_out;

void __declspec(naked) IdtEntry() {
	PTE(0)[0] = PTE(0x403018)[0];
	PTE(0)[1] = PTE(0x403018)[1];
	__asm{
		mov eax, cr3
		mov cr3, eax
	}
	g_out = *(DWORD*)0x18;
	*(DWORD*)0x18 = 0xaaaaaaaa;
 	__asm {
		iretd
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("var:%p\n", g_var);
	printf("out:%p\n", g_out);
	printf("var:%p\n", *(DWORD*)(0x403018));
	system("pause");
}
```

输出

```assembly
var:12345678
out:12345678
var:aaaaaaaa
```

# 跨进程内存访问

cp

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>


// target 8003f120
// 8053E545
// 0x4ff420

DWORD Target[3] = {0x8003f120, 0x8003f1c0, 0x8003f200};
DWORD *ServiceTable = (DWORD *)0x8003f3c0;

void SystemCallEntry();
void ReadMem();
void AllocMem();


int i;
char* p;
void __declspec(naked) IdtEntry() {
	
	p = (char*)Target[0];
	for(i=0; i<128; i++){
		*p = ((char*)SystemCallEntry)[i];
		p++;
	}

	ServiceTable[0] = 0x8003f1c0;
	ServiceTable[1] = 0x8003f200;
	__asm {
		mov eax, 0x0008f120
		mov ds:[0x8003f508], eax
		mov eax, 0x8003ee00
		mov ds:[0x8003f50c], eax
		iretd
	}
}

void __declspec(naked) SystemCallEntry() {
	
	__asm {
		mov eax, cr3
		mov ds:[0x8003f3f0], eax

		// dirbase
		mov eax, 0x003c02a0
		mov cr3, eax

		mov ecx, 0x12345678
		mov ds:[0xAAC58], ecx

		mov eax, ds:[0x8003f3f0]
		mov cr3, eax

		iretd
	}
}


void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	system("pause");
}
```

exe

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define PDE(x) ((DWORD *)(0xc0600000 + ((x >> 21) << 3)))


void __declspec(naked) IdtEntry() {
 	__asm {
		iretd
	}
}

void go() {
	__asm int 0x21;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	system("pause");
}
```

# 平行进程

parallel

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

DWORD g_cr3;
DWORD g_num = 0;


void __declspec(naked) IdtEntry() {
	__asm {
		mov eax, cr3
		mov g_cr3, eax
		iretd

		// 00401009
		mov eax, 0x12345678
		nop
		nop
		nop
		mov eax, 1
		mov g_num, eax

		mov ecx, 0xaaaaaaaa
		mov eax, ds:[0x8003f3f0]
		mov cr3, eax
		// 00401029
	}
}


void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	while(1){
		printf("cr3:%p, \t num:%d\n", g_cr3, g_num);
		Sleep(1000);
	}
	system("pause");
}
```

other

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>


DWORD g_num;

void __declspec(naked) IdtEntry() {
 	__asm {
		mov eax, cr3
		mov ds:[0x8003f3f0], eax
		
		mov eax, 0x803c0
		mov cr3, eax

		// 00401011
		mov ecx, 0x12345678
		mov ecx, 0x12345678
		mov ecx, 0x12345678
		mov ecx, 0x12345678

		// 00401025
		nop
		nop
		nop
		nop
		mov g_num, ecx

		iretd
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	system("pause");
}
```

# 延迟内存分配

页异常

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>


DWORD out = 0;
#pragma section("data_seg", read, write)
__declspec(allocate("data_seg")) DWORD var = 1;

void __declspec(naked) IdtEntry() {
 	__asm {
		mov eax, var
		mov out, eax

		iretd
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("%d\n", out);
	system("pause");
}
```

先读一下，让物理页挂上

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>


DWORD out = 0;
#pragma section("data_seg", read, write)
__declspec(allocate("data_seg")) DWORD var = 1;

void __declspec(naked) IdtEntry() {
 	__asm {
		mov eax, var
		mov out, eax

		iretd
	}
}

void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	// use CE read var
	system("pause");
	go();
	printf("%d\n", out);
	system("pause");
}
```

# 数据TLB

确保指令一条接一条执行（不产生页面异常）

确保要测试的虚拟地址已经存放在TLB中（最近的内存访问）

刷新TLB实际上是使无效TLB，不访问内存

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define PDE(x) ((DWORD *)(0xc0600000 + ((x >> 21) << 3)))

DWORD g_out = 0;
#pragma section("data_seg", read, write)
__declspec(allocate("data_seg")) DWORD page1[1024]; // 404000
__declspec(allocate("data_seg")) DWORD page2[1024]; // 405000


void __declspec(naked) IdtEntry() {
	__asm{
		mov eax, ds:[0x405000] // 确保虚拟地址在TLB中
	}
	PTE(0x405000)[0] = PTE(0x404000)[0];
	PTE(0x405000)[1] = PTE(0x404000)[1];
	g_out = page2[0];
	
	__asm {
		iretd
	}
}

void go() {
	page1[0] = 1; // 确保物理页存在
	page2[0] = 2;
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("%d\n", g_out);
	system("pause");
}
```

避免蓝屏

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define PDE(x) ((DWORD *)(0xc0600000 + ((x >> 21) << 3)))

DWORD g_out = 0;
DWORD old_pte[2];
#pragma section("data_seg", read, write)
__declspec(allocate("data_seg")) DWORD page1[1024]; // 404000
__declspec(allocate("data_seg")) DWORD page2[1024]; // 405000


void __declspec(naked) IdtEntry() {
	__asm{
		mov eax, ds:[0x405000] // 确保虚拟地址在TLB中
	}

	old_pte[0] = PTE(0x405000)[0];
	old_pte[1] = PTE(0x405000)[1];

	PTE(0x405000)[0] = PTE(0x404000)[0];
	PTE(0x405000)[1] = PTE(0x404000)[1];
	g_out = page2[0];
	
	PTE(0x405000)[0] = old_pte[0];
	PTE(0x405000)[1] = old_pte[1];

	__asm {
		iretd
	}
}

void go() {
	page1[0] = 1; // 确保物理页存在
	page2[0] = 2;
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("%d\n", g_out);
	system("pause");
}
```

## TLB刷新

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define PDE(x) ((DWORD *)(0xc0600000 + ((x >> 21) << 3)))

DWORD g_out = 0;
DWORD old_pte[2];
#pragma section("data_seg", read, write)
__declspec(allocate("data_seg")) DWORD page1[1024]; // 404000
__declspec(allocate("data_seg")) DWORD page2[1024]; // 405000


void __declspec(naked) IdtEntry() {
	__asm{
		mov eax, ds:[0x405000] // 确保虚拟地址在TLB中
	}

	old_pte[0] = PTE(0x405000)[0];
	old_pte[1] = PTE(0x405000)[1];

	PTE(0x405000)[0] = PTE(0x404000)[0];
	PTE(0x405000)[1] = PTE(0x404000)[1];
	
	__asm{
		mov eax, cr3
		mov cr3, eax
	}
	
	g_out = page2[0];
	
	PTE(0x405000)[0] = old_pte[0];
	PTE(0x405000)[1] = old_pte[1];

	__asm {
		iretd
	}
}

void go() {
	page1[0] = 1; // 确保物理页存在
	page2[0] = 2;
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("%d\n", g_out);
	system("pause");
}
```

设置G位

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define PDE(x) ((DWORD *)(0xc0600000 + ((x >> 21) << 3)))

DWORD g_out = 0;
DWORD old_pte[2];
#pragma section("data_seg", read, write)
__declspec(allocate("data_seg")) DWORD page1[1024]; // 404000
__declspec(allocate("data_seg")) DWORD page2[1024]; // 405000


void __declspec(naked) IdtEntry() {
	
	old_pte[0] = PTE(0x405000)[0];
	old_pte[1] = PTE(0x405000)[1];

	PTE(0x405000)[0] = PTE(0x404000)[0] | 0x100; // 设置G位
	PTE(0x405000)[1] = PTE(0x404000)[1];
	
	__asm{
		mov eax, cr3
		mov cr3, eax
	}

	__asm{
		mov eax, ds:[0x405000] // 确保虚拟地址在TLB中
	}
	
	g_out = page2[0];
	
	PTE(0x405000)[0] = old_pte[0];
	PTE(0x405000)[1] = old_pte[1];

	__asm {
		iretd
	}
}

void go() {
	page1[0] = 1; // 确保物理页存在
	page2[0] = 2;
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("%d\n", g_out);
	system("pause");
}
```

清空没有标记G位的TLB项

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define PDE(x) ((DWORD *)(0xc0600000 + ((x >> 21) << 3)))

DWORD g_out = 0;
DWORD old_pte[2];
#pragma section("data_seg", read, write)
__declspec(allocate("data_seg")) DWORD page1[1024]; // 404000
__declspec(allocate("data_seg")) DWORD page2[1024]; // 405000


void __declspec(naked) IdtEntry() {
	
	old_pte[0] = PTE(0x405000)[0];
	old_pte[1] = PTE(0x405000)[1];

	PTE(0x405000)[0] = PTE(0x404000)[0] | 0x100; // 设置G位
	PTE(0x405000)[1] = PTE(0x404000)[1];
	
	__asm{
		mov eax, cr3
		mov cr3, eax
	}

	__asm{
		mov eax, ds:[0x405000] // 确保虚拟地址在TLB中
	}
	
	__asm{    // 清空没有标记G位的TLB项
		mov eax, cr3
		mov cr3, eax
	}

	g_out = page2[0];
	
	PTE(0x405000)[0] = old_pte[0];
	PTE(0x405000)[1] = old_pte[1];

	__asm {
		iretd
	}
}

void go() {
	page1[0] = 1; // 确保物理页存在
	page2[0] = 2;
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("%d\n", g_out);
	system("pause");
}
```

输出1

## 对比

### 设置G位

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define PDE(x) ((DWORD *)(0xc0600000 + ((x >> 21) << 3)))

DWORD g_out = 0;
DWORD old_pte[2];
#pragma section("data_seg", read, write)
__declspec(allocate("data_seg")) DWORD page1[1024]; // 404000
__declspec(allocate("data_seg")) DWORD page2[1024]; // 405000


void __declspec(naked) IdtEntry() {
	
	old_pte[0] = PTE(0x405000)[0];
	old_pte[1] = PTE(0x405000)[1];

	PTE(0x405000)[0] = PTE(0x404000)[0] | 0x100; // 设置G位
	PTE(0x405000)[1] = PTE(0x404000)[1];
	
	__asm{
		mov eax, cr3
		mov cr3, eax
	}

	__asm{
		mov eax, ds:[0x405000] // 确保虚拟地址在TLB中
	}

	PTE(0x405000)[0] = old_pte[0];
	PTE(0x405000)[1] = old_pte[1];
	
	__asm{    // 清空没有标记G位的TLB项
		mov eax, cr3
		mov cr3, eax
	}

	g_out = page2[0];

	__asm {
		iretd
	}
}

void go() {
	page1[0] = 1; // 确保物理页存在
	page2[0] = 2;
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("%d\n", g_out);
	system("pause");
}
```

输出1

### 不设置G位

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define PDE(x) ((DWORD *)(0xc0600000 + ((x >> 21) << 3)))

DWORD g_out = 0;
DWORD old_pte[2];
#pragma section("data_seg", read, write)
__declspec(allocate("data_seg")) DWORD page1[1024]; // 404000
__declspec(allocate("data_seg")) DWORD page2[1024]; // 405000


void __declspec(naked) IdtEntry() {
	
	old_pte[0] = PTE(0x405000)[0];
	old_pte[1] = PTE(0x405000)[1];

	PTE(0x405000)[0] = PTE(0x404000)[0]; // 设置G位
	PTE(0x405000)[1] = PTE(0x404000)[1];
	
	__asm{
		mov eax, cr3
		mov cr3, eax
	}

	__asm{
		mov eax, ds:[0x405000] // 确保虚拟地址在TLB中
	}

	PTE(0x405000)[0] = old_pte[0];
	PTE(0x405000)[1] = old_pte[1];
	
	__asm{    // 清空没有标记G位的TLB项
		mov eax, cr3
		mov cr3, eax
	}

	g_out = page2[0];

	__asm {
		iretd
	}
}

void go() {
	page1[0] = 1; // 确保物理页存在
	page2[0] = 2;
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("%d\n", g_out);
	system("pause");
}
```

输出2

强行更新TLB项，无视G位

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define PDE(x) ((DWORD *)(0xc0600000 + ((x >> 21) << 3)))

DWORD g_out = 0;
DWORD old_pte[2];
#pragma section("data_seg", read, write)
__declspec(allocate("data_seg")) DWORD page1[1024]; // 404000
__declspec(allocate("data_seg")) DWORD page2[1024]; // 405000


void __declspec(naked) IdtEntry() {
	
	old_pte[0] = PTE(0x405000)[0];
	old_pte[1] = PTE(0x405000)[1];

	PTE(0x405000)[0] = PTE(0x404000)[0] | 0x100; // 设置G位
	PTE(0x405000)[1] = PTE(0x404000)[1];
	
	__asm{
		mov eax, cr3
		mov cr3, eax
	}

	__asm{
		mov eax, ds:[0x405000] // 确保虚拟地址在TLB中
	}

	PTE(0x405000)[0] = old_pte[0];
	PTE(0x405000)[1] = old_pte[1];
	
	__asm{
		invlpg ds:[0x405000]
	}

	g_out = page2[0];

	__asm {
		iretd
	}
}

void go() {
	page1[0] = 1; // 确保物理页存在
	page2[0] = 2;
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	printf("%d\n", g_out);
	system("pause");
}
```

# 指令TLB与流水线

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define PDE(x) ((DWORD *)(0xc0600000 + ((x >> 21) << 3)))

DWORD g_out = 0;
DWORD old_pte[2];
#pragma section("data_seg", read, write)
__declspec(allocate("data_seg")) DWORD page1[1024]; // 404000
__declspec(allocate("data_seg")) DWORD page2[1024]; // 405000


void __declspec(naked) IdtEntry() {
	
	old_pte[0] = PTE(0x405000)[0];
	old_pte[1] = PTE(0x405000)[1];

	__asm{
		mov eax, cr3
		mov cr3, eax

		mov eax, ds:[0x405000] // 确保虚拟地址在TLB中
	}

	PTE(0x405000)[0] = PTE(0x404000)[0]; // 设置G位
	PTE(0x405000)[1] = PTE(0x404000)[1];
	
	__asm{
		mov eax, ds:[0x405000]
		mov g_out, eax
	}

	PTE(0x405000)[0] = old_pte[0];
	PTE(0x405000)[1] = old_pte[1];

	__asm{
		mov eax, cr3
		mov cr3, eax
	}

	__asm {
		iretd
	}
}

void go() {
	page1[0] = 0xc3; // 确保物理页存在
	page2[0] = 0xc390;
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	for(int i=0; i<50000; i++){
		go();
		if(g_out != 0xc390)
			printf("%p\n", g_out);
	}
	system("pause");
}
```

有可能输出

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define PDE(x) ((DWORD *)(0xc0600000 + ((x >> 21) << 3)))

DWORD g_out = 0;
DWORD old_pte[2];
#pragma section("data_seg", read, write)
__declspec(allocate("data_seg")) DWORD page1[1024]; // 404000
__declspec(allocate("data_seg")) DWORD page2[1024]; // 405000


void __declspec(naked) IdtEntry() {
	
	old_pte[0] = PTE(0x405000)[0];
	old_pte[1] = PTE(0x405000)[1];

	__asm{
		mov eax, cr3
		mov cr3, eax
	}

	PTE(0x405000)[0] = PTE(0x404000)[0]; // 设置G位
	PTE(0x405000)[1] = PTE(0x404000)[1];
	
	__asm{
		mov eax, ds:[0x405000]
		mov g_out, eax
	}

	PTE(0x405000)[0] = old_pte[0];
	PTE(0x405000)[1] = old_pte[1];

	__asm{
		mov eax, cr3
		mov cr3, eax
	}

	__asm {
		iretd
	}
}

void go() {
	page1[0] = 0xc3; // 确保物理页存在
	page2[0] = 0xc390;
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	for(int i=0; i<50000; i++){
		go();
		if(g_out == 0xc390)
			printf("%p\n", g_out);
	}
	system("pause");
}
```

无输出

## 使代码段可执行

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define PDE(x) ((DWORD *)(0xc0600000 + ((x >> 21) << 3)))

DWORD g_out = 0;
DWORD old_pte[2];
#pragma section("data_seg", read, write)
__declspec(allocate("data_seg")) DWORD page1[1024]; // 404000
__declspec(allocate("data_seg")) DWORD page2[1024]; // 405000


void __declspec(naked) IdtEntry() {
	
	old_pte[0] = PTE(0x405000)[0];
	old_pte[1] = PTE(0x405000)[1];

	__asm{
		mov eax, cr3
		mov cr3, eax
	}

	PTE(0x405000)[0] = PTE(0x404000)[0]; // 设置G位
	PTE(0x405000)[1] = PTE(0x404000)[1];
	
	__asm{
		mov eax, ds:[0x405000]
		mov g_out, eax
	}

	PTE(0x405000)[0] = old_pte[0];
	PTE(0x405000)[1] = old_pte[1];

	__asm{
		mov eax, cr3
		mov cr3, eax
	}

	__asm {
		iretd
	}
}

void go() {
	page1[0] = 0xc3; // 确保物理页存在
	page2[0] = 0xc390;

	((void (*)())(DWORD)page1)();
	((void (*)())(DWORD)page2)();

	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	for(int i=0; i<10000; i++){
		go();
		if(g_out == 0xc390)
			printf("%p\n", g_out);
	}
	system("pause");
}
```

有一定概率打印出405000处的

# 页面异常

cpy to kernel

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>


#define K_ESP         0x8003f3f4
#define K_ESP_4       0x8003f3f0
#define K_TARGET_CR3  0x8003f3ec
#define K_CR2         0x8003f3e8

void JmpTarget();


int i;
char *p;

void __declspec(naked) IdtEntry() {
	p = (char*)0x8003f120;
	for(i=0; i<256; i++){
		*p = ((char*)JmpTarget)[i];
		p++;
	}

	__asm {
		mov eax, 0xffffffff
		mov ds:[K_TARGET_CR3], eax
		
		mov eax, cr0
		and eax, not 0x10000
		mov cr0, eax

		// do hook
		mov eax, 0x3f12068
		mov ds:[0x80541450], eax  // KiTrap0E
		mov ax, 0xc380
		mov ds:[0x80541454], ax   // KiTrap0E + 4

		xor eax, eax
		mov ds:[K_ESP], eax
		mov ds:[K_ESP_4], eax
		mov ds:[K_CR2], eax

		mov eax, cr0
		or eax, 0x10000
		mov cr0, eax
	}
}

void __declspec(naked) JmpTarget() {
	
	__asm {
		push eax
		mov eax, cr3
		cmp eax, ds:[K_TARGET_CR3]
		jnz End

		mov eax, [esp + 4]
		mov ds:[K_ESP], eax
		mov eax, [esp + 8]
		mov ds:[K_ESP_4], eax
		mov eax, cr2
		mov ds:[K_CR2], eax

End:
		pop eax
		mov word ptr [esp + 2], 0
		push 0x80541457  // KiTrap0E + 7
		ret
	}
}


void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	system("pause");
}
```

call

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define K_ESP         0x8003f3f4
#define K_ESP_4       0x8003f3f0
#define K_TARGET_CR3  0x8003f3ec
#define K_CR2         0x8003f3e8


DWORD g_esp;
DWORD g_esp_4;
DWORD g_cr2;


void __declspec(naked) IdtEntry() {

	__asm{
		mov eax, cr3
		mov ds:[K_TARGET_CR3], eax

		mov eax, ds:[K_ESP]  // error code
		mov g_esp, eax

		mov eax, ds:[K_ESP_4]  // eip
		mov g_esp_4, eax

		mov eax, ds:[K_CR2]
		mov g_cr2, eax

		xor eax, eax
		mov ds:[K_ESP_4], eax
	}
	
	__asm {
		iretd
	}
}

#pragma section(".my_code") __declspec(allocate(".my_code")) void go();
#pragma section(".my_code") __declspec(allocate(".my_code")) void main();


void go() {
	__asm int 0x20;
}

// 处在页面整边界
int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	while(1){
		go();
		if(g_esp_4){
			printf("eip:%p\terrno:%p\tcr2:%p\n", g_esp_4, g_esp, g_cr2);
		}
		Sleep(1000);
	}
	system("pause");
}
```

这个实验没有成功，蓝屏

# shadow walker

利用TLB机制实现内存隐藏的方式——ShadowWalker。这种技术利用了TLB会缓存线性地址到物理地址映射的特性，当CRC线程检查某段代码时，它使用的线性地址会缓存到TLB的数据页表缓存（Data-TLB）中。而当EIP运行到这段代码时，又会把代码的线性地址缓存到TLB的指令页表缓存（Instruction-TLB）中。这样CPU中就缓存了同一个地址的两份记录，CRC线程从数据页表缓存中读取物理地址，EIP执行流从指令页表缓存中读取物理地址，这两个物理地址是相同的。

ShadowWalker技术的核心就在于修改指令页表缓存中的物理地址，让CRC线程读取原来的代码，而程序真正执行的时候则跳转到其他代码。

这种方式在3环是不稳定的，原因是TLB经常刷新。

cpy to kernel

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>


#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define K_ESP         0x8003f3f4
#define K_ESP_4       0x8003f3f0
#define K_TARGET_CR3  0x8003f3ec
#define K_CR2         0x8003f3e8

#define K_REAL_PTE0   0x8003f3e4
#define K_REAL_PTE1   0x8003f3e0
#define K_FAKE_PTE0   0x8003f3dc
#define K_FAKE_PTE1   0x8003f3d8

void JmpTarget();


int i;
char *p;

void __declspec(naked) IdtEntry() {
	p = (char*)0x8003f120;
	for(i=0; i<256; i++){
		*p = ((char*)JmpTarget)[i];
		p++;
	}

	__asm {
		mov eax, 0xffffffff
		mov ds:[K_TARGET_CR3], eax
		
		mov eax, cr0
		and eax, not 0x10000
		mov cr0, eax

		// do hook
		mov eax, 0x3f12068
		mov ds:[0x80541450], eax  // KiTrap0E
		mov ax, 0xc380
		mov ds:[0x80541454], ax   // KiTrap0E + 4

		xor eax, eax
		mov ds:[K_ESP], eax
		mov ds:[K_ESP_4], eax
		mov ds:[K_CR2], eax

		mov eax, cr0
		or eax, 0x10000
		mov cr0, eax
	}
}

void __declspec(naked) JmpTarget() {
	
	__asm {
		pushad
		mov eax, cr3
		cmp eax, ds:[K_TARGET_CR3]
		jnz PASS

		mov eax, cr2
		shr eax, 0xc
		cmp eax, 0x402
		jnz PASS

		// read error number
		mov eax, ss:[esp + 0x20]
		test eax, 0x10
		jnz EXECUTE
		jmp READ_WRITE

EXECUTE:
	}
	// 挂真实页面
	PTE(0x402000)[0] = *(DWORD *)K_REAL_PTE0;
	PTE(0x402000)[1] = *(DWORD *)K_REAL_PTE1;
	__asm{
		mov eax, 0x00402005
		call eax
	}
	// 设置成页面不存在
	PTE(0x402000)[0] = PTE(0x402000)[1] = 0;

	__asm{
		popad
		add esp, 4
		iretd

READ_WRITE:
	}
	// 挂真实页面
	PTE(0x402000)[0] = *(DWORD *)K_FAKE_PTE0;
	PTE(0x402000)[1] = *(DWORD *)K_FAKE_PTE1;
	__asm{
		mov eax, ds:[0x402000]
	}
	// 设置成页面不存在
	PTE(0x402000)[0] = PTE(0x402000)[1] = 0;

	__asm{
		popad
		add esp, 4
		iretd

PASS:
		popad
		mov word ptr [esp + 2], 0
		push 0x80541457  // KiTrap0E + 7
		ret
	}
}


void go() {
	__asm int 0x20;
}

int main() {
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	go();
	system("pause");
}
```

call

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define PTE(x) ((DWORD *)(0xc0000000 + ((x >> 12) << 3)))
#define K_ESP         0x8003f3f4
#define K_ESP_4       0x8003f3f0
#define K_TARGET_CR3  0x8003f3ec
#define K_CR2         0x8003f3e8

#define K_REAL_PTE0   0x8003f3e4
#define K_REAL_PTE1   0x8003f3e0
#define K_FAKE_PTE0   0x8003f3dc
#define K_FAKE_PTE1   0x8003f3d8


DWORD g_esp;
DWORD g_esp_4;
DWORD g_cr2;

#pragma section("data_seg", read, write)
__declspec(allocate("data_seg")) DWORD FakePage[1024];  // 405000

void __declspec(naked) IdtEntry() {
	*(DWORD *)K_REAL_PTE0 = PTE(0x402000)[0];
	*(DWORD *)K_REAL_PTE1 = PTE(0x402000)[1];
	*(DWORD *)K_FAKE_PTE0 = PTE(0x405000)[0];
	*(DWORD *)K_FAKE_PTE1 = PTE(0x405000)[1];

	PTE(0x402000)[0] = PTE(0x402000)[1] = 0;

	__asm{
		mov eax, cr3
		mov ds:[K_TARGET_CR3], eax
	}
	
	__asm {
		iretd
	}
}

#pragma section(".my_code") __declspec(allocate(".my_code")) void go();
#pragma section(".my_code") __declspec(allocate(".my_code")) void main();


void go() {
	__asm int 0x20;
}

// 处在页面整边界
int main() {
	__asm{
		jmp L
		ret  // 00402005
L:
	}
	if ((DWORD)IdtEntry != 0x401000) {
		printf("wrong addr:%p", IdtEntry);
		exit(-1);
	}
	FakePage[0] = 0;
	go();
	int i = 0;
	while(1){
		printf("%d\n", i++);
		Sleep(1000);
	}
	system("pause");
}
```

