---
layout: post
title:  CISCN_gift
date:   2021-05-27 00:01:01 +0300
image:  2021-05-27-beach.jpg
tags:   [ctf,reverse,ciscn2021,golang]
---

运行文件，发现应该是要优化算法

```assembly
Welcome to CISCN 2021!
Here is our free flag for you as a gift:
CISCN{4b445b
```

拖入ida分析

先把所有汇编代码段中的内容选中，直接按c转为代码，然后把红色的未识别问函数的部分按p手动转为函数。

使用IDAGolangHelper恢复函数名，结果发现报错了。

Try to determine go version based on moduledata

```assembly
Traceback (most recent call last):
  File "_ctypes/callbacks.c", line 315, in 'calling callback function'
  File "D:\software\ida_pro70\IDA_Pro_v7.0\python\ida_kernwin.py", line 4147, in helper_cb
    r = self.handler(button_code)
  File "D:/software/ida_pro70/IDA_Pro_v7.0/IDAGolangHelper-master/go_entry.py", line 52, in OnButton1
    GO_SETTINGS.findModuleData()
  File "D:/software/ida_pro70/IDA_Pro_v7.0/IDAGolangHelper-master\GO_Utils\__init__.py", line 39, in findModuleData
    fmd = Firstmoduledata.findFirstModuleData(gopcln_addr, self.bt_obj)
  File "D:/software/ida_pro70/IDA_Pro_v7.0/IDAGolangHelper-master\GO_Utils\Firstmoduledata.py", line 6, in findFirstModuleData
    possible_addr = [x for x in idautils.XrefsTo(addr)]
  File "D:\software\ida_pro70\IDA_Pro_v7.0\python\idautils.py", line 188, in XrefsTo
    if xref.first_to(ea, flags):
  File "D:\software\ida_pro70\IDA_Pro_v7.0\python\ida_xref.py", line 253, in first_to
    return _ida_xref.xrefblk_t_first_to(self, *args)
TypeError: Expected an ea_t type
```

Try to determine go version based on version string

```assembly
None
```

Rename functions

```assembly
Traceback (most recent call last):
  File "_ctypes/callbacks.c", line 315, in 'calling callback function'
  File "D:\software\ida_pro70\IDA_Pro_v7.0\python\ida_kernwin.py", line 4147, in helper_cb
    r = self.handler(button_code)
  File "D:/software/ida_pro70/IDA_Pro_v7.0/IDAGolangHelper-master/go_entry.py", line 57, in OnButton3
    GO_SETTINGS.renameFunctions()
  File "D:/software/ida_pro70/IDA_Pro_v7.0/IDAGolangHelper-master\GO_Utils\__init__.py", line 56, in renameFunctions
    Gopclntab.rename(gopcln_tab, self.bt_obj)
  File "D:/software/ida_pro70/IDA_Pro_v7.0/IDAGolangHelper-master\GO_Utils\Gopclntab.py", line 42, in rename
    pos = beg + 8 #skip header
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```

 顺着报错查看源码

```assembly
def renameFunctions(self):
    gopcln_tab = self.getGopcln()
    Gopclntab.rename(gopcln_tab, self.bt_obj)
```

用print输出gopcln_tab的值

```assembly
def renameFunctions(self):
    gopcln_tab = self.getGopcln()
    print("gopcln_tab=", gopcln_tab)
    Gopclntab.rename(gopcln_tab, self.bt_obj)
```

输出

```assembly
('gopcln_tab=', None)
```

查看getGopcln()

```assembly
def getGopcln(self):
    gopcln_addr = self.getVal("gopcln")
    if gopcln_addr is None:
        gopcln_addr = Gopclntab.findGoPcLn()
        self.setVal("gopcln", gopcln_addr)
    return gopcln_addr
```

还是利用print查看变量的值

```assembly
('gopcln_tab=', None)
```

所以推测应该是Gopclntab.findGoPcLn()返回了None

查看findGoPcLn()

```assembly
def findGoPcLn():
    possible_loc = ida_search.find_binary(0, idc.BADADDR, lookup, 16, idc.SEARCH_DOWN) #header of gopclntab
    while possible_loc != idc.BADADDR:
        if check_is_gopclntab(possible_loc):
            return possible_loc
        else:
            #keep searching till we reach end of binary
            possible_loc = ida_search.find_binary(possible_loc+1, idc.BADADDR, lookup, 16, idc.SEARCH_DOWN)
    return None
```

```assembly
lookup = "FF FF FF FB 00 00" if is_be else "FB FF FF FF 00 00"
```

这里根据函数名字和作者给的注释可以推测函数的作用。

getGopcln()函数尝试查找exe中.pclntab段，并返回段的地址，如果没查找到，就调用 findGoPcln搜索lookup常数，找到以后调用check_is_gopclntab()对数据结构进行检查，通过以后返回lookup常数的地址。

所以问题就是这个exe里，没有找到gopclntab

**pclntab** 全名是 **Program Counter Line Table**，可直译为 **程序计数器行数映射表**， 在 Go 中也叫 **Runtime Symbol Table**。按 Russ Cox 在《**[Go 1.2 Runtime Symbol Information](http://golang.org/s/go12symtab)**》中的说法，引入 **pcnlntab** 这个结构的最初动机，是为 **Stack Trace** 服务的。当程序运行出错要 **panic** 的时候，runtime 需要知道当前的位置，层级关系如 pkg->src file->function or method->line number，每一层的信息 runtime 都要知道。Go 就把这些信息结构化地打包到了编译出的二进制文件中。除此之外，**pcnlntab** 中还包含了栈的动态管理用到的栈帧信息、垃圾回收用到的栈变量的生命周期信息以及二进制文件涉及的所有源码文件路径信息。

**pclntab** 的概要结构如下（其中的 **strings** 指的是 Function name string、Source File Path string，并不是整个程序中用到的所有 strings）：

- func table
- _func structs
- pcsp
- psfile
- pcline
- pcdata
- strings
- file table

**pclntab** 开头 4-Bytes 是从 Go1.2 至今不变的 **Magic Number**： **0xFFFFFFFB** ；

第 5、6个字节为 0x00，暂无实际用途；

第 7 个字节代表 **instruction size quantum**， **1** 为 x86, 4 为 ARM；

第 8 个字节为地址的大小，32bit 的为 4，64 bit 的为 8，至此的前 8 个字节可以看作是 **pclntab** 的 Header；

第 9 个字节开始是 **function table** 的起始位置，第一个 uintptr 元素为函数(pc, Program Counter) 的个数；

第 2 个 uintptr 元素为第 1 个函数(pc0) 的地址，第 3 个 uintptr 元素为第 1 个函数结构定义相对于 **pclntab** 的偏移，后面的函数信息就以此类推；

直到 function table 结束，下面就是 Source file table。Source file table 以 4 字节(**int32**)为单位，前 4 个字节代表 Source File 的数量，后面每一个 **int32** 都代表一个 Source File Path String 相对于 **pclntab** 的偏移；

**uintptr** 代表一个指针类型，在 32bit 二进制文件中，等价于 **uint32**，在 64bit 二进制文件中，等价于 **uint64** 。

所以IDAGolangHelper脚本中查找的lookup常数就是Magic Number了，没找到的原因可能是Magic Number被更换，或者pclntab的结构变了，可以用对照的方式找到这个出问题的exe中的pclntab。

截取一段特征码去另一个exe里搜索

自己编译一个strip的golang程序，查找0xFFFFFFFB，.gopclntab段的第一个结果就是我们要的pclntab，找他的交叉引用，能找到包含指向pclntab指针的一个上层数据结构moduledata，再对moduledata交叉引用。

```assembly
_rt0_amd64_linux（entry point）->
_rt0_amd64 ->
runtime_rt0_go ->
runtime_schedinit ->
runtime_modulesinit
```

在程序中搜索连续三个call指令的代码段

```assembly
.text:0000000000464172 sub_464172      proc near               ; CODE XREF: sub_464080+EB↑j
.text:0000000000464172
.text:0000000000464172 arg_0           = qword ptr  8
.text:0000000000464172 arg_8           = dword ptr  10h
.text:0000000000464172 arg_10          = qword ptr  18h
.text:0000000000464172
.text:0000000000464172                 mov     rbx, gs:28h
.text:000000000046417B                 lea     rcx, unk_56F860
.text:0000000000464182                 mov     [rbx+0], rcx
.text:0000000000464189                 lea     rax, unk_56F9E0
.text:0000000000464190                 mov     [rax], rcx
.text:0000000000464193                 mov     [rcx+30h], rax
.text:0000000000464197                 cld
.text:0000000000464198                 call    sub_446480
.text:000000000046419D                 mov     eax, [rsp+arg_8]
.text:00000000004641A1                 mov     [rsp+0], eax
.text:00000000004641A4                 mov     rax, [rsp+arg_10]
.text:00000000004641A9                 mov     [rsp+arg_0], rax
.text:00000000004641AE                 call    sub_4461A0
.text:00000000004641B3                 call    sub_431080
.text:00000000004641B8                 call    sub_439940
.text:00000000004641BD                 lea     rax, off_4F2AD0
.text:00000000004641C4                 push    rax
.text:00000000004641C5                 push    0
.text:00000000004641C7                 call    sub_4412A0
.text:00000000004641CC                 pop     rax
.text:00000000004641CD                 pop     rax
.text:00000000004641CE                 call    sub_43B360
.text:00000000004641D3                 call    sub_465FA0
.text:00000000004641D3 sub_464172      endp
```

这里有一处连续执行了三次call，分别是：

* call runtime_args
* call runtime_osinit
* call runtime_schedinit

进入sub_439940(runtime_schedinit)函数

```assembly
.text:0000000000439940 sub_439940      proc near               ; CODE XREF: sub_464172+46↓p
.text:0000000000439940                                         ; DATA XREF: .rdata:0000000000536B20↓o ...
.text:0000000000439940
.text:0000000000439940 var_58          = qword ptr -58h
.text:0000000000439940 var_50          = qword ptr -50h
.text:0000000000439940 var_48          = qword ptr -48h
.text:0000000000439940 var_40          = qword ptr -40h
.text:0000000000439940 var_34          = dword ptr -34h
.text:0000000000439940 var_30          = qword ptr -30h
.text:0000000000439940 var_28          = qword ptr -28h
.text:0000000000439940 var_20          = qword ptr -20h
.text:0000000000439940 var_18          = qword ptr -18h
.text:0000000000439940 var_10          = qword ptr -10h
.text:0000000000439940 var_8           = qword ptr -8
.text:0000000000439940
.text:0000000000439940                 mov     rcx, gs:28h
.text:0000000000439949                 mov     rcx, [rcx+0]
.text:0000000000439950                 cmp     rsp, [rcx+10h]
.text:0000000000439954                 jbe     loc_439C00
.text:000000000043995A                 sub     rsp, 58h
.text:000000000043995E                 mov     [rsp+58h+var_8], rbp
.text:0000000000439963                 lea     rbp, [rsp+58h+var_8]
.text:0000000000439968                 mov     rax, gs:28h
.text:0000000000439971                 mov     rax, [rax+0]
.text:0000000000439978                 mov     [rsp+58h+var_18], rax
.text:000000000043997D                 mov     cs:dword_56F738, 2710h
.text:0000000000439987                 nop
.text:0000000000439988                 lea     rcx, off_55DA80
.text:000000000043998F                 jmp     short loc_4399B0
```

其中lea  rcx,off_55DA80的off_55DA80，点击进入

```assembly
.data:000000000055DA80 off_55DA80      dq offset unk_4F8460    ; DATA XREF: sub_4180A0+C9↑o
.data:000000000055DA80                                         ; sub_439940+48↑o ...
.data:000000000055DA88                 dq offset aGoBuildid    ; "go.buildid"
.data:000000000055DA90                 db  40h ; @
.data:000000000055DA91                 db 0B4h
.data:000000000055DA92                 db    0
```

dq offset unk_4F8460的unk_4F8460就是moduledata。

在 Go 语言的体系中，Module 是比 Package 更高层次的概念，具体表现在一个 Module 中可以包含多个不同的 Package，而每个 Package 中可以包含多个目录和很多的源码文件。

相应地，**Moduledata** 在 Go 二进制文件中也是一个更高层次的数据结构，它包含很多其他结构的索引信息，可以看作是 Go 二进制文件中 RTSI(Runtime Symbol Information) 和 RTTI(Runtime Type Information) 的 **地图**。

根据 **Moduledata** 的定义，Moduledata 是可以串成链表的形式的，而一个完整的可执行 Go 二进制文件中，只有一个 **firstmoduledata** 包含如上完整的字段。简单介绍一下关键字段：

- 第 1 个字段 **pclntable**，即为 **pclntab** 的地址；
- 第 2 个字段 **ftab**，为 **pclntab** 中 Function Table 的地址(=pclntab_addr + 8)；
- 第 3 个字段 **filetab**，为 **pclntab** 中 Source File Table 的地址；
- 第 5 个字段 **minpc**，为 **pclntab** 中第一个函数的起始地址；
- 第 7 个字段 **text**，在普通二进制文件中，对应于 [.text] section 的起始地址；在 PIE 二进制文件中则没有这个要求；
- 字段 **types**，为存放程序中所有数据类型定义信息数据的起始地址，一般对应于 [.rodata] section 的地址；
- 字段 **typelinks**，为每个数据类型相对于 **types** 地址的偏移表，该字段与 **types** 字段在后文解析 RTTI 时要用到；
- 字段 **itablinks**，则是 Interface Table 的起始地址，该字段解析 Interface Table 时要用到。

点击进入，找到pclntab。

```assembly
.rdata:00000000004F8460 unk_4F8460      db 0FAh                 ; DATA XREF: .data:off_55DA80↓o
.rdata:00000000004F8461                 db 0FFh
.rdata:00000000004F8462                 db 0FFh
.rdata:00000000004F8463                 db 0FFh
.rdata:00000000004F8464                 db    0
.rdata:00000000004F8465                 db    0
.rdata:00000000004F8466                 db    1
.rdata:00000000004F8467                 db    8
.rdata:00000000004F8468                 db 0DAh
.rdata:00000000004F8469                 db    5
.rdata:00000000004F846A                 db    0
.rdata:00000000004F846B                 db    0
.rdata:00000000004F846C                 db    0
.rdata:00000000004F846D                 db    0
.rdata:00000000004F846E                 db    0
.rdata:00000000004F846F                 db    0
.rdata:00000000004F8470                 db 0ACh
.rdata:00000000004F8471                 db    0
.rdata:00000000004F8472                 db    0
.rdata:00000000004F8473                 db    0
.rdata:00000000004F8474                 db    0
.rdata:00000000004F8475                 db    0
.rdata:00000000004F8476                 db    0
.rdata:00000000004F8477                 db    0
.rdata:00000000004F8478                 db  40h ; @
.rdata:00000000004F8479                 db    0
.rdata:00000000004F847A                 db    0
.rdata:00000000004F847B                 db    0
.rdata:00000000004F847C                 db    0
.rdata:00000000004F847D                 db    0
.rdata:00000000004F847E                 db    0
.rdata:00000000004F847F                 db    0
.rdata:00000000004F8480                 db  80h ; €
.rdata:00000000004F8481                 db 0B4h
.rdata:00000000004F8482                 db    0
.rdata:00000000004F8483                 db    0
.rdata:00000000004F8484                 db    0
.rdata:00000000004F8485                 db    0
.rdata:00000000004F8486                 db    0
.rdata:00000000004F8487                 db    0
.rdata:00000000004F8488                 db 0A0h
.rdata:00000000004F8489                 db 0BBh
.rdata:00000000004F848A                 db    0
.rdata:00000000004F848B                 db    0
.rdata:00000000004F848C                 db    0
.rdata:00000000004F848D                 db    0
.rdata:00000000004F848E                 db    0
.rdata:00000000004F848F                 db    0
.rdata:00000000004F8490                 db 0A0h
.rdata:00000000004F8491                 db 0D9h
.rdata:00000000004F8492                 db    0
.rdata:00000000004F8493                 db    0
.rdata:00000000004F8494                 db    0
.rdata:00000000004F8495                 db    0
.rdata:00000000004F8496                 db    0
.rdata:00000000004F8497                 db    0
.rdata:00000000004F8498                 db 0A0h
.rdata:00000000004F8499                 db 0C6h
.rdata:00000000004F849A                 db    3
.rdata:00000000004F849B                 db    0
.rdata:00000000004F849C                 db    0
.rdata:00000000004F849D                 db    0
.rdata:00000000004F849E                 db    0
.rdata:00000000004F849F                 db    0
.rdata:00000000004F84A0 aGoBuildid      db 'go.buildid',0       ; DATA XREF: .data:000000000055DA88↓o
.rdata:00000000004F84AB                 db  69h ; i
.rdata:00000000004F84AC                 db  6Eh ; n
.rdata:00000000004F84AD                 db  74h ; t
```

(后来发现可以直接在字符串窗口搜索字符串go.buildid)

可以看到Magic Number变成了0xFFFFFFFA，而且结构的内容也变了。

GO语言中的很多机制都需要符号等信息（比如Stack Trace），所以函数名等信息应该还保存在exe中。可以从需要函数名的函数入手（比如Caller），分析函数名和地址的关系。

经调试可得知取函数名的操作在runtime_moduledataverify1的runtime_funcname中，runtime_moduledataverify1中有对比Magic Number的指令**cmp ebx, 0FFFFFFFBh**，所以可以查找常数0xFFFFFFFA在题目文件中定位这个函数。

在ida菜单栏点击搜索，搜索立即值0xFFFFFFFA定位到函数。

```assembly
.text:000000000044EFE0 sub_44EFE0      proc near               ; CODE XREF: sub_439940+5A↑p
.text:000000000044EFE0                                         ; DATA XREF: .rdata:00000000005375E0↓o ...
.text:000000000044EFE0
.text:000000000044EFE0 var_D8          = qword ptr -0D8h
.text:000000000044EFE0 var_D0          = qword ptr -0D0h
.text:000000000044EFE0 var_C8          = qword ptr -0C8h
.text:000000000044EFE0 var_C0          = qword ptr -0C0h
.text:000000000044EFE0 var_B4          = dword ptr -0B4h
.text:000000000044EFE0 var_B0          = qword ptr -0B0h
.text:000000000044EFE0 var_A8          = qword ptr -0A8h
.text:000000000044EFE0 var_A0          = qword ptr -0A0h
.text:000000000044EFE0 var_98          = qword ptr -98h
.text:000000000044EFE0 var_90          = qword ptr -90h
.text:000000000044EFE0 var_88          = qword ptr -88h
.text:000000000044EFE0 var_80          = qword ptr -80h
.text:000000000044EFE0 var_78          = qword ptr -78h
.text:000000000044EFE0 var_70          = qword ptr -70h
.text:000000000044EFE0 var_68          = qword ptr -68h
.text:000000000044EFE0 var_60          = qword ptr -60h
.text:000000000044EFE0 var_58          = qword ptr -58h
.text:000000000044EFE0 var_50          = qword ptr -50h
.text:000000000044EFE0 var_48          = qword ptr -48h
.text:000000000044EFE0 var_40          = qword ptr -40h
.text:000000000044EFE0 var_38          = qword ptr -38h
.text:000000000044EFE0 var_30          = qword ptr -30h
.text:000000000044EFE0 var_28          = xmmword ptr -28h
.text:000000000044EFE0 var_18          = xmmword ptr -18h
.text:000000000044EFE0 var_8           = qword ptr -8
.text:000000000044EFE0 arg_0           = qword ptr  8
.text:000000000044EFE0
.text:000000000044EFE0                 mov     rcx, gs:28h
.text:000000000044EFE9                 mov     rcx, [rcx+0]
.text:000000000044EFF0                 lea     rax, [rsp+var_58]
.text:000000000044EFF5                 cmp     rax, [rcx+10h]
.text:000000000044EFF9                 jbe     loc_44F6C0
.text:000000000044EFFF                 sub     rsp, 0D8h
.text:000000000044F006                 mov     [rsp+0D8h+var_8], rbp
.text:000000000044F00E                 lea     rbp, [rsp+0D8h+var_8]
.text:000000000044F016                 mov     rdx, [rsp+0D8h+arg_0]
.text:000000000044F01E                 mov     rbx, [rdx]
.text:000000000044F021                 mov     esi, [rbx]
.text:000000000044F023                 mov     [rsp+0D8h+var_B4], esi
.text:000000000044F027                 cmp     esi, 0FFFFFFFAh
.text:000000000044F02A                 jnz     loc_44F5F7
.text:000000000044F030                 cmp     byte ptr [rbx+4], 0
.text:000000000044F034                 jnz     loc_44F5F7
.text:000000000044F03A                 cmp     byte ptr [rbx+5], 0
.text:000000000044F03E                 xchg    ax, ax
.text:000000000044F040                 jnz     loc_44F5F7
.text:000000000044F046                 cmp     byte ptr [rbx+6], 1
.text:000000000044F04A                 jnz     loc_44F5F7
.text:000000000044F050                 cmp     byte ptr [rbx+7], 8
.text:000000000044F054                 jnz     loc_44F5F7
.text:000000000044F05A                 mov     rbx, [rdx+80h]
.text:000000000044F061                 mov     rcx, [rdx+88h]
.text:000000000044F068                 lea     rsi, [rcx-1]
.text:000000000044F06C                 xor     eax, eax
.text:000000000044F06E                 jmp     short loc_44F073
.text:000000000044F070 ; ---------------------------------------------
```

函数表在moduledata的偏移变成了 80h

```assembly
.text:000000000044F0BE                 mov     rbx, [r9+rbx+8]; 取出函数表中一项的func_struct_offset
.text:000000000044F0C3                 cmp     rcx, rbx
.text:000000000044F0C6                 jbe     loc_44F5DF
.text:000000000044F0CC                 mov     [rsp+0D8h+var_60], rdi
.text:000000000044F0D1                 mov     [rsp+0D8h+var_68], r10
.text:000000000044F0D6                 mov     [rsp+0D8h+var_70], r9
.text:000000000044F0DB                 mov     [rsp+0D8h+var_78], rax
.text:000000000044F0E0                 lea     rcx, [rbx+r8];rcx = 函数表的地址 + func_struct_offset
.text:000000000044F0E4                 cmp     rsi, r10
.text:000000000044F0E7                 jg      loc_44F358
.text:000000000044F0ED                 mov     ecx, 3
.text:000000000044F0F2                 lea     rbx, unk_4CFF75
```

struct_func

```assembly
struct Func
{
    uintptr      entry;     // start pc
    int32        name;      // name (offset to C string)
    int32        args;      // size of arguments passed to function
    int32        frame;     // size of function frame, including saved caller PC
    int32        pcsp;      // pcsp table (offset to pcvalue table)
    int32        pcfile;    // pcfile table (offset to pcvalue table)
    int32        pcln;      // pcln table (offset to pcvalue table)
    int32        nfuncdata; // number of entries in funcdata list
    int32        npcdata;   // number of entries in pcdata list
};
```

```assembly
.text:0000000000450240 sub_450240      proc near               ; CODE XREF: sub_408F80+65↑p
.text:0000000000450240                                         ; sub_4333C0+49↑p ...
.text:0000000000450240
.text:0000000000450240 var_30          = qword ptr -30h
.text:0000000000450240 var_28          = qword ptr -28h
.text:0000000000450240 var_20          = qword ptr -20h
.text:0000000000450240 var_18          = xmmword ptr -18h
.text:0000000000450240 var_8           = qword ptr -8
.text:0000000000450240 arg_0           = qword ptr  8
.text:0000000000450240 arg_8           = qword ptr  10h
.text:0000000000450240 arg_10          = qword ptr  18h
.text:0000000000450240 arg_18          = qword ptr  20h
.text:0000000000450240
.text:0000000000450240                 mov     rcx, gs:28h
.text:0000000000450249                 mov     rcx, [rcx+0]
.text:0000000000450250                 cmp     rsp, [rcx+10h]
.text:0000000000450254                 jbe     loc_4502E0
.text:000000000045025A                 sub     rsp, 30h
.text:000000000045025E                 mov     [rsp+30h+var_8], rbp
.text:0000000000450263                 lea     rbp, [rsp+30h+var_8]
.text:0000000000450268                 mov     rdx, [rsp+30h+arg_0];rdx = Function Struct
.text:000000000045026D                 test    rdx, rdx
.text:0000000000450270                 jz      short loc_450279
.text:0000000000450272                 mov     edx, [rdx+8];edx = Func.name
.text:0000000000450275                 test    edx, edx
.text:0000000000450277                 jnz     short loc_4502BE;rbx = moduledata
.text:0000000000450279
.text:0000000000450279 loc_450279:                             ; CODE XREF: sub_450240+30↑j
.text:0000000000450279                 xor     eax, eax
.text:000000000045027B
.text:000000000045027B loc_45027B:                             ; CODE XREF: sub_450240+96↓j
.text:000000000045027B                 mov     [rsp+30h+var_20], rax
.text:0000000000450280                 mov     [rsp+30h+var_30], rax
.text:0000000000450284                 call    sub_44DEA0
.text:0000000000450289                 mov     rax, [rsp+30h+var_28]
.text:000000000045028E                 xorps   xmm0, xmm0
.text:0000000000450291                 movups  [rsp+30h+var_18], xmm0
.text:0000000000450296                 mov     rcx, [rsp+30h+var_20]
.text:000000000045029B                 mov     qword ptr [rsp+30h+var_18], rcx
.text:00000000004502A0                 mov     qword ptr [rsp+30h+var_18+8], rax
.text:00000000004502A5                 mov     rcx, qword ptr [rsp+30h+var_18]
.text:00000000004502AA                 mov     [rsp+30h+arg_10], rcx
.text:00000000004502AF                 mov     [rsp+30h+arg_18], rax
.text:00000000004502B4                 mov     rbp, [rsp+30h+var_8]
.text:00000000004502B9                 add     rsp, 30h
.text:00000000004502BD                 retn
.text:00000000004502BE ; ---------------------------------------------------------------------------
.text:00000000004502BE
.text:00000000004502BE loc_4502BE:                             ; CODE XREF: sub_450240+37↑j
.text:00000000004502BE                 mov     rbx, [rsp+30h+arg_8];rbx = moduledata
.text:00000000004502C3                 mov     rcx, [rbx+10h]
.text:00000000004502C7                 mov     rbx, [rbx+8];rbx = *(moduledata+8)这是字符表的地址
.text:00000000004502CB                 movsxd  rax, edx;rax = Func.name
.text:00000000004502CE                 cmp     rcx, rax
.text:00000000004502D1                 jbe     short loc_4502D8
.text:00000000004502D3                 add     rax, rbx;string_addr = rbx + rax
.text:00000000004502D6                 jmp     short loc_45027B
.text:00000000004502D8 ; ---------------------------------------------------------------------------
```

整理得到公式：

```assembly
string_addr[i] = *(moduledata+8)+ *(func_struct+8)
func_struct = *(func_table+0x10*i+8)+func_table
func_table = *(moduledata+0x80)
```

写个python脚本

```assembly
moduledata = 0x55DA80
func_table = Qword(moduledata+0x80)
func_table_size = Qword(Qword(moduledata)+0x8) * 0x10
string_table = Qword(moduledata+0x8)
 
start_addr = func_table + 0x8
end_addr = start_addr + func_table_size
while(start_addr < end_addr):
    func_struct = func_table + Qword(start_addr)
    func_entry = Qword(func_struct)
    string_addr = string_table + Dword(func_struct+8)
    print 'renaming ' + hex(func_entry) + ' to ' + GetString(string_addr)
    del_items(func_entry, ida_bytes.DELIT_SIMPLE,1)
    add_func(func_entry)
    set_name(func_entry, GetString(string_addr), SN_NOCHECK)
    start_addr += 0x10
```

函数名恢复

查看main_main()函数

```assembly
__int64 main_main()
{
  __int64 v0; // rax
  signed __int64 v1; // rcx
  __int64 v2; // ST50_8
  __int64 v3; // r8
  __int64 v4; // r9
  __int64 i; // rcx
  char v6; // al
  __int64 v7; // rdx
  __int64 v8; // ST60_8
  __int64 v9; // ST18_8
  __int64 v10; // ST08_8
  __int64 v11; // rdx
  __int64 v12; // r8
  __int64 v13; // r9
  signed __int64 v15; // [rsp+58h] [rbp-60h]
  __int64 v16; // [rsp+68h] [rbp-50h]
  __int128 v17; // [rsp+77h] [rbp-41h]
  char v18; // [rsp+87h] [rbp-31h]
  __int64 v19; // [rsp+88h] [rbp-30h]
  __int128 v20; // [rsp+90h] [rbp-28h]
  __int128 v21; // [rsp+A0h] [rbp-18h]

  if ( (unsigned __int64)&v17 + 9 <= *(_QWORD *)(*(_QWORD *)__readgsqword(0x28u) + 16i64) )
    goto LABEL_13;
  *(_QWORD *)&v17 = 6868839719373004372i64;
  *((_QWORD *)&v17 + 1) = 846973294085968i64;
  v18 = 87;
  main_CISCN6666666(); // print "Welcome to CISCN 2021!"
  main_CISCN66666666(); // print "Here is our free flag for you as a gift:"
  main_CISCN6666666666();  print "CISCN{"
  v0 = qword_568238; // 0x20
  v16 = qword_568238;
  v1 = 0i64;
  while ( v1 < v0 )
  {
    qword_5B20E8 = 0i64;
    v7 = qword_568238;
    if ( qword_568238 <= (unsigned __int64)v1 )
      goto LABEL_12;
    v15 = v1;
    v8 = *((_QWORD *)off_568230 + v1);
    runtime_makeslice();
    v19 = v9;
    for ( i = 1i64; i <= 4; i = v2 + 1 )
    {
      v2 = i;
      main_wtf(i);
    }
    if ( (unsigned __int64)qword_5B20E8 >= 0x11 )
    {
      runtime_panicIndex(17i64);
LABEL_12:
      runtime_panicIndex(v7);
LABEL_13:
      runtime_morestack_noctxt(); // alled from runtime·morestack when more stack is needed.
    }
    v6 = *((_BYTE *)&v17 + qword_5B20E8);
    *(_QWORD *)&v21 = &unk_4B65E0;
    *((_QWORD *)&v21 + 1) = (char *)&unk_5639C0 + 8 * (unsigned __int8)(v6 ^ 0x66);
    fmt_Fprintf((__int64)&unk_4B65E0, (__int64)&unk_5639C0, v3, v4, (__int64)&v21, 1i64);
    v1 = v15 + 1;
    v0 = v16;
  }
  runtime_convT64();
  *(_QWORD *)&v20 = &unk_4B5D60;
  *((_QWORD *)&v20 + 1) = v10;
  return fmt_Fprintf((__int64)&off_4F4288, v11, v12, v13, (__int64)&v20, 1i64);
}
```

runtime.morestack_noctxt这个函数会检查是否扩容连续栈，并进入抢占调度的逻辑中。一旦所在goroutine被置为可被抢占的，那么抢占调度代码就会剥夺该Goroutine的执行权，将其让给其他goroutine。

将代码转为C语言试运行

```assembly
#include <stdio.h>
#include <stdlib.h>

int qword_5B20E8 = 0;
int v22[17] = {0x54, 0x5E, 0x52, 0x04, 0x55, 0x05, 0x53, 0x5F,
               0x50, 0x07, 0x54, 0x56, 0x51, 0x02, 0x03, 0x00, 0x57};

//'545e52045505535f500754565102030057'

int main_goooo(int* array, int size){
    int v2[5] = {0,0,0,0,0};
    for(int i=0; i<size; i++)
        v2[array[i]] ^= 1;
    return v2[1]==0 && v2[3]==0;
}

void main_wtf(int depth, int replace, int* array, int size, int size2){
    array[depth] = replace;
    if(depth==size-1){ //数组的最后一个元素
        if(main_goooo(array,size)){
            qword_5B20E8 = (qword_5B20E8+1)%17;
        }
    }else{
        for(int i=1; i<=4; i++)
            main_wtf(depth+1,i,array,size,size2);
    }
}
int main(){
    int qword_55C080[32] = {1, 3, 6, 9, 0xA,0x0B,0x0C,0x0D,0x0E,0x0F,
                            0x10,0x11,0x12,0x14,0x19,0x1E,0x28,0x42,0x66,0x0A0,
                            0x936,0x3D21,0x149A7,0x243AC,0x0CB5BE,0x47DC61,0x16C0F46,0x262C432,0x4ACE299,0x10FBC92A,
                            0x329ECDFD,0x370D7470};

    int n = 0;
    while(n<32){
        int* slice_addr = malloc(qword_55C080[n]*sizeof(int));
        for(int i=1;i<=4;i++)
            main_wtf(0,i,slice_addr,qword_55C080[n],qword_55C080[n]);
        printf("%c", v22[qword_5B20E8] ^ 0x66);
        n++;
    }
}
```

输出：4c9af8cc949

看来复现失败了，原程序的输出是：4b445b3247c4，到底是哪里错了呢？

原来全局变量qword_5B20E8在32次循环中，每一轮都会初始化为1.

```assembly
#include <stdio.h>
#include <stdlib.h>

int qword_5B20E8;
int v22[17] = {0x54, 0x5E, 0x52, 0x04, 0x55, 0x05, 0x53, 0x5F,
               0x50, 0x07, 0x54, 0x56, 0x51, 0x02, 0x03, 0x00, 0x57};

//'545e52045505535f500754565102030057'

int main_goooo(int* array, int size){
    int v2[5] = {0,0,0,0,0};
    for(int i=0; i<size; i++)
        v2[array[i]] ^= 1;
    return v2[1]==0 && v2[3]==0;
}

void main_wtf(int depth, int replace, int* array, int size, int size2){
    array[depth] = replace;
    if(depth == size-1){ //数组的最后一个元素
        if(main_goooo(array,size)){
            qword_5B20E8 = (qword_5B20E8 + 1)%17;
//            qword_5B20E8 = qword_5B20E8 - 17 * ((qword_5B20E8 + 1) >> 4)+ 1;
        }
    }else{
        for(int i=1; i<=4; i++)
            main_wtf(depth+1,i,array,size,size2);
    }
}
int main(){
    int qword_55C080[32] = {1, 3, 6, 9, 0xA,0x0B,0x0C,0x0D,0x0E,0x0F,
                            0x10,0x11,0x12,0x14,0x19,0x1E,0x28,0x42,0x66,0x0A0,
                            0x936,0x3D21,0x149A7,0x243AC,0x0CB5BE,0x47DC61,0x16C0F46,0x262C432,0x4ACE299,0x10FBC92A,
                            0x329ECDFD,0x370D7470};

    int n = 0;
    while(n<32){
        qword_5B20E8 = 0;
        int* slice_addr = malloc(qword_55C080[n]*sizeof(int));
        for(int i=1;i<=4;i++)
            main_wtf(0,i,slice_addr,qword_55C080[n],qword_55C080[n]);
        printf("%c", v22[qword_5B20E8] ^ 0x66);
        n++;
    }

}
```

由于自己算法太菜，虽然能看懂在做什么，但是不太会优化算法，只能看看有没有什么规律。

```assembly
#include <stdio.h>
#include <stdlib.h>

int qword_5B20E8;
int v22[17] = {0x54, 0x5E, 0x52, 0x04, 0x55, 0x05, 0x53, 0x5F,
               0x50, 0x07, 0x54, 0x56, 0x51, 0x02, 0x03, 0x00, 0x57};

//'545e52045505535f500754565102030057'

int main_goooo(int* array, int size){
    int v2[5] = {0,0,0,0,0};
    for(int i=0; i<size; i++)
        v2[array[i]] ^= 1;
    return v2[1]==0 && v2[3]==0;
}

void main_wtf(int depth, int replace, int* array, int size, int size2){
    array[depth] = replace;
    if(depth == size-1){ //数组的最后一个元素
        if(main_goooo(array,size)){
            qword_5B20E8 = (qword_5B20E8 + 1)%17;
//            qword_5B20E8 = qword_5B20E8 - 17 * ((qword_5B20E8 + 1) >> 4)+ 1;
        }
    }else{
        for(int i=1; i<=4; i++)
            main_wtf(depth+1,i,array,size,size2);
    }
}
int main(){
    int qword_55C080[32] = {1, 3, 6, 9, 0xA,0x0B,0x0C,0x0D,0x0E,0x0F,
                            0x10,0x11,0x12,0x14,0x19,0x1E,0x28,0x42,0x66,0x0A0,
                            0x936,0x3D21,0x149A7,0x243AC,0x0CB5BE,0x47DC61,0x16C0F46,0x262C432,0x4ACE299,0x10FBC92A,
                            0x329ECDFD,0x370D7470};

    int n = 0;
    while(n<32){
        qword_5B20E8 = 0;
        int* slice_addr = malloc(qword_55C080[n]*sizeof(int));
        for(int i=1;i<=4;i++)
            main_wtf(0,i,slice_addr,qword_55C080[n],qword_55C080[n]);
        printf("%d ", qword_5B20E8);
        n++;
    }

}
```

输出结果

```assembly
2 3 2 2 6 3 4 0 2 12 5 2
```

发现并没有什么规律，后来网上看到可以尝试计算 每一轮`qword_5B20E8` 的运行次数，来找规律。

```assembly
#include <stdio.h>
#include <stdlib.h>

int qword_5B20E8;
int count;
int v22[17] = {0x54, 0x5E, 0x52, 0x04, 0x55, 0x05, 0x53, 0x5F,
               0x50, 0x07, 0x54, 0x56, 0x51, 0x02, 0x03, 0x00, 0x57};

//'545e52045505535f500754565102030057'

int main_goooo(int* array, int size){
    int v2[5] = {0,0,0,0,0};
    for(int i=0; i<size; i++)
        v2[array[i]] ^= 1;
    return v2[1]==0 && v2[3]==0;
}

void main_wtf(int depth, int replace, int* array, int size, int size2){
    array[depth] = replace;
    if(depth == size-1){ //数组的最后一个元素
        if(main_goooo(array,size)){
            count++;
            qword_5B20E8 = (qword_5B20E8 + 1)%17;
//            qword_5B20E8 = qword_5B20E8 - 17 * ((qword_5B20E8 + 1) >> 4)+ 1;
        }
    }else{
        for(int i=1; i<=4; i++)
            main_wtf(depth+1,i,array,size,size2);
    }
}
int main(){
    int qword_55C080[32] = {1, 3, 6, 9, 0xA,0x0B,0x0C,0x0D,0x0E,0x0F,
                            0x10,0x11,0x12,0x14,0x19,0x1E,0x28,0x42,0x66,0x0A0,
                            0x936,0x3D21,0x149A7,0x243AC,0x0CB5BE,0x47DC61,0x16C0F46,0x262C432,0x4ACE299,0x10FBC92A,
                            0x329ECDFD,0x370D7470};

    int n = 0;
    while(n<32){
        qword_5B20E8 = 0;
        count = 0;
        int* slice_addr = malloc(qword_55C080[n]*sizeof(int));
        for(int i=1;i<=4;i++)
            main_wtf(0,i,slice_addr,qword_55C080[n],qword_55C080[n]);
        printf("%d ", count);
        n++;
    }

}
```

得到结果

```assembly
2 20 1056 65792 262656 1049600 4196352 16781312 67117056 268451840
```

计算得到通项公式 `2 ** n + 4 ** n`。于是直接生成32轮循环的`qword_5B20E8`结果：

```assembly
qword_55C080 = [1, 3, 6, 9, 0xA,0x0B,0x0C,0x0D,0x0E,0x0F,
                0x10,0x11,0x12,0x14,0x19,0x1E,0x28,0x42,0x66,0x0A0,
                0x936,0x3D21,0x149A7,0x243AC,0x0CB5BE,0x47DC61,0x16C0F46,0x262C432,0x4ACE299,0x10FBC92A,
                0x329ECDFD,0x370D7470]
for i in range(32):
    print(2**(qword_55C080[i]-1) + 4**(qword_55C080[i]-1))
```

结果

```assembly
2
20
1056
65792
262656
1049600
4196352
16781312
67117056
268451840
1073774592
4295032832
17180000256
274878431232
281474993487872
288230376688582656
302231454904207049490432
1361129467683753853890391917874491949056
6427752177035961102167848369367185711289268433934164747616256
533996758980227520598755426542388028650676130589893943305425853414656773861518279015568488005632
1136055529869169502964754565795159800328181980003159567925180684863281678019080648437652652264964147641119704868683862223172694900166897145023402979277742050480024502036985533417535225089468304942209480429135241087782870207169248511800774304516801629181934929319857239719899883286669956450045955948315245254303245605884071616557081919409045565481839955947959133343819060157287427072921279499484365568972119272402332262700848019011362727211555142284107034264886954418751945149190554380494515664037697048507480756967637861049737681451611644015817537111409765346588110340281764367275850765093556716155486511640835391586583366931377534474321111440141628074684466669200952254223468787627837498069861698328479998651790570735017388522606695796458844672739547710143726950962837844692811833144874065626162137834046001869111813796141828700789277473155202782982148529036286804776360912419544499513500905993011528634290718214839451912460804418006003307582115299398100386679555172958473515628482082859165770587744270477818430470628766440928610956926922168174621070472412082583518492064306444984553653213971463294678496601661251109306754413262921666970630020908103622137897545856698334307880896068719700553775408690634393006301076245367951303723146581693983602511158711406015562645753346162515606350303723529854921139363346524923821696957968082199533070920359241348004812586665644717876773842358247583351703176863670325664086549856256
10832889170035705345714730632916429436161420682519830170581877407044216897239303758791970693319269259544786226359481669502706899535663185111708103983292877175856195205936962686970876165873991706259256419577069233736800519298727699729928703251677752535114139106560901870056177042946550685180689728958026574120329401631231464439255399110517857264956779904868165081749210779214381998971175609391261842445290411130183445929024859965057708812955340992683814423622800377198023011954502266154400709626867732684639642637321878147931987664841826526844976218942405551835898643517121585500146532993495783573372658518863693763972513951165778984233902941371686677014642836984883279690360972119013798246206373018409493987733015895729674378807204817604709579597661680511185194059683882821364648144909052273120775140975839122694593903862439352282806361205949568763525533839333855611082744863695611213919994158501371514631835739014761713846018941099658380223161298462545037413243497773001937181276788084918593822037767993356803478487580002485853080738269546649614350217091242920041270618698692416536091674676571374443863015074159443653015579753318127244974565943991806693275006754622631478799778577771535993389538520275493206542868727301111263327692397176975990473273908801333834228089206819789788911436241883111184811833272306240328207238638333973179935256216312007349290771452556877956433146368358012492966344364519322335465673646193719394548809355830784240561761368439179364653528925693434726479571129861188284302688190154898413552328105675090229947629215098963303997283188200255968022775063204218470015201020346895315299654443248888979616979373259366546286326894565736852079128810735283433891907307084862406412231538821991334156013169985468161734442144996919945634475542724446411312393400374638499773224692609538933909221854510322678212053864903230413589652356855678851709912531530556210341057335789695916015058088764852010608179054235840757349153740384013253719027272906537075858071837080872923414809098431707388873402290385859164875158932537242285267548885711492134569724627240391872161412092921764678584908951048405876733753709123559877150587627680774999635301122226108423742599425694834935270409588563127436454282789464712917930528824622990622424136045944220902756188829342457073760740453445725791871887492117428698202895193033540586195921562438919142989762887683561825505003726521120460170386750612757831143049092994253507942991464423720235811610873986586186380091597319155674373512445386684573114683622605545091708695184185276034772328903973635074006666846253349932972289566857546461439868271501202017838555505750842428464798965874056109183417865852840940071040729758458713940335440046080332656112789126516193264972131906492360648019821193839628140550961312738098371496133156978330816105399202868009699524828979155302296176095591967095175880513762856725740870010811009515925034993264389734732539529046776508438845173909074144267348607758990061009028252384126948494746910780106753503992245286903827932098664060916542642904300995609007975161210264805316028213856770183862729140998887457822731614120965608646033629887817818600860654495547740435833053474929984937410059381811986693434955812838150275882062432009784707611218728115318725260813862185509130624163176941312389327368483625979146113382810875851974909249380993395350946990804374551697745931353043389723971625927381869633212541287396443806307376081295662754407923200925549093618210414813496781863237242135093375359361288825983053997757802927911751166349873896398731293660143145426754848180148278307309100464467761430326427794355116124831907225248209710884809024536683109997500436572696642974671219735030407484016561643200882798224946263625695325924128218247805678301845291391116017607320795806232753057286271265836470931841670457473736982388078010456816390737987719680330523071355632348451926523064153918161498852599443945798736336071075741363345610868199799186594617682233643295566282677389066978710168761607810234151193755977052484872917516984815321839705481287798265304178179374242836333100102112656825571535463414976476550972939622274145328160506355712846475229260315156971863398447603593509509302764984229758169611094492210979418526946127572324792923292913705741821278271605957680335768743000153642838685223459218233117981457785132609834738542162675364404129815740388914396369901969583137216020260160144004765782682807686274896638890742858263380018297240029438349133892689051941464012001547476792053156841142632123401806370642585148994817283563605790786314666452243868760454707995938715861159021077886323204695736824346969928473731941997412519658989446628641998520196749861850600597316546899636427399666722347615346154552599468918220808755502282974781578455307415206735847691773836147900281324251957208686737846491920417307402627832847228044129833753896895054507187397591279558834363707319114591456013748762010263394739416387649748360603633721719178980871595676602667553501782187497737246687108347906202571951943858600337151186316195446552662713038057717936436441174010572024340064202567294844442506977488478128059107268070755793123033002351611520159233776390590678927736569381146269555105835522597940162677786111044415442864163761254771275234514191758895419987460791985690400278027503709077040558750926461151085725049593571762455956429723826339957731376821599764759281660222597585019534562628687870270233436898707244134819110078506018869987617482445889149743461722847577473512085534153998200221810204663323554157751988917356393930453332455280934862632488189254891874909169027084722053192443562864878509654834744377588641005463122560915148231986426212707851551462667439441126211607179670364345114749287938266632948125753554004266382769670367861685469000969973879273430737674317437906367516801222745437396170002010106786636615716454925885507220961988752773938495693381220047057065614376231683958026291493446266817567776283826484392411960606180024745598782384453220913327478076125996372921523742868351429952967326972339466537175018084471105197085653519482345331164617027114430027598567270246834008074388446946102863429643672290740044479066659382160411898672019410845952937188123976231447000319145872884745980761957738173262613801836796222852446981619346369500030603718561266825566571925184969974803330662647893857647168180764427219223388030025272273907305147909759457608250851624538173818180556901993543406683252268710115511691752968900968781029325498740883485698322425070074730914327615963552529081106242507213968212374951545611989657407130759516887173832692647346191662290175158075955549222437905943514692726963110345005089976208615245652559242932140541907916249761799702333973171189708512518191763118262668580658873911771300971125553298096374101245356980251554562149769675338933640538430362993101396295291462344196306608442015231661563923596571451968296437565368891804090945883953089817813053492115743386080030729647211267027800026650696770562849711680122362538095699853602826675664159703939118917733774964696355824266201272841197869950753602053276347440246961644016482282778409292853807608676563729645967967266162427429354897189483644847577209417065787606938990777586311928809832414283715549621851889008764814415791959964722638740471333931313368692928682817784506280712032902353152170875241485852212117845997590980640183452684139090065439657855893071622517297842697194004557658226446521560175211577858015155784582767286085749348815027384331983067669847571185193274788076732516032545745380245705504234523745666617525694810695795589330296994672081953065491542762376808465203635441591193351601788491725877005432378798781353318187856761434563523721589164601225572473882800483248953288704222177143789909598102248026372277526781646309198140429094657313013221871663643932838459353756881716191294189974739433284228518554886703412698978853910281680889416121454972466181461177560896753733114100159708946816836715016705934836850752493704637397096889026820829824054574290479821015429364531525943844624785717084269295596473024124734825679354972711444474183708352150947966410106530314891534402956552762205366781396568035301878964890557835003461048461143612798115831269352196076571797435571855760278104254399222007590229656449057647008722114135866734793921941512759124129525563106724715962787814666074771762352133247799132942204831641513922223770625440442792784694416434364067433180948190253209465571120184377220735230249221593967525637711901536145413896269629504822537928398297561272538770111561380156326095769885637353827694634323336623885081913877877877838664208740718758365429355007064005256620149544919288726740650669892175685683605213499022982750651102684936366496867552535510253853851664215232794898318896081019458624987969415914677287332750923176842112600972031860607496325456613793280883772468108882572173053295759660885624175496036329647678790307505095316822761157419195214276953395270439649889101324033835670394043684148789767091074154057734208283171381597822064368054193635675009293396277540804208008487654838067072113020785657039400788620414679767562734581255854979463205289604502922078539494810066377975522318414730531957672918524260942751931069842464348872679737585371600422983346107001269864297977981577482386012707448493179766338761871750534096361341541958795561225142574854012487118307095466057933585848835119416099821953957672687042576078584414639683477132331396068444993948554651915810992251638854217831778396338323359495203665482863932156510328863993503512788992
696094442988864858536575063821364384506936361726082795079225293044785478492128474642428339142970707398592741443703759800577167271266655233821709254756704580545187606931298302029690310103760884683811751937572913879844736217508307061802242073376908474445122253857621445996589592795787751350134832944819724436131773550215710299018451443968409918263784769294668984019922291491294317997963182151575987211049107508175529693464006713511728296836479678355698919626738164483834712579580884969124667757415764312694270783274049993076965984213711054187003058990654563518575235557765930257972974003291797079162520904438097270171662487539803803040147576318938212606381492691997906733356781863369260879037964496332056837927351118052398126340176956413667236862556831796380624920142274091885641076300736904109191433689837358657736977019111739610606734198384727004656071029930703802337256576288205196806340114873872642727308518369445643731812694686789983300015246325448597523175713591663338268562761262467089735363199314350403690920897594157559368857424459076158266982787624736885073325650264006625263385689776485012927406731718669454576272545280808441878580255786916167294499033187634677261832842883260961893375644024770409918368278066386127563253652088262651484651824141301503322990143696228959848213888552740269207646477870193327053071091055255172109625815805610939269664147402002085895070193250967901561449958999292173153368096314753506385356148342115014868817187315257673151341554096717829280422827209790657893469661900429879345054767046773492142412240860252808443879045290427961495278415118513415555441837823366160528578458033976116766584438118273024804111572252648301078652644309246198567611743424466243543491262496093385176196035436439292153351373198015618075864108013752063466325611873431276385526913104537705663742859518859115936916539014690971630759771242443397722516541502025467795399459037044484584668762991217667307020188733824452089381552644385769149841875283965698614585374328100017199181314827730672807340224768150922033555855460942702897293789919668640194773177244531181837370665434559132572758362304417786345784671299424102900843950746627045167850762698941508224462719482502925894603515129652867760572590520866578499798085566382361326756445758636779291953957701843665501501953223305375227216102412007813673219727087082050492392234808840535098731206192238260920003078249854613463743925578671313709821993869590811373226173049526982045542248228898331460443414408280671939783132464677412251820597395213475596525624553613101023954779289733016925322174266212619444243080873507869875745717993884082663229697751809427801169798492461536338626622358462680548370541707814351943478958329944318561547246032445015346461091692861936350126905765025385765270224931614355179701472964434033075190383679478108166880224133207786889276317132050685270457641312396677424690049867330231908085769498753228395312544704337411932697867032189302967149499108231069575780867756396663219957736411417660110686470078490570595061741928042868088391394319115530501576022162982364041490520618942993817623632348232370249552482360095015669298199115706506907200051587343776207778723840376222449070172663945605180869048863545688833795285039419590400555630314901352937905980393223065212827599598662406849258556979465442025093109908602064544082328776533723683160876715669668933160871939707688805674608626440595508190998030101932061042646226892257704720312256762394772826180533472488306914750599179541178026232531586201632490081592567955866186574498520733068603357015380159154702151609932460821712711054964378990893628916530468341535526206447920833238422278790210295184277947334939770979832567592094831949593446535476380769823861657401736357697956155513844184585522732093147688783568031183830603775599047743225915968500047313951983432124362352899245225228339927369019001842611934504678860867794236645093748676189945810266047107243959682331933098127174136408760618918136177969311134190528289089026046326569035409354353300754314066791389772964819398038457550103776114553722114133788428867536148404190319637808851843716298643612417355704397112584217505847144763747361413826853095079284112300471626969966505447459561622437302559478301316041270819225245211281073606445498044336691194630874797079763818922178315539704289810316256454145952574108332800276309548610070230682697961785903419515598866035544826010619230175156171202735911497918634786665254787728467473695009842871486752178436375921203281802308383496069000200545152021214944651651439598096331983891759700536546159441590731535328789450849927600781501822577293550801962861112796637880203293528504006377584455387935847320581611883945225299671549674921919742553105588050967508284666781918272571234560404927265432931304035025991874074240475077547989265678511509820674440950034251628013807436045807441628833250393747767765505076982298950468436914236394655045985070582026533042447051525597975839070441144260581840966695876026861124700644212583258910076424206936725656825441473740715108454757394919976149691207475748131496505740807188345423450510336514418582866326502342423046595485118594078449975047988713846022561113669573045826572794457207288571004774564272967604429318015581478974889855573680333505403124840842617787824874602171663593543932726571717191773833873992578099983962178247872557300042167561170135342492796752527666153109962784088381606001898867536952264132894587333448744559451986253133515599850188075373890696929677259656040909907133104197547795112609441685376554182874542210792196846193763540359192682174002720335997160920816729772044696549857065882277357720015268968260474759569136403564077250936185549903000928724924357650202063137395826256363949090037243916487571290933662332026349042159282479365147926187430325544482984884120107664155778334111993182711547493831215044511488224772499087671253644944301152603027734073191885253379409691712018959351170249095300235492664779200291013991509193909724090389038413070934751475110578947819433889433811286780479158395523267300161791704333613792885694706975350896476648467536844371964284123072036004166102998662131390270041467744653968161666577092813606622728391319733952940499824590194148783566199167714469538600896026088335052318716727131510773622867365723614834652240797644372621177016013365528222090715947853171088385992531100052998920148775414828789440154351334021468817705951620758707739448760224944124689628681925616090833905824291335578536935772516531075037728190411806346609276496252355613487360758925925780618527602487427097217170880111625171318066654568439989349849510929600830479682764845466115279146118210708064525857614345755194029314870741038208216459817599174007135840097221339430172073494181564515743678607553196547649288847933475537239700950565571490123082019123803531900081911088747328189407728859297323913078206780699134373204665844754977402603897152329331768631348796529510039476623933768276991423152762724731242690106107785037355461152401740869764482380667293065564001948682104115528020761281073613887680533541122987357329877439054312059476525430769522540400742875764609901653793254749789231664097226376407101255838487614584583042449081601999267797463367676577084757885345218571937684455030034849226956926602423263523223417948499306789823070788253034201435962664810763798855951951341320803150503476572482530742744135093743791672795420182733055401050194365933023648733695905437502429751278471536584640244154649740132740006482862764801659226921068199297255115011271741933546930960204070892095681981253312069756680680007500883622783897743382494917852149389236267574046261592688587166883722035720915458184698931000137607007267979373810661039138572796708494998868661711549168619721817208750724145213020612745389092992185526081670048232608542277549546464081155244520425784347168665082395476789682444416554427448697177704789326684713920389538962525164118448872029835917951015536071369905916139845126115619935219675682843246626659365013050170183548925077789397297935933252980803775226995609089430619134980766402970549708709565066963472908301442649102800752971533101324758010248058527627781755091412368313965817439631144236016706074196735054838061506499957559945810530068226588157898612579062255281786847271200602836530553445888303567480134187627528457596611754261135078965643726185339564229554629271905519207360897878284948260360909018517937650999549145610865969736163365016207301590754618076862516050166187518996906105815856242256272353753305150446774205101849586424756230141317792201124199550943197497316459450502441260883895830851941582673657252919223618377802318140114842030642298781472119512358560826276811995313493065961350193886275649377909265900275111386964094793832914603236537961843595908523025411787930421737402157420414620833398802701493242025394757384923507339609333998244783742331676546116833017408809822984534047654461905339976677969104754508724058231360680120492420758576602923139921592842119902478669809990935155513867904244859343319586532060291286260644902027651101291643943045130382442363470054988266001925206306994935758038644134810864533847068928262849035192842672897714473511842381586715946646821488476616001517277762861807155656921045319908886445905909169400955660757421826651145647054790530212592228692038219612144158586887520586918651675119631275334000404966038798470132258274362950913014408719115880219883395958746646350414190718875085001255431065191715065845879472891858343844257078497962782969507321805879124843632181697928842100078513126735890644870491002945112326933690499936434054031848824323342309497724430177317429417728857414146894924452283914005730937806451799381594108893628310143650841331690646904520048307478804492559555090825188541389770379677614868741865393517655518543626330196251060762804156110160247519593656207412607424024590058933829558361127501344351682006078136868984078312611139580908385184430469248648940194918995710673088937959264387363327031263362126954194719319001471214228570304707803850303878518331599534782032875848145128238085778577270539789892267436272338676490596419213610998594459409942298724177505166367391516981216906560815618147648495129503199845701393066245323516056492090364936525891185266138673484332238161070384470371630340379620825346352753700917548624482954972719917363249931307871531492213195205905248996283462314335845196499857431769856780459699647288363018453003082580193972274246981694849381019459744563023760269932368269200943257627239996428886968197040779467363933519716168592643350080162073998226800384502728879731457012220109475828041544919806270138922677044287796944367655460381550534836436364662123598187115578969251787594901611685933159026346418934874919719470576424303134597131462697749646040562919459973667017304189404226053470603671760892821340333576584034819307741145275733016462381571486724630800880202449736451896374821180602266281483882797767239574894222156857186866025149048679264949487977636679104636112928911973882191546363335579805068077453677702047566184985606193781718799944167522110077263835846480685654278663048616569224789556409179356715377426505658514824844818255592653274623663568235036423503780791570228395209271522930319328672761886758104193461431417346081065924366885272511795698741713128779486806854586828120358346783952667498735982642054529720657025933809253959968754591304242557502296479304105906512185624253586305350308530430292458895389590147657160726563105080897636445310656725189728057602400971073595738208490763269653653160683778806530862217990083690424787135393544735496447178817653224592113188102841070207288500436610554576607774389996570220266801846317679620073258760410069342304464105698734415858395914000001307170041762743941591410248325856863094069158872249333520965127341716801815541093206308778087816745179021240596356057315903763830899672111666502971486825346820818541869515429086824938438974977435541420293851818924984318407556648515389961767441932902302778828987824087524292422626423479230607965100580833568545410851787989707285329174915701402639424232000786586008860331361370825649777718976151791677007014027470144204991111371424010199282138420944443176565943981172002189094556503540295966005520832617817989401199535111289969314751787246499158283979314670926143583565583002672030798396037897790718817044421777772861314463511814432132934245329746337981611586984305356197114485521119705709720114188179169736596025347808962181537677845586660940065895643714735527466858962615929245189618455063100575727469918699239317166330484969626504578124000778895462218499426606950612801446025951988958109941275116727045448497540024409112154693821416858078530115652816126559204277151307069443049834753073831776084273292256280920197952928607069439490515609459376170661398877697821090164055313549097579060443621370989695124915189
4925078000378193332670596992569732325767295512010181675316884068772718697868089171952018527338714747425365909523563024393603699883797915717043610003443774878485883034486773624219459187614448868194023811427061787998859761919607619050334690260223202271536684169742206858622357756391021088037932742164695627602680544553695709573115306750008948006019944609617580334554141722074847082606988191021789580820822136465583226155185039938685841592010348443658580062667707782846143279896900832610746639484434169033382427485429734015568643154288940754239232586308848462879655905548778841163380009620935667035913896254521668596427711027239352771462499212103769228385415423384869305073572879919658646733355859253210498722437874605829869985191603553182662461329657134742865964637224661961214402339125419347415756612425460264658637959893045042905534237705004824683530597542825975546480486181386032302293987458084322608325414768426873099313616379520424003115394115271669492605371886381016588116613581765909569173023850802595021318678891605383467562579373130912507258398218389610774508445466440722443495198457655886063950054357276428519682115264448481593595175253999036704971660241515005295211255663728954407696173992768945107048424677095797181397470382734172520389805184207411987801661119827259417300545237257398586525744652750444447820495700500313553946505500031375777324885018939238258977760653554735900379811831536898531987374407037251928139028300833997856082137282331374500725656183515871089823555106815592246017504307412793771685059521171990350861187611955300844124503242584856552618317936530351269935727308062799961421403390376808407203934108631047069981655629859774927924773040773333713070150889090822641056909056017774190361683683091134153965299464490690330588844249712298833565695948206192743157537569034127548986776323331293261456845875192973984713524734681267083033593509002137371875844592892365905602353872904841120497005653129139182723377284584509527950032348980367034015844284950278823427128283107889730694887813504642822918535244780688986463267245952720934343658687452898406163358924267883766531382200357995077430802544915369863201177182799880014237210888569287404010090413233023651422273119379256466350604661798226377105805187653242109350973143852641432586655917204533063903886280939124467053150027425212911773128135834150583786144902347175549549360747096576397705644195048278618516553078794709958904115882936944136101062010530040935797329797011284484037244082232559893009762678376882965648688047831214559512347883108918583293746825613586391131097718509747034236860345794831117540189852713972426894069571510174467476458725712412259427070110526361250476059491703866305172456830134813416584817268114422898044774560266291119148960740576935956899283696014213016038286164618853113440635518743028483295805112713381459731393986560627054692656522727791734938305576760089370024741804401260816950891776058932322247015054899325476431217156081946386996642523361213827958083297450928956470769074894708095383730630119749401874432403161012488347978433741873739397647741277067213742579048946084090965883134010718260383699064339007620473511431139653741158097508012632359937827075751161515942684391082768156020485699917931023488051426732625917722169868364834578560157150429573939506338254882561929188656126922226326007119003180708284441315079625020169560145849637722930849437268399734384240144214655040249602297278911937437340938624155296899073450677351388367109388843316669765654802530702044615518040219035445743192535880504441184431387581559691349088071571178061735348356937903021059334754400518349508963460862824314942022324840514065556756763069085129313225614051425971561018328714457901732246264915566851021134599386240668631715265516299522129179239254439261848519856712201545174161466721759975370658868479064196657191661332150517435281074290806987659502685299867772181538228255253708336567691186839824058663012975128271150805724441588309337243896050042943908276415312872735478041100882547917951739488567820659507142858574819604993878916969071038932043329476426542076730922353762398659305346862953246860213586512542336177665421399459446184823167881948423593206816452666869509881241332836397302609594714754945747634922872409357139817744867054702540746833888291045936238833839975098689297223649474090054120713982847764688716408754098130212479926151717081549722002705532740001978691872844765956956655334835203795424726497064480922735051358722369210619082408106648020171127423979083357700886670084699838532867106305053488675745309975529162471746134040851679795149640792765178393651023295264822888308798617151838180756680657096539900553432149772346903925176276031470168411873628304567052944258273181710032952579898945068545725339137142162556393990200215493042397684749951656026223547825312175398117048329245846004792896041389815241384339980837745315327860218378986633244906328223909383020238266962466998796544063325684471262845987982413055789383007467505537524804093194770381752299792721543666499979228170173979881719402389669749501165040684951374250008277371164649401414447518705299959553485272282186796551666104765381440716578203317221376970239412470323622831273614742466189979319759980700125439962245927097087482394028890958663390296313576897311899048714089737642732796429557628909569019208729319345552792093332287702727196109087430716291658627978005840486744407641716940905820187658490363642943024220291849230345484651604719578820876398373250681806345796621206662922482268221674274501606113346825428614159334448276153930181299624271106661957810132168332709690343585334712211059043030243870220953326746042137531191714089701627811251067663359858603114674053493969767509848972356555383799783134520270863593585507899289815326421111856142068972650698265946694428882344371553806742899341265022101510635404464619443384875601340769083956704665204046459639281164687982088558486318360056536193067106874502161720701554510188994798634290522102156046719663236499599990423848804619891404153570202856601199043070659482978854224557375271345039682983152835942537177575192768337116151846070683360284740748416872758983869551146390744078743687961456069076017495225462573580272763686460733846996346884800591406432655057784497544820526308369273912129604191165192685940953773991727667437292659434183999114411476045976719596077680267796091446064161794419583751971275018541097844638294327884606627440564554312200628124153681772043096262044299199073313722411551385194167046085044122102004593130249815124845535445789668216083120973173392420131854948327419677578826052164184392753068201940953795257347192878272040743907542337146253889654855448663072379399614520430926240124781104222332504730591811639971269634792408690150847061481061927607053632982037415303465410196488440383371131852926628344235016532575944851541759403074875564243327310580642244957281238547918687090819248566795433927152573018733071711201364794969761470229368704818586513292127634273375921152508986259995781840451323245912753974573255683968369819645852078760085587826915732322808417066707843799949505474365490862237565390052704017283731099529100202030898231912171915667425695896394348945847213562958341937833273156453994973181881117850357333347863878325002043158057256957250434507046551722039163592673169766555815717286247018716236323011030445539056530971206501260822610464612385569382704205779425888617121872935708806066605158003285837456649536214961513680013224322044469187158703879174723670560057694681532578606637285630865051670555660047770487866671636031296103034472913644843641278476679806596069500348278797976284764463185279262506615159887353687227334525477336287651978701682107783315905309140897869882875708591241134721480847942356265244307205375836132156581245460172822800880385206655407206871852657815792363199110584225406912852483719210438721973260315748400056197803369996177109728006907672989094919020061407757366001282838193187207196358171055908088341729605565998379740451168148925722414523296546198482641140275835209349468031126967484223901004210501449931105104545289965433703144938110039687981983000625996364203140290752773093678067323580872696757468921323927384833613917288846970906419475324722007531473125819071223899031439923819334074584621271270941349029323955349055034565089625660865259919608610489160459233844366052132425348258108916813749977105366904985865794822667980879409914809887975182465853445543580202160147560833663035952382276507204324413539641583609202600262602136408625389076397739850191639399152984822223244171467406117376083448355508687559964130145378431525955075441814963725777664367849472066593300509226131832668323733742415237635833270522487614805915874558661839802438884197467659733250311660407327394586709856293385076910735074920363893470437032961043915865689298468498626374224910288974655332706992343839532116794213098689298320589391583631866097083077802003371929252284979280645775050411206042625334139771008359258798172029168296981119366566558601743976333999708278639819906261638708928236982723672807527674642781687557482395194703015808746289637125166195527379120290072344645125029087621540751629560361692553972468607922528639459058443104316380061897644439004872783502748167361966074754502668795038241850968901146286346779751589556372064123078034053955047903403583736705656866371714869371078233546755228312854102163536841367166573448555195625435622801656108434102826815384726474074513179410670857675725592766740309583324673235271919103928020102295189566670997964881100322669033429936314919763078737513710899041133553238955599003694265391671940112092854033281904197910639287658382906830043156183276124992184685207068865513295663480746390598005486314227604406488044088167065515301235638064678892680682504425204035331051242705407302282512333463350451426208712741413628394372241488706352428274579978394495471895074943535956065478274939204167986272682253718548791798862149131821513785500541508347214363404560078849159725897991548120151161474090796520101345313017198874237685394031143761580049558516635897805414907164858252844166241373108400859776758422923618581016354188263300670177038338774742893102081913760565887409744735104463928317140857836629302846718735900319272904271855822304316740901776800658839520300468311842542655706803469533139568782809652581556487197912020211409865763668205977165597192906358868965679393037460155943085281781194332952293738300609246288168313401296102982606002502042115683104609705837973112278700468054546861876835983176594260518373381725846367696115261385364451578206315889786861173590771483090474532553244591939641460929794120240398397452121257108587915968535058684666150090303768429268302945832448735912632622888905203016209671559771196369492649049319493250817404517922315975571727621434461063622065141983769429553414570520605879822901635910674056545818501129289537164052156328956073149814647917793867021342003179158594897388051996827569843105338024380868962244999085461439291449125497376497845368839219354864622552464194112101118722760452203549014528397602420932139109748367059204684206634665283078012000505744623079498077875212200510698197303919915985271285969833380561926692486733813767237799846533222603265322348265870791143432387509691451251710501086855031132052650394
12139381654199013233291287590646652408810812936536758513014205864173404549184734876197157416880901148872315192637581662669952529079601323456335179401825742464419322233732226663284472935347583270796539888277614080356528629316105627093258901922544306855172057348466000717578059792080667292174064410915237680122972070088822678061594669508092289995954598054122350998046926038137172817323190904550307457987724797367865902898825075535697596180368343871872343992423207967993932566214948703853154501112285394986821458974297308065093462324553394772450673739314581731578522112969214446593056029282252124213052025889234491430452792055648632550569132631246970824699417728139940624992311112065893510107459515164993438086383804440147526312496823276881813027445243358916433420839751962938484922958764488744255941604695384865659273226859470539022840361389451899110484353089028180637165666004995898075298034567400954771709955884151649625202400825936815579403623115756267028947194590411725808495971477899816524774399833344228918764503697772377054549896800034248407916649448607657431875019137376191907276028499273419704451577716484601706035113668131000073191296608018940266843346991503474235302408796695326312183605124963319382025425264241092596103552942102280846258418579231327141367447507208667711301904025292359047191943644740414188015389990919145148368920135602441256787782079371665713505618304728182882537049236930938731354520311197735464958000760844484918337493558841661462348602981153457941300039571920997153899227785654128675894846056010881476651752689384722126233956093769968144679553753478365403868406022929726261048636104102222053230635751881353021350023892673899333933291671737811899823499433673172085274362832591188195507702180981399632115183178078073388355392653754104253446231623764163837370076496043556188378899702492501000512674739943503304838910339085641089830478722450711602068344148946129959566928375951855857553412114961970147599647513069878103770319256334162949247166130369544391739615598470846833493035301169463823416245182656586740820196570704937883082006310728842210715093434236764547118224407587191407198373052183374068492458028234672102627531664758235087169352175694328639072454193748860004939501432670419887895611812112947295853325493232011995053239481979937453102639743774978546926566170484926438663124727987586915331172147061202609196240914145497064767942462444900543568617739635260187249935954274382434410917183989847663555900389313194093291570972969240505328747287478201123971142136411317548905832078904391052157828506100590547075386872580184710334142865285491971542187950867260683000208564318602522584686381057575304708577597946074649955439873131176898287721494836124026460731108000059658090021547877205196574123442110506893475921141697270356374412988712985926073596158769312771479917264404028124527857142806859335508518882766406454965473300980902119952518031642742578662083782543577957329455478979391189623712806842233322910696851263923092907044340638243905483267917856351386051301709975716252058284955081689589863771462617285929397758244170708834416999261621740968686961786011406905150421925861726304245928081009990122390404985939286118239541137933854470943645882996455897130151714560825216123160300786493046238779564151086628101543077028601828691914901958004382766351078256912510327341784528984561516858156818970491100723869584303538349766904323709915694112980255813013834080321227193277890985413375401507888746970449057142382950853959176758485348820941651451989389917879505630644614544921430854661182851637446244392044734799688071144013732390744413645874952165739847263145690798352431356852659399479012292300459690296794775931287115202729133524454850616658823326084237447144573240662226079079565441439373490350786501702430697448369744805005616027335543863149008560699232803816976162853674504941638914694966817316381002008056957241561400832017343233992741387967410971434101864506054073022528476148433468652682577457895590476416096491001787140499460684619449748967521911971032541267879021320184024228970330987549766140307656509138777989068511769239895351955240056325580169787589093211937819952564187979328468165832715986450160764607168038511935527287411707286538881102074631520451923602956529239779329551969305656635120012560758257872730686883537276071863054652488754230477326272046509193349025105910839001250942235592461383712555685209269264345777376695120646617764915579685676603687699141630590682222470850565750805874706945787043972594227446541161136009710203118346676203922791632172830595779766212210480635397321403546873151110670125514635712469736662909486215181895839432590917456058051239630573720179890242287751995658624209184552891542290232454410300381134598168241289366846220441945650051629351880196219052617875674739107932168534411970840070090352098604337462035725690128043817834444193213598078506020138192966086489189971897811456493983986062054228267072470248715358885933252792775403705154534325254140595229444071030861552313714391479287148432537814168012142948563280826962802189515486200413793217131725013785494332947138143153340028978582206591754771779790675194259445865568275865102690230097055463670058246389752875405799152014769403729195087144134641592531186972282541192404141037258191645638744638364203856683346196409241598303495209733550154503077685456583858689184365629185400645036876706365594150837312580985210389528035292028129078676398057578983489185453508086886823716644113503112264331601866406701982476652602921157842404532788308752084335710328179607915614112225027745131839802158651985800896446658730663725705530223473141040515426281507723326752981608983347559897035966926761343442866263310694402709098473610106478713951486737633477410537126202696325955891925270581726402974770832761717732389305819750842867464485661101108011655166824314993908872404291875632756908034819663816883805527744067707930193675627065686431630853227094788589800176874885355135377226298890664224958206066185557198907246023792283156198446808754496619514527042660084892096886948193669432229488876335755810244549982839563034125949308861533035874149660076884830216509614318191281021815803468002317526458483494967809060038526179398057328367566956980046278535729978873547598777281246090671898254938276385081912689434615939209014485511426956998777909066409065839647247323319752405897632661459693949848388283773887842827369164590847214708247503276158407705776181680650116398023498001896078038993432408372519456678287844959142242035867513497179175074154522122523464238300694183009066918415534405536989927716816887551183918519812929082669801064018133685695825301468884622442762757298885811908372303160844363733064858928392584120124846374093654506517678123340776858688859191253107422573473844382614257322287941773781337826066231861626266938385986441751086341919037821034483380949184998120500984695393943712394050207896800230219253543907872101182147125357496090056473159876479545331082096065099409001450628102559307633306744037459228793341933538348507243193166017348748304246104138431540812704135119661044581540635619337479317266331278157182866609384264058936762786447067480737763027036804557002537810417408306088340059933901746790006671691052086246105860031445674589803548787629435298223399182245730963132816512509234975283364640845944261234283206716771612857568820388727482421170148330960112518683413234307672458801321224679623692589687751247520883195510294627790806624806880049390102153893825428601468635830148621042027083184383716636256143056299412084718342195669950100798468924625279944464675882519468524202093366540317725093271919577186187952525180928539319874255327869331635100700484355222103028128613073465040193657142101358310801336726054853009164182995627799489264233400654224588093777650779667546871457306322274925729419700230655793605747293155776276142516388400538214498863404175313119274773350460377019274661287177012604045736134164601061503067035571767973094733167685553676358063109669362507976347723962340572769055061148104679407900228937714117437869627143059970799907023839336866015687095261261244543051225594585590656445281342533206030362348998042792437790084059987256593156031343583652472659999303526849464211545601250020404948259068703926038712799743097134254677530464292008491599284042645790918791973609751066957883547107989124592528957259476024877500805123839845095540272709326520334386756768263942366262842997341281285502612551333772474069636530778853833186330953628896566033881795007964018312330822358969580708828510873169637883207322358319885648207685920417013247681791353522815268919712033324909776615988882046298141052838437726174811259127056839552096508299206236521853103688749689068331575655828278927182768034414044853483498084007083624780775747611763795105525510845183724804748826853326563565155603712676903349422916947111821464600320163944394057131471593996471693799254290508235068901637169982564819842385241604443376442607485663246976557923561128643155979332464756935875988976638387702471578177881779267816862619186028633759708250541310655687688155420229602991115987850424608931803600309038798366657752346437849112831804563474580807201019506498015819007545253742098327739610395433813927146821817451590561949116729364289708031688647408030282417329737876783789527274772703993979013371630300865816877852243769629291368134944151982537836192315243559881551272660197975574562992087275542903349696769474605934653326641785865406411050965084160916339977073389985497049777590172598320775342763426960080113329713844464923189998988946376992931932643783737507724590331659040021761875737335125527557543383629703063839443016534456692723501405716189742647436341301230203792672526852954885395107416177942593783378532477876690801380736599552243529050897108021815001347513795172325146324668636951934583757566452297945441658402909234823979470506796861048854123409974935863671161342289176902457205089050943254063182826316070864396147125636889916931112507811491764275069768013042159488711190426792969424991135136633740665591961342641085058731707087595825349994740921374568444885455011730505159076430558871392850827063611889634733574783821387061584223128532989761517855031644846225195589631108040513683032967518934601105112422995123448321611853060871412968122977519085295752073047092595928473841912898211177496502385872020701307899539229163462595269372918315635335348825147846827282280053155315962575738062909464564752688085455718730334127382020632995606923665045682975173770326378748250852026860696536134047958232283416262925974055034809181924099591740544835187461478525480267065514820596427338709481536426475331947480077249805303816130697313502306984598968643959570979191901005895613962465285069599543508889859637680467189231912474920460753864131361175080004696608158185493052419087190578913719471193983039896472338431006953337699457366283984387209269594654868136231757590475967704446184603094935853662915031132321239177883178167446597369605419851559880840491234620536511928765016394376399884498669036095301725910114847592679661468348344712800676320990077946064896914709534200436491931701281496932407650720678960521541601854661995717690925351171584510864643948038363040847738893718054062079068915948121616206738280065717881827336308513795045645826982011064136499475332141170551878768539395571658765115297819745367250612257986110919709598963556296154898673157672201852109307042642688830526151428544010800863889116545348061917844015442424688708010790002959124637100481322153714515585266748420889687089146271752899853023205366532274134018038332463943698470291298829796745577836454313235590433514208537897031249790824409527460588578276044885493850518090317020680159963862179705532964083699211657010306816045243252231613583489763410463666515374373261111170474916941819748833252341627162173217086651685660267994120028789124771180803414525185249306721927689226872403078558134897160043039978283893890230896449322582159106700552065157743005575734320085373382639246217286617568949691555421848791643527499515208595773104648845733909757804007592877320250561769684747406245207786158582508766576730150943798088190901758907628760918694535279025357388741380954291777618602899301755948330599327076942008224096253090176526739227492800195588668253938883847453121508761359718116067910533405491813977606586108258345323233885766031642602157170085059947631088018177933216226422569398543567279118890275807145740506681602071063883898894982390771897780911373886003061264206493099551137111832168206368729890440857573759352510159030449754372209529758713360834152862103983517389131781336312350372107829257298395266242578185134580453310745943363487726746965180054551975438515049210905022750686761549446553367766298999510138996271491548574834393210506566031052038559653532992495154382866836242556554961307831139458469988672262247080904434738178900310604320985823126610288635812035312406641199013332411013474009715898228280725500732319390770900983354358838892559438894621789375295405347163626228453499865930494710990043882806740210848863509786886770309447670258768000439648966070737539341402268277845291212609751091054850930324667602348590180993026773085457419386903808776176544480702745915770771329928565580992718925239591464818022699054190079890427052105830135427325676237423128613042972385077979901503544232856138248638740895711677425879601356525623917819492018013084566588849737220680993100881288111279054033634273806512254898608566501559438236975996318811056459152492267243961258398631795911302412314468912860480789034387848311067724428445110120860335019478585980089194079209631464601890915507976810883098418751109945752895440413079745763554259414800134162603896888699897256963875912535088594922100667962105758917545284430330011062682058234659728871782345259634116782262246575628973290573701934025679260914755459600842044960302547104248927125512352103749108674125046844433751297901996610023195485406746911635742420418589692746660965193218406647694136226590611069432686448551276480369390943407517297140468065844480770725917529633349135868044490383640838851407474449537287277420391498015552453188254524543042357331643694257727581844519326925815357285993636582698663598623212570491740480362285610374796129845281766121172832788654804457384997120745883490448591665679950297043188694116682189253588828149263919163030708042240092807602880792579436970196210176590924894060384648755186068784181891040471465556986364379895181971817189569226348027038904607000402040047859451727784803077825545030506105040112804675394293935206422319382204990655813062504563088725569523632024765677113871595315370312385716762009407632623336691782944913107245075533649231987224707018303085259116092738397897102308306823349772019022728264018649567951193903934122244140677266315974745234561601307063381177736928940942916266838501075267986265409845089771118506382003202116078120258311865576065098966013060053646154416248225866517894255631197120860832494218791877992101277471129915760242150203979358907427559390412945355369779852366924766260122798249499589878684506193188051948521021643234300808595844285483368598286045029695646990915087233670342935833129569832028759985377330297883904834288252946377726325964914077317996769808697906479495938331248998258715247291289588457641892003714112599081863630795835637401161554589660480625396067511613773462160886711866939981891638285140213962885296965407271677428847832082791012392152440283555635764830241086253280802086157402868737198415540381735091090873735260337325485023576443627901024812241465609801671030924748571794181618651991904779732905200254527360911022015568420642850408244022612376574755861731315872644843104142415333930362765971526935566045422291482552064241140534480268608108467006018212471565993617955086372458300939526045055973697200761604615102528589089994571859
46933104403555138462283771181726532139035106708618697254726489808913335773629611532379677297348972965084338659510088405137144854499200317492236026067125584095848080159153744441385846572155054098334661353527975988540728368935862941166770085251211987469119766681077992296253626791238496227341378873138569110057847389185552474343629630840881018387901956218443730444737648029745337733286354363197558150447149868473344228308237343905910591612297761294065776897029214877121516254817168201784381766360915675377267686511700434948033745866642574148095427579347339004939063084373016583248849485509805668972394473990116482928701394510289425079468414961693154194095782966085852188621389533482898347177143427422703579075273623828968423213799004178321467894814056667068960014961666299082141326091901477186161640832881622770772565189422070246433274723251102142651068293733579992050373873855437287905327438102556482798245503261971552894386992374901072385686478353814926505636817065156526500926910993069453379850047782366567782816093264647731235201449460888864381917915426579887849542211374087263898053033942591650755597286084692860737001174353615980011795721372961776495654568427171425122988795878791398829586906237405237257746105704825182273806432905927493924683625603506825032366792606272716309111722988436338482487888757634042074850979972271344139919746384506020360058906148674518826047136246117540511938184114835767130224086042825800073447546018348597379247970513647068553756016315529971044756766133396746093914754030331585686693720782567337316216375466525197854267942933336152240972399252325911359325853615626446858322856893388969211771533109205347716631117261714645955937166126561879601247164565771603870855092076915182288862634523987296470918585583491672823272215160605927901373742516244753292525651582356239848468690258692641888049592188835043930486169045411623022508415579756015286963201275502879639864652824433629457702160084926745844292946587874527260481796928330337925586041920591159353123616901039994017672891157808607083089439907432305047231825871015539425114914882480613305012959771686498030227887252552885404584559054924916435383189645544766040832099085551711926582727759261918779015736408554540152027207274038285832448787467182854411205345115411274074330464040400338846120657779849314407436208866140327685327845371653939856803410647386379323759621966595053697431754033796993447058425605068387684900643374712413457153680823759165348042535038401588264529768701903626549393996083111884085365910235329115421579364914789487328112752897994888446426606910870544301745245974198557461747772082951316903863429350569115131939834106585600650788991748972744038202140011280049760400155201430670018182948388821449309769953922564609554602560793603340481564590534350005675311219298224621198760206020204488555850716530677057616860035140506624203344342886727783254884388587882914326146807676008088634622569504553182552824881672917653973483412687624993251578383554158058049577127359441114558361505393781454283875982763047381313397902686016182185218487062950693434646923410715911353650543218297263270931823027752685128890103612344490699900240888936049210600640311750931977905078965431947201070230868503210058591417385595069239198827833304599703619536479165549071434555873700043584558972378304711047156185273787252922409202332488519434064182379721967131689618285985390756620021501227624598472819784526487016467846123013012235643892155874255340882278197312615104801934454618057346946720287602922960456823566069514414790238226867121133745739262429690065966695788117847312054011455088532767475954702694890397226024744659463400926386139028638068708830478775057216951348764230520519576080810875937906876481556058813623842014205553345503348500057807007659442600256717302158136706540058487692081914170182106911774432089999189434789634730488997821327844691320161921125062337285494842918935155362396483450021046371439861539012580253037578652146277396783410815731578207317018592557228366661805513524531945843248467045481395350373117664370037888106032572634815069905897161508159953073767758131741185810826892048696406980913773309574622618851173681784948449333022774267370749437287529187537549778528910366770944437049812097795161785550775985902860558993688907498433218553776778868602739429951558388016060880454078578180939785136303915961815141395267139282643623076767298604014288832259702956577062580535138748270769594730674112637484097812116863352056660085705933770757365265787949804535492955976073596853620397415432779457019183263481708117620699054333265427976650937581144526037841179870444530066022651174392694502518801056140360251080907906252807440304289299537357522982665373342661884764643999737123997120853612792551392185276700797305012757970689423919269871484925272970113093527480063733778295300441174976357453102077332312411373321925114700038131757422552825082807421362046347008431052359460731872786136173034942793452814292325274011405202626038578867681238534478183091568383694680492488861231730666474888266966821688018524440277586785500343712488143251229987910467267421798873017074683951231889647405311901524726520049870796806662696289548063317126207216299859318094258698856231074522997799146121937712405757816784988464874097969204543806497885009673306369009162114551670231021233896483915192167641955782905736754766173794736827759761808404751066008928649219510692804421745520402563994711355746189916334682307069367577505557226769336356368754355952156702470685045295102969497776389151325999722125594423404533199801076850352395978962217954951999224404010192746166519260691778331484130983008203185010739048597119818047938498635102603752135669210544189519587676588201834952526639485671889908274583100185371268636043211358011393625289562442195741313888535470834724792243132626639854429790143363289451331694440299704019632249390105741526492594374436736925368205262632585757965742726897236640777850870477634824303919369606893798765088065605139710409671700685574011844084837226056239858297701948874046278801501881573723907823982624636483406797473729091477491622858037729798917413156104446817776646196226044697868333872762225525617084176324741750564570244246261843668240223080781091054235327909600217720929360320033172947505483077674578610314495509045529064261986994697791917036815688842900545213164485363036005562233527072136554535734069267852081693678894124115890214811284504024078921738383676197966202160847732738631868729581273353144450506100361118568524501616193590014392697021046192058800971038119798196088803722306780896876787367629878747494732413212378664997555950345574218502046737385711607841547235992534041111954378577870896666527537460841311657849318292533534751168706582519437116609796372025794410292382471437212912561153772244125907826921857532506454382629826757523032753093979509340147767230895975231193870161437241514975904029404813243256570939920178292882293721912861377103678830451768635268511440940345832034485151684901173191943203556028704355051084546510322474670270379655287120846340787668931725361304636304852309027090129650107214303894500103081069165895250710803319247076874359494418549742658849872579405073795461448132854746577103834883908252048649808986403804151298276393147624311186195499030532405597027408371187262443160976294612118201234505418160920800096518367783344514651894521968619950640329239443712728150404092571224804031693818233902208091761595281829525003245605004729777206177216407363276278980400238685585018784111095600871646593235994207569931689419207598741470819224628073378223596971128920297710641377677988234493847200865731590067753043512766646487605213682730051547432627227369410837432593640168389077190111974812239356993835438242243021711607837750891049734528880713017651612576734107802519164491378168032876166225556737555134667537450900916892473183715237713386229533037371572409498518065826948563700819239452815750984801782718505064012000316941548393944738752792532594709145990804238966690710369500404018975282535637324283307284306539380342724553857337835753837901273459997486229158347085882528719410131454707029352162687310737108888466694906895707082657803813120269449080858440036445292266425280678847671444776683468455267481358699379946870894841844101214563385566923375548257415406865801150997345629718489376828603428016233490542868303284445089702646591610130307422721830310527977526284170838263981778686331913332721052669668095544215480802411787732543912385477412751286747066838741347428342400936445234834254139212223446369145501194387940996257934215617670878453135915901379382498217101745427167488617474228899341585961330137016970194838024688640122065092898952476371505915634496664460320932086075268177984924513175672314781103399095811174825745281619712608994509980718655519519742895850779698285829778552767144942292277355391098862098841022925477064190193444155454145354939871352944328558526811019403199428635192314575704052550349262045784368621752447711024582373171164463333161696425362083515986987444475648762847589191698436102720622436567793714809909731989597372874222352472510693087436740166207044998342988025555471694594002176564147210822454872350285404153740293612216252544345900225726949223316814095287949085279914743693194448712670647877216461753319559942142358507936402451728388091391168687755257507294633223682420142920261815266113202830686915326247664918709286124915027203501702800617532225781023123261938025234387597901395575547903315023723985525309404810020129643539711479683483422756390292385900496571243429022870667272271088854412124628559485959817345077528154868425016720688691023166014013849089750024293836417759685583991703013269178142624162408192598877804865069077450886661562874137501020709093689475543333327351223604470698550591609338795207526885205946118511416786740493751289040730081524141115458183005014483703426503343121487214749288366725599520849577935657585853585984277988456841927232364187599470828134969717423335191889384686346193674489330287869771540337246168203249106442859151366163203703047995627009153921971720017696208277843423964896927251323567834669686640422570061881371853004314346750274379851409777049553087156121453388698526648440123682587700152923308090362487608907849457174757107743340412970392121268659703282937763227670938711156317136940447775216887182270494024517331798132429905746130359270002575153574730876861306991991998118955842423111207696260290408069840484519481605867997133259143037040010264648064289222297407499780000185805943259783626123675941487190284394259587994614024431587466908614333712756070707389922323747827743353532337287847026125147011184115084607687279861527190772968642679567027238398296750492109377187618839858118468730301171672155012506837292067707669581219228819303793573427715899741199082245279996396351052313451663967131958055828382731891862360738859136477562168464512605955076946999785250852093274398658344831543219913229595390434438068185246179338595674386535628886353071217263872211609969634921468112649728083015202399363067993341179567219998773578388518491667917520736433121333057735180498123776784584594751504527581965550173261568157680998256379586422184381495793123482825126367589339
```

以为可以直接得到32轮的结果，发现到后面结果太大了根本计算不出来

想到另一种思路能不能给每一次的结果做映射，先求出0~16的结果

```assembly
for n in range(17):
    enc = 0
    for _ in range(2**n + 4**n):
        enc = enc - 17 * (((enc + ((
            (enc + 1) * 0xF0F0F0F0F0F0F0F1) >> 64) + 1) >> 4) -
                            ((enc + 1) >> 63)) + 1
    print(enc, end=", ")
```

结果

```assembly
2, 6, 3, 4, 0, 2, 12, 5, 2, 6, 3, 4, 0, 2, 12, 5, 2
```

得到映射：

| index | qword_55C080 | n    | 2 ** n + 4 ** n | qword_5B20E8 |
| ----- | ------------ | ---- | --------------- | ------------ |
| 0     | 1            | 0    | 2               | 2            |
| 1     | 3            | 2    | 20              | 3            |
| 2     | 6            | 5    | 1056            | 2            |
| 3     | 9            | 8    | 65792           | 2            |
| 4     | 0x0A         | 9    | 262656          | 6            |
| 5     | 0x0B         | 10   | 1049600         | 3            |
| 6     | 0x0C         | 11   | 4196352         | 4            |

可以得出n和qword_5B20E8的关系，或者(n%8)和qword_5B20E8的关系，然后求出flag

```assembly
timeLists = [
    1, 3, 6, 9, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x14,
    0x19, 0x1E, 0x28, 0x42, 0x66, 0x0A0, 0x936, 0x3D21, 0x149A7, 0x243AC,
    0x0CB5BE, 0x47DC61, 0x16C0F46, 0x262C432, 0x4ACE299, 0x10FBC92A,
    0x329ECDFD, 0x370D7470
]
sbox = [84, 94, 82, 4, 85, 5, 83, 95, 80, 7, 84, 86, 81, 2, 3, 0]
enc_cycle = [2, 6, 3, 4, 0, 2, 12, 5]
print(''.join(chr(sbox[enc_cycle[(i - 1) % 8]] ^ 0x66) for i in timeLists))
```

4b445b3247c45344c54c44734445452c

------------------------------------

在网上还看到了许多其他解法，保存一下以后学习

动态规划

```assembly
import binascii
f = [2,1,1,0]
table = binascii.unhexlify('5F53055504525E54')[::-1]
table += binascii.unhexlify('570003025156540750')[::-1]
flag = ''
qword_55C080 = [1, 3, 6, 9, 0xA,0x0B,0x0C,0x0D,0x0E,0x0F,0x10,0x11,0x12,0x14,0x19,0x1E,0x28,0x42,0x66,0x0A0,0x936,0x3D21,0x149A7,0x243AC,0x0CB5BE,0x47DC61,0x16C0F46,0x262C432,0x4ACE299,0x10FBC92A,0x329ECDFD,0x370D7470]
k = 0
for i in range(0x370D7470):
    if(i == qword_55C080[k]-1): #因为 f 的初始值是计算一次的结果，所以要减一
        flag+= chr(table[f[0]]^0x66)
        k+=1
    tmp0 = (2*f[0]+f[1]+f[2])%17
    tmp1 = (2*f[1]+f[0]+f[3])%17
    tmp2 = tmp1
    tmp3 = (2*f[3]+f[1]+f[2])%17
    f = [tmp0,tmp1,tmp2,tmp3]
 
print(flag)
```

