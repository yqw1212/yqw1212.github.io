---
layout: post
title:  AreYouRich
date:   2021-10-12 08:00:01 +0300
image:  2021-10-12-bicycles.jpg
tags:   [ctf,reverse,鹤城杯,android,apk,mobile]
---

MainActivity

```assembly
package com.test.areyourich;

import a.b.c.h;
import android.os.Bundle;
import android.widget.EditText;
import b.c.a.a;

public class MainActivity extends h {
    public EditText o;
    public EditText p;

    public MainActivity() {
        super();
    }

    public void onCreate(Bundle arg2) {
        super.onCreate(arg2);
        ((h)this).setContentView(0x7F0B001C);
        a.a = "5FQ5AaBGbqLGfYwjaRAuWGdDvyjbX5nH";
        this.o = ((h)this).findViewById(0x7F0800B6);
        this.p = ((h)this).findViewById(0x7F0800C7);
        ((h)this).findViewById(0x7F080095).setOnClickListener(new MainActivity$a(this));
    }
}
```

MainActivity$a

```assembly
package com.test.areyourich;

import android.content.Context;
import android.content.Intent;
import android.view.View$OnClickListener;
import android.view.View;
import android.widget.Toast;

public class MainActivity$a implements View$OnClickListener {
    public MainActivity$a(MainActivity arg1) {
        this.b = arg1;
        super();
    }

    public void onClick(View arg8) {
        Toast v8_1;
        String v8 = this.b.o.getText().toString();
        String v0 = this.b.p.getText().toString();
        if(v8.length() == 0 || v0.length() == 0) {
            v8_1 = Toast.makeText(this.b, "username or password empty, retry please!", 0);
        }
        else {
            String v4 = "username or password wrong, retry please!";
            if(v8.length() != 10) {
                v8_1 = Toast.makeText(this.b, ((CharSequence)v4), 0);
            }
            else {
                byte[] v1 = new byte[]{0x40, 0x30, 0x30, 49};
                byte[] v3 = v8.getBytes();
                int v5;
                for(v5 = 0; v5 < v3.length; ++v5) {
                    v3[v5] = ((byte)(v3[v5] ^ 34));
                }

                StringBuilder v5_1 = new StringBuilder();
                v5_1.append(new String(v3));
                v5_1.append(new String(v1));
                if(v0.equals(v5_1.toString())) {
                    MainActivity v1_1 = this.b;
                    StringBuilder v3_1 = new StringBuilder();
                    v3_1.append("Welcome ");
                    v3_1.append(v8);
                    v3_1.append(" !");
                    Toast.makeText(((Context)v1_1), v3_1.toString(), 0).show();
                    Intent v1_2 = new Intent(this.b.getApplicationContext(), UserActivity.class);
                    v1_2.putExtra("TOKEN", v8 + "_" + v0 + "_" + System.currentTimeMillis());
                    this.b.startActivity(v1_2);
                }
                else {
                    Toast.makeText(this.b, ((CharSequence)v4), 0).show();
                }

                return;
            }
        }

        v8_1.show();
    }
}
```

用户名和密码要满足一定的关系

UserActivity

```assembly
package com.test.areyourich;

import a.b.c.h;
import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;
import b.c.a.a;
import java.util.concurrent.ThreadLocalRandom;

public class UserActivity extends h {
    public TextView o;
    public TextView p;

    public UserActivity() {
        super();
    }

    public void onCreate(Bundle arg15) {
        byte v12;
        int v11;
        int v10;
        super.onCreate(arg15);
        ((h)this).setContentView(0x7F0B001D);
        this.o = ((h)this).findViewById(0x7F08009A);
        ((h)this).findViewById(0x7F08007C);
        this.p = ((h)this).findViewById(0x7F0800EC);
        String token = ((Activity)this).getIntent().getExtras().getString("TOKEN");
        int[] money = new int[1];
        byte[] v2 = a.b;
        byte[] tokenBytes = token.getBytes();
        ThreadLocalRandom v4 = ThreadLocalRandom.current();
        byte[] v5 = a.a.getBytes();
        int v6 = 0x100;
        byte[] v7 = new byte[v6];
        int v9;
        for(v9 = 0; v9 < v6; ++v9) {
            v7[v9] = ((byte)v9);
        }

        if(v5.length == 0) {
            v7 = null;
        }
        else {
            v9 = 0;
            v10 = 0;
            v11 = 0;
            while(v9 < v6) {
                v11 = (v5[v10] & 0xFF) + (v7[v9] & 0xFF) + v11 & 0xFF;
                v12 = v7[v9];
                v7[v9] = v7[v11];
                v7[v11] = v12;
                v10 = (v10 + 1) % v5.length;
                ++v9;
            }
        }

        int v5_1 = Math.min(tokenBytes.length, v2.length);
        v6 = 16;
        v9 = 0;
        v10 = 0;
        v11 = 0;
        while(v9 < v5_1) {
            v10 = v10 + 1 & 0xFF;
            v11 = (v7[v10] & 0xFF) + v11 & 0xFF;
            v12 = v7[v10];
            v7[v10] = v7[v11];
            v7[v11] = v12;
            if((((byte)(v7[(v7[v10] & 0xFF) + (v7[v11] & 0xFF) & 0xFF] ^ tokenBytes[v9]))) == v2[v9]) {
                v6 *= 2;
            }
            else {
                v6 = v4.nextInt(10) + v6;
            }

            ++v9;
        }

        money[0] = v6;
        StringBuilder v0 = b.a.a.a.a.e("Balance: ¥ ");
        v0.append(money[0]);
        this.o.setText(v0.toString());
        ((h)this).findViewById(0x7F080049).setOnClickListener(new UserActivity$a(this, money, token));
    }
}
```

a

```assembly
package b.c.a;

public class a {
    public static String a = "secretsecretsecretsecretsecretsecret";
    public static byte[] b;

    public static {
        a.b = new byte[]{81, -13, 84, -110, 72, 77, -96, 77, 0x20, -115, -75, -38, -97, 69, -64, 49, 8, -27, 56, 0x72, -68, -82, 76, -106, -34};
    }
}
```

UserActivity$a

```assembly
package com.test.areyourich;

import android.view.View$OnClickListener;
import android.view.View;
import android.widget.Toast;
import b.a.a.a.a;

public class UserActivity$a implements View$OnClickListener {
    public UserActivity$a(UserActivity arg1, int[] arg2, String arg3) {
        this.d = arg1;
        this.b = arg2;
        this.c = arg3;
        super();
    }

    public void onClick(View arg10) {
        int v1 = 0x1DCD64FF;
        if(this.b[0] > v1) {
            Toast.makeText(this.d, "buy success, eojoy it!", 0).show();
            String v10 = this.c;
            byte[] v2 = new byte[]{102, 108, 97, 103, 0x7B};
            byte[] v3 = new byte[]{0x7D};
            int v4 = 25;
            byte[] v5 = new byte[]{15, 70, 3, 41, 1, 0x30, 35, 0x40, 58, 50, 0, 101, 100, 99, 11, 0x7B, 52, 8, 60, 0x77, 62, 0x73, 73, 17, 16};
            byte[] v10_1 = v10.getBytes();
            if(v4 > v10_1.length) {
                v10 = "";
            }
            else {
                int v6;
                for(v6 = 0; v6 < v4; ++v6) {
                    v5[v6] = ((byte)(v5[v6] ^ v10_1[v6]));
                }

                v10 = new String(v2) + new String(v5) + new String(v3);
            }

            this.d.p.setText(((CharSequence)v10));
            this.b[0] -= v1;
            v10_2 = a.e("Balance: ¥ ");
            v10_2.append(this.b[0]);
            this.d.o.setText(v10_2.toString());
        }
        else {
            Toast.makeText(this.d, "sorry, money not enough!", 0).show();
        }
    }
}
```

money通过UserActivity类产生，然后判断如果大于0x1DCD64FF则购买成功，并输出flag。flag通过v10_1得到，v10_1是通过构造类时传入，也就是UserActivity类中的token。

可以知道如果想通过正常方法购买flag需要我们构造一个特定的username，所以我们只要让money每次都执行×2的流程，就可以购买flag，逆向得到token。

```assembly
package job;

import java.util.concurrent.ThreadLocalRandom;

/**
 * @author: 
 * @date: 2021/10/8
 * @description:
 */
public class hechengbei {
    public static void main(String[] args) {
//        getToken("cccccccccc");
//        getToken("cccccccccccc");
        getToken("vvvvipuser");
        userActivity();

    }

    static String getToken(String username){
//        String v8 = new String("aaaaaaaaaa");//2272
//        String v8 = new String("bbbbbbbbbb");//2304
        byte[] v1 = new byte[]{0x40, 0x30, 0x30, 49};
        byte[] v3 = username.getBytes();
        int v5;
        for(v5 = 0; v5 < v3.length; ++v5) {
            v3[v5] = ((byte)(v3[v5] ^ 34));
        }

        StringBuilder v5_1 = new StringBuilder();
        v5_1.append(new String(v3));
        v5_1.append(new String(v1));
        System.out.println(v5_1);
//        System.out.println(System.currentTimeMillis());
        return username+"_"+v5_1.toString()+"_"+System.currentTimeMillis();
    }

    static void userActivity(){

        byte[] v2 = new byte[]{81, -13, 84, -110, 72, 77, -96, 77, 0x20, -115, -75, -38, -97, 69, -64, 49, 8, -27, 56, 0x72, -68, -82, 76, -106, -34};
//        byte[] secret = "secretsecretsecretsecretsecretsecret".getBytes();
        byte[] secret = "5FQ5AaBGbqLGfYwjaRAuWGdDvyjbX5nH".getBytes();
        byte[] v7 = new byte[0x100];
        for(int i = 0; i < 0x100; ++i) {
            v7[i] = ((byte)i);
        }

        // 通过secret把v7打乱
        for(int i=0, v10=0, v11=0; i < 0x100; i++) {
            v11 = (secret[v10] & 0xFF) + (v7[i] & 0xFF) + v11 & 0xFF;
            byte tmp = v7[i];
            v7[i] = v7[v11];
            v7[v11] = tmp;
            v10 = (v10 + 1) % secret.length;
        }

        int v5_1 = v2.length;
//        int money = 16;
        for(int i=0, v10=0, v11=0; i < v5_1; i++) {
            v10 = v10 + 1 & 0xFF;
            v11 = (v7[v10] & 0xFF) + v11 & 0xFF;

            byte tmp = v7[v10];
            v7[v10] = v7[v11];
            v7[v11] = tmp;

            System.out.print((char)(v7[(v7[v10] & 0xFF) + (v7[v11] & 0xFF) & 0xFF] ^ v2[i]));
        }

    }

}
```

vvvvipuser_TTTTKRWQGP@001

输入username和password，得到flag

![]({{site.baseurl}}/img/2021-10-12-money.jpg)

或者直接输出flag

```assembly
package job;

import java.util.concurrent.ThreadLocalRandom;

/**
 * @author: 
 * @date: 2021/10/8
 * @description:
 */
public class hechengbei {
    public static void main(String[] args) {
//        getToken("cccccccccc");
//        getToken("cccccccccccc");
        getToken("vvvvipuser");
        userActivity();

    }

    static String getToken(String username){
//        String v8 = new String("aaaaaaaaaa");//2272
//        String v8 = new String("bbbbbbbbbb");//2304
        byte[] v1 = new byte[]{0x40, 0x30, 0x30, 49};
        byte[] v3 = username.getBytes();
        int v5;
        for(v5 = 0; v5 < v3.length; ++v5) {
            v3[v5] = ((byte)(v3[v5] ^ 34));
        }

        StringBuilder v5_1 = new StringBuilder();
        v5_1.append(new String(v3));
        v5_1.append(new String(v1));
        System.out.println(v5_1);
//        System.out.println(System.currentTimeMillis());
        return username+"_"+v5_1.toString()+"_"+System.currentTimeMillis();
    }

    static void userActivity(){

        byte[] v2 = new byte[]{81, -13, 84, -110, 72, 77, -96, 77, 0x20, -115, -75, -38, -97, 69, -64, 49, 8, -27, 56, 0x72, -68, -82, 76, -106, -34};
//        byte[] secret = "secretsecretsecretsecretsecretsecret".getBytes();
        byte[] secret = "5FQ5AaBGbqLGfYwjaRAuWGdDvyjbX5nH".getBytes();
        byte[] v7 = new byte[0x100];
        for(int i = 0; i < 0x100; ++i) {
            v7[i] = ((byte)i);
        }

        // 通过secret把v7打乱
        for(int i=0, v10=0, v11=0; i < 0x100; i++) {
            v11 = (secret[v10] & 0xFF) + (v7[i] & 0xFF) + v11 & 0xFF;
            byte tmp = v7[i];
            v7[i] = v7[v11];
            v7[v11] = tmp;
            v10 = (v10 + 1) % secret.length;
        }

        byte[] v5 = new byte[]{15, 70, 3, 41, 1, 0x30, 35, 0x40, 58, 50, 0, 101, 100, 99, 11, 0x7B, 52, 8, 60, 0x77, 62, 0x73, 73, 17, 16};

        int v5_1 = v2.length;
//        int money = 16;
        for(int i=0, v10=0, v11=0; i < v5_1; i++) {
            v10 = v10 + 1 & 0xFF;
            v11 = (v7[v10] & 0xFF) + v11 & 0xFF;

            byte tmp = v7[v10];
            v7[v10] = v7[v11];
            v7[v11] = tmp;

            System.out.print((char)(v7[(v7[v10] & 0xFF) + (v7[v11] & 0xFF) & 0xFF] ^ v2[i] ^ v5[i]));
        }

    }

}
```

y0u_h@V3_@_107_0f_m0n3y!!