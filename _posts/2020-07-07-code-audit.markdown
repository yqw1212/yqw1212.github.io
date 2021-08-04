---
layout: post
title:  代码审计
date:   2020-07-07 00:01:01 +0300
image:  2020-07-07-wolves.jpg
tags:   [ctf,web,php]
---

# extract变量覆盖

```php
<?php
$flag='xxx';
extract($_GET);
if(isset($shiyan))
{
	$content=trim(file_get_contents($flag));
	if($shiyan==$content)
	{
		echo'flag{xxx}';
	}
	else
	{
		echo'Oh.no';
	}
}
?>
```

extract() 函数从数组中将变量导入到当前的符号表。

该函数使用数组键名作为变量名，使用数组键值作为变量值。针对数组中的每个元素，将在当前符号表中创建对应的一个变量。

该函数返回成功设置的变量数目。

extract(*array,extract_rules,prefix*)

*extract_rules*:可选。extract() 函数将检查每个键名是否为合法的变量名，同时也检查和符号表中已存在的变量名是否冲突。对不合法和冲突的键名的处理将根据此参数决定。

可能的值：

* EXTR_OVERWRITE - 默认。如果有冲突，则覆盖已有的变量。

# strcmp比较字符串

```php
<?php
$flag = "flag{xxxxx}";
if (isset($_GET['a'])) {
	if (strcmp($_GET['a'], $flag) == 0) 
		//如果 str1 小于 str2 返回 < 0； 如果 str1大于 str2返回 > 0；如果两者相等，返回 0。
		//比较两个字符串（区分大小写）
		die('Flag: '.$flag);
	else
		print 'No';
}
?>
```

# urldecode二次编码绕过

```php
<?php
if(eregi("hackerDJ",$_GET[id])) {
	echo("not allowed!");
	exit();
}
$_GET[id] = urldecode($_GET[id]);
if($_GET[id] == "hackerDJ")
{
	echo "Access granted!";
	echo "flag";
}
?>
```

# 弱类型整数大小比较绕过

```php
$temp = $_GET['password'];
is_numeric($temp)?die("no numeric"):NULL;
if($temp>1336){
	echo $flag;
```

# sha()函数比较绕过

```php
<?php
$flag = "flag";
if (isset($_GET['name']) and isset($_GET['password']))
{
	var_dump($_GET['name']);
	echo "";
	var_dump($_GET['password']);
	var_dump(sha1($_GET['name']));
	var_dump(sha1($_GET['password']));
	if ($_GET['name'] == $_GET['password'])
		echo 'Your password can not be your name!';
	else if (sha1($_GET['name']) === sha1($_GET['password']))
		die('Flag: '.$flag);
	else
		echo 'Invalid password.';
	}
else
	echo 'Login first!';
?>
```

# md5加密相等绕过

```php
<?php
$md51 = md5('QNKCDZO');
$a = @$_GET['a'];
$md52 = @md5($a);
if(isset($a)){
	if ($a != 'QNKCDZO' && $md51 == $md52) {
		echo "flag{*}";
	} else {
		echo "false!!!";
	}
}
else{
    echo "please input a";
}
?>
```

PHP在处理哈希字符串时，会利用”!=”或”==”来对哈希值进行比较，它把每一个以”0E”开头的哈希值都解释为0，所以如果两个不同的密码经过哈希以后，其哈希值都是以”0E”开头的，那么PHP将会认为他们相同，都是0。

而以下这些字符串，md5哈希之后都是0e开头的：

QNKCDZO
0e830400451993494058024219903391

s878926199a
0e545993274517709034328855841020

s155964671a
0e342768416822451524974117254469

s214587387a
0e848240448830537924465865611904

s214587387a
0e848240448830537924465865611904

s878926199a
0e545993274517709034328855841020

s1091221200a
0e940624217856561557816327384675

s1885207154a
0e509367213418206700842008763514

s1502113478a
0e861580163291561247404381396064

s1885207154a
0e509367213418206700842008763514

s1836677006a
0e481036490867661113260034900752

s155964671a
0e342768416822451524974117254469

s1184209335a
0e072485820392773389523109082030

s1665632922a
0e731198061491163073197128363787

s1502113478a
0e861580163291561247404381396064

s1836677006a
0e481036490867661113260034900752

s1091221200a
0e940624217856561557816327384675

s155964671a
0e342768416822451524974117254469

s1502113478a
0e861580163291561247404381396064

s155964671a
0e342768416822451524974117254469

s1665632922a
0e731198061491163073197128363787

s155964671a
0e342768416822451524974117254469

s1091221200a
0e940624217856561557816327384675

s1836677006a
0e481036490867661113260034900752

s1885207154a
0e509367213418206700842008763514

s532378020a
0e220463095855511507588041205815

s878926199a
0e545993274517709034328855841020

s1091221200a
0e940624217856561557816327384675

s214587387a
0e848240448830537924465865611904

s1502113478a
0e861580163291561247404381396064

s1091221200a
0e940624217856561557816327384675

s1665632922a
0e731198061491163073197128363787

s1885207154a
0e509367213418206700842008763514

s1836677006a
0e481036490867661113260034900752

s1665632922a
0e731198061491163073197128363787

s878926199a
0e545993274517709034328855841020

# 十六进制与数字比较

```php
<?php
error_reporting(0);
function noother_says_correct($temp)
{
	$flag = 'flag{test}';
	$one = ord('1'); //ord — 返回字符的 ASCII 码值
	$nine = ord('9'); //ord — 返回字符的 ASCII 码值
	$number = '3735929054';
	// Check all the input characters!
	for ($i = 0; $i < strlen($number); $i++)
	{
		// Disallow all the digits!
		$digit = ord($temp{$i});
		if ( ($digit >= $one) && ($digit <= $nine) )
		{
			// Aha, digit not allowed!
			return "flase";
		}
	}
	if($number == $temp)
		return $flag;
}
$temp = $_GET['password'];
echo noother_says_correct($temp);
?>
```

# ereg正则%00截断

```php
<?php
$flag = "xxx";
if (isset ($_GET['password']))
{
	if (ereg ("^[a-zA-Z0-9]+$", $_GET['password']) === FALSE){
		echo 'You password must be alphanumeric';
	}else if (strlen($_GET['password']) < 8 && $_GET['password'] > 9999999){
		if (strpos ($_GET['password'], '-') !== FALSE) //strpos — 查找字符串首次出现的位置
		{
			die('Flag: ' . $flag);
		}
		else
		{
			echo('- have not been found');
		}
	}
	else
	{
		echo 'Invalid password';
	}
}
?>
```

```
?password[]=%00-
```

# strpos数组绕过

```php
<?php
$flag = "flag";
if (isset ($_GET['ctf'])) {
	if (@ereg ("^[1-9]+$", $_GET['ctf']) === FALSE)
		echo '必须输入数字才行';
	else if (strpos ($_GET['ctf'], '#biubiubiu') !== FALSE)
		die('Flag: '.$flag);
	else
		echo '骚年，继续努力吧啊~';
}
?>
```

# 数字验证正则绕过

```php
<?php
error_reporting(0);
$flag = 'flag{test}';
if ("POST" == $_SERVER['REQUEST_METHOD'])
{
	$password = $_POST['password'];
	if (0 >= preg_match('/^[[:graph:]]{12,}$/', $password)) //preg_match — 执行一个正则表达式匹配
	{
		echo 'flag';
		exit;
	}
	while (TRUE){
		$reg = '/([[:punct:]]+|[[:digit:]]+|[[:upper:]]+|[[:lower:]]+)/';
		if (6 > preg_match_all($reg, $password, $arr))
			break;
		$c = 0;
		$ps = array('punct', 'digit', 'upper', 'lower'); //[[:punct:]] 任何标点符号 [[:digit:]] 任何数字 [[:upper:]] 任何大写字母 [[:lower:]] 任何小写字母
		foreach ($ps as $pt){
			if (preg_match("/[[:$pt:]]+/", $password))
			$c += 1;
		}
		if ($c < 3) 
            break;
			//>=3，必须包含四种类型三种与三种以上
		if ("42" == $password) 
            echo $flag;
		else 
            echo 'Wrong password';
		exit;
	}
}
?>
```

