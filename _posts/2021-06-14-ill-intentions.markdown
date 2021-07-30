---
layout: post
title:  ill-intentions
date:   2021-06-14 00:01:01 +0300
image:  2021-06-14-dog.jpg
tags:   [ctf,reverse,googlectf2016,mobile,android,smali]
---

jeb打开，查看MainActivity

```assembly
package com.example.application;

import android.app.Activity;
import android.content.IntentFilter;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

public class MainActivity extends Activity {
    public MainActivity() {
        super();
    }

    public void onCreate(Bundle arg6) {
        super.onCreate(arg6);
        TextView v2 = new TextView(this.getApplicationContext());
        v2.setText("Select the activity you wish to interact with.To-Do: Add buttons to select activity, for now use Send_to_Activity");
        this.setContentView(((View)v2));
        IntentFilter v0 = new IntentFilter();
        v0.addAction("com.ctf.INCOMING_INTENT");
        this.registerReceiver(new Send_to_Activity(), v0, "ctf.permission._MSG", null);
    }
}
```

Send_to_Activity

```assembly
package com.example.application;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

public class Send_to_Activity extends BroadcastReceiver {
    public Send_to_Activity() {
        super();
    }

    public void onReceive(Context arg5, Intent arg6) {
        String v0 = arg6.getStringExtra("msg");
        if(v0.equalsIgnoreCase("ThisIsTheRealOne")) {
            arg5.startActivity(new Intent(arg5, ThisIsTheRealOne.class));
        }
        else if(v0.equalsIgnoreCase("IsThisTheRealOne")) {
            arg5.startActivity(new Intent(arg5, IsThisTheRealOne.class));
        }
        else if(v0.equalsIgnoreCase("DefinitelyNotThisOne")) {
            arg5.startActivity(new Intent(arg5, DefinitelyNotThisOne.class));
        }
        else {
            Toast.makeText(arg5, "Which Activity do you wish to interact with?", 1).show();
        }
    }
}
```

flag应该藏在三个广播中的一个里面。

DefinitelyNotThisOne

```assembly
package com.example.application;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View$OnClickListener;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class DefinitelyNotThisOne extends Activity {
    static {
        System.loadLibrary("hello-jni");
    }

    public DefinitelyNotThisOne() {
        super();
    }

    public native String computeFlag(String arg1, String arg2) {
    }

    public native String definitelyNotThis(String arg1, String arg2) {
    }

    public void onCreate(Bundle arg4) {
        super.onCreate(arg4);
        new TextView(((Context)this)).setText("Activity - Is_this_the_real_one");
        Button v0 = new Button(((Context)this));
        v0.setText("Broadcast Intent");
        this.setContentView(((View)v0));
        v0.setOnClickListener(new View$OnClickListener() {
            public void onClick(View arg7) {
                Intent v3 = new Intent();
                v3.setAction("com.ctf.OUTGOING_INTENT");
                DefinitelyNotThisOne.this.getResources().getString(0x7F030005);
                v3.putExtra("msg", DefinitelyNotThisOne.this.definitelyNotThis(Utilities.doBoth(DefinitelyNotThisOne.this.getResources().getString(0x7F030009)), Utilities.doBoth("Test")));
                DefinitelyNotThisOne.this.sendBroadcast(v3, "ctf.permission._MSG");
            }
        });
    }

    public native String orThat(String arg1, String arg2, String arg3) {
    }

    public native String perhapsThis(String arg1, String arg2, String arg3) {
    }
}
```

IsThisTheRealOne

```assembly
package com.example.application;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View$OnClickListener;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class IsThisTheRealOne extends Activity {
    static {
        System.loadLibrary("hello-jni");
    }

    public IsThisTheRealOne() {
        super();
    }

    public native String computeFlag(String arg1, String arg2) {
    }

    public native String definitelyNotThis(String arg1, String arg2, String arg3) {
    }

    public void onCreate(Bundle arg5) {
        this.getApplicationContext();
        super.onCreate(arg5);
        new TextView(((Context)this)).setText("Activity - Is_this_the_real_one");
        Button v0 = new Button(((Context)this));
        v0.setText("Broadcast Intent");
        this.setContentView(((View)v0));
        v0.setOnClickListener(new View$OnClickListener() {
            public void onClick(View arg9) {
                Intent v3 = new Intent();
                v3.setAction("com.ctf.OUTGOING_INTENT");
                String v0 = IsThisTheRealOne.this.getResources().getString(0x7F030007) + "\\VlphgQbwvj~HuDgaeTzuSt.@Lex^~";
                String v1 = Utilities.doBoth(IsThisTheRealOne.this.getResources().getString(0x7F030001));
                String v4 = this.getClass().getName();
                v3.putExtra("msg", IsThisTheRealOne.this.perhapsThis(v0, v1, Utilities.doBoth(v4.substring(0, v4.length() - 2))));
                IsThisTheRealOne.this.sendBroadcast(v3, "ctf.permission._MSG");
            }
        });
    }

    public native String orThat(String arg1, String arg2, String arg3) {
    }

    public native String perhapsThis(String arg1, String arg2, String arg3) {
    }
}
```

ThisIsTheRealOne

```assembly
package com.example.application;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View$OnClickListener;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class ThisIsTheRealOne extends Activity {
    static {
        System.loadLibrary("hello-jni");
    }

    public ThisIsTheRealOne() {
        super();
    }

    public native String computeFlag(String arg1, String arg2) {
    }

    public native String definitelyNotThis(String arg1, String arg2, String arg3) {
    }

    public void onCreate(Bundle arg4) {
        super.onCreate(arg4);
        new TextView(((Context)this)).setText("Activity - This Is The Real One");
        Button v0 = new Button(((Context)this));
        v0.setText("Broadcast Intent");
        this.setContentView(((View)v0));
        v0.setOnClickListener(new View$OnClickListener() {
            public void onClick(View arg8) {
                Intent v3 = new Intent();
                v3.setAction("com.ctf.OUTGOING_INTENT");
                v3.putExtra("msg", ThisIsTheRealOne.this.orThat(ThisIsTheRealOne.this.getResources().getString(0x7F030006) + "YSmks", Utilities.doBoth(ThisIsTheRealOne.this.getResources().getString(0x7F030002)), Utilities.doBoth(this.getClass().getName())));
                ThisIsTheRealOne.this.sendBroadcast(v3, "ctf.permission._MSG");
            }
        });
    }

    public native String orThat(String arg1, String arg2, String arg3) {
    }

    public native String perhapsThis(String arg1, String arg2, String arg3) {
    }
}
```

在smali中插入Log日志，打印`msg`。

用工具打开apk文件

DefinitelyNotThisOne、IsThisTheRealOne和ThisIsTheRealOne的smali分别都有两个，通过比较，要修改的应该是$1文件。

DefinitelyNotThisOne$1.smali

```smali
.class Lcom/example/application/DefinitelyNotThisOne$1;
.super Ljava/lang/Object;
.source "DefinitelyNotThisOne.java"

# interfaces
.implements Landroid/view/View$OnClickListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/example/application/DefinitelyNotThisOne;->onCreate(Landroid/os/Bundle;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/example/application/DefinitelyNotThisOne;


# direct methods
.method constructor <init>(Lcom/example/application/DefinitelyNotThisOne;)V
    .locals 0

    .prologue
    .line 28
    iput-object p1, p0, Lcom/example/application/DefinitelyNotThisOne$1;->this$0:Lcom/example/application/DefinitelyNotThisOne;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/view/View;)V
    .locals 6
    .param p1, "v"    # Landroid/view/View;

    .prologue
    .line 30
    new-instance v3, Landroid/content/Intent;

    invoke-direct {v3}, Landroid/content/Intent;-><init>()V

    .line 31
    .local v3, "intent":Landroid/content/Intent;
    const-string v4, "com.ctf.OUTGOING_INTENT"

    invoke-virtual {v3, v4}, Landroid/content/Intent;->setAction(Ljava/lang/String;)Landroid/content/Intent;

    .line 32
    iget-object v4, p0, Lcom/example/application/DefinitelyNotThisOne$1;->this$0:Lcom/example/application/DefinitelyNotThisOne;

    invoke-virtual {v4}, Lcom/example/application/DefinitelyNotThisOne;->getResources()Landroid/content/res/Resources;

    move-result-object v4

    const v5, 0x7f030005

    invoke-virtual {v4, v5}, Landroid/content/res/Resources;->getString(I)Ljava/lang/String;

    move-result-object v0

    .line 33
    .local v0, "a":Ljava/lang/String;
    iget-object v4, p0, Lcom/example/application/DefinitelyNotThisOne$1;->this$0:Lcom/example/application/DefinitelyNotThisOne;

    invoke-virtual {v4}, Lcom/example/application/DefinitelyNotThisOne;->getResources()Landroid/content/res/Resources;

    move-result-object v4

    const v5, 0x7f030009

    invoke-virtual {v4, v5}, Landroid/content/res/Resources;->getString(I)Ljava/lang/String;

    move-result-object v4

    invoke-static {v4}, Lcom/example/application/Utilities;->doBoth(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 34
    .local v1, "b":Ljava/lang/String;
    const-string v4, "Test"

    invoke-static {v4}, Lcom/example/application/Utilities;->doBoth(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    .line 35
    .local v2, "c":Ljava/lang/String;
    const-string v4, "msg"

    iget-object v5, p0, Lcom/example/application/DefinitelyNotThisOne$1;->this$0:Lcom/example/application/DefinitelyNotThisOne;

    invoke-virtual {v5, v1, v2}, Lcom/example/application/DefinitelyNotThisOne;->definitelyNotThis(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v3, v4, v5}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 36
    iget-object v4, p0, Lcom/example/application/DefinitelyNotThisOne$1;->this$0:Lcom/example/application/DefinitelyNotThisOne;

    const-string v5, "ctf.permission._MSG"

    invoke-virtual {v4, v3, v5}, Lcom/example/application/DefinitelyNotThisOne;->sendBroadcast(Landroid/content/Intent;Ljava/lang/String;)V

    .line 38
    return-void
.end method

```

最关键的是要找到插桩的位置

修改后

```smali
.class Lcom/example/application/DefinitelyNotThisOne$1;
.super Ljava/lang/Object;
.source "DefinitelyNotThisOne.java"

# interfaces
.implements Landroid/view/View$OnClickListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/example/application/DefinitelyNotThisOne;->onCreate(Landroid/os/Bundle;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/example/application/DefinitelyNotThisOne;


# direct methods
.method constructor <init>(Lcom/example/application/DefinitelyNotThisOne;)V
    .locals 0

    .prologue
    .line 28
    iput-object p1, p0, Lcom/example/application/DefinitelyNotThisOne$1;->this$0:Lcom/example/application/DefinitelyNotThisOne;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/view/View;)V
    .locals 6
    .param p1, "v"    # Landroid/view/View;

    .prologue
    .line 30
    new-instance v3, Landroid/content/Intent;

    invoke-direct {v3}, Landroid/content/Intent;-><init>()V

    .line 31
    .local v3, "intent":Landroid/content/Intent;
    const-string v4, "com.ctf.OUTGOING_INTENT"

    invoke-virtual {v3, v4}, Landroid/content/Intent;->setAction(Ljava/lang/String;)Landroid/content/Intent;

    .line 32
    iget-object v4, p0, Lcom/example/application/DefinitelyNotThisOne$1;->this$0:Lcom/example/application/DefinitelyNotThisOne;

    invoke-virtual {v4}, Lcom/example/application/DefinitelyNotThisOne;->getResources()Landroid/content/res/Resources;

    move-result-object v4

    const v5, 0x7f030005

    invoke-virtual {v4, v5}, Landroid/content/res/Resources;->getString(I)Ljava/lang/String;

    move-result-object v0

    .line 33
    .local v0, "a":Ljava/lang/String;
    iget-object v4, p0, Lcom/example/application/DefinitelyNotThisOne$1;->this$0:Lcom/example/application/DefinitelyNotThisOne;

    invoke-virtual {v4}, Lcom/example/application/DefinitelyNotThisOne;->getResources()Landroid/content/res/Resources;

    move-result-object v4

    const v5, 0x7f030009

    invoke-virtual {v4, v5}, Landroid/content/res/Resources;->getString(I)Ljava/lang/String;

    move-result-object v4

    invoke-static {v4}, Lcom/example/application/Utilities;->doBoth(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 34
    .local v1, "b":Ljava/lang/String;
    const-string v4, "Test"

    invoke-static {v4}, Lcom/example/application/Utilities;->doBoth(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    .line 35
    .local v2, "c":Ljava/lang/String;
    const-string v4, "msg"

    iget-object v5, p0, Lcom/example/application/DefinitelyNotThisOne$1;->this$0:Lcom/example/application/DefinitelyNotThisOne;

    invoke-virtual {v5, v1, v2}, Lcom/example/application/DefinitelyNotThisOne;->definitelyNotThis(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5
	
	const-string v0, "Message - "
	invoke-static {v0, v5}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
	move-result v0

    invoke-virtual {v3, v4, v5}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 36
    iget-object v4, p0, Lcom/example/application/DefinitelyNotThisOne$1;->this$0:Lcom/example/application/DefinitelyNotThisOne;

    const-string v5, "ctf.permission._MSG"

    invoke-virtual {v4, v3, v5}, Lcom/example/application/DefinitelyNotThisOne;->sendBroadcast(Landroid/content/Intent;Ljava/lang/String;)V

    .line 38
    return-void
.end method
```

IsThisTheRealOne$1.smali

```smali
.class Lcom/example/application/IsThisTheRealOne$1;
.super Ljava/lang/Object;
.source "IsThisTheRealOne.java"

# interfaces
.implements Landroid/view/View$OnClickListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/example/application/IsThisTheRealOne;->onCreate(Landroid/os/Bundle;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/example/application/IsThisTheRealOne;


# direct methods
.method constructor <init>(Lcom/example/application/IsThisTheRealOne;)V
    .locals 0

    .prologue
    .line 25
    iput-object p1, p0, Lcom/example/application/IsThisTheRealOne$1;->this$0:Lcom/example/application/IsThisTheRealOne;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/view/View;)V
    .locals 8
    .param p1, "v"    # Landroid/view/View;

    .prologue
    .line 27
    new-instance v3, Landroid/content/Intent;

    invoke-direct {v3}, Landroid/content/Intent;-><init>()V

    .line 28
    .local v3, "intent":Landroid/content/Intent;
    const-string v5, "com.ctf.OUTGOING_INTENT"

    invoke-virtual {v3, v5}, Landroid/content/Intent;->setAction(Ljava/lang/String;)Landroid/content/Intent;

    .line 29
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    iget-object v6, p0, Lcom/example/application/IsThisTheRealOne$1;->this$0:Lcom/example/application/IsThisTheRealOne;

    invoke-virtual {v6}, Lcom/example/application/IsThisTheRealOne;->getResources()Landroid/content/res/Resources;

    move-result-object v6

    const v7, 0x7f030007

    invoke-virtual {v6, v7}, Landroid/content/res/Resources;->getString(I)Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, "\\VlphgQbwvj~HuDgaeTzuSt.@Lex^~"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    .line 30
    .local v0, "a":Ljava/lang/String;
    iget-object v5, p0, Lcom/example/application/IsThisTheRealOne$1;->this$0:Lcom/example/application/IsThisTheRealOne;

    invoke-virtual {v5}, Lcom/example/application/IsThisTheRealOne;->getResources()Landroid/content/res/Resources;

    move-result-object v5

    const v6, 0x7f030001

    invoke-virtual {v5, v6}, Landroid/content/res/Resources;->getString(I)Ljava/lang/String;

    move-result-object v5

    invoke-static {v5}, Lcom/example/application/Utilities;->doBoth(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 31
    .local v1, "b":Ljava/lang/String;
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object v4

    .line 32
    .local v4, "name":Ljava/lang/String;
    const/4 v5, 0x0

    invoke-virtual {v4}, Ljava/lang/String;->length()I

    move-result v6

    add-int/lit8 v6, v6, -0x2

    invoke-virtual {v4, v5, v6}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v5

    invoke-static {v5}, Lcom/example/application/Utilities;->doBoth(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    .line 33
    .local v2, "c":Ljava/lang/String;
    const-string v5, "msg"

    iget-object v6, p0, Lcom/example/application/IsThisTheRealOne$1;->this$0:Lcom/example/application/IsThisTheRealOne;

    invoke-virtual {v6, v0, v1, v2}, Lcom/example/application/IsThisTheRealOne;->perhapsThis(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v3, v5, v6}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 34
    iget-object v5, p0, Lcom/example/application/IsThisTheRealOne$1;->this$0:Lcom/example/application/IsThisTheRealOne;

    const-string v6, "ctf.permission._MSG"

    invoke-virtual {v5, v3, v6}, Lcom/example/application/IsThisTheRealOne;->sendBroadcast(Landroid/content/Intent;Ljava/lang/String;)V

    .line 35
    return-void
.end method
```

修改后

```smali
.class Lcom/example/application/IsThisTheRealOne$1;
.super Ljava/lang/Object;
.source "IsThisTheRealOne.java"

# interfaces
.implements Landroid/view/View$OnClickListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/example/application/IsThisTheRealOne;->onCreate(Landroid/os/Bundle;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/example/application/IsThisTheRealOne;


# direct methods
.method constructor <init>(Lcom/example/application/IsThisTheRealOne;)V
    .locals 0

    .prologue
    .line 25
    iput-object p1, p0, Lcom/example/application/IsThisTheRealOne$1;->this$0:Lcom/example/application/IsThisTheRealOne;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/view/View;)V
    .locals 8
    .param p1, "v"    # Landroid/view/View;

    .prologue
    .line 27
    new-instance v3, Landroid/content/Intent;

    invoke-direct {v3}, Landroid/content/Intent;-><init>()V

    .line 28
    .local v3, "intent":Landroid/content/Intent;
    const-string v5, "com.ctf.OUTGOING_INTENT"

    invoke-virtual {v3, v5}, Landroid/content/Intent;->setAction(Ljava/lang/String;)Landroid/content/Intent;

    .line 29
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    iget-object v6, p0, Lcom/example/application/IsThisTheRealOne$1;->this$0:Lcom/example/application/IsThisTheRealOne;

    invoke-virtual {v6}, Lcom/example/application/IsThisTheRealOne;->getResources()Landroid/content/res/Resources;

    move-result-object v6

    const v7, 0x7f030007

    invoke-virtual {v6, v7}, Landroid/content/res/Resources;->getString(I)Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, "\\VlphgQbwvj~HuDgaeTzuSt.@Lex^~"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    .line 30
    .local v0, "a":Ljava/lang/String;
    iget-object v5, p0, Lcom/example/application/IsThisTheRealOne$1;->this$0:Lcom/example/application/IsThisTheRealOne;

    invoke-virtual {v5}, Lcom/example/application/IsThisTheRealOne;->getResources()Landroid/content/res/Resources;

    move-result-object v5

    const v6, 0x7f030001

    invoke-virtual {v5, v6}, Landroid/content/res/Resources;->getString(I)Ljava/lang/String;

    move-result-object v5

    invoke-static {v5}, Lcom/example/application/Utilities;->doBoth(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 31
    .local v1, "b":Ljava/lang/String;
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object v4

    .line 32
    .local v4, "name":Ljava/lang/String;
    const/4 v5, 0x0

    invoke-virtual {v4}, Ljava/lang/String;->length()I

    move-result v6

    add-int/lit8 v6, v6, -0x2

    invoke-virtual {v4, v5, v6}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v5

    invoke-static {v5}, Lcom/example/application/Utilities;->doBoth(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    .line 33
    .local v2, "c":Ljava/lang/String;
    const-string v5, "msg"

    iget-object v6, p0, Lcom/example/application/IsThisTheRealOne$1;->this$0:Lcom/example/application/IsThisTheRealOne;

    invoke-virtual {v6, v0, v1, v2}, Lcom/example/application/IsThisTheRealOne;->perhapsThis(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v6
	
	const-string v0, "Message - "
	
	invoke-static {v0, v6}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
	
	move-result v0

    invoke-virtual {v3, v5, v6}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 34
    iget-object v5, p0, Lcom/example/application/IsThisTheRealOne$1;->this$0:Lcom/example/application/IsThisTheRealOne;

    const-string v6, "ctf.permission._MSG"

    invoke-virtual {v5, v3, v6}, Lcom/example/application/IsThisTheRealOne;->sendBroadcast(Landroid/content/Intent;Ljava/lang/String;)V

    .line 35
    return-void
.end method
```

ThisIsTheRealOne$1.smali

```smali
.class Lcom/example/application/ThisIsTheRealOne$1;
.super Ljava/lang/Object;
.source "ThisIsTheRealOne.java"

# interfaces
.implements Landroid/view/View$OnClickListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/example/application/ThisIsTheRealOne;->onCreate(Landroid/os/Bundle;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/example/application/ThisIsTheRealOne;


# direct methods
.method constructor <init>(Lcom/example/application/ThisIsTheRealOne;)V
    .locals 0

    .prologue
    .line 24
    iput-object p1, p0, Lcom/example/application/ThisIsTheRealOne$1;->this$0:Lcom/example/application/ThisIsTheRealOne;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/view/View;)V
    .locals 7
    .param p1, "v"    # Landroid/view/View;

    .prologue
    .line 26
    new-instance v3, Landroid/content/Intent;

    invoke-direct {v3}, Landroid/content/Intent;-><init>()V

    .line 27
    .local v3, "intent":Landroid/content/Intent;
    const-string v4, "com.ctf.OUTGOING_INTENT"

    invoke-virtual {v3, v4}, Landroid/content/Intent;->setAction(Ljava/lang/String;)Landroid/content/Intent;

    .line 28
    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    iget-object v5, p0, Lcom/example/application/ThisIsTheRealOne$1;->this$0:Lcom/example/application/ThisIsTheRealOne;

    invoke-virtual {v5}, Lcom/example/application/ThisIsTheRealOne;->getResources()Landroid/content/res/Resources;

    move-result-object v5

    const v6, 0x7f030006

    invoke-virtual {v5, v6}, Landroid/content/res/Resources;->getString(I)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    const-string v5, "YSmks"

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    .line 29
    .local v0, "a":Ljava/lang/String;
    iget-object v4, p0, Lcom/example/application/ThisIsTheRealOne$1;->this$0:Lcom/example/application/ThisIsTheRealOne;

    invoke-virtual {v4}, Lcom/example/application/ThisIsTheRealOne;->getResources()Landroid/content/res/Resources;

    move-result-object v4

    const v5, 0x7f030002

    invoke-virtual {v4, v5}, Landroid/content/res/Resources;->getString(I)Ljava/lang/String;

    move-result-object v4

    invoke-static {v4}, Lcom/example/application/Utilities;->doBoth(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 30
    .local v1, "b":Ljava/lang/String;
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object v4

    invoke-static {v4}, Lcom/example/application/Utilities;->doBoth(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    .line 31
    .local v2, "c":Ljava/lang/String;
    const-string v4, "msg"

    iget-object v5, p0, Lcom/example/application/ThisIsTheRealOne$1;->this$0:Lcom/example/application/ThisIsTheRealOne;

    invoke-virtual {v5, v0, v1, v2}, Lcom/example/application/ThisIsTheRealOne;->orThat(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v3, v4, v5}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 32
    iget-object v4, p0, Lcom/example/application/ThisIsTheRealOne$1;->this$0:Lcom/example/application/ThisIsTheRealOne;

    const-string v5, "ctf.permission._MSG"

    invoke-virtual {v4, v3, v5}, Lcom/example/application/ThisIsTheRealOne;->sendBroadcast(Landroid/content/Intent;Ljava/lang/String;)V

    .line 33
    return-void
.end method
```

修改后

```smali
.class Lcom/example/application/ThisIsTheRealOne$1;
.super Ljava/lang/Object;
.source "ThisIsTheRealOne.java"

# interfaces
.implements Landroid/view/View$OnClickListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/example/application/ThisIsTheRealOne;->onCreate(Landroid/os/Bundle;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/example/application/ThisIsTheRealOne;


# direct methods
.method constructor <init>(Lcom/example/application/ThisIsTheRealOne;)V
    .locals 0

    .prologue
    .line 24
    iput-object p1, p0, Lcom/example/application/ThisIsTheRealOne$1;->this$0:Lcom/example/application/ThisIsTheRealOne;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/view/View;)V
    .locals 7
    .param p1, "v"    # Landroid/view/View;

    .prologue
    .line 26
    new-instance v3, Landroid/content/Intent;

    invoke-direct {v3}, Landroid/content/Intent;-><init>()V

    .line 27
    .local v3, "intent":Landroid/content/Intent;
    const-string v4, "com.ctf.OUTGOING_INTENT"

    invoke-virtual {v3, v4}, Landroid/content/Intent;->setAction(Ljava/lang/String;)Landroid/content/Intent;

    .line 28
    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    iget-object v5, p0, Lcom/example/application/ThisIsTheRealOne$1;->this$0:Lcom/example/application/ThisIsTheRealOne;

    invoke-virtual {v5}, Lcom/example/application/ThisIsTheRealOne;->getResources()Landroid/content/res/Resources;

    move-result-object v5

    const v6, 0x7f030006

    invoke-virtual {v5, v6}, Landroid/content/res/Resources;->getString(I)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    const-string v5, "YSmks"

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    .line 29
    .local v0, "a":Ljava/lang/String;
    iget-object v4, p0, Lcom/example/application/ThisIsTheRealOne$1;->this$0:Lcom/example/application/ThisIsTheRealOne;

    invoke-virtual {v4}, Lcom/example/application/ThisIsTheRealOne;->getResources()Landroid/content/res/Resources;

    move-result-object v4

    const v5, 0x7f030002

    invoke-virtual {v4, v5}, Landroid/content/res/Resources;->getString(I)Ljava/lang/String;

    move-result-object v4

    invoke-static {v4}, Lcom/example/application/Utilities;->doBoth(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 30
    .local v1, "b":Ljava/lang/String;
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object v4

    invoke-static {v4}, Lcom/example/application/Utilities;->doBoth(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    .line 31
    .local v2, "c":Ljava/lang/String;
    const-string v4, "msg"

    iget-object v5, p0, Lcom/example/application/ThisIsTheRealOne$1;->this$0:Lcom/example/application/ThisIsTheRealOne;

    invoke-virtual {v5, v0, v1, v2}, Lcom/example/application/ThisIsTheRealOne;->orThat(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5
	
	const-string v0, "Message - "
	
	invoke-static {v0, v5}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
	
	move-result v0

    invoke-virtual {v3, v4, v5}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    .line 32
    iget-object v4, p0, Lcom/example/application/ThisIsTheRealOne$1;->this$0:Lcom/example/application/ThisIsTheRealOne;

    const-string v5, "ctf.permission._MSG"

    invoke-virtual {v4, v3, v5}, Lcom/example/application/ThisIsTheRealOne;->sendBroadcast(Landroid/content/Intent;Ljava/lang/String;)V

    .line 33
    return-void
.end method
```

对Acitivity设置`android:exported="true"`属性，用命令的形式启动Activity。

```assembly
<?xml version="1.0" encoding="utf-8" standalone="no"?><manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.hellojni" platformBuildVersionCode="22" platformBuildVersionName="5.1.1-1819727">
    <permission android:description="@string/android.permission._msg" android:name="ctf.permission._MSG" android:protectionLevel="signature"/>
    <permission android:description="@string/android.permission._msg" android:name="ctf.permission._SEND"/>
    <application android:icon="@mipmap/ic_launcher" android:label="CTF Application">
        <activity android:label="Main Activity" android:name="com.example.application.MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        <activity android:exported="true" android:label="Activity: Is This The Real One" android:name="com.example.application.IsThisTheRealOne"/>
        <activity android:exported="true" android:label="This Is The Real One" android:name="com.example.application.ThisIsTheRealOne"/>
        <activity android:exported="true" android:label="Definitely Not This One" android:name="com.example.application.DefinitelyNotThisOne"/>
        <receiver android:exported="true" android:name="com.example.application.Send_to_Activity"/>
    </application>
</manifest>
```

修改后编译生成apk

用adb运行对应的活动

```assembly
adb shell am start -n com.example.hellojni/com.example.application.IsThisTheRealOne
adb shell am start -n com.example.hellojni/com.example.application.ThisIsTheRealOne
adb shell am start -n com.example.hellojni/com.example.application.DefinitelyNotThisOne
```

这里要注意的是：启动Activity后，要点击按钮才能在logcat中看到相应的广播。

```assembly
07-30 18:49:14.614: D/Message -(2559): Congratulation!YouFoundTheRightActivityHereYouGo-CTF{IDontHaveABadjokeSorry}
07-30 18:49:39.322: D/Message -(2559): KeepTryingThisIsNotTheActivityYouAreLookingForButHereHaveSomeInternetPoints!
07-30 18:50:00.938: D/Message -(2559): Told you so!
```

### 抓取安卓APP日志

```assembly
adb logcat -v time>D:log.txt
```

然后运行对应的app

操作结束ctrl+c

或者使用Android-SDK中的ddms.bat或monitor.bat工具。

