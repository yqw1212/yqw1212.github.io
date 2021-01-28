---
layout: post
title:  anniu
date:   2021-01-26 00:01:01 +0300
image:  2021-01-26-horses.jpg
tags:   [ctf,SHADOWCTF]
---

## Reverse Engineering

这场ctf的逆向是什么鬼，离谱

### Warm-up

拖入ida

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  puts("you need patience to get the flag.");
  sleep(0xE10u);
  printf("{steppingstone}", argv);
  return 0;
}
```

shadowCTF{steppingstone}

### Unchallenging

再拖

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char s1; // [rsp+10h] [rbp-100h]

  puts("What is the password?");
  gets(&s1);
  if ( !strcmp(&s1, "op3n_se5ame") )
    puts("{Ar@b1an_night5}");
  else
    puts("Wrong!!");
  return 0;
}
```

shadowCTF{Ar@b1an_night5}

### Key2success

ida

```assembly
// local variable allocation has failed, the output may be wrong!
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax

  print_intro(*(_QWORD *)&argc, argv, envp);
  if ( (unsigned int)check_password() )
  {
    slow_type("Great. Well here is your key:\n");
    print_flag();
    result = 0;
  }
  else
  {
    slow_type("Hmm. This not the key.\n");
    result = 1;
  }
  return result;
}
```

print_flag()函数

```assembly
void print_flag()
{
  char *s; // ST08_8

  s = (char *)malloc(0xFFuLL);
  *(_QWORD *)s = 8531311361045654630LL;
  *((_QWORD *)s + 1) = 6877119176937271909LL;
  *((_QWORD *)s + 2) = 7453010356431054188LL;
  *((_WORD *)s + 12) = 125;
  puts(s);
  free(s);
}
```

显然硬上不太合适，查看check_pass()函数

```assembly
_BOOL8 check_password()
{
  char s[256]; // [rsp+0h] [rbp-100h]

  printf("> ");
  fgets(s, 255, stdin);
  s[strlen(s) - 1] = 0;
  return strcmp(s, the_password) == 0;
}
```

the_password是全局变量，值为"Constant_learning_is_the_key"

运行

![]({{site.baseurl}}/img/2021-01-26-flag.jpg)

### Thirsty crow

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rax
  __int64 v4; // rax
  __int64 v5; // rax
  __int64 v6; // rax
  __int64 v7; // rax
  __int64 v8; // rax
  __int64 v9; // rax
  __int64 v10; // rax
  char v12; // [rsp+0h] [rbp-170h]
  char v13[4]; // [rsp+24h] [rbp-14Ch]
  char v14[2]; // [rsp+28h] [rbp-148h]
  char v15[2]; // [rsp+2Ah] [rbp-146h]
  char v16[2]; // [rsp+2Dh] [rbp-143h]
  char v17[4]; // [rsp+30h] [rbp-140h]
  char dest; // [rsp+34h] [rbp-13Ch]
  char v19[4]; // [rsp+3Eh] [rbp-132h]
  char v20[2]; // [rsp+43h] [rbp-12Dh]
  char v21[4]; // [rsp+45h] [rbp-12Bh]
  char v22[4]; // [rsp+49h] [rbp-127h]
  char src[2]; // [rsp+4Dh] [rbp-123h]
  char v24[4]; // [rsp+50h] [rbp-120h]
  char v25[4]; // [rsp+54h] [rbp-11Ch]
  char v26[4]; // [rsp+58h] [rbp-118h]
  char v27[4]; // [rsp+5Ch] [rbp-114h]
  char s1; // [rsp+60h] [rbp-110h]
  int v29; // [rsp+16Ch] [rbp-4h]

  strcpy(v27, "_si");
  strcpy(v26, "sin");
  strcpy(v25, "_5i");
  strcpy(v24, "rty");
  strcpy(src, "th");
  strcpy(v22, "x_r");
  strcpy(v21, "_th");
  strcpy(v20, "x");
  strcpy(v19, "irty");
  strcpy(&dest, src);
  strcat(&dest, v19);
  v3 = std::operator<<<std::char_traits<char>>(
         &std::cout,
         " The crow is thirsty and he needs your help to gather stones to fill the pot");
  v4 = std::ostream::operator<<(v3, &std::endl<char,std::char_traits<char>>);
  std::operator<<<std::char_traits<char>>(v4, " > ");
  std::operator>><char,std::char_traits<char>>(&std::cin, &s1);
  strcat(&dest, v27);
  strcat(&dest, v20);
  v29 = strcmp(&s1, &dest);
  if ( v29 )
  {
    v10 = std::operator<<<std::char_traits<char>>(&std::cout, " Not enough stones :( ");
    std::ostream::operator<<(v10, &std::endl<char,std::char_traits<char>>);
  }
  else
  {
    strcpy(v17, "Thi");
    strcpy(v16, "e_");
    strcpy(v15, "ck");
    strcpy(v14, "0");
    strcpy(v13, "p0t");
    strcpy(&v12, v17);
    strcat(&v12, v24);
    strcat(&v12, v25);
    strcat(&v12, v22);
    strcat(&v12, v14);
    strcat(&v12, v15);
    strcat(&v12, v26);
    strcat(&v12, v21);
    strcat(&v12, v16);
    strcat(&v12, v13);
    v5 = std::ostream::operator<<(&std::cout, &std::endl<char,std::char_traits<char>>);
    v6 = std::operator<<<std::char_traits<char>>(v5, "shadowCTF{");
    v7 = std::operator<<<std::char_traits<char>>(v6, &v12);
    v8 = std::operator<<<std::char_traits<char>>(v7, "} ");
    v9 = std::ostream::operator<<(v8, &std::endl<char,std::char_traits<char>>);
    std::ostream::operator<<(v9, &std::endl<char,std::char_traits<char>>);
  }
  return 0;
}
```

无脑复制粘贴

shadowCTF{Thirty_5ix_r0cksin_the_p0t}

### Vault

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4[2]; // [rsp+12h] [rbp-AEh]
  __int64 v5; // [rsp+14h] [rbp-ACh]
  __int16 v6; // [rsp+1Ch] [rbp-A4h]
  char v7; // [rsp+1Eh] [rbp-A2h]
  char v8[8]; // [rsp+1Fh] [rbp-A1h]
  int v9; // [rsp+29h] [rbp-97h]
  char v10; // [rsp+2Dh] [rbp-93h]
  char v11[2]; // [rsp+2Eh] [rbp-92h]
  __int64 v12; // [rsp+30h] [rbp-90h]
  __int64 v13; // [rsp+38h] [rbp-88h]
  __int64 v14; // [rsp+40h] [rbp-80h]
  __int64 v15; // [rsp+48h] [rbp-78h]
  __int64 v16; // [rsp+50h] [rbp-70h]
  __int64 v17; // [rsp+58h] [rbp-68h]
  __int16 v18; // [rsp+60h] [rbp-60h]
  char format[4]; // [rsp+69h] [rbp-57h]
  char s2; // [rsp+70h] [rbp-50h]
  __int64 v21; // [rsp+90h] [rbp-30h]
  __int64 v22; // [rsp+98h] [rbp-28h]
  char v23; // [rsp+A0h] [rbp-20h]
  char s1[8]; // [rsp+ADh] [rbp-13h]
  int i; // [rsp+BCh] [rbp-4h]

  strcpy(s1, "hackers_access");
  for ( i = 10; i <= 19; ++i )
    ;
  v21 = 6874871693294006126LL;
  v22 = 7237970109966541168LL;
  v23 = 0;
  strcpy(format, "sh@d0w");
  puts("     .--------.");
  printf("    / .------. \\n", argv);
  printf("   / /         \\n");
  puts("   | |        | |");
  puts("   | |        | |");
  puts("  _| |________| |_");
  puts(".' |_|        |_| '.");
  puts("'._____ ____ _____.'");
  puts("|     .'____'.     |");
  puts("'.__.'.'    '.'.__.'");
  puts("'.__  Shad0w |  __.'");
  puts("|   '.'.____.'.'   |");
  puts("'.____'.____.'____.'");
  printf("'.________________.'");
  v12 = 8319381555649605443LL;
  v13 = 7359007639830339628LL;
  v14 = 2322295453215318380LL;
  v15 = 7292860951696724603LL;
  v16 = 7954818658380309343LL;
  v17 = 7234309835706033511LL;
  v18 = 125;
  strcpy(v11, "{");
  v9 = 1932931365;
  v10 = 0;
  strcpy(v8, "reversing");
  v5 = 7811881982471008089LL;
  v6 = 25701;
  v7 = 0;
  strcpy(v4, "}");
  puts("secure vault");
  puts("Enter our password:");
  __isoc99_scanf("%16s", &s2);
  if ( !strcmp(s1, &s2) )
  {
    puts("You Win");
    printf(format, &s2);
    printf(v11);
    printf(format);
    putchar(95);
    printf(v8);
    printf("_rul3s");
    printf(v4);
  }
  else
  {
    puts("You Failed");
  }
  return 0;
}
```

无脑复制粘贴

shadowCTF{sh@d0w_reversing_rul3s}

### Secure portal

这个还算稍微正常了一点点……

pyinstxtractor解包

修改pyc文件头部，反编译

```assembly
#!/usr/bin/env python
# visit http://tool.lu/pyc/ for more information
import base64
base64_message = 'UjBja190aDNfYkA1ZQ=='
base64_password = 'Ym9i'
# WARNING: Decompyle incomplete
```

base64解码：R0ck_th3_b@5e，放入shadowCTF{}

## OSINT

### Intel Expert

`You are a Cyber Threat Intel expert and you are supposed to find information about an Advanced Persistent Threat group code named as “Office 91”. Can you help find the city they are from.`

`**Flag Format** - ShadowCTF{Nameofcity} Author - Reconmadness`

直接google“Office 91”,找到该网站

https://www.dailynk.com/english/no-91-hackers-hq-revealed/

其中有一段

The defector was unable to attend the seminar in person due to fears for his safety, but via pre-produced materials he explained how No. 91 Office is located in a set of two two-storey buildings in the Dangsang-dong of Mankyungdae-district, and how he entered the buildings on a number of occasions thanks to his relations with traders and cadres affiliated to it.

google map搜索“Mankyungdae”

![]({{site.baseurl}}/img/2021-01-26-map.jpg)

平壤用英文表达

ShadowCTF{Pyongyang}

## Forensics

### Linux Help

![]({{site.baseurl}}/img/2021-01-26-image-analysis.jpg)

记事本打开最底部得到flag

### Brutus Killer

`Brutus has planned something to kill ceaser and ceaser has dreamed to be k!lLed but brutus is hiding his mission code. Can you find that code?`

![]({{site.baseurl}}/img/2021-01-26-img1.jpg)

记事本打开最底部找到一串很像flag的字符串

3oR1r$_h!iIba_(b@pb4

结合题目描述，应该为凯撒加密

位移24

shadowCTF{3rU1u$_k!lLed_(e@se4}

## Cryptography

### Rick and morty on adventure

![]({{site.baseurl}}/img/2021-01-26-rm.jpg)

google到了密码对应字母表

此密码应该是Rick and morty动画片中所用

![]({{site.baseurl}}/img/2021-01-26-VEKXJZ6Q0XYF8.jpg)

解出

MORTYLIKESSNAKEJAZZ，变小写即flag

这个表此题没有用到，保存一下以后可能会派上用场。

![]({{site.baseurl}}/img/2021-01-26-AFL1JTUSHEFAWAUUVP.jpg)

### What are Semaphores processes ?

`I was working on some Semaphore programming and was in my night trousers. But code was lost?
The only thing that helped me cheer up was this [Photo](https://drive.google.com/file/d/12Nr28iUvMF-7lGR16bFhYKjcj-vZOqbC/view?usp=sharing) , Really cheering.
This man was outside my window. **:p**`

md没想到还有这种加密方式

![]({{site.baseurl}}/img/2021-01-26-1150a4.jpg)

找到了密文表

![]({{site.baseurl}}/img/2021-01-26-pants.jpg)

ShadowCTF{thankyouhacker}