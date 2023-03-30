#include <stdbool.h>
#include <stdio.h>
#define MX \
  ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))

/*
bool btea(unsigned int* v, int n, unsigned int* k) {
  unsigned int z = v[n - 1], y = v[0], sum = 0, e, DELTA = 0x67616C66;
  unsigned int p, q;
  if (n > 1) {
    q = 12;
    while (q-- > 0) {
      sum += DELTA;
      e = (sum >> 2) & 3;
      for (p = 0; p < n - 1; p++)
        y = v[p + 1], z = v[p] += MX;
      y = v[0];
      z = v[n - 1] += MX;
    }
    return 0;
  } else if (n < -1) {
    n = -n;
    q = 12;
    sum = 0xD89114C8;
    while (sum != 0) {
      e = (sum >> 2) & 3;
      for (p = n - 1; p > 0; p--)
        z = v[p - 1], y = v[p] -= MX;
      z = v[n - 1];
      y = v[0] -= MX;
      sum -= DELTA;
    }
    return 0;
  }
  return 1;
}

int main(int argc, char const* argv[]) {
  // test  C883B3AA  468312C4

  unsigned int v[9] = {0xC883B3AA, 0x7FB3950,
                       0x75BC5959, 0x7AB57E27,
                       0xC0249800, 0xADA35753,
                       0xBF1D493F, 0x6E14AF04,
                       0x468312C4}, key[4] = {0x04DB, 0x0000E, 0x0017, 0x02A6};
  //unsigned int v[2] = {0x12C4, 0x4683}, key[4] = {0xE, 0x000004DB, 0x2A6, 0x00000017};


  btea(v, -9, key);
  printf("%x\n", v[0]);
  return 0;
}
*/

#include <stdio.h>
#include <stdint.h>
#define MX (((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4))) ^ ((sum ^ y) + (key[(p & 3) ^ e] ^ z))
#define DELTA 0x67616C66


//XXTEA 解密，把加密的步骤反过来即可得到解密的方法
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
    unsigned int v[9] = {0xC883B3AA, 0x7FB3950,
                         0x75BC5959, 0x7AB57E27,
                         0xC0249800, 0xADA35753,
                         0xBF1D493F, 0x6E14AF04,
                         0x468312C4}, key[4] = {0x04DB, 0x0000E, 0x0017, 0x02A6};
    xxtea_uint_decrypt(v,9,key);
    for(int i=0; i<9; i++){
        printf("%x ",v[i]);
    }

    printf("\n%s", v);
    return 0;
}
// 541c290d-e89f-4539-8d24-2ccbd1ead8ae
// c144d09298e-54f-8-93-42dbcc2ae1dea8d
