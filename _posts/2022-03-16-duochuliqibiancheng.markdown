---
layout: post
title:  多处理器编程
date:   2022-03-16 00:08:01 +0300
image:  2022-03-16-hotel.jpg
tags:   [note,os]
---

如何证明线程确实共享内存

```assembly
#include "thread.h"

int x = 0;

void Thello(int id) {
  usleep(id * 100000);
  printf("Hello from thread #%c\n", "123456789ABCDEF"[x++]);
}

int main() {
  for (int i = 0; i < 10; i++) {
    create(Thello);
  }
}
```

```assembly
yqw@ubuntu:~/Documents/opsystem$ gcc -o shm-test shm-test.c -pthread
yqw@ubuntu:~/Documents/opsystem$ ./shm-test 
Hello from thread #1
Hello from thread #2
Hello from thread #3
Hello from thread #4
Hello from thread #5
Hello from thread #6
Hello from thread #7
Hello from thread #8
Hello from thread #9
Hello from thread #A
```

如何证明线程具有独立堆栈 (以及确定它们的范围)

```assembly
#include "thread.h"

// 线程局部变量
// 给每个线程创建一个副本
__thread char *base, *cur; // thread-local variables
__thread int id;

// objdump to see how thread-local variables are implemented
__attribute__((noinline)) void set_cur(void *ptr) { cur = ptr; }
__attribute__((noinline)) char *get_cur()         { return cur; }

void stackoverflow(int n) {
  set_cur(&n);
  if (n % 1024 == 0) {
    int sz = base - get_cur();
    printf("Stack size of T%d >= %d KB\n", id, sz / 1024);
  }
  stackoverflow(n + 1);
}

void Tprobe(int tid) {
  id = tid;
  base = (void *)&tid;
  stackoverflow(0);
}

int main() {
  setbuf(stdout, NULL);
  for (int i = 0; i < 4; i++) {
    create(Tprobe);
  }
}
```

对输出排序

```assembly
yqw@ubuntu:~/Documents/opsystem$ ./a.out | sort -nk 6
Stack size of T1 >= 0 KB
Stack size of T2 >= 0 KB
Stack size of T3 >= 0 KB
Stack size of T4 >= 0 KB
Stack size of T1 >= 64 KB
Stack size of T2 >= 64 KB
Stack size of T3 >= 64 KB
Stack size of T4 >= 64 KB
Stack size of T1 >= 128 KB
Stack size of T2 >= 128 KB
Stack size of T3 >= 128 KB
Stack size of T4 >= 128 KB
Stack size of T1 >= 192 KB
Stack size of T2 >= 192 KB
Stack size of T3 >= 192 KB
Stack size of T4 >= 192 KB
Stack size of T1 >= 256 KB
Stack size of T2 >= 256 KB
Stack size of T3 >= 256 KB
Stack size of T4 >= 256 KB
Stack size of T1 >= 320 KB
Stack size of T2 >= 320 KB
Stack size of T3 >= 320 KB
Stack size of T4 >= 320 KB
Stack size of T1 >= 384 KB
Stack size of T2 >= 384 KB
Stack size of T3 >= 384 KB
Stack size of T4 >= 384 KB
Stack size of T1 >= 448 KB
Stack size of T2 >= 448 KB
Stack size of T3 >= 448 KB
Stack size of T4 >= 448 KB
Stack size of T1 >= 512 KB
Stack size of T2 >= 512 KB
Stack size of T3 >= 512 KB
Stack size of T4 >= 512 KB
Stack size of T1 >= 576 KB
Stack size of T2 >= 576 KB
Stack size of T3 >= 576 KB
Stack size of T4 >= 576 KB
Stack size of T1 >= 640 KB
Stack size of T2 >= 640 KB
Stack size of T3 >= 640 KB
Stack size of T4 >= 640 KB
Stack size of T1 >= 704 KB
Stack size of T2 >= 704 KB
Stack size of T3 >= 704 KB
Stack size of T4 >= 704 KB
Stack size of T1 >= 768 KB
Stack size of T2 >= 768 KB
Stack size of T3 >= 768 KB
Stack size of T4 >= 768 KB
Stack size of T1 >= 832 KB
Stack size of T2 >= 832 KB
Stack size of T3 >= 832 KB
Stack size of T4 >= 832 KB
Stack size of T1 >= 896 KB
Stack size of T2 >= 896 KB
Stack size of T3 >= 896 KB
Stack size of T4 >= 896 KB
Stack size of T1 >= 960 KB
Stack size of T2 >= 960 KB
Stack size of T3 >= 960 KB
Stack size of T4 >= 960 KB
Stack size of T1 >= 1024 KB
Stack size of T2 >= 1024 KB
Stack size of T3 >= 1024 KB
Stack size of T4 >= 1024 KB
Stack size of T1 >= 1088 KB
Stack size of T2 >= 1088 KB
Stack size of T3 >= 1088 KB
Stack size of T4 >= 1088 KB
Stack size of T1 >= 1152 KB
Stack size of T2 >= 1152 KB
Stack size of T3 >= 1152 KB
Stack size of T4 >= 1152 KB
Stack size of T1 >= 1216 KB
Stack size of T2 >= 1216 KB
Stack size of T3 >= 1216 KB
Stack size of T4 >= 1216 KB
Stack size of T1 >= 1280 KB
Stack size of T2 >= 1280 KB
Stack size of T3 >= 1280 KB
Stack size of T4 >= 1280 KB
Stack size of T1 >= 1344 KB
Stack size of T2 >= 1344 KB
Stack size of T3 >= 1344 KB
Stack size of T4 >= 1344 KB
Stack size of T1 >= 1408 KB
Stack size of T2 >= 1408 KB
Stack size of T3 >= 1408 KB
Stack size of T4 >= 1408 KB
Stack size of T1 >= 1472 KB
Stack size of T2 >= 1472 KB
Stack size of T3 >= 1472 KB
Stack size of T4 >= 1472 KB
Stack size of T1 >= 1536 KB
Stack size of T2 >= 1536 KB
Stack size of T3 >= 1536 KB
Stack size of T4 >= 1536 KB
Stack size of T1 >= 1600 KB
Stack size of T2 >= 1600 KB
Stack size of T3 >= 1600 KB
Stack size of T4 >= 1600 KB
Stack size of T1 >= 1664 KB
Stack size of T2 >= 1664 KB
Stack size of T3 >= 1664 KB
Stack size of T4 >= 1664 KB
Stack size of T1 >= 1728 KB
Stack size of T2 >= 1728 KB
Stack size of T3 >= 1728 KB
Stack size of T4 >= 1728 KB
Stack size of T1 >= 1792 KB
Stack size of T2 >= 1792 KB
Stack size of T3 >= 1792 KB
Stack size of T4 >= 1792 KB
Stack size of T1 >= 1856 KB
Stack size of T2 >= 1856 KB
Stack size of T3 >= 1856 KB
Stack size of T4 >= 1856 KB
Stack size of T1 >= 1920 KB
Stack size of T2 >= 1920 KB
Stack size of T3 >= 1920 KB
Stack size of T4 >= 1920 KB
Stack size of T1 >= 1984 KB
Stack size of T2 >= 1984 KB
Stack size of T3 >= 1984 KB
Stack size of T4 >= 1984 KB
Stack size of T1 >= 2048 KB
Stack size of T2 >= 2048 KB
Stack size of T3 >= 2048 KB
Stack size of T4 >= 2048 KB
Stack size of T1 >= 2112 KB
Stack size of T2 >= 2112 KB
Stack size of T3 >= 2112 KB
Stack size of T4 >= 2112 KB
Stack size of T1 >= 2176 KB
Stack size of T2 >= 2176 KB
Stack size of T3 >= 2176 KB
Stack size of T4 >= 2176 KB
Stack size of T1 >= 2240 KB
Stack size of T2 >= 2240 KB
Stack size of T3 >= 2240 KB
Stack size of T4 >= 2240 KB
Stack size of T1 >= 2304 KB
Stack size of T2 >= 2304 KB
Stack size of T3 >= 2304 KB
Stack size of T4 >= 2304 KB
Stack size of T1 >= 2368 KB
Stack size of T2 >= 2368 KB
Stack size of T3 >= 2368 KB
Stack size of T4 >= 2368 KB
Stack size of T1 >= 2432 KB
Stack size of T2 >= 2432 KB
Stack size of T3 >= 2432 KB
Stack size of T4 >= 2432 KB
Stack size of T1 >= 2496 KB
Stack size of T2 >= 2496 KB
Stack size of T3 >= 2496 KB
Stack size of T4 >= 2496 KB
Stack size of T1 >= 2560 KB
Stack size of T2 >= 2560 KB
Stack size of T3 >= 2560 KB
Stack size of T4 >= 2560 KB
Stack size of T1 >= 2624 KB
Stack size of T2 >= 2624 KB
Stack size of T3 >= 2624 KB
Stack size of T4 >= 2624 KB
Stack size of T1 >= 2688 KB
Stack size of T2 >= 2688 KB
Stack size of T3 >= 2688 KB
Stack size of T4 >= 2688 KB
Stack size of T1 >= 2752 KB
Stack size of T2 >= 2752 KB
Stack size of T3 >= 2752 KB
Stack size of T4 >= 2752 KB
Stack size of T1 >= 2816 KB
Stack size of T2 >= 2816 KB
Stack size of T3 >= 2816 KB
Stack size of T4 >= 2816 KB
Stack size of T1 >= 2880 KB
Stack size of T2 >= 2880 KB
Stack size of T3 >= 2880 KB
Stack size of T4 >= 2880 KB
Stack size of T1 >= 2944 KB
Stack size of T2 >= 2944 KB
Stack size of T3 >= 2944 KB
Stack size of T4 >= 2944 KB
Stack size of T1 >= 3008 KB
Stack size of T2 >= 3008 KB
Stack size of T3 >= 3008 KB
Stack size of T4 >= 3008 KB
Stack size of T1 >= 3072 KB
Stack size of T2 >= 3072 KB
Stack size of T3 >= 3072 KB
Stack size of T4 >= 3072 KB
Stack size of T1 >= 3136 KB
Stack size of T2 >= 3136 KB
Stack size of T3 >= 3136 KB
Stack size of T4 >= 3136 KB
Stack size of T1 >= 3200 KB
Stack size of T2 >= 3200 KB
Stack size of T3 >= 3200 KB
Stack size of T4 >= 3200 KB
Stack size of T1 >= 3264 KB
Stack size of T2 >= 3264 KB
Stack size of T3 >= 3264 KB
Stack size of T4 >= 3264 KB
Stack size of T1 >= 3328 KB
Stack size of T2 >= 3328 KB
Stack size of T3 >= 3328 KB
Stack size of T4 >= 3328 KB
Stack size of T1 >= 3392 KB
Stack size of T2 >= 3392 KB
Stack size of T3 >= 3392 KB
Stack size of T4 >= 3392 KB
Stack size of T1 >= 3456 KB
Stack size of T2 >= 3456 KB
Stack size of T3 >= 3456 KB
Stack size of T4 >= 3456 KB
Stack size of T1 >= 3520 KB
Stack size of T2 >= 3520 KB
Stack size of T3 >= 3520 KB
Stack size of T4 >= 3520 KB
Stack size of T1 >= 3584 KB
Stack size of T2 >= 3584 KB
Stack size of T3 >= 3584 KB
Stack size of T4 >= 3584 KB
Stack size of T1 >= 3648 KB
Stack size of T2 >= 3648 KB
Stack size of T3 >= 3648 KB
Stack size of T4 >= 3648 KB
Stack size of T1 >= 3712 KB
Stack size of T2 >= 3712 KB
Stack size of T3 >= 3712 KB
Stack size of T4 >= 3712 KB
Stack size of T1 >= 3776 KB
Stack size of T2 >= 3776 KB
Stack size of T3 >= 3776 KB
Stack size of T4 >= 3776 KB
Stack size of T1 >= 3840 KB
Stack size of T2 >= 3840 KB
Stack size of T3 >= 3840 KB
Stack size of T4 >= 3840 KB
Stack size of T1 >= 3904 KB
Stack size of T2 >= 3904 KB
Stack size of T3 >= 3904 KB
Stack size of T4 >= 3904 KB
Stack size of T1 >= 3968 KB
Stack size of T2 >= 3968 KB
Stack size of T3 >= 3968 KB
Stack size of T4 >= 3968 KB
Stack size of T1 >= 4032 KB
Stack size of T2 >= 4032 KB
Stack size of T3 >= 4032 KB
Stack size of T4 >= 4032 KB
Stack size of T1 >= 4096 KB
Stack size of T2 >= 4096 KB
Stack size of T3 >= 4096 KB
Stack size of T4 >= 4096 KB
Stack size of T1 >= 4160 KB
Stack size of T2 >= 4160 KB
Stack size of T3 >= 4160 KB
Stack size of T4 >= 4160 KB
Stack size of T1 >= 4224 KB
Stack size of T2 >= 4224 KB
Stack size of T3 >= 4224 KB
Stack size of T4 >= 4224 KB
Stack size of T1 >= 4288 KB
Stack size of T2 >= 4288 KB
Stack size of T3 >= 4288 KB
Stack size of T4 >= 4288 KB
Stack size of T1 >= 4352 KB
Stack size of T2 >= 4352 KB
Stack size of T3 >= 4352 KB
Stack size of T4 >= 4352 KB
Stack size of T1 >= 4416 KB
Stack size of T2 >= 4416 KB
Stack size of T3 >= 4416 KB
Stack size of T4 >= 4416 KB
Stack size of T1 >= 4480 KB
Stack size of T2 >= 4480 KB
Stack size of T3 >= 4480 KB
Stack size of T4 >= 4480 KB
Stack size of T1 >= 4544 KB
Stack size of T2 >= 4544 KB
Stack size of T3 >= 4544 KB
Stack size of T4 >= 4544 KB
Stack size of T1 >= 4608 KB
Stack size of T2 >= 4608 KB
Stack size of T3 >= 4608 KB
Stack size of T4 >= 4608 KB
Stack size of T1 >= 4672 KB
Stack size of T2 >= 4672 KB
Stack size of T3 >= 4672 KB
Stack size of T4 >= 4672 KB
Stack size of T1 >= 4736 KB
Stack size of T2 >= 4736 KB
Stack size of T3 >= 4736 KB
Stack size of T4 >= 4736 KB
Stack size of T1 >= 4800 KB
Stack size of T2 >= 4800 KB
Stack size of T3 >= 4800 KB
Stack size of T4 >= 4800 KB
Stack size of T1 >= 4864 KB
Stack size of T2 >= 4864 KB
Stack size of T3 >= 4864 KB
Stack size of T4 >= 4864 KB
Stack size of T1 >= 4928 KB
Stack size of T2 >= 4928 KB
Stack size of T3 >= 4928 KB
Stack size of T4 >= 4928 KB
Stack size of T1 >= 4992 KB
Stack size of T2 >= 4992 KB
Stack size of T3 >= 4992 KB
Stack size of T4 >= 4992 KB
Stack size of T1 >= 5056 KB
Stack size of T2 >= 5056 KB
Stack size of T3 >= 5056 KB
Stack size of T4 >= 5056 KB
Stack size of T1 >= 5120 KB
Stack size of T2 >= 5120 KB
Stack size of T3 >= 5120 KB
Stack size of T4 >= 5120 KB
Stack size of T1 >= 5184 KB
Stack size of T2 >= 5184 KB
Stack size of T3 >= 5184 KB
Stack size of T4 >= 5184 KB
Stack size of T1 >= 5248 KB
Stack size of T2 >= 5248 KB
Stack size of T3 >= 5248 KB
Stack size of T4 >= 5248 KB
Stack size of T1 >= 5312 KB
Stack size of T2 >= 5312 KB
Stack size of T3 >= 5312 KB
Stack size of T4 >= 5312 KB
Stack size of T1 >= 5376 KB
Stack size of T2 >= 5376 KB
Stack size of T3 >= 5376 KB
Stack size of T4 >= 5376 KB
Stack size of T1 >= 5440 KB
Stack size of T2 >= 5440 KB
Stack size of T3 >= 5440 KB
Stack size of T4 >= 5440 KB
Stack size of T1 >= 5504 KB
Stack size of T2 >= 5504 KB
Stack size of T3 >= 5504 KB
Stack size of T4 >= 5504 KB
Stack size of T1 >= 5568 KB
Stack size of T2 >= 5568 KB
Stack size of T3 >= 5568 KB
Stack size of T4 >= 5568 KB
Stack size of T1 >= 5632 KB
Stack size of T2 >= 5632 KB
Stack size of T3 >= 5632 KB
Stack size of T4 >= 5632 KB
Stack size of T1 >= 5696 KB
Stack size of T3 >= 5696 KB
Stack size of T4 >= 5696 KB
Stack size of T1 >= 5760 KB
Stack size of T3 >= 5760 KB
Stack size of T4 >= 5760 KB
Stack size of T1 >= 5824 KB
Stack size of T3 >= 5824 KB
Stack size of T4 >= 5824 KB
Stack size of T1 >= 5888 KB
Stack size of T3 >= 5888 KB
Stack size of T4 >= 5888 KB
Stack size of T1 >= 5952 KB
Stack size of T3 >= 5952 KB
Stack size of T4 >= 5952 KB
Stack size of T1 >= 6016 KB
Stack size of T4 >= 6016 KB
Stack size of T1 >= 6080 KB
Stack size of T4 >= 6080 KB
Stack size of T1 >= 6144 KB
Stack size of T4 >= 6144 KB
Stack size of T1 >= 6208 KB
Stack size of T4 >= 6208 KB
Stack size of T1 >= 6272 KB
Stack size of T4 >= 6272 KB
Stack size of T1 >= 6336 KB
Stack size of T4 >= 6336 KB
Stack size of T1 >= 6400 KB
Stack size of T4 >= 6400 KB
Stack size of T1 >= 6464 KB
Stack size of T4 >= 6464 KB
Stack size of T1 >= 6528 KB
Stack size of T4 >= 6528 KB
Stack size of T1 >= 6592 KB
Stack size of T4 >= 6592 KB
Stack size of T1 >= 6656 KB
Stack size of T4 >= 6656 KB
Stack size of T1 >= 6720 KB
Stack size of T4 >= 6720 KB
Stack size of T1 >= 6784 KB
Stack size of T4 >= 6784 KB
Stack size of T1 >= 6848 KB
Stack size of T4 >= 6848 KB
Stack size of T1 >= 6912 KB
Stack size of T4 >= 6912 KB
Stack size of T1 >= 6976 KB
Stack size of T4 >= 6976 KB
Stack size of T1 >= 7040 KB
Stack size of T4 >= 7040 KB
Stack size of T1 >= 7104 KB
Stack size of T4 >= 7104 KB
Stack size of T1 >= 7168 KB
Stack size of T4 >= 7168 KB
Stack size of T1 >= 7232 KB
Stack size of T4 >= 7232 KB
Stack size of T1 >= 7296 KB
Stack size of T4 >= 7296 KB
Stack size of T1 >= 7360 KB
Stack size of T4 >= 7360 KB
Stack size of T1 >= 7424 KB
Stack size of T4 >= 7424 KB
Stack size of T1 >= 7488 KB
Stack size of T4 >= 7488 KB
Stack size of T1 >= 7552 KB
Stack size of T1 >= 7616 KB
Stack size of T1 >= 7680 KB
Stack size of T1 >= 7744 KB
Stack size of T1 >= 7808 KB
Stack size of T1 >= 7872 KB
Stack size of T1 >= 7936 KB
Stack size of T1 >= 8000 KB
Stack size of T1 >= 8064 KB
Stack size of T1 >= 8128 KB
```

创建线程使用的是哪个系统调用

```assembly
#include "thread.h"

void Ta() { while (1) {;} }
void Tb() { while (1) { ; } }

int main() {
  create(Tb);
}
```

使用strace工具

```assembly
yqw@ubuntu:~/Documents/opsystem$ strace ./a.out 
execve("./a.out", ["./a.out"], 0x7ffd5f762410 /* 51 vars */) = 0
brk(NULL)                               = 0x561622108000
arch_prctl(0x3001 /* ARCH_??? */, 0x7ffc54a73b80) = -1 EINVAL (Invalid argument)
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=74095, ...}) = 0
mmap(NULL, 74095, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7fe06adb5000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpthread.so.0", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\220q\0\0\0\0\0\0"..., 832) = 832
pread64(3, "\4\0\0\0\24\0\0\0\3\0\0\0GNU\0\360\2300%\360\340\363'\246\332u/\364\377\246u"..., 68, 824) = 68
fstat(3, {st_mode=S_IFREG|0755, st_size=157224, ...}) = 0
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7fe06adb3000
pread64(3, "\4\0\0\0\24\0\0\0\3\0\0\0GNU\0\360\2300%\360\340\363'\246\332u/\364\377\246u"..., 68, 824) = 68
mmap(NULL, 140408, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7fe06ad90000
mmap(0x7fe06ad96000, 69632, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x6000) = 0x7fe06ad96000
mmap(0x7fe06ada7000, 24576, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x17000) = 0x7fe06ada7000
mmap(0x7fe06adad000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1c000) = 0x7fe06adad000
mmap(0x7fe06adaf000, 13432, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7fe06adaf000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\360A\2\0\0\0\0\0"..., 832) = 832
pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
pread64(3, "\4\0\0\0\20\0\0\0\5\0\0\0GNU\0\2\0\0\300\4\0\0\0\3\0\0\0\0\0\0\0", 32, 848) = 32
pread64(3, "\4\0\0\0\24\0\0\0\3\0\0\0GNU\0\237\333t\347\262\27\320l\223\27*\202C\370T\177"..., 68, 880) = 68
fstat(3, {st_mode=S_IFREG|0755, st_size=2029560, ...}) = 0
pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
pread64(3, "\4\0\0\0\20\0\0\0\5\0\0\0GNU\0\2\0\0\300\4\0\0\0\3\0\0\0\0\0\0\0", 32, 848) = 32
pread64(3, "\4\0\0\0\24\0\0\0\3\0\0\0GNU\0\237\333t\347\262\27\320l\223\27*\202C\370T\177"..., 68, 880) = 68
mmap(NULL, 2037344, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7fe06ab9e000
mmap(0x7fe06abc0000, 1540096, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x22000) = 0x7fe06abc0000
mmap(0x7fe06ad38000, 319488, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x19a000) = 0x7fe06ad38000
mmap(0x7fe06ad86000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1e7000) = 0x7fe06ad86000
mmap(0x7fe06ad8c000, 13920, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7fe06ad8c000
close(3)                                = 0
mmap(NULL, 12288, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7fe06ab9b000
arch_prctl(ARCH_SET_FS, 0x7fe06ab9b740) = 0
mprotect(0x7fe06ad86000, 16384, PROT_READ) = 0
mprotect(0x7fe06adad000, 4096, PROT_READ) = 0
mprotect(0x561621bcb000, 4096, PROT_READ) = 0
mprotect(0x7fe06adf5000, 4096, PROT_READ) = 0
munmap(0x7fe06adb5000, 74095)           = 0
set_tid_address(0x7fe06ab9ba10)         = 4461
set_robust_list(0x7fe06ab9ba20, 24)     = 0
rt_sigaction(SIGRTMIN, {sa_handler=0x7fe06ad96bf0, sa_mask=[], sa_flags=SA_RESTORER|SA_SIGINFO, sa_restorer=0x7fe06ada43c0}, NULL, 8) = 0
rt_sigaction(SIGRT_1, {sa_handler=0x7fe06ad96c90, sa_mask=[], sa_flags=SA_RESTORER|SA_RESTART|SA_SIGINFO, sa_restorer=0x7fe06ada43c0}, NULL, 8) = 0
rt_sigprocmask(SIG_UNBLOCK, [RTMIN RT_1], NULL, 8) = 0
prlimit64(0, RLIMIT_STACK, NULL, {rlim_cur=8192*1024, rlim_max=RLIM64_INFINITY}) = 0
mmap(NULL, 8392704, PROT_NONE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_STACK, -1, 0) = 0x7fe06a39a000
mprotect(0x7fe06a39b000, 8388608, PROT_READ|PROT_WRITE) = 0
brk(NULL)                               = 0x561622108000
brk(0x561622129000)                     = 0x561622129000
clone(child_stack=0x7fe06ab99fb0, flags=CLONE_VM|CLONE_FS|CLONE_FILES|CLONE_SIGHAND|CLONE_THREAD|CLONE_SYSVSEM|CLONE_SETTLS|CLONE_PARENT_SETTID|CLONE_CHILD_CLEARTID, parent_tid=[4462], tls=0x7fe06ab9a700, child_tidptr=0x7fe06ab9a9d0) = 4462
futex(0x7fe06ab9a9d0, FUTEX_WAIT, 4462, NULL          
```

clone系统调用，就是用来创建线程的系统调用

## 原子性

山寨多线程支付宝

```assembly
#include "thread.h"

unsigned int balance = 100;

int Alipay_withdraw(int amt) {
  if (balance >= amt) {
    usleep(1);
    balance -= amt;
  }
}

void Talipay(int id){
    Alipay_withdraw(100);
}

int main(){
    create(Talipay);
    create(Talipay);
    join();
    printf("balance = %lu\n", balance);
}
```

运行结果

```assembly
yqw@ubuntu:~/Documents/opsystem$ ./a.out 
balance = 4294967196
yqw@ubuntu:~/Documents/opsystem$ ./a.out 
balance = 4294967196
yqw@ubuntu:~/Documents/opsystem$ ./a.out 
balance = 0
yqw@ubuntu:~/Documents/opsystem$ ./a.out 
balance = 4294967196
yqw@ubuntu:~/Documents/opsystem$ ./a.out 
balance = 4294967196
yqw@ubuntu:~/Documents/opsystem$ ./a.out 
balance = 4294967196
yqw@ubuntu:~/Documents/opsystem$ python3
Python 3.8.10 (default, Nov 26 2021, 20:14:08) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 2**32-100
4294967196
```

另一个小例子：求和

```assembly
#include "thread.h"

#define N 100000000

long sum = 0;

void Tsum() {
    for (int i = 0; i < N; i++){
	asm volatile("lock add $1, %0" : "+m"(sum));
       // sum++;
    }
}

int main() {
  create(Tsum);
  create(Tsum);
  join();
  printf("sum = %ld\n", sum);
}
```

> yqw@ubuntu:~/Documents/opsystem$ ./a.out 
> sum = 200000000

`printf` 还能在多线程程序里调用吗？

> man 3 printf

```assembly
ATTRIBUTES
       For  an  explanation  of  the  terms  used  in  this  section,  see at‐
       tributes(7).

       ┌────────────────────────┬───────────────┬────────────────┐
       │Interface               │ Attribute     │ Value          │
       ├────────────────────────┼───────────────┼────────────────┤
       │printf(), fprintf(),    │ Thread safety │ MT-Safe locale │
       │sprintf(), snprintf(),  │               │                │
       │vprintf(), vfprintf(),  │               │                │
       │vsprintf(), vsnprintf() │               │                │
       └────────────────────────┴───────────────┴────────────────┘
```

printf保证多线程的原子性

## 顺序

对上面的求和的程序编译优化

```assembly
yqw@ubuntu:~/Documents/opsystem$ gcc -O1 sum.c -lpthread && ./a.out 
sum = 100000000
yqw@ubuntu:~/Documents/opsystem$ gcc -O2 sum.c -lpthread && ./a.out 
sum = 200000000
```

```assembly
extern int done;

void join(){
    while(!done){
        asm volatile("":::"memory"); // 不要优化
    }
}
```

```assembly
yqw@ubuntu:~/Documents/opsystem$ objdump -d ./demo.o

./demo.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <join>:
   0:	55                   	push   %rbp
   1:	48 89 e5             	mov    %rsp,%rbp
   4:	eb 00                	jmp    6 <join+0x6>
   6:	8b 05 00 00 00 00    	mov    0x0(%rip),%eax        # c <join+0xc>
   c:	85 c0                	test   %eax,%eax
   e:	74 f6                	je     6 <join+0x6>
  10:	90                   	nop
  11:	5d                   	pop    %rbp
  12:	c3                   	retq   
```

```assembly
#include "thread.h"

int x = 0, y = 0;

atomic_int flag;
#define FLAG atomic_load(&flag)  // 原子的读
#define FLAG_XOR(val) atomic_fetch_xor(&flag, val)  // 原子的异或
#define WAIT_FOR(cond) while (!(cond)) ;

 __attribute__((noinline))
void write_x_read_y() {
  int y_val;
  asm volatile(
    "movl $1, %0;" // x = 1
    "movl %2, %1;" // y_val = y
    : "=m"(x), "=r"(y_val) : "m"(y)
  );
  printf("%d ", y_val);
}

 __attribute__((noinline))
void write_y_read_x() {
  int x_val;
  asm volatile(
    "movl $1, %0;" // y = 1
    "movl %2, %1;" // x_val = x
    : "=m"(y), "=r"(x_val) : "m"(x)
  );
  printf("%d ", x_val);
}

void T1(int id) {
  while (1) {
    WAIT_FOR((FLAG & 1));
    write_x_read_y();
    FLAG_XOR(1);
  }
}

void T2() {
  while (1) {
    WAIT_FOR((FLAG & 2));
    write_y_read_x();
    FLAG_XOR(2);
  }
}

void Tsync() {
  while (1) {
    x = y = 0;
    __sync_synchronize(); // full barrier,确保x和y=0写入内存
    usleep(1);            // + delay
    assert(FLAG == 0);  // 确保开关处于关闭状态
    FLAG_XOR(3);  // b11
    // T1 and T2 clear 0/1-bit, respectively
    WAIT_FOR(FLAG == 0);
    printf("\n"); fflush(stdout);
  }
}

int main() {
  create(T1);
  create(T2);
  create(Tsync);
}
```

```assembly
yqw@ubuntu:~/Documents/opsystem$ ./a.out | head -n 1000000 | sort | uniq -c
 606977 0 0 
 387172 0 1 
   5292 1 0 
    559 1 1 
```

单个处理器把汇编代码 (用电路) “编译” 成更小的 μops

fetch→issue→execute→commit

"mfence"指令