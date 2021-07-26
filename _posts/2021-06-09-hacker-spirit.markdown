---
layout: post
title:  黑客精神
date:   2021-06-09 00:01:01 +0300
image:  2021-06-09-swan.jpg
tags:   [ctf,reverse,mobile,adworld,android]
---

jeb查看MainActivity

```assembly
package com.gdufs.xman;

import android.app.Activity;
import android.app.AlertDialog$Builder;
import android.content.ComponentName;
import android.content.Context;
import android.content.DialogInterface$OnClickListener;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Process;
import android.util.Log;
import android.view.Menu;
import android.view.View$OnClickListener;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends Activity {
    private Button btn1;
    private static String workString;

    public MainActivity() {
        super();
    }

    static String access$000() {
        return MainActivity.workString;
    }

    public void doRegister() {
        new AlertDialog$Builder(((Context)this)).setTitle("注册").setMessage("Flag就在前方！").setPositiveButton("注册", new DialogInterface$OnClickListener() {
            public void onClick(DialogInterface arg5, int arg6) {
                Intent v1 = new Intent();
                v1.setComponent(new ComponentName("com.gdufs.xman", "com.gdufs.xman.RegActivity"));
                MainActivity.this.startActivity(v1);
                MainActivity.this.finish();
            }
        }).setNegativeButton("不玩了", new DialogInterface$OnClickListener() {
            public void onClick(DialogInterface arg2, int arg3) {
                Process.killProcess(Process.myPid());
            }
        }).show();
    }

    public void onCreate(Bundle arg6) {
        String v2;
        super.onCreate(arg6);
        this.setContentView(0x7F04001A);
        String v1 = "Xman";
        Log.d("com.gdufs.xman m=", v1);
        this.getApplication();
        int v0 = MyApp.m;
        if(v0 == 0) {
            v2 = "未注册";
        }
        else if(v0 == 1) {
            v2 = "已注册";
        }
        else {
            v2 = "已混乱";
        }

        this.setTitle(v1 + v2);
        this.btn1 = this.findViewById(0x7F0B0054);
        this.btn1.setOnClickListener(new View$OnClickListener() {
            public void onClick(View arg5) {
                MainActivity.this.getApplication();
                if(MyApp.m == 0) {
                    MainActivity.this.doRegister();
                }
                else {
                    MainActivity.this.getApplication().work();
                    Toast.makeText(MainActivity.this.getApplicationContext(), MainActivity.workString, 0).show();
                }
            }
        });
    }

    public boolean onCreateOptionsMenu(Menu arg3) {
        this.getMenuInflater().inflate(0x7F0D0000, arg3);
        return 1;
    }

    public void work(String arg1) {
        MainActivity.workString = arg1;
    }
}
```

onCreate()方法中通过MyApp.m来初始化一个状态。查看MyApp

```assembly
package com.gdufs.xman;

import android.app.Application;
import android.util.Log;

public class MyApp extends Application {
    public static int m;

    static {
        MyApp.m = 0;
        System.loadLibrary("myjni");
    }

    public MyApp() {
        super();
    }

    public native void initSN() {
    }

    public void onCreate() {
        this.initSN();
        Log.d("com.gdufs.xman m=", String.valueOf(MyApp.m));
        super.onCreate();
    }

    public native void saveSN(String arg1) {
    }

    public native void work() {
    }
}
```

三个关键函数都在native层，查看so文件，但是搜索发现找不到initSN()、saveSN()、work()。

后来了解到

Java Native Interface，（JNI）是一个标准的 Java API，它支持将 Java 代码与使用其他编程语言编写的代码相集成。在这里主要就是Java和C++的交互。

实现JNI中本地函数注册可以两种方式：

* 采用默认的本地函数注册流程。
* 自己重写JNI_OnLoad()函数。（Android中采用这种）

当Android的VM执行到C组件（*so）里的System.loadLibrary()函数时，首先会去执行C组件里的JNI_OnLoad()函数，其用途有二

* 告诉java VM此C组件使用哪一个JNI版本。如果没有提供JNI_OnLoad()函数，VM会默认使用最老得JNI1.1版本。

* 可以藉由JNI_OnLoad()来获取JNIEnv.JNIEnv代表java环境，通过JNIEnv*指针就可以对java端的代码进行操作。

本题中的JNI_OnLoad

```assembly
signed int __fastcall JNI_OnLoad(int a1)
{
  if ( !(*(int (**)(void))(*(_DWORD *)a1 + 24))() )
  {
    j___android_log_print(2, "com.gdufs.xman", "JNI_OnLoad()");
    native_class = (*(int (**)(void))(*(_DWORD *)g_env + 24))();
    if ( !(*(int (**)(void))(*(_DWORD *)g_env + 860))() )
    {
      j___android_log_print(2, "com.gdufs.xman", "RegisterNatives() --> nativeMethod() ok");
      return 65542;
    }
    j___android_log_print(6, "com.gdufs.xman", "RegisterNatives() --> nativeMethod() failed");
  }
  return -1;
}
```

搜索字符串可以发现很多线索

```assembly
.rodata:00002E6D aW3AreWhoWeAre  DCB "W3_arE_whO_we_ARE",0
.rodata:00002E6D                                         ; DATA XREF: n2+3A↑o
.rodata:00002E6D                                         ; .text:off_12EC↑o
.rodata:00002E7F aComGdufsXmanMy DCB "com/gdufs/xman/MyApp",0
.rodata:00002E7F                                         ; DATA XREF: getValue+8↑o
.rodata:00002E7F                                         ; .text:off_132C↑o ...
.rodata:00002E94 aM              DCB "m",0               ; DATA XREF: getValue+20↑o
.rodata:00002E94                                         ; .text:off_1330↑o ...
.rodata:00002E96 aI              DCB "I",0               ; DATA XREF: getValue+22↑o
.rodata:00002E96                                         ; .text:off_1334↑o ...
.rodata:00002E98 aR              DCB "r+",0              ; DATA XREF: n1+8↑o
.rodata:00002E98                                         ; .text:off_1404↑o
.rodata:00002E9B aEopaoy62Elrd   DCB "EoPAoY62@ElRD",0   ; DATA XREF: n1+60↑o
.rodata:00002E9B                                         ; .text:off_140C↑o
.rodata:00002EA9 aComGdufsXmanMa DCB "com/gdufs/xman/MainActivity",0
.rodata:00002EA9                                         ; DATA XREF: callWork+C↑o
.rodata:00002EA9                                         ; .text:off_1484↑o
.rodata:00002EC5 aInit           DCB "<init>",0          ; DATA XREF: callWork+1E↑o
.rodata:00002EC5                                         ; .text:off_1488↑o
.rodata:00002ECC aV              DCB "()V",0             ; DATA XREF: callWork+22↑o
.rodata:00002ECC                                         ; .text:off_148C↑o ...
.rodata:00002ED0 aWork           DCB "work",0            ; DATA XREF: callWork+44↑o
.rodata:00002ED0                                         ; .text:off_1490↑o ...
.rodata:00002ED5 aLjavaLangStrin DCB "(Ljava/lang/String;)V",0
.rodata:00002ED5                                         ; DATA XREF: callWork+46↑o
```

通过交叉引用可以发现3个函数n1，n2，n3

```assembly
.data:00005004 off_5004        DCD aInitsn             ; DATA XREF: JNI_OnLoad+4A↑o
.data:00005004                                         ; .text:off_1564↑o
.data:00005004                                         ; "initSN"
.data:00005008                 DCD aV                  ; "()V"
.data:0000500C                 DCD n1+1
.data:00005010                 DCD aSavesn             ; "saveSN"
.data:00005014                 DCD aLjavaLangStrin     ; "(Ljava/lang/String;)V"
.data:00005018                 DCD n2+1
.data:0000501C                 DCD aWork               ; "work"
.data:00005020                 DCD aV                  ; "()V"
.data:00005024                 DCD n3+1
```

可以看到代码后面的注释上写了initSN函数实际上就是n1, saveSN函数实际上就是n2, work函数实际上就是n3。

n1

```assembly
int __fastcall n1(int a1)
{
  int v1; // r6
  int v2; // r0
  int v3; // r4
  int v4; // r0
  int v5; // r1
  int v6; // r7
  int v7; // r5
  int v9; // r0
  int v10; // r1

  v1 = a1;
  v2 = j_fopen("/sdcard/reg.dat", "r+");
  v3 = v2;
  if ( !v2 )
  {
    v4 = v1;
    v5 = v3;
    return setValue(v4, v5);
  }
  j_fseek(v2);
  v6 = j_ftell(v3);
  v7 = j_malloc(v6 + 1);
  if ( !v7 )
  {
    j_fclose(v3);
    v4 = v1;
    v5 = 0;
    return setValue(v4, v5);
  }
  j_fseek(v3);
  j_fread(v7, v6, 1, v3);
  *(_BYTE *)(v7 + v6) = 0;
  if ( !j_strcmp(v7, "EoPAoY62@ElRD") )
  {
    v9 = v1;
    v10 = 1;
  }
  else
  {
    v9 = v1;
    v10 = 0;
  }
  setValue(v9, v10);
  return j_fclose(v3);
}
```

malloc申请一段空间，把"/sdcard/reg.dat"中的内容读到这个空间，比较是否为"EoPAoY62@ElRD"

n2

```assembly
int __fastcall n2(int a1, int a2, int a3)
{
  int v3; // r4
  int v4; // r5
  int v5; // r7
  int v7; // r6
  _BYTE *v8; // r5
  int v9; // r4
  int v10; // r0
  char v11; // r2
  int v12; // [sp+8h] [bp-38h]
  char v13[20]; // [sp+10h] [bp-30h]

  v3 = a1;
  v4 = a3;
  v5 = j_fopen("/sdcard/reg.dat", "w+");
  if ( !v5 )
    return j___android_log_print(3, (int)"com.gdufs.xman", (int)&dword_2E5A);
  strcpy(v13, "W3_arE_whO_we_ARE");
  v7 = (*(int (__fastcall **)(int, int, _DWORD))(*(_DWORD *)v3 + 676))(v3, v4, 0);
  v8 = (_BYTE *)v7;
  v12 = j_strlen();
  v9 = 2016;
  while ( 1 )
  {
    v10 = (int)&v8[-v7];
    if ( (signed int)&v8[-v7] >= v12 )
      break;
    if ( v10 % 3 == 1 )
    {
      v9 = (v9 + 5) % 16;
      v11 = v13[v9 + 1];
    }
    else if ( v10 % 3 == 2 )
    {
      v9 = (v9 + 7) % 15;
      v11 = v13[v9 + 2];
    }
    else
    {
      v9 = (v9 + 3) % 13;
      v11 = v13[v9 + 3];
    }
    *v8++ ^= v11;
  }
  j_fputs(v7, v5);
  return j_fclose(v5);
}
```

用户输入的字符sn，会进行字符计算操作，得到了新的字符串，再保存到 /sdcard/reg.dat 文件中。

n3

```assembly
__int64 __fastcall n3(int a1)
{
  int v1; // r4
  int v2; // r0
  __int64 v3; // r0

  v1 = a1;
  n1(a1);
  v2 = getValue(v1);
  if ( v2 )
  {
    if ( v2 == 1 )
      v3 = __PAIR__(&unk_2EFB, v1);
    else
      v3 = __PAIR__(&unk_2F25, v1);
  }
  else
  {
    v3 = __PAIR__(&unk_2EEB, v1);
  }
  return callWork(v3);
}
```

callWork()

```assembly
__int64 __fastcall callWork(__int64 a1)
{
  int v1; // r7
  int v2; // r4
  int v3; // r0
  int v4; // r5
  int v5; // r0
  int v6; // r6
  int v7; // r5
  int v8; // r3
  __int64 v10; // [sp+0h] [bp-20h]

  v10 = a1;
  v1 = HIDWORD(a1);
  v2 = a1;
  v3 = (*(int (**)(void))(*(_DWORD *)a1 + 24))();
  v4 = v3;
  v5 = (*(int (__fastcall **)(int, int, const char *, const char *))(*(_DWORD *)v2 + 132))(v2, v3, "<init>", "()V");
  v6 = (*(int (__fastcall **)(int, int, int))(*(_DWORD *)v2 + 112))(v2, v4, v5);
  v7 = (*(int (__fastcall **)(int, int, const char *, const char *))(*(_DWORD *)v2 + 132))(
         v2,
         v4,
         "work",
         "(Ljava/lang/String;)V");
  if ( v7 )
  {
    HIDWORD(v10) = *(_DWORD *)(*(_DWORD *)v2 + 244);
    v8 = (*(int (__fastcall **)(int, int))(*(_DWORD *)v2 + 668))(v2, v1);
    ((void (__fastcall *)(int, int, int, int))HIDWORD(v10))(v2, v6, v7, v8);
  }
  return v10;
}
```

在apk中输入"EoPAoY62@ElRD"，然后使用adb

```assembly
adb pull /sdcard/reg.dat
```

打开得到flag

201608Am!2333

之前还遗漏了一个地方，flag格式为xman{}

```assembly
.rodata:00002F06                 DCB 0xAF
.rodata:00002F07                 DCB 0x66 ; f
.rodata:00002F08                 DCB 0x6C ; l
.rodata:00002F09                 DCB 0x61 ; a
.rodata:00002F0A                 DCB 0x67 ; g
.rodata:00002F0B                 DCB 0x2C ; ,
.rodata:00002F0C                 DCB 0xE6
.rodata:00002F0D                 DCB 0xA0
.rodata:00002F0E                 DCB 0xBC
.rodata:00002F0F                 DCB 0xE5
.rodata:00002F10                 DCB 0xBC
.rodata:00002F11                 DCB 0x8F
.rodata:00002F12                 DCB 0xE4
.rodata:00002F13                 DCB 0xB8
.rodata:00002F14                 DCB 0xBA
.rodata:00002F15                 DCB 0x78 ; x
.rodata:00002F16                 DCB 0x6D ; m
.rodata:00002F17                 DCB 0x61 ; a
.rodata:00002F18                 DCB 0x6E ; n
.rodata:00002F19                 DCB 0x7B ; {
.rodata:00002F1A                 DCB 0xE2
.rodata:00002F1B                 DCB 0x80
.rodata:00002F1C                 DCB 0xA6
.rodata:00002F1D                 DCB 0xE2
```

对于这个提示，ida没有将其很好地识别为字符串。

这么做其实不对，因为加密正好是异或，异或的逆运算就是异或，所以误打误撞做出来了。

重新整理一遍，输入一个字符串，n2加密后结果如果为"EoPAoY62@ElRD"，则注册成功。

加密过程中字符串的长度不变，所以知道长度为13.

```assembly
v9 = 2016;
while ( 1 )
{
    v10 = (int)&v8[-v7];
    if ( (signed int)&v8[-v7] >= v12 )
        break;
    if ( v10 % 3 == 1 ){
        v9 = (v9 + 5) % 16;
        v11 = v13[v9 + 1];
    }
    else if ( v10 % 3 == 2 ){
        v9 = (v9 + 7) % 15;
        v11 = v13[v9 + 2];
    }
    else{
        v9 = (v9 + 3) % 13;
        v11 = v13[v9 + 3];
    }
    *v8++ ^= v11;
}
```

v10最初为0，然后依次自增，所以加密的步骤也可以知道，直接计算

```assembly
#include <stdio.h>

int main(){
    char result[13] = {'E','o','P','A','o','Y','6','2','@','E','l','R','D'};
    char key[17] = {'W','3','_','a','r','E','_','w','h','O',
                    '_','w','e','_','A','R','E'};
    int v9 = 2016, v11;
    for(int i=0; i<13; i++){
        if ( i % 3 == 1 ){
          v9 = (v9 + 5) % 16;
          v11 = key[v9 + 1];
        }
        else if ( i % 3 == 2 ){
          v9 = (v9 + 7) % 15;
          v11 = key[v9 + 2];
        }
        else{
          v9 = (v9 + 3) % 13;
          v11 = key[v9 + 3];
        }
        printf("%c", v11^result[i]);
    }
    return 0;
}
```

得到flag.