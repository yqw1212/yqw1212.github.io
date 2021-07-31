---
layout: post
title:  beginner_reverse
date:   2021-06-18 00:01:01 +0300
image:  2021-06-18-music.jpg
tags:   [ctf,reverse,Insomni'hackTeaser2019,rust]
---

beginer_reverse::main

```assembly
__int64 beginer_reverse::main::h80fa15281f646bc1()
{
  __int64 v0; // rax
  unsigned __int64 v1; // rsi
  __int64 v2; // rdx
  __int64 v3; // r13
  __int64 v4; // rax
  __int64 v5; // rcx
  __int64 v6; // r8
  char v7; // si
  char v8; // di
  int v9; // ebp
  int v10; // esi
  int v11; // edi
  __int64 v12; // rcx
  __int64 v13; // r14
  __int64 v14; // rdi
  volatile signed __int64 **v15; // rbp
  int v16; // er12
  unsigned __int64 v17; // rbx
  __int64 result; // rax
  __int64 v19; // rcx
  __int64 v20; // r15
  __int64 v21; // rcx
  bool v22; // zf
  volatile signed __int64 *v23; // [rsp+0h] [rbp-B8h] BYREF
  __int64 v24; // [rsp+8h] [rbp-B0h] BYREF
  __int128 v25; // [rsp+10h] [rbp-A8h]
  _BYTE v26[24]; // [rsp+20h] [rbp-98h] BYREF
  __int64 v27; // [rsp+38h] [rbp-80h]
  __int64 v28; // [rsp+40h] [rbp-78h]
  __int128 v29; // [rsp+48h] [rbp-70h]
  void **v30; // [rsp+58h] [rbp-60h] BYREF
  __int128 v31; // [rsp+60h] [rbp-58h]
  void *v32; // [rsp+78h] [rbp-40h]
  __int64 v33; // [rsp+80h] [rbp-38h]

  v0 = _rust_alloc(0x88LL, 4LL);
  if ( !v0 )
    alloc::alloc::handle_alloc_error::h9e3787e5722c870d(0x88LL, 4LL);
  *(_OWORD *)v0 = xmmword_564A678D8000;
  *(_OWORD *)(v0 + 0x10) = xmmword_564A678D8010;
  *(_OWORD *)(v0 + 0x20) = xmmword_564A678D8020;
  *(_OWORD *)(v0 + 0x30) = xmmword_564A678D8030;
  *(_OWORD *)(v0 + 0x40) = xmmword_564A678D8040;
  *(_OWORD *)(v0 + 0x50) = xmmword_564A678D8050;
  *(_OWORD *)(v0 + 0x60) = xmmword_564A678D8060;
  *(_OWORD *)(v0 + 0x70) = xmmword_564A678D8070;
  *(_QWORD *)(v0 + 0x80) = 0x1DE000001E2LL;
  v28 = v0;
  v29 = xmmword_564A678D8080;
  v24 = 1LL;
  v25 = 0LL;
  v23 = (volatile signed __int64 *)std::io::stdio::stdin::hcd3fd1740d5196a7();
  v1 = (unsigned __int64)&v23;
  std::io::stdio::Stdin::read_line::h85c3421ca914511e(&v30, &v23, &v24);
  if ( v30 == (void **)1 )
  {
    *(_OWORD *)v26 = v31;
    core::result::unwrap_failed::h2bf42cb74d1e7d4b(&unk_564A678D80D3, 0x13LL, v26);
  }
  if ( !_InterlockedSub64(v23, 1uLL) )
    _$LT$alloc..sync..Arc$LT$T$GT$$GT$::drop_slow::h82dbb96617da66a0(&v23);
  v3 = v24; // 输入的字符串
  v4 = *((_QWORD *)&v25 + 1);
  if ( *((_QWORD *)&v25 + 1) )
  {
    v5 = *((_QWORD *)&v25 + 1) + v24;
    v2 = *(unsigned __int8 *)(*((_QWORD *)&v25 + 1) + v24 - 1);
    v6 = 1LL;
    if ( (v2 & 0x80u) == 0LL )
    {
LABEL_7:
      v4 = *((_QWORD *)&v25 + 1) - v6;
      *((_QWORD *)&v25 + 1) = v4;
      v5 = v4 + v24;
      goto LABEL_23;
    }
    if ( v24 == v5 - 1 )
    {
      v10 = 0;
    }
    else
    {
      v7 = *(_BYTE *)(v5 - 2);
      if ( (v7 & 0xC0) == 0x80 )
      {
        if ( v24 == v5 - 2 )
        {
          v11 = 0;
        }
        else
        {
          v8 = *(_BYTE *)(v5 - 3);
          if ( (v8 & 0xC0) == 0x80 )
          {
            if ( v24 == v5 - 3 )
              v9 = 0;
            else
              v9 = (*(_BYTE *)(v5 - 4) & 7) << 6;
            v11 = v9 | v8 & 0x3F;
          }
          else
          {
            v11 = v8 & 0xF;
          }
        }
        v10 = (v11 << 6) | v7 & 0x3F;
      }
      else
      {
        v10 = v7 & 0x1F;
      }
    }
    v1 = (unsigned int)(v10 << 6);
    v2 = (unsigned int)v1 | v2 & 0x3F;
    if ( (_DWORD)v2 != 0x110000 )
    {
      if ( (unsigned int)v2 >= 0x80 )
      {
        v6 = 2LL;
        if ( (unsigned int)v2 >= 0x800 )
          v6 = 4LL - ((unsigned int)v2 < 0x10000);
      }
      goto LABEL_7;
    }
  }
  else
  {
    v4 = 0LL;
    v5 = v24;
  }
LABEL_23:
  *(_QWORD *)v26 = 4LL;
  *(_OWORD *)&v26[8] = 0LL;
  if ( v4 )
  {
    v12 = v5 - v24;
    v1 = 0LL;
    v13 = 4LL;
    v14 = 4LL;
    v15 = 0LL;
    v27 = v12;
    do
    {
      v16 = *((unsigned __int8 *)v15 + v3);
      v17 = v1;
      if ( v15 == (volatile signed __int64 **)v1 )
      {
        v17 = v1 + 1;
        if ( v1 == 0xFFFFFFFFFFFFFFFFLL )
          goto LABEL_62;
        if ( v17 < 2 * v1 )
          v17 = 2 * v1;
        if ( !is_mul_ok(4uLL, v17) )
LABEL_62:
          alloc::raw_vec::capacity_overflow::hbc659f170a622eae();
        if ( v1 )
        {
          v13 = _rust_realloc(v14, 4 * v1, 4LL, 4 * v17);
          v12 = v27;
          if ( !v13 )
            goto LABEL_63;
        }
        else
        {
          v13 = _rust_alloc(4 * v17, 4LL);
          v12 = v27;
          if ( !v13 )
LABEL_63:
            alloc::alloc::handle_alloc_error::h9e3787e5722c870d(4 * v17, 4LL);
        }
        *(_QWORD *)v26 = v13;
        *(_QWORD *)&v26[8] = v17;
        v14 = v13;
        v1 = v17;
      }
      *(_DWORD *)(v13 + 4LL * (_QWORD)v15) = v16;
      v15 = (volatile signed __int64 **)((char *)v15 + 1);
      *(_QWORD *)&v26[0x10] = v15;
    }
    while ( (volatile signed __int64 **)v12 != v15 );
  }
  else
  {
    v13 = 4LL;
    v17 = 0LL;
    v15 = 0LL;
  }
  result = 4LL * (_QWORD)v15; // v15是输入字符串的长度
  v19 = 0LL;
  while ( result != v19 )
  {
    v2 = (unsigned int)(*(_DWORD *)(v13 + v19) - 0x20);
    v19 += 4LL;
    if ( (unsigned int)v2 >= 0x5F )
      std::panicking::begin_panic::h770c088eb8f42530(
        "an error occuredSubmit this and get you'r points!\n",
        0x10LL,
        &off_564A678EBF10,
        v19);
  }
  v20 = v28;
  if ( (unsigned __int64)v15 > *((_QWORD *)&v29 + 1) )
    v15 = (volatile signed __int64 **)*((_QWORD *)&v29 + 1);
  if ( !v15 )
  {
    if ( *((_QWORD *)&v29 + 1) )
      goto LABEL_52;
    goto LABEL_51;
  }
  v2 = 0LL;
  v1 = 0LL;
  v21 = 0LL;
  do
  {
    if ( v13 == v2 ) // v13也是输入的字符串
      break;
    v22 = ((*(int *)(v28 + 4 * v1) >> 2) ^ 0xA) == *(_DWORD *)(v13 + 4 * v1); // 比较
    ++v1;
    result = v22;
    v21 += v22;
    v2 -= 4LL;
  }
  while ( v1 < (unsigned __int64)v15 );
  if ( v21 == *((_QWORD *)&v29 + 1) )
  {
LABEL_51:
    v30 = &off_564A678EBF00;
    v31 = 1uLL;
    v32 = &unk_564A678D80C8;
    v33 = 0LL;
    result = std::io::stdio::_print::h77f73d11755d3bb8(&v30, v1, v2);
  }
LABEL_52:
  if ( v17 )
    result = _rust_dealloc(v13, 4 * v17, 4LL);
  if ( (_QWORD)v25 )
    result = _rust_dealloc(v24, v25, 1LL);
  if ( (_QWORD)v29 )
    result = _rust_dealloc(v20, 4 * v29, 4LL);
  return result;
}
```

这道题rust-reversing-helper好像失效了，但是不影响做题，需要动态调式。

通过分析我们知道在程序的逻辑是一开始先自己加载数据，然后将数据加密后与输入的字符串进行比较，所以我们只需要使用同样的加密方法将程序加载的数据加密即可。

```assembly
#include <stdio.h>

int main(){
    int x[34] = {0x10E, 0x112, 0x166, 0x1C6, 0x1CE, 0xEA, 0x1FE, 0x1E2, 0x156, 0x1AE,
                0x156, 0x1E2, 0xE6, 0x1AE, 0xEE, 0x156, 0x18A, 0xFA, 0x1E2, 0x1BA,
                0x1A6, 0xEA, 0x1E2, 0xE6, 0x156, 0x1E2, 0xE6, 0x1F2, 0xE6, 0x1E2,
                0x1E6, 0xE6, 0x1E2, 0x1DE};
    for(int i=0; i<34; i++){
        printf("%c", (x[i]>>2)^0xA);
    }
    return 0;
}
```

INS{y0ur_a_r3a1_h4rdc0r3_r3v3rs3r}