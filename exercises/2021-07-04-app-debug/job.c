#include <stdio.h>
#include <stdint.h>

void decrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], sum=0x458BCD42*32, i;  /* set up */
    uint32_t delta=0x458BCD42;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<32; i++) {                         /* basic cycle start */
        v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
        v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        sum -= delta;
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}

int main() {

    uint32_t v[2]={0xF5A98FF3,0xA21873A3}, k[4]={9, 7, 8, 6};

    decrypt(v, k);
    printf("%u,%u\n",v[0],v[1]);
    puts(v);

    return 0;
}
