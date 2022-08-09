#include <stdio.h>
#include <stdint.h>
#define MX (((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4))) ^ ((sum ^ y) + (key[(p & 3) ^ e] ^ z))
#define DELTA 0x9e3779b9

//XXTEA ���ܣ��ڴ�����������ÿ������ʱ�������������ݣ�ʹ��MX�����������ֵ
static uint32_t * xxtea_uint_encrypt(uint32_t * data, size_t len, uint32_t * key) {
    uint32_t n = (uint32_t)len - 1;
    uint32_t z = data[n], y, p, q = 6 + 52 / (n + 1), sum = 0, e;

    if (n < 1) return data;

    while (0 < q--) {
        sum += DELTA;
        // ����sum ����ó�0~3�е�ĳһ����ֵ, ����MX����p��ͬ����ѡ��key������ĳ����Կֵ
        e = sum >> 2 & 3;

        //����ÿ�������ܵ�����
        for (p = 0; p < n; p++) {
            //z�ĳ�ֵΪdata[len - 1]�������������鵱���ǻ��ζ���������ģ���β������������data[0]ʱ����Ҫ�õ�data[len - 1]��data[0]��data[0 + 1]���Լ�MX���㷵�صĵ�һ������ֵ������ֵ��data[0]��Ӻ�ﵽ���ܵ�Ч��
            y = data[p + 1];
            z = data[p] += MX;
        }

        //������data[len-1]ʱ����Ҫ�õ�data[len - 2]��data[len-1]��data[0]���Լ�MX���㷵�صĵ�һ������ֵ������ֵ��data[len-1]��Ӻ�ﵽ���ܵ�Ч��
        y = data[0];
        z = data[n] += MX;
    }

    return data;
}

//XXTEA ���ܣ��Ѽ��ܵĲ��跴�������ɵõ����ܵķ���
static uint32_t * xxtea_uint_decrypt(uint32_t * data, size_t len, uint32_t * key) {
    uint32_t n = (uint32_t)len-1;
    uint32_t z, y = data[0], p, q = 6 + 52 / (n + 1), sum = q * DELTA, e;

    if (n < 1) return data;

    while (sum != 0) {
        e = sum >> 2 & 3;

        for (p = n; p > 0; p--) {
            z = data[p - 1];
            y = data[p] -= MX;
        }

        z = data[n];
        y = data[0] -= MX;
        sum -= DELTA;
    }

    return data;
}

int main(int argc, char const *argv[])
{
    uint32_t v[8]={0x10BD3B47, 0x6155E0F9,
                   0x6AF7EBC5, 0x8D23435F,
                   0x1A091605, 0xD43D40EF,
                   0xB4B16A67, 0x6B3578A9},key[4]={0x1234,0x2345,0x4567,0x6789};
    xxtea_uint_decrypt(v,8,key);
    for(int i=0; i<8; i++){
        printf("%x",v[i]);
    }
    return 0;
}
// 49f7 1293 d427 cd36 9ca0 ef6c 99fb 88af
// 7f943921724d63dc0ac9c6febf99fa88
