---
layout: post
title:  Tea_tube_pot
date:   2021-08-17 00:01:01 +0300
image:  2021-08-17-tea.jpg
tags:   [ctf,reverse,吃瓜杯,tea]
---

main

```assembly
__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  if ( (unsigned int)sub_C11(a1, a2, a3) && (unsigned int)sub_CA5() && (unsigned int)sub_D45() )
    puts("Congrts!Your Flag is 'ctfshow{'+PART1+PART2+PART3+'}'!");
  return 0LL;
}
```

sub_C11

```assembly
_BOOL8 sub_C11()
{
  __int128 v1; // [rsp+0h] [rbp-20h]
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  v1 = 0uLL;
  puts("Part1 Flag:");
  __isoc99_scanf("%8s", &v1);
  sub_71A(&v1, &unk_202010);
  return v1 == 0x958320465FD744F6LL;
}
```

sub_71A

```assembly
__int64 __fastcall sub_71A(unsigned int *a1, _DWORD *a2)
{
  __int64 result; // rax
  unsigned int v3; // [rsp+1Ch] [rbp-24h]
  unsigned int v4; // [rsp+20h] [rbp-20h]
  int v5; // [rsp+24h] [rbp-1Ch]
  unsigned int i; // [rsp+28h] [rbp-18h]

  v3 = *a1;
  v4 = a1[1];
  v5 = 0;
  for ( i = 0; i <= 0x1F; ++i )
  {
    v5 -= 1640531527;
    v3 += (v4 + v5) ^ (16 * v4 + *a2) ^ ((v4 >> 5) + a2[1]);
    v4 += (v3 + v5) ^ (16 * v3 + a2[2]) ^ ((v3 >> 5) + a2[3]);
  }
  *a1 = v3;
  result = v4;
  a1[1] = v4;
  return result;
}
```

sub_CA5

```assembly
_BOOL8 sub_CA5()
{
  __int128 v1; // [rsp+10h] [rbp-20h]
  unsigned __int64 v2; // [rsp+28h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  v1 = 0uLL;
  puts("Part2 Flag:");
  __isoc99_scanf("%8s", &v1);
  sub_7F8(32LL, &v1, &unk_202010);
  return v1 == 0x6662CB90FD731313LL;
}
```

sub_7F8

```assembly
__int64 __fastcall sub_7F8(unsigned int a1, unsigned int *a2, __int64 a3)
{
  __int64 result; // rax
  unsigned int i; // [rsp+24h] [rbp-14h]
  unsigned int v5; // [rsp+28h] [rbp-10h]
  unsigned int v6; // [rsp+2Ch] [rbp-Ch]
  unsigned int v7; // [rsp+30h] [rbp-8h]

  v5 = *a2;
  v6 = a2[1];
  v7 = 0;
  for ( i = 0; i < a1; ++i )
  {
    v5 += (((v6 >> 5) ^ 16 * v6) + v6) ^ (*(_DWORD *)(4LL * (v7 & 3) + a3) + v7);
    v7 -= 1640531527;
    v6 += (((v5 >> 5) ^ 16 * v5) + v5) ^ (*(_DWORD *)(4LL * ((v7 >> 11) & 3) + a3) + v7);
  }
  *a2 = v5;
  result = v6;
  a2[1] = v6;
  return result;
}
```

sub_D45

```assembly
_BOOL8 sub_D45()
{
  __int128 v1; // [rsp+10h] [rbp-20h]
  unsigned __int64 v2; // [rsp+28h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  v1 = 0uLL;
  puts("Part3 Flag:");
  __isoc99_scanf("%8s", &v1);
  sub_8D3(&v1, 2LL, &unk_202010);
  return v1 == 0x1A6E96134B136C82LL;
}
```

sub_8D3

```assembly
__int64 __fastcall sub_8D3(unsigned int *a1, signed int a2, __int64 a3)
{
  unsigned int v3; // ST20_4
  unsigned int *v4; // rax
  unsigned int *v5; // rax
  __int64 result; // rax
  unsigned int v7; // ST24_4
  unsigned int *v8; // rax
  unsigned int v9; // ST24_4
  int v10; // [rsp+Ch] [rbp-2Ch]
  unsigned int v11; // [rsp+20h] [rbp-18h]
  unsigned int v12; // [rsp+24h] [rbp-14h]
  unsigned int v13; // [rsp+28h] [rbp-10h]
  unsigned int v14; // [rsp+28h] [rbp-10h]
  unsigned int j; // [rsp+2Ch] [rbp-Ch]
  unsigned int i; // [rsp+2Ch] [rbp-Ch]
  int v17; // [rsp+30h] [rbp-8h]
  int v18; // [rsp+30h] [rbp-8h]
  int v19; // [rsp+34h] [rbp-4h]
  unsigned int v20; // [rsp+34h] [rbp-4h]

  if ( a2 <= 1 )
  {
    if ( a2 < -1 )
    {
      v10 = -a2;
      v18 = 52 / -a2 + 6;
      v14 = -1640531527 * v18;
      v11 = *a1;
      do
      {
        v20 = (v14 >> 2) & 3;
        for ( i = v10 - 1; i; --i )
        {
          v7 = a1[i - 1];
          v8 = &a1[i];
          *v8 -= ((v11 ^ v14) + (v7 ^ *(_DWORD *)(4LL * (v20 ^ i & 3) + a3))) ^ ((4 * v11 ^ (v7 >> 5))
                                                                               + ((v11 >> 3) ^ 16 * v7));
          v11 = *v8;
        }
        v9 = a1[v10 - 1];
        *a1 -= ((4 * v11 ^ (v9 >> 5)) + ((v11 >> 3) ^ 16 * v9)) ^ ((v11 ^ v14) + (v9 ^ *(_DWORD *)(4LL * v20 + a3)));
        result = *a1;
        v11 = *a1;
        v14 += 1640531527;
        --v18;
      }
      while ( v18 );
    }
  }
  else
  {
    v17 = 52 / a2 + 6;
    v13 = 0;
    v12 = a1[a2 - 1];
    do
    {
      v13 -= 1640531527;
      v19 = (v13 >> 2) & 3;
      for ( j = 0; j < a2 - 1; ++j )
      {
        v3 = a1[j + 1];
        v4 = &a1[j];
        *v4 += ((v3 ^ v13) + (v12 ^ *(_DWORD *)(4LL * (v19 ^ j & 3) + a3))) ^ ((4 * v3 ^ (v12 >> 5))
                                                                             + ((v3 >> 3) ^ 16 * v12));
        v12 = *v4;
      }
      v5 = &a1[a2 - 1];
      *v5 += ((*a1 ^ v13) + (v12 ^ *(_DWORD *)(4LL * (v19 ^ j & 3) + a3))) ^ ((4 * *a1 ^ (v12 >> 5))
                                                                            + ((*a1 >> 3) ^ 16 * v12));
      result = *v5;
      v12 = result;
      --v17;
    }
    while ( v17 );
  }
  return result;
}
```

三个加密函数分别是标准的tea，xtea，xxtea算法。

密钥都是

```assembly
.data:0000000000202010 unk_202010      db  54h ; T             ; DATA XREF: sub_C11+4F↑o
.data:0000000000202010                                         ; sub_CA5+59↑o ...
.data:0000000000202011                 db  68h ; h
.data:0000000000202012                 db  69h ; i
.data:0000000000202013                 db  73h ; s
.data:0000000000202014                 db  5Fh ; _
.data:0000000000202015                 db  69h ; i
.data:0000000000202016                 db  73h ; s
.data:0000000000202017                 db  5Fh ; _
.data:0000000000202018                 db  74h ; t
.data:0000000000202019                 db  65h ; e
.data:000000000020201A                 db  61h ; a
.data:000000000020201B                 db  74h ; t
.data:000000000020201C                 db  75h ; u
.data:000000000020201D                 db  62h ; b
.data:000000000020201E                 db  65h ; e
.data:000000000020201F                 db  21h ; !
```

编写脚本

```assembly
#include <stdio.h>
#include <stdint.h>

#define DELTA 0x9e3779b9
#define MX (((z>>5^y<<2) + (y>>3^z<<4)) ^ ((sum^y) + (key[(p&3)^e] ^ z)))

//tea加密函数
void encrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], sum=0, i;           /* set up */
    uint32_t delta=0x9e3779b9;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i < 32; i++) {                       /* basic cycle start */
        sum += delta;
        v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        v1 += ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}

//tea解密函数
void decrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], sum=0xC6EF3720, i;  /* set up */
    uint32_t delta=0x9e3779b9;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<32; i++) {                         /* basic cycle start */
        v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
        v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        sum -= delta;
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}

/* take 64 bits of data in v[0] and v[1] and 128 bits of key[0] - key[3] */
void encipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {
    unsigned int i;
    uint32_t v0=v[0], v1=v[1], sum=0, delta=0x9E3779B9;
    for (i=0; i < num_rounds; i++) {
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
        sum += delta;
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
    }
    v[0]=v0; v[1]=v1;
}

void decipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {
    unsigned int i;
    uint32_t v0=v[0], v1=v[1], delta=0x9E3779B9, sum=delta*num_rounds;
    for (i=0; i < num_rounds; i++) {
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
        sum -= delta;
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
    }
    v[0]=v0; v[1]=v1;
}

void btea(uint32_t *v, int n, uint32_t const key[4])
{
    uint32_t y, z, sum;
    unsigned p, rounds, e;
    if (n > 1){            /* Coding Part */
        rounds = 6 + 52/n;
        sum = 0;
        z = v[n-1];
        do{
            sum += DELTA;
            e = (sum >> 2) & 3;
            for (p=0; p<n-1; p++)
            {
                y = v[p+1];
                z = v[p] += MX;
            }
            y = v[0];
            z = v[n-1] += MX;
        }
        while (--rounds);
    }
    else if (n < -1){      /* Decoding Part */
        n = -n;
        rounds = 6 + 52/n;
        sum = rounds*DELTA;
        y = v[0];
        do{
            e = (sum >> 2) & 3;
            for (p=n-1; p>0; p--){
                z = v[p-1];
                y = v[p] -= MX;
            }
            z = v[n-1];
            y = v[0] -= MX;
            sum -= DELTA;
        }
        while (--rounds);
    }
}

int main(){

    //uint32_t const k[4]={0x54686973, 0x5F69735F, 0x74656174, 0x75626521};
    uint32_t const k[4]={0x73696854,0x5F73695F,0x74616574,0x21656275};

    //uint32_t v[2]={0x95832046, 0x5FD744F6};
    uint32_t v[2]={0x5FD744F6, 0x95832046};
    // v为要加密的数据是两个32位无符号整数
    // k为加密解密密钥，为4个32位无符号整数，即密钥长度为128位
    //encrypt(v, k);
    decrypt(v, k);
    printf("%x%x",v[0],v[1]);

    //uint32_t vv[2]={0x6662CB90, 0xFD731313};
    uint32_t vv[2]={0xFD731313, 0x6662CB90};
    unsigned int r=32;//num_rounds建议取值为32
    // v为要加密的数据是两个32位无符号整数
    // k为加密解密密钥，为4个32位无符号整数，即密钥长度为128位
    //encipher(r, v, k);
    decipher(r, vv, k);
    printf("%x%x",vv[0], vv[1]);

    //uint32_t vvv[2] = {0x1A6E9613, 0x4B136C82};
    uint32_t vvv[2] = {0x4B136C82, 0x1A6E9613};
    int n = 2; //n的绝对值表示v的长度，取正表示加密，取负表示解密
    // v为要加密的数据是两个32位无符号整数
    // k为加密解密密钥，为4个32位无符号整数，即密钥长度为128位
    //btea(v, n, k);
    btea(vvv, -n, k);
    printf("%x%x",vvv[0], vvv[1]);

    return 0;
}
```

796e315472434e456974507931416e3069726f39214d6837

十六进制转字符串

`yn1TrCNEitPy1An0iro9!Mh7`

这道题还有一些细节要注意

key的十六进制存储形式是

```assembly
54 68 69 73 5F 69 73 5F  74 65 61 74 75 62 65 21
```

但并不是

```assembly
uint32_t const k[4]={0x54686973, 0x5F69735F, 0x74656174, 0x75626521}
```

而是

```assembly
uint32_t const k[4]={0x73696854,0x5F73695F,0x74616574,0x21656275};
```

最后得到的字符串顺序是倒的，应该改回来。

ctfshow{T1nyENCryPti0nA19ori7hM!}