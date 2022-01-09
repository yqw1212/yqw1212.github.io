---
layout: post
title:  greek_to_me[FlareOn6]
date:   2022-01-09 00:08:01 +0300
image:  2022-01-09-star.jpg
tags:   [ctf,reverse,FlareOn]
---

关键函数

```assembly
int __usercall sub_401008@<eax>(int _EDI@<edi>, _DWORD *a2@<esi>)
{
  _BYTE *v2; // eax
  char v3; // dl
  bool v5; // cf
  unsigned int v6; // ett
  int v7; // edx
  int v9; // [esp-4h] [ebp-1Ch]
  char buf[4]; // [esp+10h] [ebp-8h] BYREF
  SOCKET s; // [esp+14h] [ebp-4h]
  int savedregs; // [esp+18h] [ebp+0h] BYREF

  s = sub_401121(buf);
  if ( !s )
    return 0;
  v2 = &loc_40107C;
  v3 = buf[0];
  do
  {
    *v2 = (v3 ^ *v2) + 0x22;
    ++v2;
  }
  while ( (int)v2 < (int)&loc_40107C + 0x79 );
  if ( (unsigned __int16)sub_4011E6(&loc_40107C, 0x79) == 0xFB5E )
  {
    _EBX = *(_DWORD *)(v9 + 0x16810611);
    __asm { lock xor bl, [edi+61791C4h] }
    v5 = __CFADD__(*(_DWORD *)(8 * (_DWORD)a2 + 0xFB5E), 0xF1158106);
    *(_DWORD *)(8 * (_DWORD)a2 + 0xFB5E) -= 0xEEA7EFA;
    if ( v9 == 1 )
    {
      v6 = v5 + 0x198106F2;
      v5 = MEMORY[0xFB5E] < v6;
      MEMORY[0xFB5E] -= v6;
    }
    __asm { icebp }
    *a2 -= v5 + 0x1F99C4F0;
    v7 = *(_DWORD *)(v9 - 1 + 0x1D81061C);
    __outbyte(6u, 0x5Eu);
    *(_DWORD *)(v7 - 0x11) &= 0xF2638106;
    MEMORY[0xFB41] &= 0x66199C4u;
    a2[0xFFFFFFEF] &= 0xE6678106;
    *(_DWORD *)(8 * (_DWORD)&savedregs + 0xFB5E + 6) &= 0x69D6581u;
    *(_DWORD *)(v7 - 0xE) -= 0x66B99C4;
    MEMORY[0xFB07] += 0x10967EFA;
    *(_DWORD *)((char *)a2 + 0xFFFFFFEE) += 0x51907EFA;
    *(_DWORD *)(_EBX + 6) -= 0x6EF6D81;
    *(_DWORD *)(v7 - 0x17) ^= 0x7C738106u;
    send(s, "Congratulations! But wait, where's my flag?", 0x2B, 0);
  }
  else
  {
    send(s, "Nope, that's not it.", 0x14, 0);
  }
  closesocket(s);
  return WSACleanup();
}
```

sub_401121

```assembly
SOCKET __cdecl sub_401121(char *buf)
{
  SOCKET v2; // esi
  SOCKET v3; // eax
  SOCKET v4; // edi
  struct WSAData WSAData; // [esp+0h] [ebp-1A0h] BYREF
  struct sockaddr name; // [esp+190h] [ebp-10h] BYREF

  if ( WSAStartup(0x202u, &WSAData) )
    return 0;
  v2 = socket(2, 1, 6);
  if ( v2 != 0xFFFFFFFF )
  {
    name.sa_family = 2;
    *(_DWORD *)&name.sa_data[2] = inet_addr("127.0.0.1");
    *(_WORD *)name.sa_data = htons(0x8AEu);
    if ( bind(v2, &name, 0x10) != 0xFFFFFFFF && listen(v2, 0x7FFFFFFF) != 0xFFFFFFFF )
    {
      v3 = accept(v2, 0, 0);
      v4 = v3;
      if ( v3 != 0xFFFFFFFF )
      {
        if ( recv(v3, buf, 4, 0) > 0 )
          return v4;
        closesocket(v4);
      }
    }
    closesocket(v2);
  }
  WSACleanup();
  return 0;
}
```

监听了本地端口2222(0x8AE)，接收到的内容存入buf，然后与另一个变量做异或。由于不知道值是多少，爆破

```assembly
import sys
import os
import socket

ip = '127.0.0.1'
port = 2222
for i in range(255):
    os.startfile("D:\\文档\\CTF\\buuoj\\逆向\\[FlareOn4]greek_to_me\\greek_to_me.exe")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(i.to_bytes(1, "big"))
    data = s.recv(1024)
    s.close()
    print(data)
    if 'Congratulations' in str(data, encoding="utf-8"):
        print("%x" % i)
        break
```

> b"Congratulations! But wait, where's my flag?"
> a2

动调，下断点在0x00401063的位置

发送该数据

```assembly
ip = '127.0.0.1'
port = 2222
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
s.send(chr(0xa2))
s.close()
```

到断点断下，跳到40107c处发现ida未识别为代码

![]({{site.baseurl}}/img/2022-01-09-40107c.jpg)

按C强制分析

```assembly
.text:0040107C mov     bl, 65h ; 'e'
.text:0040107E mov     [ebp+var_2B], bl
.text:00401081 mov     [ebp+var_2A], 74h ; 't'
.text:00401085 mov     dl, 5Fh ; '_'
.text:00401087 mov     [ebp+var_29], dl
.text:0040108A mov     [ebp+var_28], 74h ; 't'
.text:0040108E mov     [ebp+var_27], 75h ; 'u'
.text:00401092 mov     [ebp+var_26], dl
.text:00401095 mov     [ebp+var_25], 62h ; 'b'
.text:00401099 mov     [ebp+var_24], 72h ; 'r'
.text:0040109D mov     [ebp+var_23], 75h ; 'u'
.text:004010A1 mov     [ebp+var_22], 74h ; 't'
.text:004010A5 mov     [ebp+var_21], bl
.text:004010A8 mov     [ebp+var_20], dl
.text:004010AB mov     [ebp+var_1F], 66h ; 'f'
.text:004010AF mov     [ebp+var_1E], 6Fh ; 'o'
.text:004010B3 mov     [ebp+var_1D], 72h ; 'r'
.text:004010B7 mov     [ebp+var_1C], 63h ; 'c'
.text:004010BB mov     [ebp+var_1B], bl
.text:004010BE mov     [ebp+var_1A], 40h ; '@'
.text:004010C2 mov     [ebp+var_19], 66h ; 'f'
.text:004010C6 mov     [ebp+var_18], 6Ch ; 'l'
.text:004010CA mov     [ebp+var_17], 61h ; 'a'
.text:004010CE mov     [ebp+var_16], 72h ; 'r'
.text:004010D2 mov     [ebp+var_15], bl
.text:004010D5 mov     [ebp+var_14], 2Dh ; '-'
.text:004010D9 mov     [ebp+var_13], 6Fh ; 'o'
.text:004010DD mov     [ebp+var_12], 6Eh ; 'n'
.text:004010E1 mov     [ebp+var_11], 2Eh ; '.'
.text:004010E5 mov     [ebp+var_10], 63h ; 'c'
.text:004010E9 mov     [ebp+var_F], 6Fh ; 'o'
.text:004010ED mov     [ebp+var_E], 6Dh ; 'm'
```

查看dl，bl寄存器的值，得到flag

et_tu_brute_force@flare-on.com

