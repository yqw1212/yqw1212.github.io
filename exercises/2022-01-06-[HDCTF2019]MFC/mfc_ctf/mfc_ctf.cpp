// mfc_ctf.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <Windows.h>
#include <stdio.h>

int main()
{
	HWND h = FindWindowA(NULL, "Flag就在控件里");
	if (h){
		SendMessage(h, 0x0464, 0, 0);
		printf("success");
	} else {
		printf("failure");
	}
}
