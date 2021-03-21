---
layout: post
title:  very_success(FlareOn2)
date:   2021-03-21 00:01:01 +0300
image:  2021-03-21-street.jpg
tags:   [ctf,reverse,FlareOn]
---

这道题网上的wp不是很详细，所以来写一下。

ida打开只有三个函数

sub_401000

```assembly
BOOL __usercall sub_401000@<eax>(int a1@<ebp>)
{
  HANDLE v1; // ST1C_4
  BOOL result; // eax
  HANDLE v3; // [esp-Ch] [ebp-Ch]
  signed int v4; // [esp-8h] [ebp-8h]
  int v5; // [esp-4h] [ebp-4h]
  int retaddr; // [esp+0h] [ebp+0h]

  v5 = a1;
  v1 = GetStdHandle(0xFFFFFFF6);
  v3 = GetStdHandle(0xFFFFFFF5);
  WriteFile(v3, aYouCrushedThat, 0x43u, (LPDWORD)&v4, 0);
  ReadFile(v1, &unk_402159, 0x32u, (LPDWORD)&v4, 0);
  if ( sub_401084((int)&v4, retaddr, (char *)&unk_402159, v4) )
    result = WriteFile(v3, aYouAreSuccess, 0x11u, (LPDWORD)&v4, 0);
  else
    result = WriteFile(v3, aYouAreFailure, 0x11u, (LPDWORD)&v4, 0);
  return result;
}
```

sub_401084

```assembly
int __usercall sub_401084@<eax>(int result@<eax>, int a2, char *a3, signed int a4)
{
  __int16 v4; // bx
  signed int v5; // ecx
  char *v6; // esi
  _BYTE *v7; // edi
  char v8; // al
  unsigned int v9; // et0
  char v10; // cf
  __int16 v11; // ax
  bool v12; // zf
  int v13; // edi
  int v14; // [esp+0h] [ebp-Ch]

  v4 = 0;
  v5 = 37;
  if ( a4 >= 37 )
  {
    v6 = a3;
    v7 = (_BYTE *)(a2 + 36);
    while ( 1 )
    {
      LOWORD(result) = 455;
      v14 = result;
      v8 = *v6++;
      v9 = __readeflags();
      __writeeflags(v9);
      v11 = (unsigned __int8)(__ROL1__(1, v4 & 3) + v10 + (v14 ^ v8));
      v4 += v11;
      v12 = *v7 == (_BYTE)v11;
      v13 = (int)(v7 + 1);
      if ( !v12 )
        LOWORD(v5) = 0;
      result = v14;
      if ( !v5 )
        break;
      v7 = (_BYTE *)(v13 - 2);
      if ( !--v5 )
        return result;
    }
  }
  return 0;
}
```

在ida中，这个函数其实有些冗余的代码，为了更直观的分析，先把它简化一下。

```assembly
int __usercall sub_401084@<eax>(int result@<eax>, int a2, char *a3, signed int a4)
{
  __int16 v4; // bx
  signed int v5; // ecx
  _BYTE *v7; // edi
  char v8; // al
  char v10; // cf
  __int16 v11; // ax

  v4 = 0;
  v5 = 37;
  if ( a4 >= 37 )
  {
    v7 = (_BYTE *)(a2 + 36);
    while ( 1 )
    {
      v8 = *a3++;

      v11 = (1 << v4 & 3) + v10 + (455 ^ v8));
      v4 += v11;
    
      if ( *v7 != (_BYTE)v11 )
        v5 = 0;
      result = 455;
      if ( !v5 ) // v5 != 0
        break;
      v7 = (_BYTE *)(v7 - 1);
      if ( !--v5 )
        return result;  // true result != 0
    }
  }
  return 0;
}
```

v8来自a3，通过调试可以知道是我们输入的字符串，计算得到v11的值，与v7作比较。v7来自a2，从地址a2+36处开始递减。查看调用sub_401084函数的sub_401000函数传入的参数，sub_401084((int)&v4, retaddr, (char *)&unk_402159, v4)，a2对应的是retaddr，但是我们不知道这个的值。

用ghidra打开文件，查看此函数的调用。

```assembly
iVar1 = FUN_00401084(unaff_retaddr,&DAT_00402159,local_4);
```

查看汇编代码

```assembly
00401054 ff  75  fc       PUSH      dword ptr [EBP  + local_4 ]
00401057 68  59  21       PUSH      DAT_00402159
         40  00
0040105c ff  75  f0       PUSH      dword ptr [EBP  + local_10 ]
0040105f e8  20  00       CALL      FUN_00401084
         00  00

```

我们要的值就是[EBP  + local_4 ]，对于这个变量，ghidra给了提示。

```assembly
//
// .text 
// ram: 00401000-004011ff
//
***************************FUNCTION******************************
undefined  __stdcall  FUN_00401000 (void )
undefined         AL:1           <RETURN>
undefined4        Stack[-0x4]:4  local_4            XREF[4]:     00401022 (*) ,                                                                  00401038 (*) ,                                                                  0040104e (*) ,                                                                  00401054 (R)   
undefined4        Stack[-0x8]:4  local_8            XREF[3]:     0040101d (W) , 
                                                                 0040102d (R) , 
                                                                 00401077 (R)   undefined4        Stack[-0xc]:4  local_c            XREF[2]:     00401012 (W) , 
                                                                 00401043 (R)   
undefined4        Stack[-0x10]   local_10           XREF[2]:     00401007 (W) , 
                                                                 0040105c (R)   
```

查找Stack[-0x4]，得到数据。

```assembly
                             *************************************************************
                             *                           FUNCTION                         
                             *************************************************************
undefined  entry ()
undefined         AL:1           <RETURN>
undefined1        Stack[-0x4]:1  local_4
                  entry                   XREF[2]: Entry Point (*), 00400068 (*)   
004010df e8  1c  ff       CALL       FUN_00401000   undefined FUN_00401000(void)
         ff  ff
004010e4 af              SCASD      ES :EDI
004010e5 aa              STOSB      ES :EDI
004010e6 ad              LODSD      ESI
004010e7 eb  ae           JMP        LAB_00401097
004010e9 aa              ??         AAh
004010ea ec              ??         ECh
004010eb a4              ??         A4h
004010ec ba              ??         BAh
004010ed af              ??         AFh
004010ee ae              ??         AEh
004010ef aa              ??         AAh
004010f0 8a              ??         8Ah
004010f1 c0              ??         C0h
004010f2 a7              ??         A7h
004010f3 b0              ??         B0h
004010f4 bc              ??         BCh
004010f5 9a              ??         9Ah
004010f6 ba              ??         BAh
004010f7 a5              ??         A5h
004010f8 a5              ??         A5h
004010f9 ba              ??         BAh
004010fa af              ??         AFh
004010fb b8              ??         B8h
004010fc 9d              ??         9Dh
004010fd b8              ??         B8h
004010fe f9              ??         F9h
004010ff ae              ??         AEh
00401100 9d              ??         9Dh
00401101 ab              ??         ABh
00401102 b4              ??         B4h
00401103 bc              ??         BCh
00401104 b6              ??         B6h
00401105 b3              ??         B3h
00401106 90              ??         90h
00401107 9a              ??         9Ah
00401108 a8              ??         A8h
```

编写C语言脚本

```assembly
#include <stdio.h>

int main(){
    int v7[37] = {0xa8,0x9a,0x90,0xb3,0xb6,0xbc,0xb4,0xab,0x9d,0xae,
                  0xf9,0xb8,0x9d,0xb8,0xaf,0xba,0xa5,0xa5,0xba,0x9a,
                  0xbc,0xb0,0xa7,0xc0,0x8a,0xaa,0xae,0xaf,0xba,0xa4,
                  0xec,0xaa,0xae,0xeb,0xad,0xaa,0xaf};
    int v10 = 1, v4 = 0;
    for(int i=0;i<37;i++){
        int v8 = (v7[i] - v10 - (1 << (v4 & 3))%256)%256 ^ 455;
        v4 += v7[i];
        printf("%c", v8);
    }
    return 0;
}
```

得到flag

`flag{a_Little_b1t_harder_plez@flare-on.com}`