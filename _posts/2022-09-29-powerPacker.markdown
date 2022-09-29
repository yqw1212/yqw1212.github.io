---
layout: post
title:  powerPacked(CFI-CTF 2018)
date:   2022-09-29 00:08:01 +0300
image:  2022-09-29-loosestrife.jpg
tags:   [ctf,reverse,powerPC]
---

powerPC架构，用Retdec可以实现反编译

> python retdec-decompiler.py powerPacker

```assembly
// Address range: 0x100006bc - 0x100007f4
int main(int argc, char ** argv) {
    char * v1 = (char *)0x45484b7d; // bp-48, 0x100006f0
    int32_t v2; // 0x100006bc
    printf("Insert password : ", (int32_t)argv, v2, 0x45484b7d, 0x6b616e71, 0x78676172, L"mg", 0x7265);
    int32_t v3; // bp-80, 0x100006bc
    scanf("%31s", &v3, v2, 0x45484b7d, 0x6b616e71, 0x78676172, L"mg", 0x7265);
    for (int32_t i = 0; i < 21; i++) {
        char * v4 = (char *)(i + (int32_t)&v1); // 0x10000760
        *v4 = (char)((0x1000000 * (int32_t)*v4 - 0x2000000) / 0x1000000);
    }
    // 0x10000798
    if (strcmp(&v3, (int32_t *)&v1) == 0) {
        // 0x100007b8
        puts("Password is correct. Submit this as the flag.");
    } else {
        // 0x100007c8
        puts("Wrong password.");
    }
    // 0x100007d4
    return 0;
}
```

flag{i_love_powerpc}