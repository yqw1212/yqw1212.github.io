---
layout: post
title:  PixelShooter[MRCTF2020]
date:   2020-08-09 00:01:01 +0300
image:  2020-08-09-glass.jpg
tags:   [ctf,reverse,cs]
---

下载文件是一个apk文件，手机没报病毒，于是先安装到手机上大致了解一下是什么软件，

安装好可以看到是一个打飞机的游戏，试着玩一玩找找flag的线索

![]({{site.baseurl}}/img/2020-08-09-screenshot.jpg)

我在这里用jeb打开文件查看源码，在所有类中找了一年都没找到有用的信息。

后来改变思路

Unity3d 是基于 Mono的，我们平时写的 C# 脚本都被编译到了 Assembly-CSharp.dll ，然后 再由 Mono 来加载、解析、然后执行。

于是解压apk文件在，在./assets/bin/Data/Managed目录下找到了Assembly-CSharp.dll文件

dnSpy打开文件，找到游戏的入口类GameController

根据游戏死亡后的给出线索，flag应该和游戏中的死亡有关，自然而然查看这个类的GameOver()函数

```c#
public void GameOver()
{
	this.isGameOver = true;
	this.UI.GetComponent<UIController>().GameOver(this.score, this.bestScore);
	if (PlayerPrefs.HasKey("bestScore"))
	{
		this.bestScore = Mathf.Max(this.score, PlayerPrefs.GetInt("bestScore"));
	}
	else
	{
		this.bestScore = this.score;
	}
	base.GetComponent<AudioSource>().Stop();
}
```

其中判断语句是负责记录历史最好成绩的，应该和flag没关系。所以查看GameOver(this.score, this.bestScore)函数，得到flag。