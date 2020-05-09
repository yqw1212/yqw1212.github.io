---
layout: post
title:  PHP学习(一)
date:   2020-04-23 14:02:00 +0300
image:  5-loveourplanet.jpg
tags:   [PHP]
---

## date函数的格式参数表：

| 字符       | 说明                              | 返回值                         |
| ---------- | --------------------------------- | ------------------------------ |
| d          | 月份中的第几天，有前导零的2位数字 | 01到31                         |
| D          | 英文星期几，3个字母               | Mon到Sun                       |
| j          | 月份中的第几天，没有前导零        | 1到31                          |
| l（大写i） | 英文星期几                        | Sunday到Saturday               |
| N          | 1格式数字表示的星期               | 1(表示星期一)到7               |
| S          | 每月天数后面的英文后缀，2个字符   | st,nd,rd或者th。可以和jg一起用 |
| w(小写)    | 星期中的第几天,数字表示           | 0(表示星期天)到6               |
| z          | 一年中的第几天                    | 0到366                         |
| W          | 年份中的第几周，每周从星期一开始  |                                |
| F          | 月份，完整的文本格式              | January到December              |
| m          | 数字表示月份，有前导零            | 01到12                         |
| M          | 3个字母缩写表示的月份             | Jan到Dec                       |
| n          | 数字表示月份，没有前导零          | 1到12                          |
| t          | 给定月份所应有的天数              | 28到31                         |
| L          | 是否为闰年                        | 如果是闰年为1，否则为0         |
| o          | 格式年份数字                      | 例如2007                       |
| Y          | 4位数字完整表示年份               | 例如1999或2008                 |
| y          | 2位数字表示的年份                 | 例如99或08                     |
| a          | 小写的上午和下午                  | am和pm                         |
| A          | 大写的上午和下午                  | AM和PM                         |
| g          | 小时，12小时格式，没有前导零      | 1到12                          |
| G          | 小时，24小时格式，没有前导零      | 0到23                          |
| i          | 有前导零的分钟数                  | 00到59                         |
| s          | 秒数，有前导零                    | 00到59                         |
| e          | 时区标识                          |                                |
| U          | 从Unix纪元开始至今的秒数          | 长整型数字                     |

### mktime(时,分,秒,月,日,年)

### strtotime()

```php
<?php
//now为现在的当前时间
echo strtotime("now")."<br />";
//2000年9月10日
echo strtotime("10 September 2000")."<br />";
//当前时间加一天
echo strtotime("+1 day")."<br />";
//当前时间加一周
echo strtotime("+1 week")."<br />";
//当前时间加一周2天4小时2秒
echo strtotime("+1 week 2 days 4 hours 2 seconds")."<br />";
//下一个星期四
echo strtotime("next Thursday")."<br />";
//上一个星期一
echo strtotime("last Monday")."<br />";
?>
```

## 常用字符串函数

| 函数名             | 描述                                   | 实例                                              |
| ------------------ | -------------------------------------- | ------------------------------------------------- |
| trim()             | 删除字符串两端的空格或其他预定义字符   |                                                   |
| rtrim()            | 删除字符串右端的空格或其他预定义字符   |                                                   |
| chop()             | rtrim()的别名                          |                                                   |
| ltrim()            | 删除字符串左端的空格或其他预定义字符   |                                                   |
| dirname()          | 回路径中的目录部分                     |                                                   |
| str_pad()          | 把字符串填充为指定的长度               | str_pad($str,20)                                  |
| str_repeat()       | 重复使用指定字符串                     | str_repeat("",13)                                 |
| str_split()        | 把字符串分割到数组中去                 |                                                   |
| strrev()           | 反转字符串                             |                                                   |
| wordwrap()         | 按照指定长度对字符串进行拆行处理       |                                                   |
| str_shuffle()      | 随机地打乱字符串中所有字符             |                                                   |
| parse_str()        | 将字符串解析成变量                     |                                                   |
| number_format()    | 通过千位分组来格式化数字               |                                                   |
| strtolower()       |                                        |                                                   |
| strtoupper()       |                                        |                                                   |
| ucfirst()          | 字符串首字母大写                       |                                                   |
| ucwords()          | 字符串每个单词首字母转为大写           |                                                   |
| htmlentities()     | 把字符转为HTML实体                     |                                                   |
| htmlspecialchars() | 预定义字符转html编码                   |                                                   |
| nl2br              | \n转义为标签                           |                                                   |
| strip_tags()       | 剥去HTML,XML以及PHP的标签              |                                                   |
|                    |                                        |                                                   |
| addcslashes()      | 在指定的字符前添加反斜线转义字符中字符 | echo addcslashes($str,'m');                       |
| stripcslashes()    | 删除由addcslashes()添加的反斜线        |                                                   |
| addslashes()       | 指定预定义字符前添加反斜线             | $str = "Who's John Adams?";echo addslashes($str); |
| stripslashes()     | 删除由addslashes()添加的转义字符       |                                                   |
| quotemeta()        | 在字符串中某些预定义的字符前添加反斜线 |                                                   |
|                    |                                        |                                                   |
| chr()              | CII值返回字符                          | echo chr(052);                                    |
| ord()              | 一个字符的ASCII值                      | echo ord("hello");                                |
| strcasecmp()       | 不区分大小写比较两字符串               |                                                   |

## 操作数组函数

| 函数          | 功能                   |
| ------------- | ---------------------- |
| array_shift   | 弹出数组中的第一个元素 |
| array_unshift | 在数组的开始压入元素   |
| array_push    | 在数组的末尾处压入元素 |
| array_pop     |                        |
| current       | 读出指针当前位置的值   |
| key           | 读出指针当前位置的键   |
| next          | 指针向下移             |
| prev          | 向上移                 |
| reset         | 指针到开始处           |
| end           | 指针到结束处           |

## 数组常用函数

| 函数名称             | 功能                                                   |
| -------------------- | ------------------------------------------------------ |
| array_combine()      | 生成一个数组,用一个数组的值作为键名,另一个数组值作为值 |
| range()              | 创建并返回一个包含指定范围的元素的数组。               |
| compact()            | 创建一个由参数所带变量组成的数组                       |
| array_chunk()        | 把一个数组分割为新的数组块                             |
| array_merge()        | 把两个或多个数组合并为一个数组                         |
| array_diff()         | 返回两个数组的差集数组                                 |
| array_search()       | 在数组中搜索给定的值，如果成功则返回相应的键名         |
| array_splice()       | 把数组中的一部分去掉并用其它值取代                     |
| array_sum()          | 计算数组中所有值的和                                   |
| in_array()           | 检查数组中是否存在某个值                               |
| array_key_exists()   | 检查给定的键名或索引是否存在于数组中                   |
| shuffle()            | 将数组打乱,保留键值                                    |
| count()              | 计算数组中的单元数目或对象中的属性个数                 |
| array_flip()         | 返回一个键值反转后的数组                               |
| array_keys()         | 返回数组所有的键,组成一个数组                          |
| array_values()       | 返回数组中所有值，组成一个数组                         |
| array_reverse()      | 返回一个元素顺序相反的数组                             |
| array_count_values() | 统计数组中所有的值出现的次数                           |
| array_rand()         | 从数组中随机抽取一个或多个元素,注意是键名              |
| array_unique()       | 删除重复值，返回剩余数组                               |
|                      |                                                        |
| sort()               | 按升序对给定数组的值排序,不保留键名                    |
| rsort()              | 对数组逆向排序,不保留键名                              |
| asort()              | 对数组排序,保持索引关系                                |
| arsort()             | 对数组逆向排序,保持索引关系                            |
| ksort()              | 按键名对数组排序                                       |
| krsort()             | 将数组按照键逆向排序                                   |
| natsort()            | 用自然顺序算法对数组中的元素排序                       |
| natcasesort()        | 自然排序,不区分大小写                                  |
|                      |                                                        |
| array_filter()       | 去掉数组中的空元素或者预定元素                         |
| extract              | 将键变为变量名，将值变为变量值                         |

