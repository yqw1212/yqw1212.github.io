---
layout: post
title:  Dashen Decode AES
date:   2021-06-08 00:01:01 +0300
image:  2021-06-08-umbrella.jpg
tags:   [ctf,reverse,mobile,android,frida,Bytectf]
---

jeb打开查看MainActivity

```assembly
package com.zj.zjtdctf;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class MainActivity extends Activity {
    public EditText b;
    public MyApplication c;

    public MainActivity() {
        super();
        this.b = null;
    }

    public void onCreate(Bundle arg2) {
        super.onCreate(arg2);
        ((Activity)this).setContentView(0x7F0A001C);
        View v2 = ((Activity)this).findViewById(0x7F070042);
        this.b = ((Activity)this).findViewById(0x7F070058);
        this.c = ((Activity)this).getApplication();
        ((Button)v2).setOnClickListener(new MainActivity$a(this));
    }
}
```

发现没有关键代码，查看其他Activity

MainActivity$a

```assembly
package com.zj.zjtdctf;

import android.view.View$OnClickListener;
import android.view.View;
import android.widget.Toast;
import ba;

public class MainActivity$a implements View$OnClickListener {
    public MainActivity$a(MainActivity arg1) {
        this.b = arg1;
        super();
    }

    public void onClick(View arg3) {
        if(ba.d(this.b.b.getText().toString(), this.b.c.a().d().b(), this.b.c.a().d().a())) {
            Toast.makeText(this.b.getApplicationContext(), "get it", 1).show();
        }
        else {
            Toast.makeText(this.b.getApplicationContext(), "try again", 1).show();
        }
    }
}
```

ba类

```assembly
import java.security.Key;
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class ba {
    public static String a(byte[] arg6) {
        StringBuilder v0 = new StringBuilder();
        int v1 = arg6.length;
        int v3;
        for(v3 = 0; v3 < v1; ++v3) {
            v0.append(String.format("%02x", Integer.valueOf(arg6[v3] & 0xFF)));
        }

        return v0.toString();
    }

    public static String b(String arg3, String arg4, String arg5) {
        try {
            SecretKeySpec v0 = new SecretKeySpec(ba.c(arg4), "AES");
            Cipher v4 = Cipher.getInstance("AES/CBC/PKCS5Padding");
            v4.init(1, ((Key)v0), new IvParameterSpec(arg5.getBytes()));
            return ba.a(v4.doFinal(arg3.getBytes()));
        }
        catch(Exception v3) {
            v3.printStackTrace();
            return "";
        }
    }

    public static byte[] c(String arg7) {
        int v0 = arg7.length();
        byte[] v1 = new byte[v0 / 2];
        int v2;
        for(v2 = 0; v2 < v0; v2 += 2) {
            v1[v2 / 2] = ((byte)((Character.digit(arg7.charAt(v2), 16) << 4) + Character.digit(arg7.charAt(v2 + 1), 16)));
        }

        return v1;
    }

   public static boolean d(String arg1, String arg2, String arg3) {
        if(ba.b(arg1, arg2, arg3).equals("db6427960a6622ffac27ef5437acf1459a592d1a96b73e75490c8badb0ed294c1e9232213e63461dd2d9f6d327e51641".subSequence(2, 98))) {
            return 1;
        }

        return 0;
   }

       
}
```

有是一个AES加密方法，还有一个对加密的结果进行比较的方法，如果结果为"db6427960a6622ffac27ef5437acf1459a592d1a96b73e75490c8badb0ed294c1e9232213e63461dd2d9f6d327e51641"则正确。只要拿到key和iv就可以对其直接解密。

查看传入这个函数的参数，this.b.b.getText().toString(), this.b.c.a().d().b(), this.b.c.a().d().a())

第一个自然是我们输入的字符串，第二个b是MainActivity，b.c是MyApplication

```assembly
package com.zj.zjtdctf;

import aa;
import android.app.Application;
import android.content.Context;
import android.util.Log;

public class MyApplication extends Application {
    public aa b;

    public MyApplication() {
        super();
    }

    public aa a() {
        return this.b;
    }

    public void onCreate() {
        super.onCreate();
        Log.d("CTF Android APP", "APPLICATION onCreate");
        aa v0 = new aa(((Context)this));
        this.b = v0;
        try {
            v0.c();
            this.b.e();
        }
        catch(Exception v0_1) {
            v0_1.printStackTrace();
        }
    }

    public void onTerminate() {
        Log.d("CTF Android APP", "APPLICATION onTerminate");
        super.onTerminate();
    }
}
```

a()返回一个aa类的变量

```assembly
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase$CursorFactory;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteException;
import android.database.sqlite.SQLiteOpenHelper;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

public class aa extends SQLiteOpenHelper {
    public final Context b;
    public SQLiteDatabase c;
    public static String d = "db.db";
    public static String e = "/data/data/com.zj.zjtdctf/databases/";
    public static String f = "public";

    public static {
        StringBuilder v0 = new StringBuilder();
        v0.append("UPDATE ");
        v0.append(aa.f);
        v0.append(" SET d=?");
        v0.toString();
    }

    public aa(Context arg4) {
        super(arg4, aa.d, null, 1);
        this.b = arg4;
    }

    public final boolean a() {
        SQLiteDatabase v1_1;
        SQLiteDatabase$CursorFactory v1 = null;
        try {
            StringBuilder v2 = new StringBuilder();
            v2.append(String.valueOf(aa.e));
            v2.append(aa.d);
            v1_1 = SQLiteDatabase.openDatabase(v2.toString(), v1, 1);
            goto label_12;
        }
        catch(SQLiteException ) {
        label_12:
            if(v1_1 != null) {
                v1_1.close();
            }

            if(v1_1 != null) {
                return 1;
            }

            return 0;
        }
    }

    public final void b() {
        InputStream v0 = this.b.getAssets().open(aa.d);
        StringBuilder v2 = new StringBuilder();
        v2.append(String.valueOf(aa.e));
        v2.append(aa.d);
        FileOutputStream v1 = new FileOutputStream(v2.toString());
        byte[] v2_1 = new byte[0x400];
        while(true) {
            int v3 = v0.read(v2_1);
            if(v3 <= 0) {
                break;
            }

            ((OutputStream)v1).write(v2_1, 0, v3);
        }

        ((OutputStream)v1).flush();
        ((OutputStream)v1).close();
        v0.close();
    }

    public void c() {
        if(!this.a()) {
            ((SQLiteOpenHelper)this).getReadableDatabase();
            try {
                this.b();
            }
            catch(IOException ) {
                throw new Error("Error copying database");
            }
        }
    }

    public void close() {
        __monitor_enter(this);
        try {
            if(this.c != null) {
                this.c.close();
            }

            super.close();
        }
        catch(Throwable v0) {
            __monitor_exit(this);
            throw v0;
        }

        __monitor_exit(this);
    }

    public z9 d() {
        z9 v0 = new z9();
        Cursor v1 = this.c.rawQuery("SELECT  * FROM  config1 WHERE a=1", null);
        if(v1.moveToFirst()) {
            boolean v2 = false;
            v0.d(v1.getInt(0));
            v0.f(v1.getString(1));
            v0.e(v1.getString(2));
            if(v1.getInt(3) <= 0) {
            }
            else {
                v2 = true;
            }

            v0.i(v2);
            v0.g(v1.getString(4));
            v0.h(v1.getString(5));
            v0.c(v1.getString(7));
        }

        return v0;
    }

    public void e() {
        String v0_1 = String.valueOf(aa.e) + aa.d;
        File v1 = new File(v0_1);
        v1.exists();
        v1.length();
        SQLiteDatabase$CursorFactory v1_1 = null;
        int v2 = 17;
        try {
            this.c = SQLiteDatabase.openDatabase(v0_1, v1_1, v2);
        }
        catch(Exception v0_2) {
            v0_2.printStackTrace();
        }
    }

    public void onCreate(SQLiteDatabase arg1) {
    }

    public void onUpgrade(SQLiteDatabase arg1, int arg2, int arg3) {
    }
}
```

看起来AES的key和iv是保存在数据库中的，我们没有办法采用静态的方法直接获取。

可以使用Frida hook拿到AES的key，iv还有密文

#### Frida Hook

连接手机，打开frida server

```assembly
import frida
import sys

PACKAGE = 'bin.mt.plus'

if __name__ == '__main__':
    jscode = open('./script.js', 'r').read() # 获取js脚本内容
    # get_usb_device获取设备（就是你手机）
    # attach（翻译：链接）我所理解是连接给定包名的app的进程，为什么是我所理解，因为官网没有写
    process = frida.get_usb_device().attach(PACKAGE) # 获取给定包名的app进程
    print(process) # 打印看看是嘛玩意儿
    script = process.create_script(jscode) # 这里是把你的js脚本给塞进了process，源码在这https://github.com/frida/frida-python/blob/master/frida/core.py#L147
    # script.on('message', on_message)
    print('[*] Running CTF')
    script.load() # 加载脚本，https://github.com/frida/frida-python/blob/master/frida/core.py#L191
    sys.stdin.read()
```

编写对应的"script.js"脚本

运行py文件，运行模拟器中的apk，执行的函数就会被替换。

script.js

```assembly
Java.perform(function(){
    Java.use("ba").b.implementation = function (input, key, iv)
    {
        var result = this.b(input, key, iv);
        console.log("args0: "+input+" args1: "+key+" args2: "+iv+" result: "+result);
        return result;
    }
});
```

结果：

```assembly
Session(pid=2942)
[*] Running CTF
args0: 11 args1: 37eaae0141f1a3adf8a1dee655853766 args2: a5efdbd57b84ca88 result: a82a927033e068ff44a029f805b05673
args0: 000 args1: 37eaae0141f1a3adf8a1dee655853766 args2: a5efdbd57b84ca88 result: 3c000d61a71eebbed6c3dfaca65930d6
```

Aes解密，python2

```assembly
from Crypto.Cipher import AES

def AESdecrypt(data, key, iv):
    aes1 = AES.new(key, AES.MODE_CBC, iv)
    decrypted = aes1.decrypt(data)
    return decrypted

aeskey = "37eaae0141f1a3adf8a1dee655853766".decode("hex")

iv = "a5efdbd57b84ca88"
data = "db6427960a6622ffac27ef5437acf1459a592d1a96b73e75490c8badb0ed294c1e9232213e63461dd2d9f6d327e51641".decode("hex")
print(AESdecrypt(data, aeskey, iv))
```

ByteCTF{fl-ag-IS-to-ng-xu-el-ih-ai}