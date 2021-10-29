---
layout: post
title:  Linux programming(1)
date:   2021-10-19 00:08:01 +0300
image:  2021-10-19-coffee.jpg
tags:   [note]
---

## ch01 INTRODUCTION

#### 常用的gcc选项：

* -c  只编译，不连接成为可执行文件。编译器只是由输入的.c等源代码文件生成.o为后缀的目标文件，通常用于编译不包含主程序的子程序文件。

* -E   只运行C预编译器。

* -g   生成调试信息，GNU调试器可利用该信息。

* -S   停止于编译步骤之后，不进行汇编步骤，最后的输出文件类型为汇编源代码文件。GCC 产生的汇编语言文件的缺省扩展名是 .s 。

* -O1  让gcc对源代码进行基本优化，这些优化在大多数情况下都会使程序执行得更快。

* -O2  让gcc产生尽可能小和尽可能快的代码，-O2选项将使编译的速度比使用-O1时慢，但通常产生的代码执行速度会更快。

* -o FILE 确定输出文件的名称为FILE，同时这个名称不能和源文件同名。如果不给出这个选项，gcc就给出系统预设的可执行文件a.out。 

* -Wall  生成所有警告信息。

* -w 不生成任何警告信息。

* -IDIRECTORY 指定额外的头文件搜索路径DIRECTORY。 

* -LDIRECTORY 指定额外的函数库搜索路径DIRECTORY。

静态库

fred.c

```assembly
#include <stdio.h>

void fred(int arg){
    printf("fred: you passed %d\n", arg);
}
```

bill.c

```assembly
#include <stdio.h>

void bill(char *arg){
    printf("bill: you passed %s\n", arg);
}
```

lib.h

```assembly
void bill(char *);
void fred(int);
```

program.c

```
#include "lib.h"

int main(){
    bill("Hello World");
    exit(0);
}
```

编译

```assembly
gcc -c bill.c fred.c
gcc -c program.c
gcc -o program program.o bill.o
```

归档

```assembly
ar crv libfoo.a bill.o fred.o
```

编译

```
gcc -o program program.o libfoo.a
gcc -o program program.o -L. -lfoo
```

#### 系统信息

df

```assembly
└─$ df 
Filesystem     1K-blocks     Used Available Use% Mounted on
udev              974596        0    974596   0% /dev
tmpfs             202264     1164    201100   1% /run
/dev/sda1       81000912 21477880  55362420  28% /
tmpfs            1011312    28176    983136   3% /dev/shm
tmpfs               5120        0      5120   0% /run/lock
tmpfs             202260       64    202196   1% /run/user/1000
```

du

```assembly
└─$ du
52      .
```

free

```assembly
└─$ free       
               total        used        free      shared  buff/cache   available
Mem:         2022628      975556      128936       52064      918136      820032
Swap:         998396        2584      995812
```

## ch02 Debugging and make

#### Debugging

```assembly
#include <stdio.h>

typedef struct{
	char *data;
	int key;
}item;

item array[] = {
	{"bill", 3},
	{"neil", 4},
	{"john", 2},
	{"rick", 5},
	{"alex", 1},
};

sort(a, n)
item *a;
{
	int i=0, j=0;
	int s = 1;
	
	for(; i<n && s!=0; i++){
		s = 0;
		for(j=0; j<n; j++){
			if(a[j].key > a[j+1].key){
				item t = a[j];
				a[j] = a[j+1];
				a[j+1] = t;
				s++;
			}
		}
		n--;
	}
}

main(){
	sort(array, 5);
	for(int i=0; i<5; i++){
		printf("array[%d] = {%s, %d}\n", i, array[i].data, array[i].key);
	}
}
```

编译

```assembly
cc -g -o debug3 debug3.c
```

加上-g 选项，会保留代码的文字信息，便于调试

**gdb命令**

* run
* backtrace
* print
* list
* break
* @\<number\>
* cont
* display
* commands
* info
* disable
* next

一个有错误的C源程序

```assembly
#include <stdio.h>
#include <stdlib.h>

static char buff[256];
static char *string;

int main(){
	printf("Please input a string:");
	gets(string);

	printf("\nYour string is: %s\n", string);
}
```

使用gdb查找程序中出现的问题

```assembly
└─$ gdb bugging
GNU gdb (Debian 10.1-2) 10.1.90.20210103-git
Copyright (C) 2021 Free Software Foundation, Inc.                            
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from bugging...
(gdb) list
3
4       static char buff[256];
5       static char *string;
6
7       int main(){
8               printf("Please input a string:");
9               gets(string);
10
11              printf("\nYour string is: %s\n", string);
12      }
(gdb) b 9
Breakpoint 3 at 0x55555555515a: file bugging.c, line 9.
(gdb) r
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /home/kali/Documents/linux/ch2/bugging 

Breakpoint 3, main () at bugging.c:9
9               gets(string);
(gdb) print string
$1 = 0x0
(gdb) set variable string=&buff
(gdb) print string
$2 = 0x555555558060 <buff> ""
(gdb) c
Continuing.
Please input a string:hello

Breakpoint 1, main () at bugging.c:11
11              printf("\nYour string is: %s\n", string);
(gdb) c
Continuing.

Your string is: hello
[Inferior 1 (process 2273) exited normally]
(gdb) q
```

#### Makefile自动化变量

关于自动化变量可以理解为由 Makefile 自动产生的变量。在模式规则中，规则的目标和依赖的文件名代表了一类的文件。规则的命令是对所有这一类文件的描述。我们在 Makefile 中描述规则时，依赖文件和目标文件是变动的，显然在命令中不能出现具体的文件名称，否则模式规则将失去意义。

那么模式规则命令中该如何表示文件呢？就需要使用“自动化变量”，自动化变量的取值根据执行的规则来决定，取决于执行规则的目标文件和依赖文件。下面是对所有的自动化变量进行的说明：

| 自动化变量 | 说明                                                         |
| ---------- | ------------------------------------------------------------ |
| $@         | 表示规则的目标文件名。如果目标是一个文档文件（Linux 中，一般成 .a 文件为文档文件，也成为静态的库文件）， 那么它代表这个文档的文件名。在多目标模式规则中，它代表的是触发规则被执行的文件名。 |
| $%         | 当目标文件是一个静态库文件时，代表静态库的一个成员名。       |
| $<         | 规则的第一个依赖的文件名。如果是一个目标文件使用隐含的规则来重建，则它代表由隐含规则加入的第一个依赖文件。 |
| $?         | 所有比目标文件更新的依赖文件列表，空格分隔。如果目标文件时静态库文件，代表的是库文件（.o 文件）。 |
| $^         | 代表的是所有依赖文件列表，使用空格分隔。如果目标是静态库文件，它所代表的只能是所有的库成员（.o 文件）名。 一个文件可重复的出现在目标的依赖中，变量“$^”只记录它的第一次引用的情况。就是说变量“$^”会去掉重复的依赖文件。 |
| $+         | 类似“$^”，但是它保留了依赖文件中重复出现的文件。主要用在程序链接时库的交叉引用场合。 |
| $*         | 在模式规则和静态模式规则中，代表“茎”。“茎”是目标模式中“%”所代表的部分（当文件名中存在目录时， “茎”也包含目录部分）。 |

实例：

```
test:test.o test1.o test2.o
	gcc -o $@ $^
test.o:test.c test.h
	gcc -o $@ $<
test1.o:test1.c test1.h
	gcc -o $@ $<
test2.o:test2.c test2.h
	gcc -o $@ $<
```

这个规则模式中用到了 "$@" 、"$<" 和 "$^" 这三个自动化变量，对比之前写的 Makefile 中的命令，我们可以发现 "$@" 代表的是目标文件test，“$^”代表的是依赖的文件，“$<”代表的是依赖文件中的第一个。我们在执行 make 的时候，make 会自动识别命令中的自动化变量，并自动实现自动化变量中的值的替换，这个类似于编译C语言文件的时候的预处理的作用。

#### 伪目标实现多文件编辑

如果在一个文件里想要同时生成多个可执行文件，我们可以借助伪目标来实现。使用方式如下：

```assembly
.PHONY:all
all:test1 test2 test3
test1:test1.o
	gcc -o $@ $^
test2:test2.o
	gcc -o $@ $^
test3:test3.o
	gcc -o $@ $^
```

我们在当前目录下创建了三个源文件，目的是把这三个源文件编译成为三个可执行文件。将重建的规则放到 Makefile 中，约定使用 "all" 的伪目标来作为最终目标，它的依赖文件就是要生成的可执行文件。这样的话只需要一个 make 命令，就会同时生成三个可执行文件。

之所以这样写，是因为伪目标的特性，它总会被执行，所以它依赖的三个文件的目标就不如 "all" 这个目标新，所以，其他的三个目标的规则总是被执行，这也就达到了我们一口气生成多个目标的目的。我们也可以实现单独的编译这三个中的任意一个源文件（我们想去重建 test1，我们可以执行命令`make test1` 来实现 ）。 

#### macro宏

```
all: myapp

# Which compiler
CC = gcc

# Where are include files kept
INCLUDE = .

# Options for development
CFLAGS = -g -Wall -ansi

# Options for release
# CFLAGS = -O -Wall -ansi

myapp: main.o 2.o 3.o
	${CC} -o myapp main.o 2.o 3.o
main.o: main.c a.h
	${CC} -I${INCLUDE} ${CFLAGS} -c main.c
2.o: 2.c a.h b.h
	${CC} -I${INCLUDE} ${CFLAGS} -c 2.c
3.o: 3.c b.h c.h
	${CC} -I${INCLUDE} ${CFLAGS} -c 3.c
```

加上-g 选项，会保留代码的文字信息，便于调试

-Wall，强制输出所有警告，用于调试。

-ansi 是使用c++98标准去编译代码

## ch03 Working with Files

/dev/console这个设备代表的是控制台。错误信息和诊断信息通常会被发送到这个设备上。

/dev/tty如果一个进程有控制终端的话，那么特殊文件/dev/tty就是这个终端的的别名。

/dev/null这是空设备。所有写向这个设备的输出都将被丢弃。

#### open

```
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

int open(const char *path, int oflags);
int open(const char *path, int oflags, mode_t mode);
```

aflags

| Mode     | Description                                                  |
| -------- | ------------------------------------------------------------ |
| O_RDONLY | Open for read-only                                           |
| O_WRONLY | Open for write-only                                          |
| O_RDWR   | Open for reading ang writing                                 |
| O_APPEND | Place written data at the end of the file                    |
| O_TRUNG  | Set the length of the file to zero, discarding existing contents |
| O_CREAT  | Creates the file, if necessary, with permissions given in mode |
| O_EXCL   | Used with O_CREAT, ensures that the caller creates the file. This protects against two programs creating the file at the same time. If the file already exists, open will fail |

mode

* S_IRUSR: Read permission, owner
* S_IWUSR: Write permission, owner
* S_IXUSR: Execute permission, owner
* S_IRGRP: Read permission, group
* S_IWGRP: Write permission, group
* S_IXGRP: Execute permission, group
* S_IROTH: Read permission, others
* S_IWOTH: Write permission, others
* S_IXOTH: Execute permission, others

umask是一个系统变量，它的作用是：当文件创建时，为文件的访问权限设定一个掩码。

我们这里使用time工具对这个程序运行的时间进行了测算。Linux使用TIMEFORMAT变量来重置默认的**POSIX****时间输出格式**，POSIX时间格式不包括CPU使用率。

user值表示程序本身以及它所调用的**库中的子例程**使用的时间。sys是由程序直接或间接调用的**系统调用**执行的时间。

**C语言lseek()函数：移动文件的读写位置**

头文件：

```assembly
#include <unistd.h>
#include <sys/types.h>
```

定义函数:

```assembly
off_t lseek(int fildes, off_t offset, int whence);
```

函数说明：
每一个已打开的文件都有一个读写位置, 当打开文件时通常其读写位置是指向文件开头, 若是以附加的方式打开文件(如O_APPEND), 则读写位置会指向文件尾. 当read()或write()时, 读写位置会随之增加,lseek()便是用来控制该文件的读写位置. 

参数fildes 为已打开的文件描述词, 参数offset 为根据参数whence来移动读写位置的位移数.

* SEEK_SET: offset is an absolute position
* SEEK_CUR: offset is relative to the current position
* SEEK_END: offset is relative to the end of the file

### stat

头文件：

```assembly
#include <sys/stat.h>
#include <unistd.h>
```

定义函数：

```assembly
int stat(const char *file_name, struct stat *buf);
```

函数说明：stat()用来将参数file_name 所指的文件状态, 复制到参数buf 所指的结构中。

下面是struct stat 内各参数的说明：

```assembly
struct stat
{
  dev_t st_dev; //device 文件的设备编号
  ino_t st_ino; //inode 文件的i-node
  mode_t st_mode; //protection 文件的类型和存取的权限
  nlink_t st_nlink; //number of hard links 连到该文件的硬连接数目, 刚建立的文件值为1.
  uid_t st_uid; //user ID of owner 文件所有者的用户识别码
  gid_t st_gid; //group ID of owner 文件所有者的组识别码
  dev_t st_rdev; //device type 若此文件为装置设备文件, 则为其设备编号
  off_t st_size; //total size, in bytes 文件大小, 以字节计算
  unsigned long st_blksize; //blocksize for filesystem I/O 文件系统的I/O 缓冲区大小.
  unsigned long st_blocks; //number of blocks allocated 占用文件区块的个数, 每一区块大小为512 个字节.
  
  time_t st_atime; //time of lastaccess 文件最近一次被存取或被执行的时间, 一般只有在用mknod、utime、read、write 与tructate 时改变.
  time_t st_mtime; //time of last modification 文件最后一次被修改的时间, 一般只有在用mknod、utime 和write 时才会改变
  time_t st_ctime; //time of last change i-node 最近一次被更改的时间, 此参数会在文件所有者、组、权限被更改时更新
};
```

File-type flags include:

* S_IFBLK: Entry is a block special device区块装置
* S_IFDIR: Entry is a directory目录
* S_IFCHR: Entry is a character special device字符装置

* S_IFIFO: Entry is a FIFO (named pipe)先进先出

* S_IFREG: Entry is a regular file一般文件

* S_IFLNK: Entry is a symbolic link符号连接

Other mode flags include:

* S_ISUID: Entry has setUID on execution文件的 (set user-id on execution)位

* S_ISGID: Entry has setGID on execution文件的 (set group-id on execution)位

Masks to interpret the st_mode flags include:

* S_IFMT: File type文件类型的位遮罩

* S_IRWXU: User read/write/execute permissions

* S_IRWXG: Group read/write/execute permissions

* S_IRWXO: Others’ read/write/execute permissions

There are some **macros** defined to help with determining file types.

* S_ISBLK: Test for block special file

* S_ISCHR: Test for character special file是否为字符装置文件

* S_ISDIR: Test for directory是否为目录

* S_ISFIFO: Test for FIFO是否为先进先出
* S_ISREG: Test for regular file是否为一般文件
* S_ISLNK: Test for symbolic link判断是否为符号连接

### Advanced Topics：mmap

```assembly
int munmap(void *start, size_t length)
```

start：要取消映射的内存区域的起始地址
length：要取消映射的内存区域的大小。
返回说明
成功执行时munmap()返回0。失败时munmap返回-1.

## ch04 Processes and Signals

编程过程中，有时需要让一个进程等待另一个进程，最常见的是父进程等待自己的子进程，或者父进程回收自己的子进程资源包括僵尸进程。当父进程忘了用wait()函数等待已终止的子进程时,子进程就会进入一种无父进程的状态,此时子进程就是僵尸进程.

系统调用函数：wait()

函数原型是

```assembly
#include <sys/types.h>
#include <wait.h>
int wait(int *status)
```

父进程一旦调用了wait就立即阻塞自己，由wait自动分析是否当前进程的某个子进程已经退出，如果让它找到了这样一个已经变成僵尸的子进程，wait就会收集这个子进程的信息，并把它彻底销毁后返回；如果没有找到这样一个子进程，wait就会一直阻塞在这里，直到有一个出现为止。

参数status用来保存被收集进程退出时的一些状态，它是一个指向int类型的指针。但如果我们对这个子进程是如何死掉毫不在意，只想把这个僵尸进程消灭掉，（事实上绝大多数情况下，我们都会这样想），我们就可以设定这个参数为NULL，就像下面这样：

```
pid = wait(NULL);
```

如果参数status的值不是NULL，wait就会把子进程退出时的状态取出并存入其中， 这是一个整数值（int），指出了子进程是正常退出还是被非正常结束的，以及正常结束时的返回值，或被哪一个信号结束的等信息。由于这些信息 被存放在一个整数的不同二进制位中，所以用常规的方法读取会非常麻烦，人们就设计了一套专门的宏（macro）来完成这项工作，其中最常用的两个：

* WIFEXITED(status) 这个宏用来指出子进程是否为正常退出的，如果是，它会返回一个非零值。（请注意，虽然名字一样，这里的参数status并不同于wait唯一的参数–指向整数的指针status，而是那个指针所指向的整数，切记不要搞混了。）
* WEXITSTATUS(status) 当WIFEXITED返回非零值时，我们可以用这个宏来提取子进程的返回值，如果子进程调用exit(5)退出，WEXITSTATUS(status) 就会返回5；如果子进程调用exit(7)，WEXITSTATUS(status)就会返回7。请注意，如果进程不是正常退出的，也就是说， WIFEXITED返回0，这个值就毫无意义

```assembly
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>

int main(){
	pid_t pid;
	char *message;
	int n;
	int exit_code;

	printf("fork program starting\n");
	pid = fork();
	switch(pid){
		case -1:{
			perror("fork failed");
			exit(1);
		}
		case 0:{
			message = "This is the child";
			n = 5;
			exit_code = 37;
			break;
		}
		default:{
			message = "This is the parent";
			n = 3;
			exit_code = 0;
			break;
		}
	}

	for(; n>0; n--){
		puts(message);
		sleep(1);
	}

	if(pid != 0){
		int stat_val;
		pid_t child_pid;

		child_pid = wait(&stat_val);
		printf("child has finished: PID = %d\n", child_pid);

		if(WIFEXITED(stat_val)){
			printf("child exited with code %d\n", WEXITSTATUS(stat_val));
		}
		else{
			printf("child terminated abnormally\n");
		}		
	}
	exit(exit_code);
}
```

运行结果

```assembly
└─$ ./wait  
fork program starting
This is the parent
This is the child
This is the child
This is the parent
This is the child
This is the parent
This is the child
This is the child
child has finished: PID = 1275
child exited with code 37
```
