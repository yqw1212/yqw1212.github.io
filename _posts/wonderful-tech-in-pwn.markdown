## 程序没有leak时的巧妙思路

### Magic Gadget

BUUOJ cscctf_2019_qual_signal

栈溢出

无leak

NO-PIE/有ELF基址

如果程序是用g++编译，则会存在这个gadget

```assembly
add dword ptr [rbp - 0x3d], ebx ;
nop dword ptr [rax + rax] ;
ret
```

gadet + ret2csu = AAW！实现任意地址写值

### ret2libsyscall

Patial overwrite

利用覆盖低位字节，达到不需要leak也可以修改目标值，可能存在一定的爆破。

假设某个got值为     0x7feff7a7b950

one_gadget地址为 0x7feff7z8a780

由于相对地址固定，可以直接覆写got的后3字节。

库函数（2.27）的惊喜

<read + 15> syscall

<write + 18> syscall

<open64 + 76> syscall

<alarm + 5> syscall

<close + 18> syscall

华为云ctf-game

#### 控制rax：

atoi()

read()返回read的字符数

其他函数

#### 控制rdx：

open("fn", 0, 0);

ret2csu

其他函数

## 通过House of Husk入门IO_FILE

覆盖__printf_arginfo_table

覆盖__printf_function_table

触发printf

fastbin的free机制

## SROP以及拓展

