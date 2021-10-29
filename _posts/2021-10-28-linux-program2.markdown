---
layout: post
title:  Linux programming(2)
date:   2021-10-28 00:08:01 +0300
image:  2021-10-28-girl.jpg
tags:   [note]
---

## ch05 sockets

本地套接字的名字是Linux文件系统中的文件，跟一个目录相关联；如果是网络，跟一个端口相关联。

对于网络套接字，它的名字是与客户连接的特定网络有关的服务标识符（端口号或访问点）。

Bind给socket命名。

Listen设置队列的长度，维护一个队列，让新来的等待。

Accept监听，返回一个new socket

SOCK_STREAM是TCP的

SOCK_DGRAM是UDP的

### 本地socket通信

AF_UNIX本地通信才用

server

```assembly
#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <sys/un.h>
#include <unistd.h>

int main(){

    struct sockaddr_un server_address, client_address;

    unlink("server_socket");
    int server_sockfd = socket(AF_UNIX, SOCK_STREAM, 0);
    server_address.sun_family = AF_UNIX;
    strcpy(server_address.sun_path, "server_socket");

    bind(server_sockfd, (struct sockaddr *)&server_address, sizeof(server_address));

    listen(server_sockfd, 5);
    while(1){
        char ch;

        printf("server waiting\n");
        int client_sockfd = accept(server_sockfd, (struct sockaddr *)&client_address, sizeof(client_address));

        read(client_sockfd, &ch, 1);
        ch++;
        write(client_sockfd, &ch, 1);

        close(client_sockfd);
    }

}
```

client

```assembly
#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <sys/un.h>
#include <unistd.h>

int main(){
    
    char ch = 'A';

    int sockfd = socket(AF_UNIX, SOCK_STREAM, 0);
    
    struct sockaddr_un address;
    address.sun_family = AF_UNIX;
    strcpy(address.sun_path, "server_socket");

    int result = connect(sockfd, (struct sockaddr *)&address, sizeof(address));

    if(result == -1){
        perror("oops: client1");
        exit(1);
    }

    write(sockfd, &ch, 1);
    read(sockfd, &ch, 1);
    printf("char from server = %c\n", ch);
    close(sockfd);

    exit(0);
}
```

sockaddr_un结构体

```assembly
struct sockaddr_un{
	sa_family_t sun_family;  /* AF_UNIX */
	char        sun_path[];  /* pathname */
};
```

### socket网络通信

sockaddr_in结构体

```assembly
struct sockaddr_in{
	short int           sin_family;  /* AF_INET */
	unsigned short int  sin_port;    /* Port number */
	struct in_addr      sin_addr;    /* Internet address */
};
```

in_addr结构体

```assembly
struct in_addr{
	unsigned long int  s_addr;
};
```

#### bind

bind调用需要将一个特定的地址结构指针转换为指向通用地址类型(struct sockaddr *)。

```assembly
#include <sys/socket.h>

int bind(int socket, const struct sockaddr *address, size_t address_len);
```

#### listen

```assembly
#include <sys/socket.h>

int listen(int socket, int backlog);
```

#### accept

```assembly
#include <sys/socket.h>

int accept(int socket, struct sockaddr *address, size_t *address_len);
```

accept有阻塞行为

#### connect

```assembly
#include <sys/socket.h>

int connect(int socket, const struct sockaddr *address, size_t address_len);
```

server

```assembly
#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(){

    struct sockaddr_in server_address, client_address;

    int server_sockfd = socket(AF_INET, SOCK_STREAM, 0);

    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = inet_addr("127.0.0.1");
    server_address.sin_port = htons(9734);
    bind(server_sockfd, (struct sockaddr *)&server_address, sizeof(server_address));

    listen(server_sockfd, 5);
    while(1){
        char ch;

        printf("server waiting\n");
        int client_sockfd = accept(server_sockfd, (struct sockaddr *)&client_address, sizeof(client_address));

        read(client_sockfd, &ch, 1);
        ch++;
        write(client_sockfd, &ch, 1);

        close(client_sockfd);
    }

}
```

client

```assembly
#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(){
    
    char ch = 'A';

    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    
    struct sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = inet_addr("127.0.0.1");
    address.sin_port = htons(9734);

    int result = connect(sockfd, (struct sockaddr *)&address, sizeof(address));

    if(result == -1){
        perror("oops: client1");
        exit(1);
    }

    write(sockfd, &ch, 1);
    read(sockfd, &ch, 1);
    printf("char from server = %c\n", ch);
    close(sockfd);

    exit(0);
}
```

#### 测试自己的电脑是大端还是小端

```assembly
#include <stdio.h>

union data{
    int a;  // 01 00 00 00
    char b; // 01
};

int main(){
    union data d;
    d.a = 1;

    if(d.b == 1){
        printf("小端\n");
    }else{
        printf("大端\n");
    }

    return 0;
}
```

以unsigned int value = 0x12345678为例，在两种字节序下其存储情况

**Big-Endian: 低地址存放高位，如下：**

buf[0] (0x12) -- 高位字节

buf[1] (0x34)

buf[2] (0x56)

buf[3] (0x78) -- 低位字节

**Little-Endian: 低地址存放低位，如下：**

buf[0] (0x78) -- 低位字节

buf[1] (0x56)

buf[2] (0x34)

buf[3] (0x12) -- 高位字节

### Network Information

#### hostent结构体

```assembly
struct hostent
{
    char *h_name;         //正式主机名
    char **h_aliases;     //主机别名
    int h_addrtype;       //主机IP地址类型：IPV4-AF_INET
    int h_length;		  //主机IP地址字节长度，对于IPv4是四字节，即32位
    char **h_addr_list;	  //主机的IP地址列表
};
	
#define h_addr h_addr_list[0]   //保存的是IP地址
```

保存一台主机的所有信息。

#### servent

```assembly
struct servent {
    char  *s_name;       /* name of the service */
    char  **s_aliases;   /* list of aliases(alternative names)服务别名列表 */
    int   s_port;        /* The IP port number */
	char  *s_proto;      /* The service type, usually "tcp" or "udp" */
};
```

获取网络信息

```assembly
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netdb.h>
#include <stdio.h>

int main(int argc, char *argv[]){
    char *host, **names, **addrs;
    struct hostent *hostinfo;

    if(argc == 1){
        char myname[256];
        gethostname(myname, 255);
        host = myname;
    }else {
        host = argv[1];
    }

    hostinfo = gethostbyname(host);
    if(!hostinfo){
        fprintf(stderr, "cannot get info for host: %s\n", host);
        exit(1);
    }

    printf("results for host %s:\n", host);
    printf("Name: %s\n", hostinfo->h_name);
    printf("Aliases:");
    names = hostinfo->h_aliases;
    while(*names){
        printf(" %s", *names);
        names++;
    }
    printf("\n");

    if(hostinfo->h_addrtype != AF_INET){
        fprintf(stderr, "Not an IP host!\n");
        exit(1);
    }

    addrs = hostinfo->h_addr_list;
    while(*addrs){
        printf(" %s", inet_ntoa(*(struct in_addr *)*addrs));
        addrs++;
    }
    printf("\n");

    exit(0);
}
```

连接一个标准服务

```assembly
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]){
    char *host;
    int sockfd;
    int len, result;
    struct sockaddr_in address;
    struct hostent *hostinfo;
    struct servent *servinfo;
    char buffer[128];

    if(argc==1){
        host = "localhost";
    }else{
        host = argv[1];
    }

    hostinfo = gethostbyname(host);
    if(!hostinfo){
        fprintf(stderr, "no host: %s\n", host);
        exit(1);
    }

    servinfo = getservbyname("daytime", "tcp");
    if(!servinfo){
        fprintf(stderr, "no daytime service\n");
        exit(1);
    }
    printf("daytime port is %d\n", ntohs(servinfo->s_port));

    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    address.sin_family = AF_INET;
    address.sin_port = servinfo->s_port;
    address.sin_addr = *(struct in_addr *)*hostinfo->h_addr_list;
    len = sizeof(address);

    result = connect(sockfd, (struct sockaddr *)&address, len);
    if(result == -1){
        perror("oops: getdate");
        exit(1);
    }

    result = read(sockfd, buffer, sizeof(buffer));
    buffer[result] = '\0';
    printf("read %d bytes: %s", result, buffer);

    close(sockfd);
    
    exit(0);
}
```

udp服务

```assembly
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]){
    char *host;
    int sockfd;
    int len, result;
    struct sockaddr_in address;
    struct hostent *hostinfo;
    struct servent *servinfo;
    char buffer[128];

    if(argc == 1){
        host = "localhost";
    }else{
        host = argv[1];
    }

    hostinfo = gethostbyname(host);
    if(!hostinfo){
        fprintf(stderr, "no host: %s\n", host);
        exit(1);
    }

    servinfo = getservbyname("daytime", "udp");
    if(!servinfo){
        fprintf(stderr, "no daytime service\n");
        exit(1);
    }
    printf("daytime port is %d\n", ntohs(servinfo->s_port));

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    address.sin_family = AF_INET;
    address.sin_port = servinfo->s_port;
    address.sin_addr = *(struct in_addr *)*hostinfo->h_addr_list;
    len = sizeof(address);

    result = sendto(sockfd, buffer, 1, 0, (struct sockaddr *)&address, len);
    result = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)&address, &len);
    buffer[result] = '\0';
    printf("read %d bytes: %s", result, buffer);

    close(sockfd);

    exit(0);
}
```

开启服务

```assembly
sudo apt install sysv-rc-conf
sudo apt install xinetd
sysv-rc-conf --list
sudo sysv-rc-conf daytime-udp on
service xinetd restart
```

#### select

timeval结构体

```assembly
struct timeval
{
    time_t      tv_sec;     /* seconds */
    suseconds_t tv_usec;    /* microseconds */
};
```

select监控三个集合里有没有就绪的，返回一定是有文件描述符就绪了或超时了。

调用以前集合中是就绪的文件描述符，返回后集合中是就绪的文件描述符。

```assembly
#include <sys/types.h>
#include <sys/time.h>

int select(int nfds, fd_set *readfds, fd_set *writefds, fd_set *errorfds, struct timeval *timeout);
```

程序

```assembly
#include <sys/types.h>
#include <sys/time.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <unistd.h>

int main(){
    char buffer[128];
    int result, nread;
    fd_set inputs, testfds;
    struct timeval timeout;

    FD_ZERO(&inputs);
    FD_SET(0, &inputs);

    while(1){
        testfds = inputs;
        timeout.tv_sec = 2;
        timeout.tv_usec = 500000;

        result = select(FD_SETSIZE, &testfds, (fd_set *)NULL, (fd_set *)NULL, &timeout);

        switch(result){
            case 0:{
                printf("timeout\n");
                break;
            }
            case -1:{
                perror("select");
                exit(1);
            }
            default:{
                if(FD_ISSET(0, &testfds)){
                    ioctl(0, FIONREAD, &nread);
                    if(nread == 0){
                        printf("keyboard done\n");
                        exit(0);
                    }
                    nread = read(0, buffer, nread);
                    buffer[nread] = 0;
                    printf("read %d from keyboard: %s", nread, buffer);
                }
                break;
            }
        }

    }
    return 0;
}
```

## ch06 the linux environment

```
int main(int argc, char *argv[])
```

Shell接受用户输入的命令行，将命令行分解成单词，然后把这些单词放入argv数组。

```assembly
#include <stdio.h>

int main(int argc, char *argv[]){

    for(int arg=0; arg<argc; arg++){
        if(argv[arg][0] == '-'){
            printf("option: %s\n", argv[arg]+1);
        }else{
            printf("argument %d: %s\n", arg, argv[arg]);
        }
    }
    exit(0);

}
```

输出

```assembly
└─$ ./args -i -lr 'hi there' -f fred.c
argument 0: ./args
option: i
option: lr
argument 3: hi there
option: f
argument 5: fred.c
```

#### getopt()

```assembly
#include <unistd.h>

int getopt(int argc, char *const argv[], const char *optstring);

extern char *optarg;
extern int optind, opterr, optopt;
```

getopt函数将传递给程序的main函数的argc和argv作为参数，同时接受一个选项指定字符串optstring， 该字符串告诉getopt哪些选项可用，以及每个选项是否有关联值。

optstring只是一个字符列表，每个字符代表一个单字符选项。如果一个字符后面紧跟一个冒号，则表明该选项有一个关联值作为下一个参数。

如果':'后有值，返回到*optarg里。

'?'选项未知不可识别，存到*optopt。

外部变量optind被设置为下一个待处理参数的索引。getopt用它来记录自己的进度。当所有选项都处理完毕后，optind指向argv数组尾部------可以找到其余参数的地方。

还要注意的是默认情况下getopt会重新排列命令行参数的顺序，所以到最后所有不包含选项的命令行参数都安排到最后。

根据POSIX规范的说法，如果opterr变量是非零值，getopt就会向stderr打印一条出错信息。

```assembly
#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]){
    int opt;

    while((opt = getopt(argc, argv, "if:lr")) != -1){
        switch(opt){
            case 'i':
            case 'l':
            case 'r':
                printf("option: %c\n", opt);
                break;
            case 'f':
                printf("filename: %s\n", optarg);
                break;
            case ':':
                printf("option needs a value\n");
                break;
            case '?':
                printf("unknow option: %c\n", optopt);
                break;
        }
    }
    for(; optind<argc; optind++){
        printf("argument: %s\n", argv[optind]);
    }
    exit(0);
}
```

结果

```assembly
└─$ ./argopt -i -lr 'hi there' -f fred.c -q
option: i
option: l
option: r
filename: fred.c
./argopt: invalid option -- 'q'
unknow option: q
argument: hi there
```

#### env

```assembly
#include <stdlib.h>

char *getenv(const char *name);
int putenv(const char *string);
```

程序

```assembly
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]){
    char *var, *value;
    if(argc == 1 || argc > 3){
        fprintf(stderr, "usage: environ var [value]\n");
        exit(1);
    }

    var = argv[1];
    value = getenv(var);
    if(value){
        printf("Variable %s has value %s\n", var, value);
    }else{
        printf("Variable %s has no value\n", var);
    }

    if(argc == 3){
        char *string;
        value = argv[2];
        string = malloc(strlen(var) + strlen(value) + 2);
        if(!string){
            fprintf(stderr, "out of memory\n");
            exit(1);
        }
        strcpy(string, var);
        strcat(string, "=");
        strcat(string, value);
        printf("Calling putenv with: %s\n", string);
        if(putenv(string) != 0){
            fprintf(stderr, "putenv failed\n");
            free(string);
            exit(1);
        }

        value = getenv(var);
        if(value){
            printf("New value of %s is %s\n", var, value);
        }else{
            printf("New value of %s is null??\n", var);
        }
    }
    
    exit(0);
}
```

结果

```assembly
┌──(kali㉿kali)-[~/Documents/linux]
└─$ ./environ HOME                         
Variable HOME has value /home/kali
                                                                             
┌──(kali㉿kali)-[~/Documents/linux]
└─$ ./environ FRED
Variable FRED has no value
                                                                             
┌──(kali㉿kali)-[~/Documents/linux]
└─$ ./environ FRED melody
Variable FRED has no value
Calling putenv with: FRED=melody
New value of FRED is melody
                                                                             
┌──(kali㉿kali)-[~/Documents/linux]
└─$ ./environ FRED       
Variable FRED has no value
```

#### time

```assembly
#include <time.h>

time_t time(time_t *tloc);

double difftime(time_t time1, time_t time2);

struct tm *gmtime(const time_t timeval);
```

gmtime函数把底层时间分解为一个结构。

```assembly
struct tm { 
    int tm_sec;		      /* 秒–取值区间为[0,59] */ 　　
    int tm_min;           /* 分 - 取值区间为[0,59] */ 　　
    int tm_hour; 	      /* 时 - 取值区间为[0,23] */ 　　
    int tm_mday;          /* 一个月中的日期 - 取值区间为[1,31] */ 　
    int tm_mon;		      /* 月份（从一月开始，0代表一月） - 取值区间为[0,11] */ 
    int tm_year; 	      /* 年份，其值从1900开始 */ 　
    int tm_wday; 	      /* 星期–取值区间为[0,6]，其中0代表星期天，1代表星期一，以此类推 */ 　
    int tm_yday; 	      /* 从每年的1月1日开始的天数–取值区间为[0,365]，其中0代表1月1日，1代表1月2日，以此类推 */ 　
    int tm_isdst; 	      /* 夏令时标识符，实行夏令时的时候，tm_isdst为正。不实行夏令时的进候，tm_isdst为0；不了解情况时，tm_isdst()为负。*/ 　
    long int tm_gmtoff;	  /*指定了日期变更线东面时区中UTC东部时区正秒数或UTC西部时区的负秒数*/ 　　
    const char *tm_zone;  /*当前时区的名字(与环境变量TZ有关)*/ 　
}; 
```

t 是否夏令时。

```assembly
#include <time.h>
#include <stdio.h>
#include <unistd.h>

int main(){
    time_t the_time;

    for(int i=1; i<=10; i++){
        the_time = time((time_t *)0);
        printf("The time is %ld\n", the_time);
        sleep(2);
    }
    
    exit(0);
}
```

```assembly
#include <time.h>
#include <stdio.h>

int main(){
    struct tm *tm_ptr;
    time_t the_time;

    (void)time(&the_time);

    tm_ptr = gmtime(&the_time);

    printf("Raw time is %ld\n", the_time);
    printf("gmtime gives: \n");
    printf("date: %02d/%02d/%02d\n", tm_ptr->tm_year, tm_ptr->tm_mon+1, tm_ptr->tm_mday);
    printf("time: %02d:%02d:%02d\n", tm_ptr->tm_hour, tm_ptr->tm_min, tm_ptr->tm_sec);

    exit(0);
}
```

localtime()

```assembly
#include <time.h>

struct tm *localtime(const time_t *timeval);
```

返回本地时间

mktime

```assembly
time_t mktime(struct tm *timeptr);
```

将时间转换为自1970年1月1日以来持续时间的秒数，发生错误时返回-1

```assembly
#include <time.h>

char *asctime(const struct tm *timeptr);
char *ctime(const time_t *timeval);
```

程序

```assembly
#include <time.h>
#include <stdio.h>

int main(){
    time_t timeval;

    (void)time(&timeval);
    printf("The data is: %s", ctime(&timeval));
    exit(0);
}
```

#### logging

```assembly
#include <syslog.h>

void syslog(int priority, const char *message, arguments...);
```

syslog函数向系统的日志设施(facility)发送一条日志信息。每条信息都有一个priority参数，该参数是一个严重级别与与一个设施值的按位或。严重级别控制日志信息的处理方式，设施值记录日志信息的来源。

设施值

* LOG_LOCAL0
* LOG_LOCAL1
* LOG_LOCAL2
* LOG_LOCAL3
* LOG_LOCAL4
* LOG_LOCAL5
* LOG_LOCAL6
* LOG_LOCAL7

它们的含义由本地管理员指定。

严重级别按优先级递减排列

| 优先级      | 说明                         |
| ----------- | ---------------------------- |
| LOG_EMERG   | 紧急情况                     |
| LOG_ALERT   | 高优先级故障，例如数据库崩溃 |
| LOG_CRIT    | 严重错误                     |
| LOG_ERR     | 错误                         |
| LOG_WARNING | 警告                         |
| LOG_NOTICE  | 需要注意的特殊情况           |
| LOG_INFO    | 一般信息                     |
| LOG_DEBUG   | 调试信息                     |

```
#include <syslog.h>
#include <stdio.h>

int main(){
    FILE *f;
    f = open("not_here", "r");
    if(!f){
        syslog(LOG_ERR | LOG_USER, "oops - %m\n");
    }
    exit(0);
}
```

运行这个程序并没有输出，但是/var/log/messages文件尾会有记录

？？？

```assembly
#include <syslog.h>

void closelog(void);
void openlog(const char *ident, int logopt, int facility);
int setlogmask(int maskpri);
```

可以通过调用openlog函数来改变日志信息的表示方式。

* 设置一个字符串ident，该字符串会添加在日志信息的前面。可以通过它来指明哪个程序创建了这条信息。

* facility参数记录一个将被用于后续syslog调用的默认设施值。其默认值是LOG_USER。

* logopt参数对后续syslog调用的行为进行配置。

  | logopt参数 | 说明                                                         |
  | ---------- | ------------------------------------------------------------ |
  | LOG_PID    | 在日志信息中包含进程标识符，这是系统分配给每个进程的一个唯一值 |
  | LOG_CONS   | 如果信息不能被记录到日志文件中，就把它们发送到控制台         |
  | LOG_ODELAY | 在第一次调用syslog时才打开日志设施                           |
  | LOG_NDELAY | 立即打开日志设施，而不是等到第一次记录日志时                 |

openlog函数会分配并打开一个文件描述符，并通过它来写日志。可以通过调用closelog函数来关闭它。

我们可以用LOG_MASK(priority)为日志信息创建一个掩码，它的作用是创建一个只包含一个优先级的掩码。我们还可以用LOG_UPTO(priority)来创建一个由指定优先级之前的所有优先级（包括指定优先级）构成的掩码。

```assembly
#include <syslog.h>
#include <stdio.h>
#include <unistd.h>

int main(){
    int logmask;

    openlog("logmask", LOG_PID | LOG_CONS, LOG_USER);
    
    syslog(LOG_INFO, "informative message, pid = %d", getpid());
    syslog(LOG_DEBUG, "debug message, should appear");

    logmask = setlogmask(LOG_UPTO(LOG_NOTICE));
    syslog(LOG_DEBUG, "debug message, should not appear");
    exit(0);
}
```

在/var/log/messages文件尾：

```assembly
Oct 17 01:50:11 kali logmask[1708]: informative message, pid = 1708
```

在/var/log/debug文件尾：

```assembly
Oct 17 01:50:11 kali logmask[1708]: debug message, should appear
```

## ch07 data management

### malloc

#### memory1.c

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#define A_MEGABYTE (1024*1024)

int main(){
    char *some_memory;
    int megabyte = A_MEGABYTE;
    int exit_code = EXIT_FAILURE;

    some_memory = (char *)malloc(megabyte);
    if(some_memory != NULL){
        sprintf(some_memory, "Hello World\n");
        printf("%s", some_memory);
        exit_code = EXIT_SUCCESS;
    }
    
    exit(exit_code);
}
```

#### memory2.c

无限申请内存空间

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#define A_MEGABYTE (1024*1024)
#define PHY_MEM_MEGS 1024 * 1024

int main(){
    char *some_memory;
    int megs_obtained = 0;

    while(megs_obtained < (PHY_MEM_MEGS * 2)){
        some_memory = (char *)malloc(A_MEGABYTE);
        if(some_memory != NULL){
            megs_obtained++;
            sprintf(some_memory, "Hello World");
            printf("%s - now allocated %d Megabytes\n", some_memory, megs_obtained);
        } else {
            exit(EXIT_FAILURE);
        }
    }

    exit(EXIT_SUCCESS);
}
```

运行

```assembly
Hello World - now allocated 232192 Megabytes
Hello World - now allocated 232193 Megabytes
Hello World - now allocated 232194 Megabytes
Hello World - now allocated 232195 Megabyteszsh: killed     ./memory2
```

232195M

```
>>> 232195//1024
226
```

#### memory3.c

逐次申请1M空间

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#define ONE_K (1024)

int main(){
    char *some_memory;
    int size_to_allocate = ONE_K;
    int megs_obtained = 0;
    int ks_obtained = 0;

    while(1){
        for(ks_obtained = 0; ks_obtained<1024; ks_obtained++){
            some_memory = (char *)malloc(size_to_allocate);
            if(some_memory == NULL){
                exit(EXIT_FAILURE);
            }
            sprintf(some_memory, "Hello World");
        }
        megs_obtained++;
        printf("Now allocated %d Megabytes\n", megs_obtained);
    }

    exit(EXIT_SUCCESS);
}
```

运行结果

```assembly
Now allocated 1201 Megabytes
Now allocated 1202 Megabytes
Now allocated 1203 Megabytes
Now allocated 1204 Megabytes
Now allocated 1205 Megabytes
Now allocated 1206 Megabytes
Now allocated 1207 Megabytes
Now allocated 1208 Megabytes
zsh: killed     ./memory3
```

#### memory4.c

```assembly
#include <stdlib.h>

#define ONE_K (1024)

int main(){

    char *some_memory = (char *)malloc(ONE_K);

    if(some_memory == NULL){
        exit(EXIT_FAILURE);
    }

    char *scan_ptr = some_memory;
    while(1){
        *scan_ptr = '\0';
        scan_ptr++;
    }
    
    exit(EXIT_SUCCESS);
}
```

运行结果

```assembly
└─$ ./memory4
zsh: segmentation fault  ./memory4
```

#### memory5.c

访问空指针

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

int main(){
    char *some_memory = (char *)0;

    printf("A read from null %s\n", some_memory);
    sprintf(some_memory, "A write to null\n");
    
    exit(EXIT_SUCCESS);
}
```

运行结果

```assembly
└─$ ./memory5
A read from null (null)
zsh: segmentation fault  ./memory5
```

#### memory5b.c

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

int main(){
    char *z = *(const char *)0;

    printf("I read from location zero\n");
    
    exit(EXIT_SUCCESS);
}
```

运行结果

```assembly
└─$ ./memory5b
zsh: segmentation fault  ./memory5b
```

### 文件锁

#### lock1.c

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>

int main(){
    int file_desc;
    int save_errno;

    file_desc = open("/tmp/LCK.test", O_RDWR | O_CREAT | O_EXCL, 0444);
    if(file_desc == -1){
        save_errno = errno;
        printf("Open failed with error %d\n", save_errno);
    }else{
        printf("Open succeeded\n");
    }

    exit(EXIT_SUCCESS);
}
```

运行

```assembly
┌──(kali㉿kali)-[~/Documents/linux/ch7]
└─$ ./lock1   
Open succeeded
                                                                             
┌──(kali㉿kali)-[~/Documents/linux/ch7]
└─$ ./lock1
Open failed with error 17
```

#### lock2.c

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>

const char * lock_file = "/tmp/LCK.test2";

int main(){
    int file_desc;
    int tries = 10;

    while(tries--){
        file_desc = open(lock_file, O_RDWR | O_CREAT | O_EXCL, 0444);
        if(file_desc == -1){
            printf("%d - LOCK already present\n", getpid());
        }else{
            printf("%d - I have exclusive access\n", getpid());
            sleep(1);
            (void)close(file_desc);
            (void)unlink(lock_file);
            sleep(2);
        }
    }

    exit(EXIT_SUCCESS);
}
```

struct flock

```
struct flock {
    short l_type;   /* F_RDLCK, F_WRLCK, or F_UNLCK */
    off_t l_start;  /* offset in bytes, relative to l_whence */
    short l_whence; /* SEEK_SET, SEEK_CUR, or SEEK_END */
    off_t l_len;    /* length, in bytes; 0 means lock to EOF */
    pid_t l_pid;    /* returned with F_GETLK */
};
```

fcntl

```assembly
#include <fcntl.h>

int fcntl(int fildes, int command, struct flock *flock_structure);
```

* F_GETLK
* F_SETLK
* F_SETLKW

lock3.c

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>

const char *test_file = "/tmp/test_lock";

int main(){
    char *byte_to_write = "A";
    struct flock region_1;
    struct flock region_2;
    int res;

    int file_desc = open(test_file, O_RDWR | O_CREAT, 0666);
    if(!file_desc){
        fprintf(stderr, "Unable to open %s for read/write\n", test_file);
        exit(EXIT_FAILURE);
    }

    for(int byte_count=0; byte_count<100; byte_count++){
        (void)write(file_desc, byte_to_write, 1);
    }

    region_1.l_type = F_RDLCK;
    region_1.l_whence = SEEK_SET;
    region_1.l_start = 10;
    region_1.l_len = 20;

    region_2.l_type = F_WRLCK;
    region_2.l_whence = SEEK_SET;
    region_2.l_start = 40;
    region_2.l_len = 10;

    printf("Process %d locking file\n", getpid());
    
    res = fcntl(file_desc, F_SETLK, &region_1);
    if(res == -1){
        fprintf(stderr, "Failed to lock region 1\n");
    }
    res = fcntl(file_desc, F_SETLK, &region_2);
    if(res == -1){
        fprintf(stderr, "Failed to lock region 2\n");
    }

    sleep(60);
    printf("Process %d closing file\n", getpid());
    close(file_desc);

    exit(EXIT_SUCCESS);

}
```

运行结果

```assembly
└─$ ./lock3              
Process 1860 locking file
Process 1860 closing file
```

lock4.c

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>

const char *test_file = "/tmp/test_lock";

#define SIZE_TO_TRY 5

void show_lock_info(struct flock *to_show);

int main(){
    struct flock region_to_test;
    int res;

    int file_desc = open(test_file, O_RDWR | O_CREAT, 0666);
    if(!file_desc){
        fprintf(stderr, "Unable to open %s for read/write\n", test_file);
        exit(EXIT_FAILURE);
    }

    for(int start_byte=0; start_byte<99; start_byte++){
        region_to_test.l_type = F_RDLCK;
        region_to_test.l_whence = SEEK_SET;
        region_to_test.l_start = start_byte;
        region_to_test.l_len = SIZE_TO_TRY;
        region_to_test.l_pid = -1;

        printf("Testing F_RDLCK on region from %d to %d\n", start_byte, start_byte+SIZE_TO_TRY);

        res = fcntl(file_desc, F_GETLK, &region_to_test);
        if(res == -1){
            fprintf(stderr, "F_GETLK failed\n");
            exit(EXIT_FAILURE);
        }

        if(region_to_test.l_pid != -1){
            printf("Lock would failed. F_GETLK returned:\n");
            show_lock_info(&region_to_test);
        }else{
            printf("F_RDLCK - Lock would succeed\n");
        }
        
    }

    close(file_desc);
    exit(EXIT_SUCCESS);
}

void show_lock_info(struct flock *to_show){
    printf("\tl_type %d, ", to_show->l_type);
    printf("l_whence %d, ", to_show->l_whence);
    printf("l_start %d, ", (int)to_show->l_start);
    printf("l_len %d, ", (int)to_show->l_len);
    printf("l_pid %d\n", to_show->l_pid);
}
```

运行结果

```assembly
└─$ ./lock4
Testing F_RDLCK on region from 0 to 5
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 1 to 6
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 2 to 7
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 3 to 8
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 4 to 9
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 5 to 10
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 6 to 11
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 7 to 12
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 8 to 13
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 9 to 14
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 10 to 15
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 11 to 16
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 12 to 17
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 13 to 18
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 14 to 19
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 15 to 20
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 16 to 21
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 17 to 22
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 18 to 23
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 19 to 24
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 20 to 25
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 21 to 26
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 22 to 27
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 23 to 28
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 24 to 29
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 25 to 30
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 26 to 31
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 27 to 32
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 28 to 33
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 29 to 34
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 30 to 35
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 31 to 36
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 32 to 37
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 33 to 38
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 34 to 39
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 35 to 40
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 36 to 41
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 37 to 42
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 38 to 43
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 39 to 44
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 40 to 45
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 41 to 46
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 42 to 47
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 43 to 48
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 44 to 49
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 45 to 50
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 46 to 51
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 47 to 52
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 48 to 53
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 49 to 54
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 50 to 55
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 51 to 56
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 52 to 57
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 53 to 58
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 54 to 59
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 55 to 60
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 56 to 61
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 57 to 62
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 58 to 63
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 59 to 64
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 60 to 65
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 61 to 66
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 62 to 67
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 63 to 68
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 64 to 69
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 65 to 70
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 66 to 71
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 67 to 72
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 68 to 73
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 69 to 74
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 70 to 75
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 71 to 76
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 72 to 77
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 73 to 78
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 74 to 79
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 75 to 80
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 76 to 81
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 77 to 82
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 78 to 83
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 79 to 84
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 80 to 85
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 81 to 86
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 82 to 87
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 83 to 88
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 84 to 89
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 85 to 90
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 86 to 91
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 87 to 92
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 88 to 93
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 89 to 94
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 90 to 95
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 91 to 96
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 92 to 97
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 93 to 98
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 94 to 99
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 95 to 100
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 96 to 101
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 97 to 102
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 98 to 103
F_RDLCK - Lock would succeed
```

先运行lock3，再运行lock4

```assembly
└─$ ./lock4
Testing F_RDLCK on region from 0 to 5
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 1 to 6
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 2 to 7
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 3 to 8
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 4 to 9
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 5 to 10
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 6 to 11
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 7 to 12
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 8 to 13
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 9 to 14
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 10 to 15
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 11 to 16
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 12 to 17
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 13 to 18
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 14 to 19
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 15 to 20
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 16 to 21
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 17 to 22
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 18 to 23
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 19 to 24
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 20 to 25
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 21 to 26
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 22 to 27
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 23 to 28
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 24 to 29
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 25 to 30
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 26 to 31
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 27 to 32
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 28 to 33
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 29 to 34
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 30 to 35
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 31 to 36
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 32 to 37
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 33 to 38
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 34 to 39
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 35 to 40
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 36 to 41
Lock would failed. F_GETLK returned:
        l_type 1, l_whence 0, l_start 40, l_len 10, l_pid 2068
Testing F_RDLCK on region from 37 to 42
Lock would failed. F_GETLK returned:
        l_type 1, l_whence 0, l_start 40, l_len 10, l_pid 2068
Testing F_RDLCK on region from 38 to 43
Lock would failed. F_GETLK returned:
        l_type 1, l_whence 0, l_start 40, l_len 10, l_pid 2068
Testing F_RDLCK on region from 39 to 44
Lock would failed. F_GETLK returned:
        l_type 1, l_whence 0, l_start 40, l_len 10, l_pid 2068
Testing F_RDLCK on region from 40 to 45
Lock would failed. F_GETLK returned:
        l_type 1, l_whence 0, l_start 40, l_len 10, l_pid 2068
Testing F_RDLCK on region from 41 to 46
Lock would failed. F_GETLK returned:
        l_type 1, l_whence 0, l_start 40, l_len 10, l_pid 2068
Testing F_RDLCK on region from 42 to 47
Lock would failed. F_GETLK returned:
        l_type 1, l_whence 0, l_start 40, l_len 10, l_pid 2068
Testing F_RDLCK on region from 43 to 48
Lock would failed. F_GETLK returned:
        l_type 1, l_whence 0, l_start 40, l_len 10, l_pid 2068
Testing F_RDLCK on region from 44 to 49
Lock would failed. F_GETLK returned:
        l_type 1, l_whence 0, l_start 40, l_len 10, l_pid 2068
Testing F_RDLCK on region from 45 to 50
Lock would failed. F_GETLK returned:
        l_type 1, l_whence 0, l_start 40, l_len 10, l_pid 2068
Testing F_RDLCK on region from 46 to 51
Lock would failed. F_GETLK returned:
        l_type 1, l_whence 0, l_start 40, l_len 10, l_pid 2068
Testing F_RDLCK on region from 47 to 52
Lock would failed. F_GETLK returned:
        l_type 1, l_whence 0, l_start 40, l_len 10, l_pid 2068
Testing F_RDLCK on region from 48 to 53
Lock would failed. F_GETLK returned:
        l_type 1, l_whence 0, l_start 40, l_len 10, l_pid 2068
Testing F_RDLCK on region from 49 to 54
Lock would failed. F_GETLK returned:
        l_type 1, l_whence 0, l_start 40, l_len 10, l_pid 2068
Testing F_RDLCK on region from 50 to 55
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 51 to 56
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 52 to 57
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 53 to 58
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 54 to 59
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 55 to 60
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 56 to 61
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 57 to 62
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 58 to 63
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 59 to 64
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 60 to 65
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 61 to 66
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 62 to 67
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 63 to 68
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 64 to 69
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 65 to 70
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 66 to 71
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 67 to 72
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 68 to 73
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 69 to 74
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 70 to 75
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 71 to 76
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 72 to 77
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 73 to 78
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 74 to 79
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 75 to 80
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 76 to 81
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 77 to 82
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 78 to 83
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 79 to 84
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 80 to 85
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 81 to 86
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 82 to 87
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 83 to 88
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 84 to 89
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 85 to 90
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 86 to 91
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 87 to 92
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 88 to 93
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 89 to 94
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 90 to 95
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 91 to 96
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 92 to 97
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 93 to 98
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 94 to 99
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 95 to 100
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 96 to 101
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 97 to 102
F_RDLCK - Lock would succeed
Testing F_RDLCK on region from 98 to 103
F_RDLCK - Lock would succeed
```

lock5.c

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>

const char *test_file = "/tmp/test_lock";

int main(){
    struct flock region_to_lock;
    int res;

    int file_desc = open(test_file, O_RDWR | O_CREAT, 0666);
    if(!file_desc){
        fprintf(stderr, "Unable to open %s for read/write\n", test_file);
        exit(EXIT_FAILURE);
    }

    region_to_lock.l_type = F_RDLCK;
    region_to_lock.l_whence = SEEK_SET;
    region_to_lock.l_start = 10;
    region_to_lock.l_len = 5;
    printf("Process %d, trying F_RDLCK, region %d to %d\n", getpid(), (int)region_to_lock.l_start, (int)(region_to_lock.l_start+region_to_lock.l_len));

    res = fcntl(file_desc, F_SETLK, &region_to_lock);
    if(res == -1){
        printf("Process %d - failed to lock region\n", getpid());
    }else{
        printf("Process %d - obtained lock region\n", getpid());
    }

    region_to_lock.l_type = F_UNLCK;
    region_to_lock.l_whence = SEEK_SET;
    region_to_lock.l_start = 10;
    region_to_lock.l_len = 5;
    printf("Process %d, trying F_UNLCK, region %d to %d\n", getpid(), (int)region_to_lock.l_start, (int)(region_to_lock.l_start+region_to_lock.l_len));

    res = fcntl(file_desc, F_SETLK, &region_to_lock);
    if(res == -1){
        printf("Process %d - failed to unlock region\n", getpid());
    }else{
        printf("Process %d - unlock region\n", getpid());
    }

    region_to_lock.l_type = F_UNLCK;
    region_to_lock.l_whence = SEEK_SET;
    region_to_lock.l_start = 0;
    region_to_lock.l_len = 50;
    printf("Process %d, trying F_UNLCK, region %d to %d\n", getpid(), (int)region_to_lock.l_start, (int)(region_to_lock.l_start+region_to_lock.l_len));

    res = fcntl(file_desc, F_SETLK, &region_to_lock);
    if(res == -1){
        printf("Process %d - failed to unlock region\n", getpid());
    }else{
        printf("Process %d - unlock region\n", getpid());
    }

    region_to_lock.l_type = F_WRLCK;
    region_to_lock.l_whence = SEEK_SET;
    region_to_lock.l_start = 16;
    region_to_lock.l_len = 5;
    printf("Process %d, trying F_WRLCK, region %d to %d\n", getpid(), (int)region_to_lock.l_start, (int)(region_to_lock.l_start+region_to_lock.l_len));
    
    res = fcntl(file_desc, F_SETLK, &region_to_lock);
    if(res == -1){
        printf("Process %d - failed to lock region\n", getpid());
    }else{
        printf("Process %d - obtained lock on region\n", getpid());
    }

    region_to_lock.l_type = F_RDLCK;
    region_to_lock.l_whence = SEEK_SET;
    region_to_lock.l_start = 40;
    region_to_lock.l_len = 10;
    printf("Process %d, trying F_RDLCK, region %d to %d\n", getpid(), (int)region_to_lock.l_start, (int)(region_to_lock.l_start+region_to_lock.l_len));

    res = fcntl(file_desc, F_SETLK, &region_to_lock);
    if(res == -1){
        printf("Process %d - failed to lock region\n", getpid());
    }else{
        printf("Process %d - obtained lock on region\n", getpid());
    }

    region_to_lock.l_type = F_WRLCK;
    region_to_lock.l_whence = SEEK_SET;
    region_to_lock.l_start = 16;
    region_to_lock.l_len = 5;
    printf("Process %d, trying F_WRLCK, region %d to %d\n", getpid(), (int)region_to_lock.l_start, (int)(region_to_lock.l_start+region_to_lock.l_len));
    
    res = fcntl(file_desc, F_SETLK, &region_to_lock);
    if(res == -1){
        printf("Process %d - failed to lock region\n", getpid());
    }else{
        printf("Process %d - obtained lock on region\n", getpid());
    }
    
    printf("Process %d ending\n", getpid());
    close(file_desc);
    exit(EXIT_SUCCESS);
}
```

## ch08 inter-process communications

```assembly
#include <stdio.h>

FILE *popen(const char *command, const char *open_mode);
int pclose(FILE *stream_to_close);
```

#### popen1.c

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(){
    char buffer[BUFSIZ + 1];
    memset(buffer, '\0', sizeof(buffer));
    FILE *read_fp = popen("uname -a", "r");
    if(read_fp != NULL){
        int chars_read = fread(buffer, sizeof(char), BUFSIZ, read_fp);
        if(chars_read > 0){
            printf("Output was: -\n%s\n", buffer);
        }
        pclose(read_fp);
        exit(EXIT_SUCCESS);
    }
    exit(EXIT_FAILURE);

}
```

#### popen2.c

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(){
    char buffer[BUFSIZ + 1];

    sprintf(buffer, "Once upon a time, there was...\n");
    FILE *write_fp = popen("od -c", "w");
    if(write_fp != NULL){
        fwrite(buffer, sizeof(char), strlen(buffer), write_fp);
        pclose(write_fp);
        exit(EXIT_SUCCESS);
    }
    exit(EXIT_FAILURE);
}
```

运行结果

```assembly
└─$ ./popen2
0000000   O   n   c   e       u   p   o   n       a       t   i   m   e
0000020   ,       t   h   e   r   e       w   a   s   .   .   .  \n
0000037
```

### pipe

```assembly
#include <unistd.h>

int pipe(int file_descriptor[2]);
```

#### pipe1.c

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

int main(){
    int file_pipes[2];
    const char some_data[] = "123";
    char buffer[BUFSIZ + 1];

    memset(buffer, '\0', sizeof(buffer));

    if(pipe(file_pipes)==0){
        int data_processed = write(file_pipes[1], some_data, strlen(some_data));
        printf("Wrote %d bytes\n", data_processed);

        data_processed = read(file_pipes[0], buffer, BUFSIZ);
        printf("Read %d bytes: %s\n", data_processed, buffer);

        exit(EXIT_SUCCESS);
    }

    exit(EXIT_FAILURE);
}
```

#### pipe2.c

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(){
    int data_processed;
    int file_pipes[2];
    const char some_data[] = "123";
    char buffer[BUFSIZ + 1];

    memset(buffer, '\0', sizeof(buffer));

    if(pipe(file_pipes) == 0){
        pid_t fork_result = fork();
        
        if(fork_result == -1){
            fprintf(stderr, "Fork failure");
            exit(EXIT_FAILURE);
        }
        if(fork_result == 0){
            data_processed = read(file_pipes[0], buffer, BUFSIZ);
            printf("Read %d bytes: %s\n", data_processed, buffer);
            exit(EXIT_SUCCESS);
        }else{
            data_processed = write(file_pipes[1], some_data, strlen(some_data));
            printf("Wrote %d bytes\n", data_processed);
        }
    }

    exit(EXIT_SUCCESS);
}
```

只有把父子进程中的针对管道的写文件描述符都关闭，管道才会被认为是关闭了，对管道的read调用才会失败。

我们可以在命令行上创建命名管道，也可以在程序中创建它。

> mknod filename p
>
> mkfifo filename

```assembly
#include <sys/types.h>
#include <sys/stat.h>
	
int mkfifo(const char *filename, mode_t mode);
int mknod(const char *filename, mode_t mode | S_IFIFO, (dev_t) 0);
```

可以用mknod函数建立许多特殊类型的文件。要想通过这个函数创建一个命名管道，唯一具有可移植性的方法是使用一个dev_t类型的值0，并将文件访问模式与S_IFIFO按位或。

#### fifo1.c

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>

int main(){
    int res = mkfifo("/tmp/my_fifo", 0777);
    if(res == 0){
        printf("FIFO created\n");
    }
    exit(EXIT_SUCCESS);
}
```

输入重定向

```assembly
cat < /tmp/my_fifo
echo "adsasd" > /tmp/my_fifo
```

### open

```assembly
open(const char *path, O_RDONLY);
open(const char *path, O_RDONLY | O_NONBLOCK);
open(const char *path, O_WRONLY);
open(const char *path, O_WRONLY | O_NONBLOCK);
```

#### fifo2.c

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

#define FIFO_NAME "/tmp/my_fifo"

int main(int argc, char *argv[]){
    int res;
    int open_mode = 0;

    if(argc < 2){
        fprintf(stderr, "Usage: %s <some combination of O_RDONLY O_WRONLY O_NONBLOCK>\n", *argv);
        exit(EXIT_FAILURE);
    }

    argv++;
    if(strncmp(*argv, "O_RDONLY", 8) == 0){
        open_mode |= O_RDONLY;
    }
    if(strncmp(*argv, "O_WRONLY", 8) == 0){
        open_mode |= O_WRONLY;
    }
    if(strncmp(*argv, "O_NONBLOCK", 10) == 0){
        open_mode |= O_NONBLOCK;
    }

    argv++;
    if(*argv){
        if(strncmp(*argv, "O_RDONLY", 8) == 0){
            open_mode |= O_RDONLY;
        }
        if(strncmp(*argv, "O_WRONLY", 8) == 0){
            open_mode |= O_WRONLY;
        }
        if(strncmp(*argv, "O_NONBLOCK", 10) == 0){
            open_mode |= O_NONBLOCK;
        }
    }

    if(access(FIFO_NAME, F_OK) == -1){
        res == mkfifo(FIFO_NAME, 0777);
        if(res != 0){
            fprintf(stderr, "Could not create fifo %s\n", FIFO_NAME);
            exit(EXIT_FAILURE);
        }
    }

    printf("Process %d opening FIFO\n", getpid());
    res = open(FIFO_NAME, open_mode);
    printf("Process %d result %d\n", getpid(), res);
    sleep(5);
    if(res != -1){
        (void)close(res);
    }
    printf("Process %d finished\n", getpid());

    exit(EXIT_SUCCESS);
}
```

没有血缘关系的进程通过FIFO通信

#### fifo3.c生产者

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <limits.h>
#include <sys/types.h>
#include <sys/stat.h>

#define FIFO_NAME "/tmp/my_fifo"

#define BUFFER_SIZE PIPE_BUF
#define TEN_MEG (1024*1024*10)

int main(){
    int res;
    int open_mode = O_WRONLY;
    int bytes_sent = 0;
    char buffer_sent = 0;
    char buffer[BUFFER_SIZE + 1];

    if(access(FIFO_NAME, F_OK) == -1){
        res == mkfifo(FIFO_NAME, 0777);
        if(res != 0){
            fprintf(stderr, "Could not create fifo %s\n", FIFO_NAME);
            exit(EXIT_FAILURE);
        }
    }

    printf("Process %d opening FIFO O_WRONLY\n", getpid());
    int pipe_fd = open(FIFO_NAME, open_mode);
    printf("Proicess %d result %d\n", getpid(), pipe_fd);

    if(pipe_fd != -1){
        while(bytes_sent < TEN_MEG){
            res = write(pipe_fd, buffer, BUFFER_SIZE);
            if(res == -1){
                fprintf(stderr, "Write error on pipe\n");
                exit(EXIT_FAILURE);
            }
            bytes_sent += res;
        }
        (void)close(pipe_fd);
    }else {
        exit(EXIT_FAILURE);
    }

    printf("Process %d finished\n", getpid());
    exit(EXIT_SUCCESS);
}
```

#### fifo4.c消费者

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <limits.h>
#include <sys/types.h>
#include <sys/stat.h>

#define FIFO_NAME "/tmp/my_fifo"
#define BUFFER_SIZE PIPE_BUF

int main(){
    int res;
    int open_mode = O_RDONLY;
    int bytes_read = 0;
    char buffer[BUFFER_SIZE + 1];

    memset(buffer, '\0', sizeof(buffer));

    printf("Process %d opening FIFO O_WRONLY\n", getpid());
    int pipe_fd = open(FIFO_NAME, open_mode);
    printf("Proicess %d result %d\n", getpid(), pipe_fd);

    if(pipe_fd != -1){
        do{
            res = read(pipe_fd, buffer, BUFFER_SIZE);
            bytes_read += res;
        }while(res > 0);
        (void)close(pipe_fd);
    }else {
        exit(EXIT_FAILURE);
    }

    printf("Process %d finished, %d bytes read\n", getpid(), bytes_read);
    exit(EXIT_SUCCESS);
}
```

### 信号量

所有的Linux信号量函数都是针对成组的通用信号量进行操作而不是只针对一个二进制信号量。

```assembly
int semget(key_t key, int num_sems, int sem_flags);
int semop(int sem_id, struct sembuf *sem_ops, size_t num_sem_ops);
int semctl(int sem_id, int sem_num, int command, ...);
```

sembuf结构体

```
struct sembuf{
	short sem_num;
	short sem_op;
	short sem_flg;
}
```

最后一个成员sem_flg通常被设置为SEM_UNDO。它将使得操作系统跟踪当前进程对这个信号量得修改情况，如果这个进程在没有释放该信号量的情况下终止，操作系统将自动释放该进程持有得信号量。

Semop调用的一切动作都是一次性完成的，这是为了避免出现因使用多个信号量而可能发生的竞争条件。

#### sem1.c

```assembly
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>

#include "semun.h"

static int set_semvalue(void);
static void del_semvalue(void);
static int semaphore_p(void);
static int semaphore_v(void);

static int sem_id;

int main(int argc, char *argv[]){
    int i;
    int pause_time;
    char op_char = 'O';

    srand((unsigned int)getpid());
    sem_id = semget((key_t)1234, 1, 0666 | IPC_CREAT);

    if(argc > 1){
        if(!set_semvalue()){
            fprintf(stderr, "Failed to initialize semaphore\n");
            exit(EXIT_FAILURE);
        }
        op_char = 'X';
        sleep(2);
    }

    for(i=0; i<10; i++){
        if(!semaphore_p()){
            exit(EXIT_FAILURE);
        }
        printf("%c", op_char);
        fflush(stdout);

        pause_time = rand() % 3;
        sleep(pause_time);
        
        printf("%c", op_char);
        fflush(stdout);

        if(!semaphore_v()){
            exit(EXIT_FAILURE);
        }
        pause_time = rand() % 2;
        sleep(pause_time);
    }

    printf("\n%d - finished\n", getpid());

    if(argv > 1){
        sleep(10);
        del_semvalue();
    }

    exit(EXIT_SUCCESS);
}

static int set_semvalue(void){
    union semun sem_union;

    sem_union.val = 1;
    if(semctl(sem_id, 0, SETVAL, sem_union) == -1){
        return 0;
    }
    return 1;
}

static void del_semvalue(void){
    union semun sem_union;
    if(semctl(sem_id, 0, IPC_RMID, sem_union) == -1){
        fprintf(stderr, "Failed to delete semaphore\n");
    }
}

static int semaphore_p(void){
    struct sembuf sem_b;

    sem_b.sem_num = 0;
    sem_b.sem_op = -1;
    sem_b.sem_flg = SEM_UNDO;
    if(semop(sem_id, &sem_b, 1) == -1){
        fprintf(stderr, "semaphore_p failed\n");
        return 0;
    }

    return 1;
}

static int semaphore_v(void){
    struct sembuf sem_b;

    sem_b.sem_num = 0;
    sem_b.sem_op = 1;
    sem_b.sem_flg = SEM_UNDO;
    if(semop(sem_id, &sem_b, 1) == -1){
        fprintf(stderr, "semaphore_v failed\n");
        return 0;
    }
    return 1;
}
```

