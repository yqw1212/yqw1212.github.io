---
layout: post
title:  whereiscode(网鼎杯2022青龙组)
date:   2022-09-18 00:08:01 +0300
image:  2022-09-18-butterfly.jpg
tags:   [ctf,reverse,android,网鼎杯]
---

解压apk包，查看dex文件

classes2.dex

```assembly
package com.example.nothingcode;

import android.os.Bundle;
import android.view.View$OnClickListener;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity implements View$OnClickListener {
    Button button;
    EditText editText1;
    EditText editText2;

    public MainActivity() {
    }

    public void onClick(View arg8) {
    }

    protected void onCreate(Bundle arg6) {
    }
}
```

```assembly
package com.example.nothingcode;

public class Checkfxxk {
    public Checkfxxk() {
    }

    private int[] byteToInt(byte[] arg12, int arg13) {
        return null;
    }

    public boolean check(String arg25, String arg26) {
        return 0;
    }

    private byte[] intToByte(int[] arg12, int arg13) {
        return null;
    }

    private static int transform(byte arg7) {
        return 0;
    }
}
```

可以看到函数的内容全部为空，而且函数并不是在native层。

![]({{site.baseurl}}/img/whereiscode/2022-09-18-zero.jpg)

classes3.dex

![]({{site.baseurl}}/img/whereiscode/2022-09-18-luoyesiqiu.jpg)

看到luoyesiqiu的包名，上网找到关于其的线索https://www.cnblogs.com/luoyesiqiu/p/dpt.html，得知其是一个函数抽取的技术

博客中说

CodeItem是dex文件中存放函数字节码相关数据的结构。下图显示的就是CodeItem大概的样子。

![]({{site.baseurl}}/img/whereiscode/2022-09-18-codeitem.jpg)

说是提取CodeItem，其实我们提取的是CodeItem中的insns，它里面存放的是函数真正的字节码。

所以我们要对这部分进行还原。

用010editor打开dex文件

![]({{site.baseurl}}/img/whereiscode/struct.jpg)

接下来我们需要定位到被抽取的函数的code_item的位置，在安卓的[官网](https://source.android.com/docs/core/dalvik/dex-format?hl=zh-cn#encoded-method)查找code_item

![]({{site.baseurl}}/img/whereiscode/code_item.jpg)

可以看到引用自 encoded_method，查找encoded_method

![]({{site.baseurl}}/img/whereiscode/class_data_item.jpg)

现在可以在010editor中确定code_item的位置

![]({{site.baseurl}}/img/whereiscode/pos1.jpg)

![]({{site.baseurl}}/img/whereiscode/pos2.jpg)

在官网中得到函数的字节码保存在ins数组中，点击查看，确实ins数组中的值都为0

接下来就要恢复被抽取的函数的字节码。

查看Manifest

```assembly
<?xml version="1.0" encoding="UTF-8"?>
<manifest android:compileSdkVersion="31" android:compileSdkVersionCodename="12" android:versionCode="1" android:versionName="1.0" package="com.example.testchouqu" platformBuildVersionCode="31" platformBuildVersionName="12" xmlns:android="http://schemas.android.com/apk/res/android">
  <uses-sdk android:minSdkVersion="23" android:targetSdkVersion="31" />
  <application android:allowBackup="true" android:appComponentFactory="androidx.core.app.CoreComponentFactory" android:debuggable="true" android:extractNativeLibs="true" android:icon="@mipmap/ic_launcher" android:label="@string/app_name" android:name="com.luoyesiqiu.shell.ProxyApplication" android:roundIcon="@mipmap/ic_launcher_round" android:supportsRtl="true" android:testOnly="true" android:theme="@style/Theme.Testchouqu">
    <activity android:name="com.example.nothingcode.MainActivity">
      <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
      </intent-filter>
    </activity>
    <provider android:authorities="com.example.testchouqu.androidx-startup" android:exported="false" android:name="androidx.startup.InitializationProvider">
      <meta-data android:name="androidx.emoji2.text.EmojiCompatInitializer" android:value="androidx.startup" />
      <meta-data android:name="androidx.lifecycle.ProcessLifecycleInitializer" android:value="androidx.startup" />
    </provider>
  </application>
</manifest>
```

可以看到程序最开始运行的是com.luoyesiqiu.shell.ProxyApplication这个类，定位到这个类

```assembly
package com.luoyesiqiu.shell;

import android.app.Application;
import android.content.Context;
import android.text.TextUtils;
import android.util.Log;
import com.luoyesiqiu.shell.util.FileUtils;
import com.luoyesiqiu.shell.util.ShellClassLoader;

public class ProxyApplication extends Application {
    private static final String TAG;
    public static boolean initialized;

    static {
        ProxyApplication.TAG = ProxyApplication.class.getSimpleName();
        ProxyApplication.initialized = false;
    }

    public ProxyApplication() {
        super();
    }

    protected void attachBaseContext(Context arg4) {
        super.attachBaseContext(arg4);
        String v0 = ProxyApplication.TAG;
        Log.d(v0, "dpt attachBaseContext");
        Log.d(v0, "attachBaseContext classloader = " + arg4.getClassLoader());
        if(!ProxyApplication.initialized) {
            Log.d(v0, "ProxyApplication init");
            JniBridge.ia(arg4, arg4.getClassLoader());
            JniBridge.mde(arg4.getClassLoader(), ShellClassLoader.loadDex(arg4));
        }
    }

    public void onCreate() {
        super.onCreate();
        String v0 = ProxyApplication.TAG;
        Log.d(v0, "dpt onCreate");
        Log.d(v0, "onCreate() classLoader = " + this.getApplicationContext().getClassLoader());
        v0 = FileUtils.readAppName(this.getApplicationContext());
        if(!TextUtils.isEmpty(((CharSequence)v0))) {
            JniBridge.craa(this.getApplicationContext(), v0);
        }

        if(!TextUtils.isEmpty(((CharSequence)v0))) {
            JniBridge.craoc(v0);
        }
    }
}
```

attachBaseContext函数中调用了JniBridge类的两个函数，查看JniBridge类

```assembly
package com.luoyesiqiu.shell;

import android.content.Context;

public class JniBridge {
    static {
        System.loadLibrary("dpt");
    }

    public JniBridge() {
        super();
    }

    public static native void craa(Context arg0, String arg1) {
    }

    public static native void craoc(String arg0) {
    }

    public static native String gap(ClassLoader arg0) {
    }

    public static native void ia(Context arg0, ClassLoader arg1) {
    }

    public static native void mde(ClassLoader arg0, ClassLoader arg1) {
    }

    public static native String rcf(ClassLoader arg0) {
    }
}
```

可见这些函数在native层，用ida打开so文件

因为是动态加载函数，所以定位到JNI_OnLoad函数

```assembly
jint JNI_OnLoad(JavaVM *vm, void *reserved)
{
  _JNIEnv *v4; // [sp+10h] [bp-10h] BYREF

  v4 = 0;
  if ( _JavaVM::GetEnv((_JavaVM *)vm, (void **)&v4, 0x10004) )
    return 0xFFFFFFFF;
  if ( !registerNativeMethods(v4) )
    return 0xFFFFFFFF;
  init_dpt(v4);
  _android_log_print(4, "dpt_native", "JNI_OnLoad called!");
  return 0x10004;
}
```

注意到有一个registerNativeMethods函数，进入查看

```assembly
bool __fastcall registerNativeMethods(_JNIEnv *a1)
{
  int v1; // r0

  v1 = _JNIEnv::FindClass(a1, "com/luoyesiqiu/shell/JniBridge");
  return _JNIEnv::RegisterNatives(a1, v1, off_33000, 6) == 0;
}
```

off_33000处即为函数的名字

```assembly
.data:00033000 off_33000       DCD aCraoc              ; DATA XREF: registerNativeMethods(_JNIEnv *)+18↑o
.data:00033000                                         ; registerNativeMethods(_JNIEnv *)+1A↑o ...
.data:00033000                                         ; "craoc"
.data:00033004                 DCD aLjavaLangStrin_0   ; "(Ljava/lang/String;)V"
.data:00033008                 DCD _Z27callRealApplicationOnCreateP7_JNIEnvP7_jclassP8_jstring+1 ; callRealApplicationOnCreate(_JNIEnv *,_jclass *,_jstring *)
.data:0003300C                 DCD aCraa               ; "craa"
.data:00033010                 DCD aLandroidConten_1   ; "(Landroid/content/Context;Ljava/lang/St"...
.data:00033014                 DCD _Z25callRealApplicationAttachP7_JNIEnvP7_jclassP8_jobjectP8_jstring+1 ; callRealApplicationAttach(_JNIEnv *,_jclass *,_jobject *,_jstring *)
.data:00033018                 DCD aIa                 ; "ia"
.data:0003301C                 DCD aLandroidConten_2   ; "(Landroid/content/Context;Ljava/lang/Cl"...
.data:00033020                 DCD _Z8init_appP7_JNIEnvP7_jclassP8_jobjectS4_+1 ; init_app(_JNIEnv *,_jclass *,_jobject *,_jobject *)
.data:00033024                 DCD aGap                ; "gap"
.data:00033028                 DCD aLjavaLangClass     ; "(Ljava/lang/ClassLoader;)Ljava/lang/Str"...
.data:0003302C                 DCD _Z10getApkPathP7_JNIEnvP7_jclassP8_jobject+1 ; getApkPath(_JNIEnv *,_jclass *,_jobject *)
.data:00033030                 DCD aRcf                ; "rcf"
.data:00033034                 DCD aLjavaLangClass     ; "(Ljava/lang/ClassLoader;)Ljava/lang/Str"...
.data:00033038                 DCD _Z23readAppComponentFactoryP7_JNIEnvP7_jclassP8_jobject+1 ; readAppComponentFactory(_JNIEnv *,_jclass *,_jobject *)
.data:0003303C                 DCD aMde                ; "mde"
.data:00033040                 DCD aLjavaLangClass_0   ; "(Ljava/lang/ClassLoader;Ljava/lang/Clas"...
.data:00033044                 DCD _Z16mergeDexElementsP7_JNIEnvP7_jclassP8_jobjectS4_+1 ; mergeDexElements(_JNIEnv *,_jclass *,_jobject *,_jobject *)
```

ia

```assembly
int __fastcall init_app(_JNIEnv *a1, int a2, int a3, int a4)
{
  int result; // r0
  int v5; // r0
  const void *v6; // r0
  off_t v7; // [sp+10h] [bp-40h]
  const char *v8; // [sp+14h] [bp-3Ch]
  int v9; // [sp+18h] [bp-38h]
  int v10; // [sp+1Ch] [bp-34h]
  AAsset *asset; // [sp+20h] [bp-30h]
  int v12; // [sp+28h] [bp-28h]
  int v13; // [sp+2Ch] [bp-24h]
  int v14; // [sp+30h] [bp-20h]
  int v15; // [sp+34h] [bp-1Ch]

  _android_log_print(3, "dpt_native", "init_app!");
  if ( a3 )
  {
    asset = (AAsset *)getAsset(a1, a3, "OoooooOooo");
    dword_3307C = _JNIEnv::NewGlobalRef(a1, a3);
    v10 = _JNIEnv::GetObjectClass(a1, a3);
    v9 = W_CallObjectMethod(a1, v10, a3, "getPackageName", "()Ljava/lang/String;");
    v8 = (const char *)_JNIEnv::GetStringUTFChars(a1, v9, 0);
    dword_33080 = _JNIEnv::NewGlobalRef(a1, v9);
    result = _android_log_print(3, "dpt_native", "init_app %s", v8);
    if ( asset )
    {
      v7 = AAsset_getLength(asset);
      v6 = AAsset_getBuffer(asset);
      result = readCodeItem(a1, a2, v6, v7);
    }
  }
  else
  {
    v15 = getApkPath(a1, a2, a4);
    v14 = _JNIEnv::NewStringUTF(a1, "assets/OoooooOooo");
    v13 = readFromZip(a1, v15, v14);
    v12 = _JNIEnv::GetArrayLength(a1, v13);
    if ( v12 > 0 )
    {
      _android_log_print(3, "dpt_native", "readCodeItem data len = %d", v12);
      v5 = _JNIEnv::GetByteArrayElements(a1, v13, 0);
      result = readCodeItem(a1, a2, v5, v12);
    }
    else
    {
      result = _android_log_print(6, "dpt_native", "readCodeItem Cannot read code item file!");
    }
  }
  return result;
}
```

首先在加载`OoooooOooo`资源文件，然后分别获取资源的长度和内容，传入`readCodeItem`函数

```assembly
int __fastcall readCodeItem(int a1, int a2, unsigned __int8 *buffer, MultiDexCode *length)
{
  int v4; // r0
  int v5; // r0
  int v7; // [sp+14h] [bp-94h]
  int v8; // [sp+1Ch] [bp-8Ch]
  int v9; // [sp+3Ch] [bp-6Ch]
  int j; // [sp+40h] [bp-68h]
  unsigned __int16 methodCount; // [sp+46h] [bp-62h]
  unsigned int v12; // [sp+48h] [bp-60h]
  int v13; // [sp+4Ch] [bp-5Ch]
  MultiDexCode *v14; // [sp+50h] [bp-58h]
  char v17[8]; // [sp+64h] [bp-44h] BYREF
  char v18[8]; // [sp+6Ch] [bp-3Ch] BYREF
  int v19; // [sp+74h] [bp-34h]
  CodeItem *v20; // [sp+78h] [bp-30h]
  unsigned int v21; // [sp+7Ch] [bp-2Ch] BYREF
  int v22; // [sp+80h] [bp-28h]
  int i; // [sp+84h] [bp-24h]
  int DexCount; // [sp+88h] [bp-20h] BYREF
  char v25[8]; // [sp+8Ch] [bp-1Ch] BYREF
  char v26[8]; // [sp+94h] [bp-14h] BYREF

  if ( buffer )
  {
    v14 = (MultiDexCode *)MultiDexCode::getInst(length);
    MultiDexCode::init(v14, buffer, (int)length);
    v9 = MultiDexCode::readVersion(v14);        // 2bytes
    v4 = MultiDexCode::readDexCount(v14);       // 2bytes
    DexCount = 0;
    _android_log_print(4, "dpt_native", "readCodeItem : version = %d , dexCount = %d", v9, v4);
    v13 = MultiDexCode::readDexCodeIndex(v14, &DexCount);
    for ( i = 0; i < DexCount; ++i )
    {
      _android_log_print(4, "dpt_native", "readCodeItem : dexCodeIndex[%d] = %d", i, *(_DWORD *)(v13 + 4 * i));
      v12 = *(_DWORD *)(v13 + 4 * i);
      methodCount = MultiDexCode::readUInt16(v14, v12);
      _android_log_print(
        3,
        "dpt_native",
        "readCodeItem : dexCodeOffset[%d] = %d,methodCount[%d] = %d",
        i,
        v12,
        i,
        methodCount);
      v8 = operator new(0x14u);
      sub_124D2();
      v22 = v8;
      v21 = v12 + 2;
      for ( j = 0; j < methodCount; ++j )
      {
        v20 = (CodeItem *)MultiDexCode::nextCodeItem(v14, &v21);
        v19 = CodeItem::getMethodIdx(v20);
        v7 = v22;
        std::pair<int,CodeItem *>::pair<unsigned int &,CodeItem *&,false>();
        std::unordered_map<int,CodeItem *>::insert<std::pair<int,CodeItem *>,void>(v26, v7, v18);
      }
      std::pair<int,std::unordered_map<int,CodeItem *> *>::pair<int &,std::unordered_map<int,CodeItem *> *&,false>();
      std::unordered_map<int,std::unordered_map<int,CodeItem *> *,std::hash<int>,std::equal_to<int>,std::allocator<std::pair<int const,std::unordered_map<int,CodeItem *> *>>>::insert<std::pair<int,std::unordered_map<int,CodeItem *> *>,void>(
        v25,
        &dexMap,
        v17);
    }
    v5 = sub_12600(&dexMap);
    _android_log_print(3, "dpt_native", "readCodeItem map size = %ld", v5);
  }
  return _stack_chk_guard;
}
```

分析号资源文件的结构后，写脚本还原dex文件

```assembly
import code
from ctypes import *
import struct

def read_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

file = read_file("./assets/OoooooOooo")
dex_file = list(read_file("./classes2.dex"))

print("Shell version: ", c_uint16(struct.unpack_from("<H", file, 0)[0]).value)

DexCount = c_uint16(struct.unpack_from("<H", file, 2)[0]).value
print("Count dex: ", DexCount)

dex_code_index = 4

dex_insns_file = []
for i in range(DexCount):
    offset = c_uint32(struct.unpack_from("<I", file, dex_code_index+4*i)[0]).value
    methodCount = c_uint16(struct.unpack_from("<H", file, offset)[0]).value

    offset += 2
    method_code_item = []
    for j in range(methodCount):
        code_item = []
        code_item.append(c_uint32(struct.unpack_from("<I", file, offset)[0]).value)
        
        offset += 4
        code_item.append(c_uint32(struct.unpack_from("<I", file, offset)[0]).value)

        offset += 4
        code_item.append(c_uint32(struct.unpack_from("<I", file, offset)[0]).value) # 字节码长度

        offset += 4
        code_item.append(offset) # 在资源文件中的偏移

        offset += code_item[2]
        method_code_item.append(code_item)
        print(code_item)

    dex_insns_file.append(method_code_item)

for i in dex_insns_file[1]:
    dex_file[i[1] : i[1]+i[2]] = file[i[3] : i[3]+i[2]]

with open("./classes2_dec.dex", "wb") as f:
    f.write(bytes(dex_file))
```

