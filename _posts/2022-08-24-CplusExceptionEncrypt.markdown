---
layout: post
title:  CplusExceptionEncrypt(SCTF2021)
date:   2022-08-24 00:08:01 +0300
image:  2022-08-24-cat.jpg
tags:   [ctf,reverse,SCTF,exception]
---

一段c++测试代码

```assembly
#include <iostream>

using namespace std;

int main(){
    try{
        int a;
        cin >> a;
        if (a == 0){
            throw("a==0");
        }
    }catch (const char* msg){
        std::cout << msg << " error";
    }
}
```

### MSVC x86

会变成类似windows SEH进行处理

![]({{site.baseurl}}/img/CplusExceptionEncrypt/msvcx86.jpg)

使用`_CxxThrowException`函数抛出异常，之后在 SEH 异常处理器中捕获异常并转到异常处理代码中。而使用 IDA 进行反编译时，是无法正常分析出反编译结果的:

```assembly

int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v4; // [esp+0h] [ebp-30h] BYREF
  const char *pExceptionObject; // [esp+14h] [ebp-1Ch] BYREF
  int v6[6]; // [esp+18h] [ebp-18h] BYREF

  v6[2] = (int)&v4;
  v6[5] = 0;
  std::istream::operator>>(std::cin, v6);
  if ( !v6[0] )
  {
    pExceptionObject = "a==0";
    CxxThrowException(&pExceptionObject, (_ThrowInfo *)&PA.deinit);
  }
  return 0;
}
```

可以对汇编代码进行一些修改。将 call throw的指令修改为 jmp 到catch块内，使得强制发生跳转，即可使得 IDA 进行分析

### MSVC x64

![]({{site.baseurl}}/img/CplusExceptionEncrypt/msvcx64.jpg)

可以看到catch的块根本不在main函数中，通过搜索字符串的交叉引用定位到catch块

```assembly
.text:0000000140002080 sub_140002080   proc near               ; DATA XREF: .pdata:000000014000618C↓o
.text:0000000140002080
.text:0000000140002080 arg_8           = qword ptr  10h
.text:0000000140002080
.text:0000000140002080                 mov     [rsp+arg_8], rdx
.text:0000000140002085                 push    rbp
.text:0000000140002086                 sub     rsp, 20h
.text:000000014000208A                 mov     rbp, rdx
.text:000000014000208D                 mov     rdx, [rbp+28h]
.text:0000000140002091                 mov     rcx, cs:?cout@std@@3V?$basic_ostream@DU?$char_traits@D@std@@@1@A ; std::ostream std::cout
.text:0000000140002098                 call    sub_140001060
.text:000000014000209D                 mov     rcx, rax
.text:00000001400020A0                 lea     rdx, aError     ; " error"
.text:00000001400020A7                 call    sub_140001060
.text:00000001400020AC                 nop
.text:00000001400020AD                 mov     rax, 0
.text:00000001400020B7                 add     rsp, 20h
.text:00000001400020BB                 pop     rbp
.text:00000001400020BC                 retn
.text:00000001400020BC ; ---------------------------------------------------------------------------
.text:00000001400020BD                 db 0CCh
.text:00000001400020BD sub_140002080   endp
```

对汇编代码进行一些修改。将 call throw的指令修改为 jmp 到catch块内，使得强制发生跳转，即可使得 IDA 进行分析

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax
  __int64 pExceptionObject; // [rsp+20h] [rbp-28h] BYREF
  int v5; // [rsp+30h] [rbp-18h] BYREF

  std::istream::operator>>(std::cin, &v5, envp);
  if ( v5 )
    result = 0;
  else
    result = sub_140002080(&pExceptionObject, &_TI2PEAD);
  return result;
}
```

### Clang x64

![]({{site.baseurl}}/img/CplusExceptionEncrypt/clang.jpg)

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  _QWORD *v3; // rdi
  int v5; // [rsp+28h] [rbp-8h] BYREF
  int v6; // [rsp+2Ch] [rbp-4h]

  v6 = 0;
  std::istream::operator>>(&std::cin, &v5, envp);
  if ( !v5 )
  {
    v3 = __cxa_allocate_exception(8uLL);
    *v3 = "a==0";
    __cxa_throw(v3, (struct type_info *)&`typeinfo for'char const*, 0LL);
  }
  return v6;
}
```

## 题目

有了上面的基础，这道题做起来就比较容易了，main函数F5显示的内容很少

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  void *rbx3; // rbx
  uint8_t cmp_arr[32]; // [rsp+160h] [rbp+E0h]
  unsigned __int8 encdata[32]; // [rsp+180h] [rbp+100h]
  char data[32]; // [rsp+1A0h] [rbp+120h] BYREF
  char v8; // [rsp+1C7h] [rbp+147h] BYREF
  int length; // [rsp+1D8h] [rbp+158h]
  int control1; // [rsp+1DCh] [rbp+15Ch]
  uint32_t sum2; // [rsp+204h] [rbp+184h]
  uint32_t sum1; // [rsp+208h] [rbp+188h]
  uint32_t v3; // [rsp+20Ch] [rbp+18Ch]
  uint32_t v2; // [rsp+210h] [rbp+190h]
  uint32_t v1; // [rsp+214h] [rbp+194h]
  uint32_t v0; // [rsp+218h] [rbp+198h]
  int w; // [rsp+21Ch] [rbp+19Ch]

  _main(argc, argv, envp);
  control1 = 0;
  *(_QWORD *)data = 0i64;
  *(_QWORD *)&data[8] = 0i64;
  *(_QWORD *)&data[0x10] = 0i64;
  *(_QWORD *)&data[0x18] = 0i64;
  *(_QWORD *)encdata = 0i64;
  *(_QWORD *)&encdata[8] = 0i64;
  *(_QWORD *)&encdata[0x10] = 0i64;
  *(_QWORD *)&encdata[0x18] = 0i64;
  *(_QWORD *)cmp_arr = 0i64;
  *(_QWORD *)&cmp_arr[8] = 0i64;
  *(_QWORD *)&cmp_arr[0x10] = 0i64;
  *(_QWORD *)&cmp_arr[0x18] = 0i64;
  printf("---------------------Welcome_to_SCTF_2021---------------------\n");
  printf("Please input your flag: \n");
  scanf("%s", data);
  length = strlen(data);
  if ( length == 0x20 )
  {
    w = 0;
    v0 = *(_DWORD *)data;
    v1 = *(_DWORD *)&data[4];
    v2 = *(_DWORD *)&data[8];
    v3 = *(_DWORD *)&data[0xC];
    sum1 = 0;
    sum2 = 0;
    rbx3 = _cxa_allocate_exception(0x20ui64);
    std::allocator<char>::allocator(&v8);
    std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(rbx3, "init_part", &v8);
    std::allocator<char>::~allocator(&v8);
    _cxa_throw(
      rbx3,
      (struct type_info *)&`typeinfo for'std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>,
      refptr__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEED1Ev);
  }
  printf("length error!\n");
  return 0;
}
```

所以利用上面的方法，将控制流jmp到catch块中，从而使得可以在ida中转为代码分析

ida中每一个catche块都有一个owned by addr的提示可以给我们很好的帮助

operation1

```assembly
uint32_t __cdecl operation1(uint32_t a, uint32_t b)
{
  op1 *v2; // rbx
  void *v3; // rax
  void *v5; // rbx
  uint32_t v6; // ebx
  op1_0 temp; // [rsp+24h] [rbp-5Ch]

  v2 = (op1 *)_cxa_allocate_exception(8ui64);
  op1::op1(v2, a, b);
  v5 = v3;
  if ( &`typeinfo for'op1 == (void **)1 )
  {
    temp = *(op1_0 *)_cxa_get_exception_ptr(v3);
    _cxa_begin_catch(v5);
    v6 = temp.a + temp.b;
  }
  else
  {
    _cxa_begin_catch(v3);
    v6 = 0;
  }
  _cxa_end_catch();
  return v6;
}
```

operation2

```assembly
uint32_t __cdecl operation2(uint32_t a)
{
  op2 *v1; // rbx
  void *v2; // rax
  void *v4; // rbx
  uint32_t v5; // ebx
  op2_0 temp; // [rsp+28h] [rbp-58h]

  v1 = (op2 *)_cxa_allocate_exception(4ui64);
  op2::op2(v1, a);
  v4 = v2;
  if ( &`typeinfo for'op2 == (void **)1 )
  {
    temp.a = *(_DWORD *)_cxa_get_exception_ptr(v2);
    _cxa_begin_catch(v4);
    v5 = 0x10 * temp.a;
  }
  else
  {
    _cxa_begin_catch(v2);
    v5 = 0;
  }
  _cxa_end_catch();
  return v5;
}
```

operation3

```assembly
uint32_t __cdecl operation3(uint32_t a, uint32_t b)
{
  op4 *v2; // rbx
  void *v3; // rax
  void *v5; // rbx
  uint32_t v6; // ebx
  op4_0 temp; // [rsp+24h] [rbp-5Ch]

  v2 = (op4 *)_cxa_allocate_exception(8ui64);
  op4::op4(v2, a, b);
  v5 = v3;
  if ( &`typeinfo for'op4 == (void **)1 )
  {
    temp = *(op4_0 *)_cxa_get_exception_ptr(v3);
    _cxa_begin_catch(v5);
    v6 = temp.a ^ temp.b;
  }
  else
  {
    _cxa_begin_catch(v3);
    v6 = 0;
  }
  _cxa_end_catch();
  return v6;
}
```

operation4

```assembly
uint32_t __cdecl operation4(uint32_t a)
{
  op3 *v1; // rbx
  void *v2; // rax
  void *v4; // rbx
  uint32_t v5; // ebx
  op temp; // [rsp+28h] [rbp-58h]

  v1 = (op3 *)_cxa_allocate_exception(4ui64);
  op3::op3(v1, a);
  v4 = v2;
  if ( &`typeinfo for'op3 == (void **)1 )
  {
    temp.a = *(_DWORD *)_cxa_get_exception_ptr(v2);
    _cxa_begin_catch(v4);
    v5 = temp.a >> 5;
  }
  else
  {
    _cxa_begin_catch(v2);
    v5 = 0;
  }
  _cxa_end_catch();
  return v5;
}
```

switch中的catch块

```assembly
.text:0000000000402C3C loc_402C3C:                             ; CODE XREF: main+31C↑j
.text:0000000000402C3C ;   catch(struct_of_step1) // owned by 40273D
.text:0000000000402C3C ;   catch(struct_of_step2) // owned by 40273D
.text:0000000000402C3C ;   catch(struct_of_step3) // owned by 40273D
.text:0000000000402C3C ;   catch(...) // owned by 40273D
.text:0000000000402C3C                 cmp     rdx, 3
```

修复40273D处的call指令

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  void *rbx3a; // rbx
  void *v4; // rax
  struct_of_step1 *v5; // rbx
  void *v6; // rax
  struct_of_step2 *v7; // rbx
  struct_of_step3 *v8; // rbx
  last_struct *v9; // rbx
  void *v11; // rbx
  void *v12; // rax
  uint32_t v13; // ebx
  uint32_t v14; // eax
  uint32_t v15; // esi
  uint32_t v16; // edi
  uint32_t v17; // eax
  uint32_t v18; // eax
  uint32_t v19; // eax
  uint32_t v20; // eax
  uint32_t v21; // ebx
  uint32_t v22; // eax
  uint32_t v23; // esi
  uint32_t v24; // edi
  uint32_t v25; // eax
  uint32_t v26; // eax
  uint32_t v27; // eax
  uint32_t v28; // eax
  uint32_t v29; // ebx
  uint32_t v30; // eax
  uint32_t v31; // esi
  uint32_t v32; // edi
  uint32_t v33; // eax
  uint32_t v34; // eax
  uint32_t v35; // eax
  uint32_t v36; // eax
  uint32_t v37; // ebx
  uint32_t v38; // eax
  uint32_t v39; // esi
  uint32_t v40; // edi
  uint32_t v41; // eax
  uint32_t v42; // eax
  uint32_t v43; // eax
  uint32_t v44; // eax
  std::__cxx11::string init; // [rsp+20h] [rbp-60h] BYREF
  uint8_t key[16]; // [rsp+110h] [rbp+90h] BYREF
  unsigned __int8 out1[16]; // [rsp+130h] [rbp+B0h]
  uint32_t dst[4]; // [rsp+140h] [rbp+C0h]
  uint32_t inp[4]; // [rsp+150h] [rbp+D0h]
  uint8_t cmp_arr[32]; // [rsp+160h] [rbp+E0h]
  unsigned __int8 encdata[32]; // [rsp+180h] [rbp+100h]
  char data[32]; // [rsp+1A0h] [rbp+120h] BYREF
  char v53; // [rsp+1C7h] [rbp+147h] BYREF
  uint32_t k3_0; // [rsp+1C8h] [rbp+148h]
  uint32_t k2_0; // [rsp+1CCh] [rbp+14Ch]
  uint32_t k1_0; // [rsp+1D0h] [rbp+150h]
  uint32_t k0_0; // [rsp+1D4h] [rbp+154h]
  int length; // [rsp+1D8h] [rbp+158h]
  int control1; // [rsp+1DCh] [rbp+15Ch]
  int cnt; // [rsp+1FCh] [rbp+17Ch]
  int i; // [rsp+200h] [rbp+180h]
  uint32_t sum2; // [rsp+204h] [rbp+184h]
  uint32_t sum1; // [rsp+208h] [rbp+188h]
  uint32_t v3; // [rsp+20Ch] [rbp+18Ch]
  uint32_t v2; // [rsp+210h] [rbp+190h]
  uint32_t v1; // [rsp+214h] [rbp+194h]
  uint32_t v0; // [rsp+218h] [rbp+198h]
  int w; // [rsp+21Ch] [rbp+19Ch]

  _main(argc, argv, envp);
  control1 = 0;
  *(_QWORD *)data = 0i64;
  *(_QWORD *)&data[8] = 0i64;
  *(_QWORD *)&data[0x10] = 0i64;
  *(_QWORD *)&data[0x18] = 0i64;
  *(_QWORD *)encdata = 0i64;
  *(_QWORD *)&encdata[8] = 0i64;
  *(_QWORD *)&encdata[0x10] = 0i64;
  *(_QWORD *)&encdata[0x18] = 0i64;
  *(_QWORD *)cmp_arr = 0i64;
  *(_QWORD *)&cmp_arr[8] = 0i64;
  *(_QWORD *)&cmp_arr[0x10] = 0i64;
  *(_QWORD *)&cmp_arr[0x18] = 0i64;
  *(_QWORD *)inp = 0i64;
  *(_QWORD *)&inp[2] = 0i64;
  printf("---------------------Welcome_to_SCTF_2021---------------------\n");
  printf("Please input your flag: \n");
  scanf("%s", data);
  length = strlen(data);
  if ( length == 0x20 )
  {
    w = 0;
    inp[0] = *(_DWORD *)data;
    inp[1] = *(_DWORD *)&data[4];
    inp[2] = *(_DWORD *)&data[8];
    inp[3] = *(_DWORD *)&data[0xC];
    v0 = *(_DWORD *)data;
    v1 = *(_DWORD *)&data[4];
    v2 = *(_DWORD *)&data[8];
    v3 = *(_DWORD *)&data[0xC];
    sum1 = 0;
    sum2 = 0;
    *(_QWORD *)dst = 0i64;
    *(_QWORD *)&dst[2] = 0i64;
    *(_QWORD *)out1 = 0i64;
    *(_QWORD *)&out1[8] = 0i64;
    rbx3a = _cxa_allocate_exception(0x20ui64);
    std::allocator<char>::allocator(&v53);
    std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(rbx3a, "init_part", &v53);
    v4 = (void *)std::allocator<char>::~allocator(&v53);
    v11 = v4;
    if ( &`typeinfo for'std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>> != (void **)1 )
      Unwind_Resume(v4);
    v12 = _cxa_get_exception_ptr(v4);
    std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(&init, v12);
    _cxa_begin_catch(v11);
    qmemcpy(key, "Welcome_to_sctf!", sizeof(key));
    k0_0 = *(_DWORD *)key;
    k1_0 = *(_DWORD *)&key[4];
    k2_0 = *(_DWORD *)&key[8];
    k3_0 = *(_DWORD *)&key[0xC];
    cmp_arr[0] = 0xBE;
    cmp_arr[1] = 0x1C;
    cmp_arr[2] = 0xB3;
    cmp_arr[3] = 0xF3;
    cmp_arr[4] = 0xA1;
    cmp_arr[5] = 0xF4;
    cmp_arr[6] = 0xE4;
    cmp_arr[7] = 0x63;
    cmp_arr[8] = 0x11;
    cmp_arr[9] = 0xE1;
    cmp_arr[0xA] = 0x1C;
    cmp_arr[0xB] = 0x6B;
    cmp_arr[0xC] = 0x54;
    cmp_arr[0xD] = 0xA;
    cmp_arr[0xE] = 0xDF;
    cmp_arr[0xF] = 0x74;
    cmp_arr[0x10] = 0xF2;
    cmp_arr[0x11] = 0x93;
    cmp_arr[0x12] = 0x55;
    cmp_arr[0x13] = 0xDA;
    cmp_arr[0x14] = 0x48;
    cmp_arr[0x15] = 0xFC;
    cmp_arr[0x16] = 0xA2;
    cmp_arr[0x17] = 0x3C;
    cmp_arr[0x18] = 0x89;
    cmp_arr[0x19] = 0x63;
    cmp_arr[0x1A] = 0x2E;
    cmp_arr[0x1B] = 0x7F;
    cmp_arr[0x1C] = 0x8D;
    cmp_arr[0x1D] = 0xA4;
    cmp_arr[0x1E] = 0x6D;
    cmp_arr[0x1F] = 0x4E;
    std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&init);
    _cxa_end_catch();
    i = 0;
LABEL_4:
    if ( i > 0x1F )
    {
      v9 = (last_struct *)_cxa_allocate_exception(1ui64);
      text_84(v9);
      _cxa_throw(v9, (struct type_info *)&`typeinfo for'last_struct, 0i64);
    }
    cnt = 0;
    srand(0x53435446u);
    while ( 1 )
    {
      control1 = rand();
      switch ( control1 )
      {
        case 0x5208:
          v8 = (struct_of_step3 *)_cxa_allocate_exception(1ui64);
          struct_of_step3::struct_of_step3(v8);
          _cxa_throw(v8, (struct type_info *)&`typeinfo for'struct_of_step3, 0i64);
        case 0x6591:
          v5 = (struct_of_step1 *)_cxa_allocate_exception(1ui64);
          struct_of_step1::struct_of_step1(v5);
          if ( &`typeinfo for'struct_of_step1 == (void **)3 )
          {
            _cxa_begin_catch(v6);
            v13 = operation1(sum1, i);
            v14 = operation4(v1);
            v15 = operation1(v14, k3_0);
            v16 = operation1(v1, sum1);
            v17 = operation2(v1);
            v18 = operation1(v17, k2_0);
            v19 = operation3(v18, v16);
            v20 = operation3(v19, v15);
            v0 += operation3(v20, v13);
            v21 = operation1(sum2, i);
            v22 = operation4(v3);
            v23 = operation1(v22, k3_0);
            v24 = operation1(v3, sum2);
            v25 = operation2(v3);
            v26 = operation1(v25, k2_0);
            v27 = operation3(v26, v24);
            v28 = operation3(v27, v23);
            v2 += operation3(v28, v21);
            _cxa_end_catch();
          }
          else if ( &`typeinfo for'struct_of_step1 == (void **)4 )
          {
            _cxa_begin_catch(v6);
            v29 = operation1(sum1, i);
            v30 = operation4(v0);
            v31 = operation1(v30, k1_0);
            v32 = operation1(v0, sum1);
            v33 = operation2(v0);
            v34 = operation1(v33, k0_0);
            v35 = operation3(v34, v32);
            v36 = operation3(v35, v31);
            v1 += operation3(v36, v29);
            v37 = operation1(sum2, i);
            v38 = operation4(v2);
            v39 = operation1(v38, k1_0);
            v40 = operation1(v2, sum1);
            v41 = operation2(v2);
            v42 = operation1(v41, k0_0);
            v43 = operation3(v42, v40);
            v44 = operation3(v43, v39);
            v3 += operation3(v44, v37);
            _cxa_end_catch();
          }
          else
          {
            if ( &`typeinfo for'struct_of_step1 != (void **)2 )
            {
              _cxa_begin_catch(v6);
              _cxa_end_catch();
              return 0;
            }
            _cxa_begin_catch(v6);
            sum1 = operation1(sum1, delta);
            sum2 = operation1(sum2, delta);
            _cxa_end_catch();
          }
          break;
        case 0x10A9:
          v7 = (struct_of_step2 *)_cxa_allocate_exception(1ui64);
          struct_of_step2::struct_of_step2(v7);
          _cxa_throw(v7, (struct type_info *)&`typeinfo for'struct_of_step2, 0i64);
      }
      if ( ++cnt == 3 )
      {
        ++i;
        goto LABEL_4;
      }
    }
  }
  printf("length error!\n");
  return 0;
}
```

修复last struct

最后还原为

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  void *rbx9a; // rbx
  void *v4; // rax
  struct_of_step1 *v5; // rbx
  void *v6; // rax
  struct_of_step2 *v7; // rbx
  struct_of_step3 *v8; // rbx
  last_struct *v9; // rbx
  void *v10; // rax
  int v11; // eax
  enc_next_ready_struct *v12; // rbx
  enc_next_struct *v13; // rbx
  void *v15; // rbx
  void *v16; // rax
  uint32_t v17; // ebx
  uint32_t v18; // eax
  uint32_t v19; // esi
  uint32_t v20; // edi
  uint32_t v21; // eax
  uint32_t v22; // eax
  uint32_t v23; // eax
  uint32_t v24; // eax
  uint32_t v25; // ebx
  uint32_t v26; // eax
  uint32_t v27; // esi
  uint32_t v28; // edi
  uint32_t v29; // eax
  uint32_t v30; // eax
  uint32_t v31; // eax
  uint32_t v32; // eax
  uint32_t v33; // ebx
  uint32_t v34; // eax
  uint32_t v35; // esi
  uint32_t v36; // edi
  uint32_t v37; // eax
  uint32_t v38; // eax
  uint32_t v39; // eax
  uint32_t v40; // eax
  uint32_t v41; // ebx
  uint32_t v42; // eax
  uint32_t v43; // esi
  uint32_t v44; // edi
  uint32_t v45; // eax
  uint32_t v46; // eax
  uint32_t v47; // eax
  uint32_t v48; // eax
  void *v49; // rbx
  void *v50; // rax
  uint8_t *v51; // rdx
  uint8_t *v52; // rbx
  std::__cxx11::string init; // [rsp+20h] [rbp-60h] BYREF
  enc_next_struct_0 temp_4; // [rsp+D0h] [rbp+50h]
  enc_next_ready_struct_0 temp_3; // [rsp+F0h] [rbp+70h]
  uint8_t key[16]; // [rsp+110h] [rbp+90h] BYREF
  uint8_t ciphertext[16]; // [rsp+120h] [rbp+A0h] BYREF
  unsigned __int8 out1[16]; // [rsp+130h] [rbp+B0h] BYREF
  uint32_t dst[4]; // [rsp+140h] [rbp+C0h] BYREF
  uint32_t inp[4]; // [rsp+150h] [rbp+D0h]
  uint8_t cmp_arr[32]; // [rsp+160h] [rbp+E0h]
  unsigned __int8 encdata[32]; // [rsp+180h] [rbp+100h]
  char data[32]; // [rsp+1A0h] [rbp+120h] BYREF
  char v64; // [rsp+1C7h] [rbp+147h] BYREF
  uint32_t k3_0; // [rsp+1C8h] [rbp+148h]
  uint32_t k2_0; // [rsp+1CCh] [rbp+14Ch]
  uint32_t k1_0; // [rsp+1D0h] [rbp+150h]
  uint32_t k0_0; // [rsp+1D4h] [rbp+154h]
  int length; // [rsp+1D8h] [rbp+158h]
  int control1; // [rsp+1DCh] [rbp+15Ch]
  int j_0; // [rsp+1E0h] [rbp+160h]
  int i_1; // [rsp+1E4h] [rbp+164h]
  int i_0; // [rsp+1E8h] [rbp+168h]
  int x; // [rsp+1ECh] [rbp+16Ch]
  int k; // [rsp+1F0h] [rbp+170h]
  int j; // [rsp+1F4h] [rbp+174h]
  int m; // [rsp+1F8h] [rbp+178h]
  int cnt; // [rsp+1FCh] [rbp+17Ch]
  int i; // [rsp+200h] [rbp+180h]
  uint32_t sum2; // [rsp+204h] [rbp+184h]
  uint32_t sum1; // [rsp+208h] [rbp+188h]
  uint32_t v3; // [rsp+20Ch] [rbp+18Ch]
  uint32_t v2; // [rsp+210h] [rbp+190h]
  uint32_t v1; // [rsp+214h] [rbp+194h]
  uint32_t v0; // [rsp+218h] [rbp+198h]
  int w; // [rsp+21Ch] [rbp+19Ch]

  _main(argc, argv, envp);
  control1 = 0;
  *(_QWORD *)data = 0i64;
  *(_QWORD *)&data[8] = 0i64;
  *(_QWORD *)&data[0x10] = 0i64;
  *(_QWORD *)&data[0x18] = 0i64;
  *(_QWORD *)encdata = 0i64;
  *(_QWORD *)&encdata[8] = 0i64;
  *(_QWORD *)&encdata[0x10] = 0i64;
  *(_QWORD *)&encdata[0x18] = 0i64;
  *(_QWORD *)cmp_arr = 0i64;
  *(_QWORD *)&cmp_arr[8] = 0i64;
  *(_QWORD *)&cmp_arr[0x10] = 0i64;
  *(_QWORD *)&cmp_arr[0x18] = 0i64;
  *(_QWORD *)inp = 0i64;
  *(_QWORD *)&inp[2] = 0i64;
  printf("---------------------Welcome_to_SCTF_2021---------------------\n");
  printf("Please input your flag: \n");
  scanf("%s", data);
  length = strlen(data);
  if ( length != 0x20 )
  {
    printf("length error!\n");
    return 0;
  }
  w = 0;
LABEL_4:
  if ( w > 1 )
  {
    for ( j_0 = 0; j_0 <= 0x1F; ++j_0 )
    {
      if ( encdata[j_0] != cmp_arr[j_0] )
      {
        printf("Sorry!Your flag is wrong!!!!\n");
        exit(0);
      }
    }
    printf("\ncongratulations!!!!your flag is \nSCTF{ %s }", data);
    return 0;
  }
  if ( !w )
  {
    inp[0] = *(_DWORD *)data;
    inp[1] = *(_DWORD *)&data[4];
    inp[2] = *(_DWORD *)&data[8];
    inp[3] = *(_DWORD *)&data[0xC];
  }
  if ( w == 1 )
  {
    inp[0] = *(_DWORD *)&data[0x10];
    inp[1] = *(_DWORD *)&data[0x14];
    inp[2] = *(_DWORD *)&data[0x18];
    inp[3] = *(_DWORD *)&data[0x1C];
  }
  v0 = inp[0];
  v1 = inp[1];
  v2 = inp[2];
  v3 = inp[3];
  sum1 = 0;
  sum2 = 0;
  *(_QWORD *)dst = 0i64;
  *(_QWORD *)&dst[2] = 0i64;
  *(_QWORD *)out1 = 0i64;
  *(_QWORD *)&out1[8] = 0i64;
  rbx9a = _cxa_allocate_exception(0x20ui64);
  std::allocator<char>::allocator(&v64);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(rbx9a, "init_part", &v64);
  v4 = (void *)std::allocator<char>::~allocator(&v64);
  v15 = v4;
  if ( &`typeinfo for'std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>> != (void **)1 )
    Unwind_Resume(v4);
  v16 = _cxa_get_exception_ptr(v4);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(&init, v16);
  _cxa_begin_catch(v15);
  qmemcpy(key, "Welcome_to_sctf!", sizeof(key));
  k0_0 = *(_DWORD *)key;
  k1_0 = *(_DWORD *)&key[4];
  k2_0 = *(_DWORD *)&key[8];
  k3_0 = *(_DWORD *)&key[0xC];
  cmp_arr[0] = 0xBE;
  cmp_arr[1] = 0x1C;
  cmp_arr[2] = 0xB3;
  cmp_arr[3] = 0xF3;
  cmp_arr[4] = 0xA1;
  cmp_arr[5] = 0xF4;
  cmp_arr[6] = 0xE4;
  cmp_arr[7] = 0x63;
  cmp_arr[8] = 0x11;
  cmp_arr[9] = 0xE1;
  cmp_arr[0xA] = 0x1C;
  cmp_arr[0xB] = 0x6B;
  cmp_arr[0xC] = 0x54;
  cmp_arr[0xD] = 0xA;
  cmp_arr[0xE] = 0xDF;
  cmp_arr[0xF] = 0x74;
  cmp_arr[0x10] = 0xF2;
  cmp_arr[0x11] = 0x93;
  cmp_arr[0x12] = 0x55;
  cmp_arr[0x13] = 0xDA;
  cmp_arr[0x14] = 0x48;
  cmp_arr[0x15] = 0xFC;
  cmp_arr[0x16] = 0xA2;
  cmp_arr[0x17] = 0x3C;
  cmp_arr[0x18] = 0x89;
  cmp_arr[0x19] = 0x63;
  cmp_arr[0x1A] = 0x2E;
  cmp_arr[0x1B] = 0x7F;
  cmp_arr[0x1C] = 0x8D;
  cmp_arr[0x1D] = 0xA4;
  cmp_arr[0x1E] = 0x6D;
  cmp_arr[0x1F] = 0x4E;
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&init);
  _cxa_end_catch();
  for ( i = 0; i <= 0x1F; ++i )
  {
    cnt = 0;
    srand(0x53435446u);
    do
    {
      control1 = rand();
      switch ( control1 )
      {
        case 0x5208:
          v8 = (struct_of_step3 *)_cxa_allocate_exception(1ui64);
          struct_of_step3::struct_of_step3(v8);
          _cxa_throw(v8, (struct type_info *)&`typeinfo for'struct_of_step3, 0i64);
        case 0x6591:
          v5 = (struct_of_step1 *)_cxa_allocate_exception(1ui64);
          struct_of_step1::struct_of_step1(v5);
          if ( &`typeinfo for'struct_of_step1 == (void **)3 )
          {
            _cxa_begin_catch(v6);
            v17 = operation1(sum1, i);
            v18 = operation4(v1);
            v19 = operation1(v18, k3_0);
            v20 = operation1(v1, sum1);
            v21 = operation2(v1);
            v22 = operation1(v21, k2_0);
            v23 = operation3(v22, v20);
            v24 = operation3(v23, v19);
            v0 += operation3(v24, v17);
            v25 = operation1(sum2, i);
            v26 = operation4(v3);
            v27 = operation1(v26, k3_0);
            v28 = operation1(v3, sum2);
            v29 = operation2(v3);
            v30 = operation1(v29, k2_0);
            v31 = operation3(v30, v28);
            v32 = operation3(v31, v27);
            v2 += operation3(v32, v25);
            _cxa_end_catch();
          }
          else if ( &`typeinfo for'struct_of_step1 == (void **)4 )
          {
            _cxa_begin_catch(v6);
            v33 = operation1(sum1, i);
            v34 = operation4(v0);
            v35 = operation1(v34, k1_0);
            v36 = operation1(v0, sum1);
            v37 = operation2(v0);
            v38 = operation1(v37, k0_0);
            v39 = operation3(v38, v36);
            v40 = operation3(v39, v35);
            v1 += operation3(v40, v33);
            v41 = operation1(sum2, i);
            v42 = operation4(v2);
            v43 = operation1(v42, k1_0);
            v44 = operation1(v2, sum1);
            v45 = operation2(v2);
            v46 = operation1(v45, k0_0);
            v47 = operation3(v46, v44);
            v48 = operation3(v47, v43);
            v3 += operation3(v48, v41);
            _cxa_end_catch();
          }
          else
          {
            if ( &`typeinfo for'struct_of_step1 != (void **)2 )
              goto LABEL_65;
            _cxa_begin_catch(v6);
            sum1 = operation1(sum1, delta);
            sum2 = operation1(sum2, delta);
            _cxa_end_catch();
          }
          break;
        case 0x10A9:
          v7 = (struct_of_step2 *)_cxa_allocate_exception(1ui64);
          struct_of_step2::struct_of_step2(v7);
          _cxa_throw(v7, (struct type_info *)&`typeinfo for'struct_of_step2, 0i64);
      }
      ++cnt;
    }
    while ( cnt != 3 );
  }
  v9 = (last_struct *)_cxa_allocate_exception(1ui64);
  text_84(v9);
  if ( &`typeinfo for'last_struct != (void **)6 )
    Unwind_Resume(v10);
  _cxa_begin_catch(v10);
  dst[0] = v0 ^ HIBYTE(delta);
  dst[1] = v1 ^ BYTE2(delta);
  dst[2] = v2 ^ BYTE1(delta);
  dst[3] = v3 ^ (unsigned __int8)delta;
  _cxa_end_catch();
  m = 0;
  for ( j = 0; j <= 3; ++j )
  {
    for ( k = 0; k <= 3; ++k )
      out1[m++] = *((_BYTE *)&dst[j] + k);
  }
  x = 0;
  srand(0x53435446u);
  while ( 1 )
  {
    if ( x == 2 )
    {
      if ( !w )
      {
        for ( i_0 = 0; i_0 <= 0xF; ++i_0 )
          encdata[i_0] = ciphertext[i_0];
      }
      if ( w == 1 )
      {
        for ( i_1 = 0; i_1 <= 0xF; ++i_1 )
          encdata[i_1 + 0x10] = ciphertext[i_1];
      }
      ++w;
      goto LABEL_4;
    }
    v11 = rand();
    if ( v11 == 0x10A9 )
    {
      v13 = (enc_next_struct *)_cxa_allocate_exception(0x18ui64);
      enc_next_struct::enc_next_struct(v13, (uint8_t *)&init, out1, ciphertext);
      _cxa_throw(v13, (struct type_info *)&`typeinfo for'enc_next_struct, 0i64);
    }
    if ( v11 == 0x6591 )
      break;
LABEL_33:
    ++x;
  }
  v12 = (enc_next_ready_struct *)_cxa_allocate_exception(0x10ui64);
  enc_next_ready_struct::enc_next_ready_struct(v12, key, (uint8_t *)&init);
  v49 = v6;
  if ( &`typeinfo for'enc_next_ready_struct == (void **)7 )
  {
    v50 = _cxa_get_exception_ptr(v6);
    v51 = (uint8_t *)*((_QWORD *)v50 + 1);
    temp_3.ourciphertext = *(uint8_t **)v50;
    temp_3.ourroundkeys = v51;
    _cxa_begin_catch(v49);
    enc_next_ready(temp_3.ourciphertext, temp_3.ourroundkeys);
    _cxa_end_catch();
    goto LABEL_33;
  }
  if ( &`typeinfo for'enc_next_ready_struct == (void **)8 )
  {
    temp_4 = *(enc_next_struct_0 *)_cxa_get_exception_ptr(v6);
    _cxa_begin_catch(v49);
    v52 = temp_4.ourroundkeys;
    _cxa_end_catch();
    Unwind_Resume(v52);
  }
LABEL_65:
  _cxa_begin_catch(v6);
  _cxa_end_catch();
  return 0;
}
```

但是switch

```assembly
switch ( control1 ){
    case 0x5208:
        v8 = (struct_of_step3 *)_cxa_allocate_exception(1ui64);
        struct_of_step3::struct_of_step3(v8);
        _cxa_throw(v8, (struct type_info *)&`typeinfo for'struct_of_step3, 0i64);
    case 0x6591:
        v5 = (struct_of_step1 *)_cxa_allocate_exception(1ui64);
        struct_of_step1::struct_of_step1(v5);
        if ( &`typeinfo for'struct_of_step1 == (void **)3 )
        {
        _cxa_begin_catch(v6);
        v17 = operation1(sum1, i);
        v18 = operation4(v1);
        v19 = operation1(v18, k3_0);
        v20 = operation1(v1, sum1);
        v21 = operation2(v1);
        v22 = operation1(v21, k2_0);
        v23 = operation3(v22, v20);
        v24 = operation3(v23, v19);
        v0 += operation3(v24, v17);
        v25 = operation1(sum2, i);
        v26 = operation4(v3);
        v27 = operation1(v26, k3_0);
        v28 = operation1(v3, sum2);
        v29 = operation2(v3);
        v30 = operation1(v29, k2_0);
        v31 = operation3(v30, v28);
        v32 = operation3(v31, v27);
        v2 += operation3(v32, v25);
        _cxa_end_catch();
        }
        else if ( &`typeinfo for'struct_of_step1 == (void **)4 )
        {
        _cxa_begin_catch(v6);
        v33 = operation1(sum1, i);
        v34 = operation4(v0);
        v35 = operation1(v34, k1_0);
        v36 = operation1(v0, sum1);
        v37 = operation2(v0);
        v38 = operation1(v37, k0_0);
        v39 = operation3(v38, v36);
        v40 = operation3(v39, v35);
        v1 += operation3(v40, v33);
        v41 = operation1(sum2, i);
        v42 = operation4(v2);
        v43 = operation1(v42, k1_0);
        v44 = operation1(v2, sum1);
        v45 = operation2(v2);
        v46 = operation1(v45, k0_0);
        v47 = operation3(v46, v44);
        v48 = operation3(v47, v43);
        v3 += operation3(v48, v41);
        _cxa_end_catch();
        }
        else
        {
        if ( &`typeinfo for'struct_of_step1 != (void **)2 )
            goto LABEL_65;
        _cxa_begin_catch(v6);
        sum1 = operation1(sum1, delta);
        sum2 = operation1(sum2, delta);
        _cxa_end_catch();
        }
        break;
    case 0x10A9:
        v7 = (struct_of_step2 *)_cxa_allocate_exception(1ui64);
        struct_of_step2::struct_of_step2(v7);
        _cxa_throw(v7, (struct type_info *)&`typeinfo for'struct_of_step2, 0i64);
}
```

这里的逻辑还是比较模糊，我们可以查看块

![]({{site.baseurl}}/img/CplusExceptionEncrypt/rdx.jpg)

可以知道执行哪个操作是由寄存器rdx的值来决定的，通过动调来知道每个值对应的操作，

我们可以知道程序加密由三部分组成，第一部分是魔改的tea，第二部分是异或操作，第三部分是魔改的AES加密，对轮秘钥生成和第一次`AddRoundKey`和`SubBytes`做了修改。

```assembly
void __cdecl enc_next_ready(uint8_t *key, uint8_t *roundkeys)
{
  uint8_t *v2; // rdx
  uint8_t *v3; // rax
  char *v4; // rax
  char v5; // r8
  uint8_t v6; // cl
  uint8_t *v7; // rax
  uint8_t temp_1; // [rsp+5h] [rbp-1Bh]
  uint8_t temp_2; // [rsp+6h] [rbp-1Ah]
  uint8_t temp_3; // [rsp+7h] [rbp-19h]
  uint8_t i; // [rsp+17h] [rbp-9h]
  uint8_t ia; // [rsp+17h] [rbp-9h]
  uint8_t *last4bytes; // [rsp+18h] [rbp-8h]

  for ( i = 0; i <= 0xFu; ++i )
  {
    v2 = key++;
    v3 = roundkeys++;
    *v3 = *v2;
  }
  last4bytes = roundkeys + 0xFFFFFFFC;
  for ( ia = 0; ia <= 9u; ++ia )
  {
    temp_3 = S[*last4bytes];
    temp_1 = S[last4bytes[2]];
    temp_2 = S[last4bytes[3]];
    *roundkeys = roundkeys[0xFFFFFFF0] ^ S[last4bytes[1]] ^ RC[ia];
    roundkeys[1] = roundkeys[0xFFFFFFF1i64] ^ temp_1;
    roundkeys[2] = roundkeys[0xFFFFFFF2i64] ^ temp_2;
    roundkeys[3] = roundkeys[0xFFFFFFF3i64] ^ temp_3;
    roundkeys[4] = roundkeys[0xFFFFFFF4i64] ^ last4bytes[4];
    roundkeys[5] = roundkeys[0xFFFFFFF5i64] ^ last4bytes[5];
    roundkeys[6] = roundkeys[0xFFFFFFF6i64] ^ last4bytes[6];
    roundkeys[7] = roundkeys[0xFFFFFFF7i64] ^ last4bytes[7];
    roundkeys[8] = roundkeys[0xFFFFFFF8i64] ^ last4bytes[8];
    roundkeys[9] = roundkeys[0xFFFFFFF9i64] ^ last4bytes[9];
    roundkeys[0xA] = roundkeys[0xFFFFFFFAi64] ^ last4bytes[0xA];
    roundkeys[0xB] = roundkeys[0xFFFFFFFBi64] ^ last4bytes[0xB];
    roundkeys[0xC] = roundkeys[0xFFFFFFFCi64] ^ last4bytes[0xC];
    roundkeys[0xD] = roundkeys[0xFFFFFFFDi64] ^ last4bytes[0xD];
    roundkeys[0xE] = roundkeys[0xFFFFFFFEi64] ^ last4bytes[0xE];
    v4 = (char *)(last4bytes + 0xF);
    last4bytes += 0x10;
    v5 = *v4;
    v6 = roundkeys[0xFFFFFFFFi64];
    v7 = roundkeys + 0xF;
    roundkeys += 0x10;
    *v7 = v6 ^ v5;
  }
}
```

这里不知道为什么main函数种调不出来enc_next

```assembly
void __cdecl enc_next(uint8_t *roundkeys, uint8_t *plaintext, uint8_t *ciphertext)
{
  _DWORD *v3; // rax
  _BYTE *v4; // rax
  __int64 v5; // rdx
  _DWORD *v6; // rax
  _QWORD *v7; // rax
  void *v8; // rbx
  uint8_t *v9; // rax
  uint8_t *v10; // rax
  void *v11; // rbx
  void *v12; // rax
  uint8_t *v13; // rax
  std::__cxx11::string temp_2; // [rsp+20h] [rbp-60h] BYREF
  uint8_t tmp[16]; // [rsp+40h] [rbp-40h] BYREF
  char v16; // [rsp+5Eh] [rbp-22h] BYREF
  uint8_t t; // [rsp+5Fh] [rbp-21h]
  double temp_1; // [rsp+60h] [rbp-20h]
  int temp_0; // [rsp+6Ch] [rbp-14h]
  char temp; // [rsp+73h] [rbp-Dh]
  int a; // [rsp+74h] [rbp-Ch]
  int cnt; // [rsp+78h] [rbp-8h]
  uint8_t j; // [rsp+7Eh] [rbp-2h]
  uint8_t i; // [rsp+7Fh] [rbp-1h]

  v3 = _cxa_allocate_exception(4ui64);
  *v3 = 1;
  if ( refptr__ZTIi != (struct type_info *const)1 )
    Unwind_Resume((__int64)v3);
  a = *(_DWORD *)_cxa_begin_catch(v3);
  for ( i = 0; i <= 0xFu; ++i )
  {
    v10 = roundkeys++;
    ciphertext[i] = *v10 ^ plaintext[i] ^ 0x66;
  }
  _cxa_end_catch();
  j = 1;
LABEL_2:
  if ( j <= 9u )
  {
    for ( cnt = 0; ; ++cnt )
    {
      if ( cnt == 4 )
      {
        ++j;
        goto LABEL_2;
      }
      if ( cnt == 1 )
      {
        v6 = _cxa_allocate_exception(4ui64);
        *v6 = 0x29A;
        _cxa_throw(v6, refptr__ZTIi, 0i64);
      }
      if ( cnt > 1 )
      {
        if ( cnt == 2 )
        {
          v7 = _cxa_allocate_exception(8ui64);
          *v7 = 0x4050AA3D70A3D70Ai64;
          _cxa_throw(v7, refptr__ZTId, 0i64);
        }
        if ( cnt != 3 )
          continue;
        v8 = _cxa_allocate_exception(0x20ui64);
        std::allocator<char>::allocator(&v16);
        std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(v8, "66666\n", &v16);
        v4 = (_BYTE *)std::allocator<char>::~allocator(&v16);
        v5 = (__int64)&`typeinfo for'std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>;
      }
      else
      {
        if ( cnt )
          continue;
        v4 = _cxa_allocate_exception(1ui64);
        *v4 = 0x36;
        v5 = (__int64)refptr__ZTIc;
      }
      v11 = v4;
      if ( v5 == 2 )
      {
        temp = *(_BYTE *)_cxa_begin_catch(v4);
        for ( i = 0; i <= 0xFu; ++i )
          tmp[i] = INV_S[ciphertext[i]];
        goto LABEL_40;
      }
      if ( v5 > 2 )
      {
        if ( v5 == 3 )
        {
          temp_1 = *(double *)_cxa_begin_catch(v4);
          for ( i = 0; i <= 0xFu; i += 4 )
          {
            t = tmp[i + 2] ^ tmp[i + 1] ^ tmp[i] ^ tmp[i + 3];
            ciphertext[i] = t ^ tmp[i] ^ mul2(tmp[i] ^ tmp[i + 1]);
            ciphertext[i + 1] = t ^ tmp[i + 1] ^ mul2(tmp[i + 1] ^ tmp[i + 2]);
            ciphertext[i + 2] = t ^ tmp[i + 2] ^ mul2(tmp[i + 2] ^ tmp[i + 3]);
            ciphertext[i + 3] = t ^ tmp[i + 3] ^ mul2(tmp[i + 3] ^ tmp[i]);
          }
LABEL_40:
          _cxa_end_catch();
          continue;
        }
        if ( v5 != 4 )
        {
LABEL_50:
          _cxa_begin_catch(v4);
          _cxa_end_catch();
          return;
        }
        v12 = _cxa_get_exception_ptr(v4);
        std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(&temp_2, v12);
        _cxa_begin_catch(v11);
        for ( i = 0; i <= 0xFu; ++i )
        {
          v13 = roundkeys++;
          ciphertext[i] ^= *v13;
        }
        std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&temp_2);
        _cxa_end_catch();
      }
      else
      {
        if ( v5 != 1 )
          goto LABEL_50;
        temp_0 = *(_DWORD *)_cxa_begin_catch(v4);
        inv_shift_rows(tmp);
        _cxa_end_catch();
      }
    }
  }
  for ( i = 0; i <= 0xFu; ++i )
    ciphertext[i] = S[ciphertext[i]];
  shift_rows(ciphertext);
  for ( i = 0; i <= 0xFu; ++i )
  {
    v9 = roundkeys++;
    ciphertext[i] ^= *v9;
  }
}
```

这里不想做了，网上抄一个脚本

```assembly
#include <stdint.h>
#include <stdio.h>

#include "aes.h"
#include <stdlib.h>

 /*
  * round constants
  */
static uint8_t RC[] = { 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36 };

/*
 * Sbox
 */
static uint8_t SBOX[256] = {
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16 };

/*
 * Inverse Sboxs
 */
static uint8_t INV_SBOX[256] = {
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d };

/**
 * https://en.wikipedia.org/wiki/Finite_field_arithmetic
 * Multiply two numbers in the GF(2^8) finite field defined
 * by the polynomial x^8 + x^4 + x^3 + x + 1 = 0
 * We do use mul2(int8_t a) but not mul(uint8_t a, uint8_t b)
 * just in order to get a higher speed.
 */
static inline uint8_t mul2(uint8_t a)
{
    return (a & 0x80) ? ((a << 1) ^ 0x1b) : (a << 1);
}

/**
 * @purpose:    ShiftRows
 * @descrption:
 *  Row0: s0  s4  s8  s12   <<< 0 byte
 *  Row1: s1  s5  s9  s13   <<< 1 byte
 *  Row2: s2  s6  s10 s14   <<< 2 bytes
 *  Row3: s3  s7  s11 s15   <<< 3 bytes
 */
static void shift_rows(uint8_t* state)
{
    uint8_t temp;
    // row1
    temp = *(state + 1);
    *(state + 1) = *(state + 5);
    *(state + 5) = *(state + 9);
    *(state + 9) = *(state + 13);
    *(state + 13) = temp;
    // row2
    temp = *(state + 2);
    *(state + 2) = *(state + 10);
    *(state + 10) = temp;
    temp = *(state + 6);
    *(state + 6) = *(state + 14);
    *(state + 14) = temp;
    // row3
    temp = *(state + 15);
    *(state + 15) = *(state + 11);
    *(state + 11) = *(state + 7);
    *(state + 7) = *(state + 3);
    *(state + 3) = temp;
}

/**
 * @purpose:    Inverse ShiftRows
 * @description
 *  Row0: s0  s4  s8  s12   >>> 0 byte
 *  Row1: s1  s5  s9  s13   >>> 1 byte
 *  Row2: s2  s6  s10 s14   >>> 2 bytes
 *  Row3: s3  s7  s11 s15   >>> 3 bytes
 */
static void inv_shift_rows(uint8_t* state)
{
    uint8_t temp;
    // row1
    temp = *(state + 13);
    *(state + 13) = *(state + 9);
    *(state + 9) = *(state + 5);
    *(state + 5) = *(state + 1);
    *(state + 1) = temp;
    // row2
    temp = *(state + 14);
    *(state + 14) = *(state + 6);
    *(state + 6) = temp;
    temp = *(state + 10);
    *(state + 10) = *(state + 2);
    *(state + 2) = temp;
    // row3
    temp = *(state + 3);
    *(state + 3) = *(state + 7);
    *(state + 7) = *(state + 11);
    *(state + 11) = *(state + 15);
    *(state + 15) = temp;
}

void aes_key_schedule_128(const uint8_t* key, uint8_t* roundkeys)
{

    uint8_t temp[4];
    uint8_t* last4bytes; // point to the last 4 bytes of one round
    uint8_t* lastround;
    uint8_t i;

    for (i = 0; i < 16; ++i)
    {
        *roundkeys++ = *key++;
    }

    last4bytes = roundkeys - 4;
    for (i = 0; i < AES_ROUNDS; ++i)
    {
        // k0-k3 for next round
        temp[3] = SBOX[*last4bytes++];
        temp[0] = SBOX[*last4bytes++];
        temp[1] = SBOX[*last4bytes++];
        temp[2] = SBOX[*last4bytes++];
        temp[0] ^= RC[i];
        lastround = roundkeys - 16;
        *roundkeys++ = temp[0] ^ *lastround++;
        *roundkeys++ = temp[1] ^ *lastround++;
        *roundkeys++ = temp[2] ^ *lastround++;
        *roundkeys++ = temp[3] ^ *lastround++;
        // k4-k7 for next round
        *roundkeys++ = *last4bytes++ ^ *lastround++;
        *roundkeys++ = *last4bytes++ ^ *lastround++;
        *roundkeys++ = *last4bytes++ ^ *lastround++;
        *roundkeys++ = *last4bytes++ ^ *lastround++;
        // k8-k11 for next round
        *roundkeys++ = *last4bytes++ ^ *lastround++;
        *roundkeys++ = *last4bytes++ ^ *lastround++;
        *roundkeys++ = *last4bytes++ ^ *lastround++;
        *roundkeys++ = *last4bytes++ ^ *lastround++;
        // k12-k15 for next round
        *roundkeys++ = *last4bytes++ ^ *lastround++;
        *roundkeys++ = *last4bytes++ ^ *lastround++;
        *roundkeys++ = *last4bytes++ ^ *lastround++;
        *roundkeys++ = *last4bytes++ ^ *lastround++;
    }
}

void aes_encrypt_128(const uint8_t* roundkeys, const uint8_t* plaintext, uint8_t* ciphertext)
{

    uint8_t tmp[16], t;
    uint8_t i, j;

    // first AddRoundKey
    for (i = 0; i < AES_BLOCK_SIZE; ++i)
    {
        *(ciphertext + i) = *(plaintext + i) ^ *roundkeys++ ^ 0x66;
    }

    // 9 rounds
    for (j = 1; j < AES_ROUNDS; ++j)
    {

        // SubBytes
        for (i = 0; i < AES_BLOCK_SIZE; ++i)
        {
            *(tmp + i) = INV_SBOX[*(ciphertext + i)];
        }
        inv_shift_rows(tmp);
        /*
         * MixColumns
         * [02 03 01 01]   [s0  s4  s8  s12]
         * [01 02 03 01] . [s1  s5  s9  s13]
         * [01 01 02 03]   [s2  s6  s10 s14]
         * [03 01 01 02]   [s3  s7  s11 s15]
         */
        for (i = 0; i < AES_BLOCK_SIZE; i += 4)
        {
            t = tmp[i] ^ tmp[i + 1] ^ tmp[i + 2] ^ tmp[i + 3];
            ciphertext[i] = mul2(tmp[i] ^ tmp[i + 1]) ^ tmp[i] ^ t;
            ciphertext[i + 1] = mul2(tmp[i + 1] ^ tmp[i + 2]) ^ tmp[i + 1] ^ t;
            ciphertext[i + 2] = mul2(tmp[i + 2] ^ tmp[i + 3]) ^ tmp[i + 2] ^ t;
            ciphertext[i + 3] = mul2(tmp[i + 3] ^ tmp[i]) ^ tmp[i + 3] ^ t;
        }

        // AddRoundKey
        for (i = 0; i < AES_BLOCK_SIZE; ++i)
        {
            *(ciphertext + i) ^= *roundkeys++;
        }
    }

    // last round
    for (i = 0; i < AES_BLOCK_SIZE; ++i)
    {
        *(ciphertext + i) = SBOX[*(ciphertext + i)];
    }
    shift_rows(ciphertext);
    for (i = 0; i < AES_BLOCK_SIZE; ++i)
    {
        *(ciphertext + i) ^= *roundkeys++;
    }
}

void aes_decrypt_128(const uint8_t* roundkeys, const uint8_t* ciphertext, uint8_t* plaintext)
{

    uint8_t tmp[16];
    uint8_t t, u, v;
    uint8_t i, j;

    roundkeys += 160;

    // first round
    for (i = 0; i < AES_BLOCK_SIZE; ++i)
    {
        *(plaintext + i) = *(ciphertext + i) ^ *(roundkeys + i);
    }
    roundkeys -= 16;
    inv_shift_rows(plaintext);
    for (i = 0; i < AES_BLOCK_SIZE; ++i)
    {
        *(plaintext + i) = INV_SBOX[*(plaintext + i)];
    }

    for (j = 1; j < AES_ROUNDS; ++j)
    {

        // Inverse AddRoundKey
        for (i = 0; i < AES_BLOCK_SIZE; ++i)
        {
            *(tmp + i) = *(plaintext + i) ^ *(roundkeys + i);
        }

        /*
         * Inverse MixColumns
         * [0e 0b 0d 09]   [s0  s4  s8  s12]
         * [09 0e 0b 0d] . [s1  s5  s9  s13]
         * [0d 09 0e 0b]   [s2  s6  s10 s14]
         * [0b 0d 09 0e]   [s3  s7  s11 s15]
         */
        for (i = 0; i < AES_BLOCK_SIZE; i += 4)
        {
            t = tmp[i] ^ tmp[i + 1] ^ tmp[i + 2] ^ tmp[i + 3];
            plaintext[i] = t ^ tmp[i] ^ mul2(tmp[i] ^ tmp[i + 1]);
            plaintext[i + 1] = t ^ tmp[i + 1] ^ mul2(tmp[i + 1] ^ tmp[i + 2]);
            plaintext[i + 2] = t ^ tmp[i + 2] ^ mul2(tmp[i + 2] ^ tmp[i + 3]);
            plaintext[i + 3] = t ^ tmp[i + 3] ^ mul2(tmp[i + 3] ^ tmp[i]);
            u = mul2(mul2(tmp[i] ^ tmp[i + 2]));
            v = mul2(mul2(tmp[i + 1] ^ tmp[i + 3]));
            t = mul2(u ^ v);
            plaintext[i] ^= t ^ u;
            plaintext[i + 1] ^= t ^ v;
            plaintext[i + 2] ^= t ^ u;
            plaintext[i + 3] ^= t ^ v;
        }

        // Inverse ShiftRows
        shift_rows(plaintext);

        // Inverse SubBytes
        for (i = 0; i < AES_BLOCK_SIZE; ++i)
        {
            *(plaintext + i) = SBOX[*(plaintext + i)];
        }

        roundkeys -= 16;
    }

    // last AddRoundKey
    for (i = 0; i < AES_BLOCK_SIZE; ++i)
    {
        *(plaintext + i) ^= *(roundkeys + i) ^ 0x66;
    }
}

void tea_encrypt(uint32_t* v, uint32_t* k) {
    uint32_t v0 = v[0], v1 = v[1], v2 = v[2], v3 = v[3], sum1 = 0, sum2 = 0, i;           /* set up */
    uint32_t delta = 0x73637466;                     /* a key schedule constant */
    uint32_t k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];   /* cache key */
    uint32_t temp;
    for (i = 0; i < 32; i++) {                       /* basic cycle start */
        sum1 += delta;
        sum2 += delta;
        temp = ((v1 << 4) + k2) ^ (v1 + sum1) ^ ((v1 >> 5) + k3) ^ (sum1+i);
        v0 += temp;
        temp = ((v3 << 4) + k2) ^ (v3 + sum2) ^ ((v3 >> 5) + k3) ^ (sum2+i);
        v2 += temp;


        temp = ((v0 << 4) + k0) ^ (v0 + sum1) ^ ((v0 >> 5) + k1) ^ (sum1+i);
        v1 += temp;

        temp = ((v2 << 4) + k0) ^ (v2 + sum2) ^ ((v2 >> 5) + k1) ^ (sum2+i);
        v3 += temp;

    }                                              /* end cycle */
    v[0] = v0; v[1] = v1; v[2] = v2; v[3] = v3;
    printf("sum: %x\n", sum1);

}
//解密函数
void tea_decrypt(uint32_t* v, uint32_t* k)
{
    uint32_t v0 = v[0], v1 = v[1], v2 = v[2], v3 = v[3], sum1 = 0x6c6e8cc0, sum2 = 0x6c6e8cc0;// 0x6c6e90a0;
    uint32_t delta = 0x73637466;
    uint32_t k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];
    for (int i = 31; i >= 0; i--)
    {
        v3 -= ((v2 << 4) + k0) ^ (v2 + sum2) ^ ((v2 >> 5) + k1) ^ (sum2+i);

        v1 -= ((v0 << 4) + k0) ^ (v0 + sum1) ^ ((v0 >> 5) + k1) ^ (sum1+i);


        v2 -= ((v3 << 4) + k2) ^ (v3 + sum2) ^ ((v3 >> 5) + k3) ^ (sum2+i);

        v0 -= ((v1 << 4) + k2) ^ (v1 + sum1) ^ ((v1 >> 5) + k3) ^ (sum1+i);

        sum2 -= delta;
        sum1 -= delta;
    }
    v[0] = v0;
    v[1] = v1; 
    v[2] = v2; 
    v[3] = v3;
    // printf("v:%s", v);
}
int main()
{
    unsigned char* dec1 = (unsigned char*)malloc(0x20);
    unsigned char* dec = (unsigned char*)malloc(0x20);
    unsigned char* roundKeys = (unsigned char*)malloc(0x200);
    aes_key_schedule_128("Welcome_to_sctf!", roundKeys);
    unsigned char enc1[] = { 0xBE, 0x1C, 0xB3, 0xF3, 0xA1, 0xF4, 0xE4, 0x63, 0x11, 0xE1,
                             0x1C, 0x6B, 0x54, 0x0A, 0xDF, 0x74 };
    unsigned char enc2[] = { 0xF2, 0x93, 0x55, 0xDA,0x48, 0xFC, 0xA2, 0x3C, 
                             0x89, 0x63, 0x2E, 0x7F, 0x8D, 0xA4,0x6D, 0x4E };
  

    aes_decrypt_128(roundKeys, enc1, dec);
    ((uint32_t*)dec)[0] ^= 0x73;
    ((uint32_t*)dec)[1] ^= 0x63;
    ((uint32_t*)dec)[2] ^= 0x74;
    ((uint32_t*)dec)[3] ^= 0x66;

    tea_decrypt((uint32_t*)(dec), "Welcome_to_sctf!");
    puts("\nflag1:");
    for (int i = 0; i < 16; i++)
    {
        printf("%c", dec[i]);
    }
    
    aes_decrypt_128(roundKeys, enc2, dec);
    ((uint32_t*)dec)[0] ^= 0x73;
    ((uint32_t*)dec)[1] ^= 0x63;
    ((uint32_t*)dec)[2] ^= 0x74;
    ((uint32_t*)dec)[3] ^= 0x66;

    tea_decrypt((uint32_t*)(dec), "Welcome_to_sctf!");
    puts("\nflag2:");
    for (int i = 0; i < 16; i++)
    {
        printf("%c", dec[i]);
    }

    return 0;
}
```

SCTF{5277cc2af8f1155f7a61030f46fdf9df}