---
layout: post
title:  Flag_system
date:   2021-06-17 00:01:01 +0300
image:  2021-06-17-sheet.jpg
tags:   [ctf,reverse,mobile,adworld,android,ab,rctf2015]
---

android备份文件，改后缀为.ab文件。

解析.ab文件

```assembly
java -jar abe.jar unpack Flag_system.ab Flag_system.tar
```

使用abe.jar，但是得到的tar文件无法打开。

正确的ab文件头

![]({{site.baseurl}}/img/2021-06-17-ab-header.jpg)

查看ab文件的头，将其改为：

```assembly
41 4E 44 52 4F 49 44 20  42 41 43 4B 55 50 0A 31
0A 31 0A 6E 6F 6E 65 0A  78 DA EC B9 07 50 93 61
```

解压后会得到两个apk。

zi中的apk没发现flag。分析mybackup，用jeb打开，查看SQLiteDatabaseDemo

```assembly
package com.example.mybackup;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView$OnItemClickListener;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import net.sqlcipher.Cursor;
import net.sqlcipher.database.SQLiteDatabase;

public class SQLiteDatabaseDemo extends Activity implements AdapterView$OnItemClickListener {
    public class BooksListAdapter extends BaseAdapter {
        private Context mContext;
        private Cursor mCursor;

        public BooksListAdapter(SQLiteDatabaseDemo arg1, Context arg2, Cursor arg3) {
            SQLiteDatabaseDemo.this = arg1;
            super();
            this.mContext = arg2;
            this.mCursor = arg3;
        }

        public int getCount() {
            int v0 = this.mCursor == null ? 0 : this.mCursor.getCount();
            return v0;
        }

        public Object getItem(int arg2) {
            return null;
        }

        public long getItemId(int arg3) {
            return 0;
        }

        public View getView(int arg5, View arg6, ViewGroup arg7) {
            TextView v0 = new TextView(this.mContext);
            if(this.mCursor != null) {
                this.mCursor.moveToPosition(arg5);
                if("Flag".equals(this.mCursor.getString(1))) {
                    v0.setText("Flag is here!");
                }
                else {
                    v0.setText(String.valueOf(this.mCursor.getString(1)) + "___" + this.mCursor.getString(2));
                }
            }

            return ((View)v0);
        }
    }

    private int BOOK_ID;
    private EditText BookAuthor;
    private EditText BookName;
    private ListView BooksList;
    protected static final int MENU_ADD = 1;
    protected static final int MENU_DELETE = 2;
    protected static final int MENU_UPDATE = 3;
    private BooksDB mBooksDB;
    private Cursor mCursor;

    public SQLiteDatabaseDemo() {
        super();
        this.mCursor = null;
        this.BOOK_ID = 0;
    }

    public void add() {
        String v1 = this.BookName.getText().toString();
        String v0 = this.BookAuthor.getText().toString();
        if(!v1.equals("") && !v0.equals("")) {
            this.mBooksDB.insert(v1, v0);
            if(this.mCursor != null) {
                this.mCursor.requery();
            }

            this.BooksList.invalidateViews();
            this.BookName.setText("");
            this.BookAuthor.setText("");
            Toast.makeText(((Context)this), "Add Successed!", 0).show();
        }
    }

    public void delete() {
        if(this.BOOK_ID != 0) {
            this.mBooksDB.delete(this.BOOK_ID);
            if(this.mCursor != null) {
                this.mCursor.requery();
            }

            this.BooksList.invalidateViews();
            this.BookName.setText("");
            this.BookAuthor.setText("");
            Toast.makeText(((Context)this), "Delete Successed!", 0).show();
        }
    }

    public void onCreate(Bundle arg2) {
        super.onCreate(arg2);
        this.setContentView(0x7F030001);
        SQLiteDatabase.loadLibs(((Context)this));
        this.setUpViews();
    }

    public boolean onCreateOptionsMenu(Menu arg5) {
        super.onCreateOptionsMenu(arg5);
        arg5.add(0, 1, 0, "ADD");
        arg5.add(0, 2, 0, "DELETE");
        arg5.add(0, 2, 0, "UPDATE");
        return 1;
    }

    public void onItemClick(AdapterView arg4, View arg5, int arg6, long arg7) {
        if(this.mCursor != null) {
            this.mCursor.moveToPosition(arg6);
            this.BOOK_ID = this.mCursor.getInt(0);
            if("Flag".equals(this.mCursor.getString(1))) {
                this.BookName.setText("Guess");
                this.BookAuthor.setText("Flag is here!");
            }
            else {
                this.BookName.setText(this.mCursor.getString(1));
                this.BookAuthor.setText(this.mCursor.getString(2));
            }
        }
    }

    public boolean onOptionsItemSelected(MenuItem arg2) {
        super.onOptionsItemSelected(arg2);
        switch(arg2.getItemId()) {
            case 1: {
                this.add();
                break;
            }
            case 2: {
                this.delete();
                break;
            }
            case 3: {
                this.update();
                break;
            }
        }

        return 1;
    }

    public void setUpViews() {
        this.mBooksDB = new BooksDB(((Context)this));
        this.BookName = this.findViewById(0x7F070000);
        this.BookAuthor = this.findViewById(0x7F070001);
        this.BooksList = this.findViewById(0x7F070002);
        this.BooksList.setAdapter(new BooksListAdapter(this, ((Context)this), this.mCursor));
        this.BooksList.setOnItemClickListener(((AdapterView$OnItemClickListener)this));
    }

    public void update() {
        String v1 = this.BookName.getText().toString();
        String v0 = this.BookAuthor.getText().toString();
        if(!v1.equals("") && !v0.equals("")) {
            this.mBooksDB.update(this.BOOK_ID, v1, v0);
            if(this.mCursor != null) {
                this.mCursor.requery();
            }

            this.BooksList.invalidateViews();
            this.BookName.setText("");
            this.BookAuthor.setText("");
            Toast.makeText(((Context)this), "Update Successed!", 0).show();
        }
    }
}
```

猜测flag在db文件中，而打开它需要一个key。

在BooksDB中可以找到对数据库的初始化

```assembly
package com.example.mybackup;

import android.content.ContentValues;
import android.content.Context;
import net.sqlcipher.Cursor;
import net.sqlcipher.database.SQLiteDatabase;
import net.sqlcipher.database.SQLiteOpenHelper;

public class BooksDB extends SQLiteOpenHelper {
    public static final String BOOK_AUTHOR = "book_author";
    public static final String BOOK_ID = "book_id";
    public static final String BOOK_NAME = "book_name";
    private static final String DATABASE_NAME = "BOOKS.db";
    private static final int DATABASE_VERSION = 1;
    private static final String TABLE_NAME = "books_table";
    private SQLiteDatabase db;
    private SQLiteDatabase dbr;
    private String k;

    public BooksDB(Context arg4) {
        super(arg4, "BOOKS.db", null, 1);
        this.k = Test.getSign(arg4);
        this.db = this.getWritableDatabase(this.k);
        this.dbr = this.getReadableDatabase(this.k);
    }

    public void delete(int arg5) {
        this.db.delete("books_table", "book_id = ?", new String[]{Integer.toString(arg5)});
    }

    public long insert(String arg7, String arg8) {
        ContentValues v0 = new ContentValues();
        v0.put("book_name", arg7);
        v0.put("book_author", arg8);
        return this.db.insert("books_table", null, v0);
    }

    public void onCreate(SQLiteDatabase arg2) {
        arg2.execSQL("CREATE TABLE books_table (book_id INTEGER primary key autoincrement, book_name text, book_author text);");
    }

    public void onUpgrade(SQLiteDatabase arg2, int arg3, int arg4) {
        arg2.execSQL("DROP TABLE IF EXISTS books_table");
        this.onCreate(arg2);
    }

    public Cursor select() {
        return this.dbr.query("books_table", null, null, null, null, null, null);
    }

    public void update(int arg6, String arg7, String arg8) {
        String[] v2 = new String[]{Integer.toString(arg6)};
        ContentValues v0 = new ContentValues();
        v0.put("book_name", arg7);
        v0.put("book_author", arg8);
        this.db.update("books_table", v0, "book_id = ?", v2);
    }
}
```

Test

```assembly
public static String getSign(Context arg7) {
    Object v3;
    Iterator v1 = arg7.getPackageManager().getInstalledPackages(0x40).iterator();
    do {
        if(v1.hasNext()) {
            v3 = v1.next();
            if(!((PackageInfo)v3).packageName.equals(arg7.getPackageName())) {
                continue;
            }

            break;
        }
        else {
            return "";
        }
    }
    while(true);

    String v5 = Test.SHA1(((PackageInfo)v3).signatures[0].toCharsString());
    return v5;
}
```

**public abstract PackageManager getPackageManager()**

功能：获得一个PackageManger对象

**public abstract List\<PackageInfo\> getInstalledPackages(int flags)**

参数：
　　flag为一般为GET_UNINSTALLED_PACKAGES，那么此时会返回所有ApplicationInfo。我们可以对ApplicationInfo 　　的flags过滤,得到我们需要的。

功能：返回给定条件的所有PackageInfo

分析代码，key就是取apk的签名信息

因为不知道签名到底是什么，所以修改smali代码，用日志打印变量。

```smali
const-string v1, "Hello"
 
invoke-static {v1, v5}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
```

发现signature就是META-INF\CERT.RSA文件的16进制数据。

SHA-1加密后为：7087d05a7aee9efd3c7ad6636784d7b71b040b0a，即key

然后坑点就是要选择尝试正确的sqlcipher版本进行解密即可。

```assembly
sqlite> PRAGMA KEY = 'KEY';
sqlite> .schema
CREATE TABLE android_metadata (locale TEXT);
CREATE TABLE books_table (book_id INTEGER primary key autoincrement, book_name t
ext, book_author text);
sqlite> select * from books_table
```

或者利用backup的apk中提供的sqlcipher库进行重写读取数据库也是可以获取到BOOKS.db内容。