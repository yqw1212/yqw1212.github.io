---
layout: post
title:  2020-之江杯-工业控制(ICS)
date:   2021-06-19 00:01:01 +0300
image:  2021-06-19-drop.jpg
tags:   [ctf,iot,之江杯2020]
---

### 异常的工程文件

直接使用findstr查找flag

1、在当前目录及所有子目录下的所有文件中查找

在当前目录及所有子目录下的所有文件中查找"backup"这个字符串，*.*表示所有类型的文件。

```assembly
findstr /s /i "backup" *.*
```

2、查找带有空格的字符串

在当前目录及所有子目录下查找"backup jobs"

```assembly
findstr /s /i /c:"backup jobs" *.*
```

3、指定路径查找字符串"cmd"

在C:\tmp\查找所有txt文件的字符串"cmd"

```assembly
findstr /s /i /c:"cmd" C:\tmp\*.txt
```

查找

```assembly
异常的工程文件>findstr /s /i "flag" *.*
drw\untitled.drw:    MASTER    c   "   ?  r?     E        竛錍诃禖  €?     flag{854P_l  pA  pA                                          r?     E        F4﨏b:D??     工控安全大赛 D
FINDSTR: 写入错误
```

flag显示存在问题，直接在drw\untitled.drw文件中查看。

flag{854P_l5q2_9Y4a_30Yw}

### 病毒文件恢复

使用360在线[勒索病毒解密](https://lesuobingdu.360.cn/)

flag{fngD_vwfW_JTqI_E4Kl}

### 注册表分析

此为某黑客主机注册表文件，请分析出此黑客进行连接的WiFi名称

直接notepad打开然后找到wifi段

```assembly
[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged\010103000F0000F0080000000F0000F022B6203E5D064771A2ED7FF97A155B329CB0B7491D1532A465ED7ABDACC13138]
"ProfileGuid"="{9B5BA71F-779F-4CE6-A6D4-33C2FD55317A}"
"Description"="网络"
"Source"=dword:00000008
"DnsSuffix"="<无>"
"FirstNetwork"="网络"
"DefaultGatewayMac"=hex:d4,5d,64,7c,1d,08

[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged\010103000F0000F0080000000F0000F08E693D017C5FABC122E97AF7540491021AEC959B69A490D6884EB0101F5129E1]
"ProfileGuid"="{6E6D2E56-BC24-47D5-8F55-8891506C0C3F}"
"Description"="OPPO Reno"
"Source"=dword:00000008
"DnsSuffix"="<无>"
"FirstNetwork"="OPPO Reno"
"DefaultGatewayMac"=hex:6e,58,6e,70,69,44
```

flag{OPPOReno}