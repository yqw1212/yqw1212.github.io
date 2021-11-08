---
layout: post
title:  Eat_something(陇原战"疫"2021网络安全大赛)
date:   2021-11-08 00:08:01 +0300
image:  2021-11-08-woman.jpg
tags:   [ctf,reverse,wasm]
---

点击click按钮，显示

> You are wrong!

查看该按钮的属性

```assembly
<button type="button" onclick="nice()">clickme</button>
```

查看js代码中的nice函数

```assembly
function nice(){
    var inpObj = document.getElementById("id1");
    document.write(checkright(inpObj.value))
    if(checkright(inpObj.value) === "You are right!"){
        document.write(inpObj.value)
    }
}
    
```

查看Eat_something.js，在其中搜索checkright函数

```assembly
/** @type {function(...*):?} */
var _checkright = Module["_checkright"] = createExportWrapper("checkright");
```

至此确认是wasm无疑

#### jeb反编译

在浏览器把wasm文件（其实是wat文件）下载下来，使用[wabt](https://github.com/WebAssembly/wabt)中的[wat2wasm](https://webassembly.github.io/wabt/doc/wat2wasm.1.html)工具转为wasm文件，在jeb中打开反编译

```assembly
int checkright(int param0) {
    int v0 = __g0 - 96;

    *(int*)(v0 + 88) = param0;
    *(unsigned short*)(v0 + 72) = gvar_418;
    *(unsigned long long*)(v0 + 64) = gvar_410;
    *(unsigned long long*)((int)&gvar_38 + v0) = gvar_408;
    *(unsigned long long*)(v0 + 48) = gvar_400;
    *(long long*)(v0 + 40) = *(long long*)&aYou_are_right_[7];
    *(long long*)(v0 + 33) = *(long long*)&aYou_are_right_[0];
    *(long long*)(v0 + 25) = *(long long*)&aYou_are_wrong_[7];
    *(long long*)(v0 + 18) = *(long long*)&aYou_are_wrong_[0];
    *(int*)(v0 + 12) = 0;
    while(*(int*)(v0 + 12) < 26) {
        if((int)*(char*)(*(int*)(v0 + 88) + *(int*)(v0 + 12)) * 2 != *(int*)(v0 + 12)) {
            *(int*)(v0 + 92) = v0 + 18;
            return *(int*)(v0 + 92);
        }
        *(int*)(v0 + 12) = *(int*)(v0 + 12) + &gvar_1;
    }

    *(int*)(v0 + 92) = v0 + 33;
    return *(int*)(v0 + 92);
}
```

gvar_400、gvar_408、gvar_410、gvar_418

```assembly
.data:00000400    gvar_400         dq AFF089AC85AA8B86h                      ; xref: checkright+7Ah (data-adv)
.data:00000408    gvar_408         dq E56EBFB2DDD669D8h                      ; xref: checkright+6Bh (data-adv)
.data:00000410    gvar_410         dq 7DF28BBCD5CC99AEh                      ; xref: checkright+51h (data-adv)
.data:00000418    gvar_418         dw E37Ah    
```

如果比较不相等则失败，v0 + 12为索引值0~26，v0 + 88为传入的参数即正确的flag，这里要求flag字符串中的字符等于索引值，明显存在问题，换用其他方法。

#### wasm2c

将wasm文件[**wasm2c**](https://webassembly.github.io/wabt/doc/wasm2c.1.html)工具转为c文件

```assembly
wasm2c Eat_something.wasm -o Eat_something.c
```

将c文件编译

```assembly
gcc -c Eat_something.c
```

得到.o文件，ida打开

```assembly
__int64 __fastcall w2c_checkright(unsigned int a1)
{
  __int64 v2; // [rsp+10h] [rbp-160h]
  unsigned int v3; // [rsp+20h] [rbp-150h]
  unsigned int v4; // [rsp+24h] [rbp-14Ch]
  __int64 v5; // [rsp+30h] [rbp-140h]
  __int64 v6; // [rsp+38h] [rbp-138h]
  __int64 v7; // [rsp+40h] [rbp-130h]
  __int64 v8; // [rsp+48h] [rbp-128h]
  __int64 v9; // [rsp+50h] [rbp-120h]
  __int64 v10; // [rsp+58h] [rbp-118h]
  char v11; // [rsp+B8h] [rbp-B8h]
  unsigned int v12; // [rsp+BCh] [rbp-B4h]
  int v13; // [rsp+C4h] [rbp-ACh]
  int v14; // [rsp+C8h] [rbp-A8h]
  unsigned int v15; // [rsp+D4h] [rbp-9Ch]
  unsigned int v16; // [rsp+148h] [rbp-28h]
  unsigned int v17; // [rsp+164h] [rbp-Ch]

  if ( ++wasm_rt_call_stack_depth > 0x1F4u )
    wasm_rt_trap(7LL);
  v17 = w2c_g0 - 0x60;
  i32_store(&w2c_memory, (unsigned int)(w2c_g0 - 0x60) + 0x58LL, a1);
  v16 = i32_load16_u(&w2c_memory, 0x418LL);
  i32_store16(&w2c_memory, v17 + 0x48, v16);
  v10 = i64_load(&w2c_memory, 0x410LL);
  i64_store(&w2c_memory, v17 + 0x40, v10);
  v9 = i64_load(&w2c_memory, 0x408LL);
  i64_store(&w2c_memory, v17 + 0x38, v9);
  v8 = i64_load(&w2c_memory, 0x400LL);
  i64_store(&w2c_memory, v17 + 0x30, v8);
  v7 = i64_load(&w2c_memory, 0x421LL);
  i64_store(&w2c_memory, v17 + 0x28, v7);
  v6 = i64_load(&w2c_memory, 0x41ALL);
  i64_store(&w2c_memory, v17 + 0x21, v6);
  v5 = i64_load(&w2c_memory, 0x430LL);
  i64_store(&w2c_memory, v17 + 0x19, v5);
  v2 = i64_load(&w2c_memory, 0x429LL);
  i64_store(&w2c_memory, v17 + 0x12, v2);
  i32_store(&w2c_memory, v17 + 0xCLL, 0LL);
  while ( (int)i32_load(&w2c_memory, v17 + 0xCLL) < 0x1A )
  {
    v15 = i32_load(&w2c_memory, v17 + 0xCLL) + v17 + 0x30;
    v14 = (unsigned __int8)i32_load8_u(&w2c_memory, v15);
    v13 = i32_load(&w2c_memory, v17 + 0x58LL);
    v12 = i32_load(&w2c_memory, v17 + 0xCLL) + v13;
    v11 = i32_load8_u(&w2c_memory, v12);
    if ( v14 != ((unsigned int)i32_load(&w2c_memory, v17 + 0xCLL) ^ (2 * v11)) )
    {
      i32_store(&w2c_memory, v17 + 0x5CLL, v17 + 0x12);
      goto LABEL_9;
    }
    v3 = i32_load(&w2c_memory, v17 + 0xCLL) + 1;
    i32_store(&w2c_memory, v17 + 0xCLL, v3);
  }
  i32_store(&w2c_memory, v17 + 0x5CLL, v17 + 0x21);
LABEL_9:
  v4 = i32_load(&w2c_memory, v17 + 0x5CLL);
  --wasm_rt_call_stack_depth;
  return v4;
}
```

看一下i32_load函数

```assembly
__int64 __fastcall i32_load(_QWORD *a1, __int64 a2)
{
  return *(unsigned int *)(*a1 + a2);
}
```

i32_load8_u

```assembly
__int64 __fastcall i32_load8_u(_QWORD *a1, __int64 a2)
{
  return *(unsigned __int8 *)(*a1 + a2);
}
```

简单分析一下循环体

i32_load(&w2c_memory, v17 + 0xCLL)为索引，相当于w2c_memory[v17 + 0xCLL]

v15 = i32_load(&w2c_memory, v17 + 0xCLL) + v17 + 0x30即v17 + 0x30+index，是一个地址，而根据之前jeb反编译的结果我们知道v17 + 0x30是程序中预设的一串字符串（jeb中的gvar_400）。

v14是在上一步的地址取值，即程序中的字符串

v13 = i32_load(&w2c_memory, v17 + 0x58LL)是传入函数的参数，也就是正确的字符串的首地址

v12即v13+index，是一个地址。

v11在v12地址取值，取得的是传入的字符串

然后进行比较，要满足条件

程序中的字符串==索引^(2*正确的字符串)

到data段提取字符串（jeb的话是小端，注意顺序），写python脚本解密

```assembly
data = [0x86, 0x8B, 0xAA, 0x85, 0xAC, 0x89, 0xF0, 0xAF, 0xD8, 0x69,
        0xD6, 0xDD, 0xB2, 0xBF, 0x6E, 0xE5, 0xAE, 0x99, 0xCC, 0xD5,
        0xBC, 0x8B, 0xF2, 0x7D, 0x7A, 0xE3]

flag = ""
for i in range(len(data)):
    flag += chr((data[i] ^ i)//2)

print(flag)
```

CETCTF{Th0nk_Y0u_DocTOr51}

#### [**wasm-decompile**](https://webassembly.github.io/wabt/doc/wasm-decompile.1.html)

发现使用这个方法也不是不能看

```assembly
export memory memory(initial: 256, max: 256);

global g_a:int = 5243984;
global g_b:int = 0;
global g_c:int = 0;

export table indirect_function_table:funcref(min: 1, max: 1);

data d_inzYouarerightYouarewrong(offset: 1024) = 
  "\86\8b\aa\85\ac\89\f0\af\d8i\d6\dd\b2\bfn\e5\ae\99\cc\d5\bc\8b\f2}z\e3"
  "You are right!\00You are wrong!\00";

export function wasm_call_ctors() {
  emscripten_stack_init()
}

export function checkright(a:int):int {
  var b:int = g_a;
  var c:int = 96;
  var d:int_ptr = b - c;
  d[22] = a;
  var e:int = 48;
  var f:int = d + e;
  var g:long_ptr = f;
  var h:int = 24;
  var i:short_ptr = g + h;
  var j:int = 0;
  var k:int = j[524]:ushort;
  i[0] = k;
  var l:int = 16;
  var m:long_ptr = g + l;
  var rb:long = j[130]:long;
  m[0] = rb;
  var n:int = 8;
  var o:long_ptr = g + n;
  var sb:long = j[129]:long;
  o[0] = sb;
  var tb:long = j[128]:long;
  g[0] = tb;
  var p:int = 33;
  var q:int = d + p;
  var r:long_ptr@1 = q;
  var s:int = 7;
  var t:long_ptr@1 = r + s;
  var u:long_ptr@1 = 0;
  var ub:long = u[1057];
  t[0] = ub;
  var vb:long = u[1050];
  r[0] = vb;
  var v:int = 18;
  var w:int = d + v;
  var x:long_ptr@1 = w;
  var y:int = 7;
  var z:long_ptr@1 = x + y;
  var aa:long_ptr@1 = 0;
  var wb:long = aa[1072];
  z[0] = wb;
  var xb:long = aa[1065];
  x[0] = xb;
  var ba:int = 0;
  d[3] = ba;
  loop L_c {
    var ca:int = d[3];
    var da:int = 26;
    var ea:int = ca;
    var fa:int = da;
    var ga:int = ea < fa;
    var ha:int = 1;
    var ia:int = ga & ha;
    if (eqz(ia)) goto B_b;
    var ja:int = d[3];
    var ka:int = 48;
    var la:int = d + ka;
    var ma:int = la;
    var na:ubyte_ptr = ma + ja;
    var oa:int = na[0];
    var pa:int = 255;
    var qa:int = oa & pa;
    var ra:int = d[22];
    var sa:int = d[3];
    var ta:ubyte_ptr = ra + sa;
    var ua:int = ta[0];
    var va:int = 24;
    var wa:int = ua << va;
    var xa:int = wa >> va;
    var ya:int = 1;
    var za:int = xa << ya;
    var ab:int = d[3];
    var bb:int = za ^ ab;
    var cb:int = qa;
    var db:int = bb;
    var eb:int = cb == db;
    var fb:int = 1;
    var gb:int = eb & fb;
    if (eqz(gb)) goto B_e;
    goto B_d;
    label B_e:
    var hb:int = 18;
    var ib:int = d + hb;
    var jb:int = ib;
    d[23] = jb;
    goto B_a;
    label B_d:
    var kb:int = d[3];
    var lb:int = 1;
    var mb:int = kb + lb;
    d[3] = mb;
    continue L_c;
  }
  unreachable;
  label B_b:
  var nb:int = 33;
  var ob:int = d + nb;
  var pb:int = ob;
  d[23] = pb;
  label B_a:
  var qb:int = d[23];
  return qb;
}

export function stackSave():int {
  return g_a
}

export function stackRestore(a:int) {
  g_a = a
}

export function stackAlloc(a:int):int {
  var b:int = g_a - a & -16;
  g_a = b;
  return b;
}

export function emscripten_stack_init() {
  g_c = 5243984;
  g_b = 1100 + 15 & -16;
}

export function emscripten_stack_get_free():int {
  return g_a - g_b
}

export function emscripten_stack_get_end():int {
  return g_b
}

function f_i(a:int):int {
  return 1
}

function f_j(a:int) {
}

function f_k(a:int) {
}

function f_l(a:int) {
}

function f_m():int {
  f_k(1080);
  return 1088;
}

function f_n() {
  f_l(1080)
}

export function fflush(a:int_ptr):int {
  var c:int;
  var b:int;
  if (eqz(a)) goto B_b;
  if (a[19] > -1) goto B_c;
  return f_p(a);
  label B_c:
  b = f_i(a);
  c = f_p(a);
  if (eqz(b)) goto B_a;
  f_j(a);
  return c;
  label B_b:
  c = 0;
  if (eqz(0[273]:int)) goto B_d;
  c = fflush(0[273]:int);
  label B_d:
  a = f_m()[0]:int;
  if (eqz(a)) goto B_e;
  loop L_f {
    b = 0;
    if (a[19] < 0) goto B_g;
    b = f_i(a);
    label B_g:
    if (a[5] <= a[7]) goto B_h;
    c = f_p(a) | c;
    label B_h:
    if (eqz(b)) goto B_i;
    f_j(a);
    label B_i:
    a = a[14];
    if (a) continue L_f;
  }
  label B_e:
  f_n();
  label B_a:
  return c;
}

function f_p(a:int):int {
  var c:int;
  if (a[5]:int <= a[7]:int) goto B_a;
  call_indirect(a, 0, 0, a[9]:int);
  if (a[5]:int) goto B_a;
  return -1;
  label B_a:
  var b:int = a[1]:int;
  if (b >= (c = a[2]:int)) goto B_b;
  call_indirect(a, i64_extend_i32_s(b - c), 1, a[10]:int);
  label B_b:
  a[7]:int = 0;
  a[2]:long = 0L;
  a[1]:long@4 = 0L;
  return 0;
}

export function errno_location():int {
  return 1096
}
```

