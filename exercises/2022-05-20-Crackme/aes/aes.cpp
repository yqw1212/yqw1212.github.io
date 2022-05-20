// aes.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <Windows.h>
#include <stdio.h>
#include <wincrypt.h>

int main()
{
    BYTE pbData[] = { 0x5c,0x53,0xa4,0xa4,0x1d,0x52,0x43,0x7a,0x9f,0xa1,0xe9,0xc2,0x6c,0xa5,0x90,0x90,0x0 };  //key_buf
    BYTE flag_encrypt[] = { 0x5B, 0x9C, 0xEE, 0xB2, 0x3B, 0xB7, 0xD7, 0x34, 0xF3, 0x1B, 0x75, 0x14, 0xC6, 0xB2, 0x1F, 0xE8, 0xDE, 0x33, 0x44, 0x74, 0x75, 0x1B, 0x47, 0x6A, 0xD4, 0x37, 0x51, 0x88, 0xFC, 0x67, 0xE6, 0x60, 0xDA, 0x0D, 0x58, 0x07, 0x81, 0x43, 0x53, 0xEA, 0x7B, 0x52, 0x85, 0x6C, 0x86, 0x65, 0xAF, 0xB4,0x0 };
    DWORD dwDataLen = 0x10;
    DWORD ddwDataLen;
    DWORD* pdwDataLen = &ddwDataLen;
    *pdwDataLen = 0x20;


    BOOL v6; // [esp+4h] [ebp-18h]
    HCRYPTKEY phKey; // [esp+Ch] [ebp-10h] BYREF
    HCRYPTPROV phProv; // [esp+10h] [ebp-Ch] BYREF
    HCRYPTHASH phHash; // [esp+14h] [ebp-8h] BYREF

    phProv = 0;
    phHash = 0;
    phKey = 0;
    v6 = CryptAcquireContextA(&phProv, 0, 0, 0x18u, 0xF0000000);
    if (v6)
    {
        v6 = CryptCreateHash(phProv, 0x8003u, 0, 0, &phHash);
        if (v6)
        {
            v6 = CryptHashData(phHash, pbData, dwDataLen, 0);
            if (v6)
            {
                v6 = CryptDeriveKey(phProv, 0x660Eu, phHash, 1u, &phKey);// key的md5值再生成aes密钥
                if (v6)
                    v6 = CryptDecrypt(phKey, 0, 1, 0, flag_encrypt, pdwDataLen);
                printf("%s", flag_encrypt);
            }
        }
    }
    if (phKey)
        CryptDestroyKey(phKey);
    if (phHash)
        CryptDestroyHash(phHash);
    if (phProv)
        CryptReleaseContext(phProv, 0);
    return v6;
}
