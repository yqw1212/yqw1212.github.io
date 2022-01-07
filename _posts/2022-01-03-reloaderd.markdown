---
layout: post
title:  Reloadered[FlareOn6]
date:   2022-01-03 00:08:01 +0300
image:  2022-01-03-river.jpg
tags:   [ctf,reverse,FlareOn]
---

ida打开查看sub_FFFF10D0函数

```assembly
int sub_FFFF10D0()
{
  char *v0; // ecx
  int v1; // eax
  unsigned int v2; // esi
  unsigned int i; // edi
  unsigned int v4; // eax
  unsigned int v5; // eax
  int result; // eax
  char Str[256]; // [esp+0h] [ebp-104h] BYREF

  v0 = sub_FFFF1060(0x21u);
  v1 = 0;
  if ( !*v0 )
    goto LABEL_24;
  do
    ++v1;
  while ( v0[v1] );
  if ( v1 == 0xB
    && ((unsigned __int8)v0[1] ^ 0x31) == 0x5E
    && (v0[2] & 0xFFFFFFF) == 0x54
    && v0[0xA] == 0x47
    && v0[7] == 0x52
    && ((unsigned __int8)v0[3] ^ (unsigned __int8)v0[4]) == 0x41
    && (unsigned int)(3 * *v0 - 0xF6) < 2
    && (unsigned int)(0xC800 * v0[8] - 0x520800) < 3
    && v0[6] == 0x65
    && (v0[5] & 1) == 0
    && v0[9] == 0x6E )
  {
    v2 = 0;
    do
      ++v2;
    while ( v0[v2] );
    for ( i = 0; i < 0x25; ++i )
    {
      Str[i] = byte_FFFF3108[i] ^ v0[i % v2];
      v4 = i;
    }
    Str[v4] = 0;
    v5 = v4 + 1;
    if ( v5 == 0x100 )
    {
      result = sub_FFFF16A0("\nERROR: Invalid decryption length!\n", Str[0]);
    }
    else if ( v5 >= 0x100 )
    {
      __report_rangecheckfailure();
      result = sub_FFFF1290();
    }
    else
    {
      Str[v5] = 0;
      if ( strstr(Str, ".com") )
        result = sub_FFFF16A0("Here is your prize:\n\n\t%s\n", (char)Str);
      else
        result = sub_FFFF16A0("\nERROR: Decryption failed! Wrong key?\n", Str[0]);
    }
  }
  else
  {
LABEL_24:
    sub_FFFF16A0("\nERROR: Wrong key!\n", Str[0]);
    result = sub_FFFF1000(byte_FFFF3108, 0x25u);
  }
  return result;
}
```

设法找到符合if判断的字符串

> RoT3rHeRinG

但是给了一个假的flag

```assembly
data = [0x1C, 0x5C, 0x22, 0x00, 0x00, 0x17, 0x02, 0x62, 0x07, 0x00, 
  0x06, 0x0D, 0x08, 0x75, 0x45, 0x17, 0x17, 0x3C, 0x3D, 0x1C, 
  0x31, 0x32, 0x02, 0x2F, 0x12, 0x72, 0x39, 0x0D, 0x23, 0x1E, 
  0x28, 0x29, 0x69, 0x31, 0x00, 0x39]

key = "RoT3rHeRinG"

for i in range(len(data)):
    data[i] ^= ord(key[i%len(key)])

print("".join(chr(i) for i in data))
```

N3v3r_g0nnA_g!ve_You_uP@FAKEFLAG.com

所以可知程序正常情况应该不期望运行到此，而且main函数中的sub_FFFF1290函数的内容在运行时没有输出

```assembly
.text:FFFF1290 sub_FFFF1290    proc near               ; CODE XREF: _main↓p
.text:FFFF1290                 push    offset asc_FFFF31C0 ; "\n\n\n+--------------------------------"...
.text:FFFF1295                 call    sub_FFFF16A0
.text:FFFF129A                 push    offset asc_FFFF31FC ; "|                                      "...
.text:FFFF129F                 call    sub_FFFF16A0
.text:FFFF12A4                 push    offset aReloaderd ; "|                     ReLoaDerd        "...
.text:FFFF12A9                 call    sub_FFFF16A0
.text:FFFF12AE                 push    offset asc_FFFF31FC ; "|                                      "...
.text:FFFF12B3                 call    sub_FFFF16A0
.text:FFFF12B8                 push    offset asc_FFFF326C ; "+--------------------------------------"...
.text:FFFF12BD                 call    sub_FFFF16A0
.text:FFFF12C2                 add     esp, 14h
.text:FFFF12C5                 retn
.text:FFFF12C5 sub_FFFF1290    endp
```

ida动调程序，检查执行流程

```assembly
+---------------------------------------------------+
|                                                   |
|                     ReLoaDerd                     |
|                                                   |
+---------------------------------------------------+


Enter key: RoT3rHeRinG
Here is your prize:

        N3v3r_g0nnA_g!ve_You_uP@FAKEFLAG.com

```

可以知道程序存在反调试，使用ollydbg调试，因为程序中有许多nop指令，怀疑是在程序初始使对该部分进行填充，所以断点不要下在main函数处，下在__scrt_common_main_seh中 

定位代码位置

可以看到有一个call esi指令

![]({{site.baseurl}}/img/2022-01-03-esi.jpg)

单步调试，当程序执行到call esi时，可以看到程序跳转到了0x112D0，即原来的nop处

我们可以在ollydbg中将填充好的代码dump出来，方便我们静态分析（右键→backup→backup to file）

将dump出的文件用ida打开，发现原来nop处的位置有了代码，而且可以F5反编译

```assembly
int __usercall sub_FFFF1ED0@<eax>(int a1@<ebx>, int a2@<edi>, int a3@<esi>)
{
  unsigned __int64 v3; // rax
  unsigned __int64 v4; // kr08_8
  unsigned int v6; // esi
  int v21; // esi
  unsigned __int64 v22; // kr10_8
  unsigned __int64 v23; // kr18_8
  bool v24; // zf
  __int64 v25; // rax
  int v26; // esi
  unsigned int v27; // edx
  int v28; // eax
  unsigned int i; // ecx
  unsigned int j; // esi
  _BYTE *v32; // esi
  int v33; // eax
  int v34; // eax
  int v35; // eax
  unsigned int v36; // edi
  unsigned int k; // ecx
  unsigned int v38; // eax
  unsigned int v39; // eax
  int v40; // eax
  int v41; // [esp-10h] [ebp-1C4h]
  int v44; // [esp-4h] [ebp-1B8h]
  unsigned int v45; // [esp+8h] [ebp-1ACh]
  int v46; // [esp+Ch] [ebp-1A8h]
  unsigned int v47; // [esp+Ch] [ebp-1A8h]
  int v48; // [esp+10h] [ebp-1A4h]
  unsigned int v49; // [esp+14h] [ebp-1A0h]
  unsigned int v50; // [esp+18h] [ebp-19Ch]
  __int64 v51; // [esp+1Ch] [ebp-198h]
  unsigned int v52; // [esp+24h] [ebp-190h]
  int v53; // [esp+28h] [ebp-18Ch]
  int v54; // [esp+2Ch] [ebp-188h]
  unsigned int v55; // [esp+30h] [ebp-184h]
  int v56; // [esp+34h] [ebp-180h]
  int v57; // [esp+38h] [ebp-17Ch]
  int v58; // [esp+3Ch] [ebp-178h]
  _DWORD v59[9]; // [esp+40h] [ebp-174h]
  __int128 v60; // [esp+64h] [ebp-150h]
  __int128 v61; // [esp+74h] [ebp-140h]
  _DWORD v62[4]; // [esp+84h] [ebp-130h] BYREF
  int v63; // [esp+94h] [ebp-120h]
  char v64; // [esp+98h] [ebp-11Ch]

  v44 = a1;
  v60 = MEMORY[0x132A8];
  v63 = MEMORY[0x132D8];
  v61 = MEMORY[0x132B8];
  v64 = MEMORY[0x132DC];
  v53 = 0;
  *(_OWORD *)v62 = MEMORY[0x132C8];
  do
  {
    v46 = 0x3E8;
    HIDWORD(v51) = 0;
    v49 = 0;
    v3 = __rdtsc();
    v50 = 0;
    do
    {
      v4 = v3;
      v3 = __rdtsc();
      v49 = (v3 - v4 + __PAIR64__(v49, v50)) >> 0x20;
      v50 += v3 - v4;
      --v46;
    }
    while ( v46 );
    v48 = 0x3E8;
    v51 = 0i64;
    _RAX = __rdtsc();
    v52 = 0;
    v6 = _RAX;
    v47 = (unsigned __int8)v51;
    while ( 1 )
    {
      LODWORD(_RAX) = 1;
      LODWORD(v51) = HIDWORD(_RAX);
      v55 = v6;
      v41 = a1;
      __asm { cpuid }
      _EAX = 2;
      __asm { cpuid }
      _EAX = 3;
      __asm { cpuid }
      v21 = _EBX;
      a1 = v41;
      v56 = _EAX;
      v57 = v21;
      v58 = _ECX;
      v59[0] = _EDX;
      v22 = __rdtsc();
      v54 = HIDWORD(v22);
      v6 = v22;
      v23 = v22 - __PAIR64__(v51, v55) + __PAIR64__(v52, v47);
      v47 += v22 - v55;
      v24 = v48-- == 1;
      v52 = HIDWORD(v23);
      if ( v24 )
        break;
      HIDWORD(_RAX) = v54;
    }
    v25 = ((__int64 (__cdecl *)(_DWORD, _DWORD, int, _DWORD, int, int, int))dword_FFFF2F90[0])(
            v23,
            HIDWORD(v23),
            0x3E8,
            0,
            a2,
            a3,
            v44);
    if ( v25 - ((__int64 (__cdecl *)(unsigned int))dword_FFFF2F90[0])(v45) > 0x1B58 || v49 == 0x12345678 )
      return sub_FFFF1C00(0x112D0, 0x3A5);
    ++v45;
  }
  while ( v45 < 0x3E8 );
  v26 = MEMORY[0x13004]();
  HIDWORD(v51) = 0x620;
  v52 = 0x91A;
  v27 = 0;
  v53 = 0xAAC;
  v54 = 0xAAE;
  v55 = 0xC0F;
  v56 = 0xE05;
  v57 = 0xE66;
  v58 = 0xFED;
  do
  {
    if ( *(unsigned __int8 *)(v27 + v26 + 0x11000) == (((unsigned __int8)(v27 + 0x42) - v27) ^ 0x8E) )
    {
      v28 = 0;
      while ( v27 != *((_DWORD *)&v51 + v28 + 1) )
      {
        if ( (unsigned int)++v28 >= 8 )
          return sub_FFFF1C00(0x112D0, 0x3A5);
      }
    }
    ++v27;
  }
  while ( v27 < 0x13CA );
  if ( NtCurrentPeb()->BeingDebugged )
    return sub_FFFF1C00(0x112D0, 0x3A5);
  for ( i = 0; i < 0x539; ++i )
  {
    for ( j = 0; j < 0x34; ++j )
    {
      if ( !(i % 3) || !(i % 7) )
        *((_BYTE *)v59 + j) ^= i;
    }
  }
  v32 = (_BYTE *)MEMORY[0x13050]();
  sub_FFFF22A0(0x13130, 0xE);
  v33 = MEMORY[0x130C0](0);
  MEMORY[0x130B8](v32, 0xE, v33);
  v32[0xD] = 0;
  v34 = 0;
  if ( *v32 )
  {
    do
      ++v34;
    while ( v32[v34] );
  }
  if ( v32[v34 - 1] == 0xA )
  {
    v35 = 0;
    if ( *v32 )
    {
      do
        ++v35;
      while ( v32[v35] );
    }
    v32[v35 - 1] = 0;
  }
  v36 = 0;
  if ( *v32 )
  {
    do
      ++v36;
    while ( v32[v36] );
  }
  for ( k = 0; k < 0x35; ++k )
  {
    *((_BYTE *)&v62[1] + k) = *((_BYTE *)v59 + k) ^ v32[k % v36];
    v38 = k;
  }
  *((_BYTE *)&v62[1] + v38) = 0;
  v39 = v38 + 1;
  if ( v39 < 0x100 )
  {
    *((_BYTE *)&v62[1] + v39) = 0;
    if ( !MEMORY[0x1303C](&v62[1], 0x132E0) )
    {
      sub_FFFF22A0(0x1313C, 0);
      MEMORY[0x130A4](0);
    }
    sub_FFFF22A0(0x131A4, (char)v62);
    MEMORY[0x130A4](0);
  }
  v40 = sub_FFFF240A();
  sub_FFFF1E90(v40);
  return sub_FFFF1CD0();
}
```

隐藏函数由四部分组成:反虚拟机代码、反调试代码、解密隐藏的秘密，和密码的测试。首先运行的是反虚拟机代码。它使用基于时间的方法检测虚拟机的存在。特别是代码将首先计算两次调用rdtsc之间传递的平均周期

```assembly
for (i = 0; i < 1000; i++) {
	last = cur;
	cur = __rdtsc();
	avg += (cur - last);
}
```

接下来，如果在对rdtsc的调用之间调用了cpuid，代码将计算经过的平均周期，如图4所示。由于cpuid是一个经常被虚拟机监控程序捕获的指令，因此第二次计算的平均时间很可能比第一次在虚拟机存在时的计算要高得多。如果平均值之间的差足够大(超过7000个周期)，代码就假定它在虚拟机中运行。

在这种情况下，代码将调用一个辅助函数(0x11000)，该函数用nop覆盖隐藏的秘密和隐藏的函数，并继续程序的正常执行。

```assembly
for (i = 0; i < 1000; i++) {
	last = cur;
	__cpuid(cpuid_result, 1);
	__cpuid(cpuid_result, 2);
	__cpuid(cpuid_result, 3);
	cur = __rdtsc();
	avg2 += (cur - last);
}
```

在反虚拟机检查之后，请执行两个反调试检查。首先，该函数搜索文本部分中包含的所有0xCC字节，以便检测断点。如果找到任何0xCC字节，函数会将其与白名单进行比较。如果文本部分中的0xCC字节不属于白名单的一部分，则该函数假定存在一个调试器，并且检查失败。

此外，该函数还检查进程PEB中正在调试的字节的值。如果设置了字节，则函数假定存在调试器，并且检查失败。如果两个反调试检查中有一个失败，二进制文件将使用上述方法从内存中删除自己。

一旦anti-vm和anti-debug检查成功，隐藏函数就会对隐藏的秘密进行解码。隐藏的秘密被存储在一个本地堆栈变量中，并被多次XOR编码。

静态解码循环删除除最后一个外的所有XOR编码。循环如图5所示。静态解码循环本质上是单字节XOR，它使用0到1337之间的所有数字来解码隐藏的秘密，这些数字要么为0，要么能被3或7整除。

```assembly
for (i = 0; i < 1337; i++) {
    for (j = 0; j < 52; j++) {
        if (i % 3 == 0 || i % 7 == 0) {
        	hidden_secret[j] = (hidden_secret[j] ^ i) & 0xff
        }
    }
}
```

可以发现dump出的文件的偏移与ollydbg中的偏移不一样，为了方便分析记录一下：

* ollydbg：12D0

* ida：1ED0

为了获得加密后的flag，我们需要定位到对应的内存。首先执行到隐藏函数的开始0x112d0

![]({{site.baseurl}}/img/2022-01-03-112d0.jpg)

接下来执行程序到0x11334的反调试函数之前

跳过该反调试函数，跳转到0x11533，然后执行这部分隐藏代码中的获取输入

![]({{site.baseurl}}/img/2022-01-03-real.jpg)

在ida中找到对密文的操作，定位0x35，在0x2207。最后设置断点到0x115f0，运行，即可在栈中得到加密后的数据

![]({{site.baseurl}}/img/2022-01-03-data.jpg)

```assembly
7A 17 08 34 17 31 3B 25 5B 18 2E 3A 15 56 0E 11
3E 0D 11 3B 24 21 31 06 3C 26 7C 3C 0D 24 16 3A
7E 93 07 49 EB 10 FB B3 C0 C1 C1 C1 AE C0 20 3E
40 08 0A 14 
```

将输入作为密钥，异或解密一段密文，其中一部分是@flare-on.com，那么我们通过这部分已知明文可以先算出密钥

```assembly
data = [0x7A, 0x17, 0x08, 0x34, 0x17, 0x31, 0x3B, 0x25, 0x5B, 0x18, 0x2E, 0x3A, 0x15, 0x56, 0x0E, 0x11,
0x3E, 0x0D, 0x11, 0x3B, 0x24, 0x21, 0x31, 0x06, 0x3C, 0x26, 0x7C, 0x3C, 0x0D, 0x24, 0x16, 0x3A,
0x7E, 0x93, 0x07, 0x49, 0xEB, 0x10, 0xFB, 0xB3, 0xC0, 0xC1, 0xC1, 0xC1, 0xAE, 0xC0, 0x20, 0x3E,
0x40, 0x08, 0x0A, 0x14]

c=[0x73,0x2E,0x09,0x00,0x16,0x00,0x49,0x22,0x01,0x40,0x08,0x0A,0x14] 
f="@flare-on.com"
for i in range(len(c)):
    print(chr(c[i]^ord(f[i])),end="")
```

3HeadedMonkey

输入程序得到flag

I_mUsT_h4vE_leFt_it_iN_mY_OthEr_p4nTs?!@flare-on.com