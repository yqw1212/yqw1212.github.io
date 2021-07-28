---
layout: post
title:  基础android
date:   2021-06-11 00:01:01 +0300
image:  2021-06-11-cormorants.jpg
tags:   [ctf,reverse,swpuctf,mobile,android]
---

jeb打开查看MainActivity

```assembly
package com.example.test.ctf02;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View$OnClickListener;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    private Button login;
    private EditText passWord;

    public MainActivity() {
        super();
    }

    static EditText access$000(MainActivity arg1) {
        return arg1.passWord;
    }

    protected void onCreate(Bundle arg3) {
        super.onCreate(arg3);
        this.setContentView(0x7F04001A);
        this.passWord = this.findViewById(0x7F0B0055);
        this.login = this.findViewById(0x7F0B0056);
        this.login.setOnClickListener(new View$OnClickListener() {
            public void onClick(View arg7) {
                if(new Check().checkPassword(MainActivity.this.passWord.getText().toString())) {
                    Toast.makeText(MainActivity.this, "Good,Please go on!", 0).show();
                    MainActivity.this.startActivity(new Intent(MainActivity.this, MainActivity2.class));
                    MainActivity.this.finish();
                }
                else {
                    Toast.makeText(MainActivity.this, "Failed", 0).show();
                }
            }
        });
    }
}
```

检查函数new Check().checkPassword()

```assembly
package com.example.test.ctf02;

public class Check {
    public Check() {
        super();
    }

    public boolean checkPassword(String arg7) {
        int v5 = 12;
        boolean v2 = false;
        char[] v1 = arg7.toCharArray();
        if(v1.length == v5) {
            int v0 = 0;
            while(true) {
                if(v0 < v1.length) {
                    v1[v0] = ((char)(0xFF - v0 - 100 - v1[v0]));
                    if(v1[v0] == 0x30 && v0 < v5) {
                        ++v0;
                        continue;
                    }
                }
                else {
                    break;
                }

                return v2;
            }

            v2 = true;
        }

        return v2;
    }
}
```

简单的加密，用python计算一下

```assembly
>>> 0xff-100-0x30
107
>>> chr(107)
'k'
>>> chr(107-11)
'`'
```

所以为：

kjihgfedcba`

输入后发现还有一关

```assembly
MainActivity.this.startActivity(new Intent(MainActivity.this, MainActivity2.class));
```

查看MainActivity2

```assembly
package com.example.test.ctf02;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View$OnClickListener;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;

public class MainActivity2 extends AppCompatActivity {
    Button button;
    EditText editText;
    ImageView imageView;

    public MainActivity2() {
        super();
    }

    public void init() {
        this.imageView = this.findViewById(0x7F0B0029);
        this.imageView.setImageResource(0x7F020053);
        this.editText = this.findViewById(0x7F0B0057);
        this.button = this.findViewById(0x7F0B0056);
    }

    protected void onCreate(Bundle arg3) {
        super.onCreate(arg3);
        this.setContentView(0x7F04001B);
        this.init();
        this.button.setOnClickListener(new View$OnClickListener() {
            public void onClick(View arg4) {
                MainActivity2.this.sendBroadcast(new Intent(MainActivity2.this.editText.getText().toString()));
            }
        });
    }
}
```

这里发送了一个广播，内容为第二关的输入框中的字符串。

由于android的广播机制还不太熟悉，上网寻求帮助，得知广播应该会在manifest.xml中注册。

查看manifest.xml

```assembly
<?xml version="1.0" encoding="UTF-8"?>
<manifest android:versionCode="1" android:versionName="1.0" package="com.example.test.ctf02" platformBuildVersionCode="24" platformBuildVersionName="7.0" xmlns:android="http://schemas.android.com/apk/res/android">
  <uses-sdk android:minSdkVersion="14" android:targetSdkVersion="24" />
  <application android:allowBackup="true" android:debuggable="true" android:icon="@mipmap/ic_launcher" android:label="@string/app_name" android:supportsRtl="true" android:theme="@style/AppTheme">
    <activity android:name="com.example.test.ctf02.MainActivity">
      <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
      </intent-filter>
    </activity>
    <receiver android:enabled="true" android:exported="true" android:name="com.example.test.ctf02.GetAndChange">
      <intent-filter>
        <action android:name="android.is.very.fun" />
      </intent-filter>
    </receiver>
    <activity android:name="com.example.test.ctf02.NextContent" />
    <activity android:name="com.example.test.ctf02.MainActivity2" />
  </application>
</manifest>
```

触发该广播需要输入"android.is.very.fun"，而GetAndChange为广播的接收器。

```assembly
package com.example.test.ctf02;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class GetAndChange extends BroadcastReceiver {
    public GetAndChange() {
        super();
    }

    public void onReceive(Context arg3, Intent arg4) {
        arg3.startActivity(new Intent(arg3, NextContent.class));
    }
}
```

GetAndChange接收到广播后会跳到NextContent。

```assembly
package com.example.test.ctf02;

import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.ImageView;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;

public class NextContent extends AppCompatActivity {
    ImageView imageView;

    public NextContent() {
        super();
    }

    public void Change() {
        String v6 = this.getApplicationContext().getDatabasePath("img.jpg").getAbsolutePath();
        try {
            File v3 = new File(v6);
            if(!v3.exists()) {
                goto label_9;
            }

            v3.delete();
        }
        catch(Exception v2) {
            v2.printStackTrace();
        }

        try {
        label_9:
            InputStream v5 = this.getApplicationContext().getResources().getAssets().open("timg_2.zip");
            FileOutputStream v4 = new FileOutputStream(v6);
            byte[] v0 = new byte[0x400];
            while(true) {
                int v1 = v5.read(v0);
                if(v1 <= 0) {
                    break;
                }

                v4.write(v0, 0, v1);
            }

            v4.flush();
            v4.close();
            v5.close();
        }
        catch(Exception v2) {
            v2.printStackTrace();
        }

        this.imageView.setImageBitmap(BitmapFactory.decodeFile(v6));
    }

    public void init() {
        this.imageView = this.findViewById(0x7F0B0059);
    }

    protected void onCreate(Bundle arg2) {
        super.onCreate(arg2);
        this.setContentView(0x7F04001C);
        this.init();
        this.Change();
    }
}
```

在NextContent中应该会给出flag。

本来在第二关输入"android.is.very.fun"应该可以成功，但是不知道为什么我这里崩了，所以换用其他办法。

使用adb工具构造广播直接唤出flag。

```assembly
adb shell am broadcast -a android.is.very.fun
```

还有一种方法，看懂解密最后一步直接解压出apk中assets目录中的timg_2.zip文件。

将timg_2.zip后缀改为jpg，得到flag。

![]({{site.baseurl}}/img/2021-06-11-timg_2.jpg)

flag{08067-wlecome}

