#include <stdio.h>

int main(){
    int g_a1[10] = {0};

    for(int i=32; i<127; i++){
        //printf("\n%d ", i);
        for(int j=32; j<127; j++){
            for(int m=32; m<127; m++){
                for(int n=32; n<127; n++){
                    int a1[10] = {0};
                    a1[1] = i;
                    a1[2] = 24;
                    a1[1] <<= a1[2];
                    a1[9] = a1[1];

                    a1[1] = j;
                    a1[2] = 16;
                    a1[1] <<= a1[2];
                    a1[9] += a1[1];

                    a1[1] = m;
                    a1[2] = 8;
                    a1[1] <<= a1[2];
                    a1[9] += a1[1];

                    a1[1] = n;
                    a1[9] += a1[1];

                    a1[1] = a1[9];
                    a1[2] = 5;
                    a1[1] >>= a1[2];
                    a1[1] ^= a1[9];
                    a1[9] = a1[1];
                    a1[2] = 7;
                    a1[1] <<= a1[2];
                    a1[2] = 0x98f17723;
                    a1[1] &= a1[2];
                    a1[1] ^= a1[9];
                    a1[9] = a1[1];
                    a1[2] = 24;
                    a1[1] <<= a1[2];
                    a1[2] = 0x35e4b920;
                    a1[1] &= a1[2];
                    a1[1] ^= a1[9];
                    a1[9] = a1[1];
                    a1[2] = 18;
                    a1[1] >>= a1[2];
                    a1[1] ^= a1[9];
                    //printf("%x\n", a1[1]);
                    if( a1[1] == 0x6FEBF967 ){
                        printf("%c%c%c%c", i, j, m, n);
                        //puts("");
                        for(int k=0; k<10; k++){
                            //g_a1[k] = a1[k];
                            //printf("%d, ", a1[k]);
                        }
                        break;
                    }
                }
            }
        }
    }

    //for(int i=0; i<=0xffffffff; i++){

    for(int i=32; i<127; i++){
        for(int j=32; j<127; j++){
            for(int m=32; m<127; m++){
                for(int n=32; n<127; n++){

                    unsigned int a1[10] = {0};

                    a1[1] = i; // 0x62
                    a1[2] = 24;
                    a1[1] <<= a1[2];
                    a1[9] = a1[1];

                    a1[1] = j; // 0x30
                    a1[2] = 16;
                    a1[1] <<= a1[2];
                    a1[9] += a1[1];

                    a1[1] = m; // 0x36
                    a1[2] = 8;
                    a1[1] <<= a1[2];
                    a1[9] += a1[1];

                    a1[1] = n; // 0x63
                    a1[9] += a1[1];

                    //a1[9] = i;

                    a1[1] = a1[9]; // 0x62303663
                    a1[3] = 32;
                    a1[1] *= a1[3]; // 正常应该是0xc4606cc60, 溢出后变成0x4606cc60
                    a1[4] = a1[1]; // 正常应该是0xc4606cc60, 溢出后变成0x4606cc60
                    a1[1] ^= a1[9]; // 0xc2436fa03, 溢出0x2436fa03
                    a1[2] = 17;
                    a1[1] >>= a1[2]; // 0x6121b, 溢出0x121b
                    a1[5] = a1[1]; // 0x6121b, 溢出0x121b
                    a1[1] = a1[5]; // 0x6121b, 溢出0x121b
                    a1[1] ^= a1[4]; // 0xc4600de7b, 溢出0x4606de7b
                    a1[1] ^= a1[9]; // 0xc2430e818, 溢出0x2436e818
                    a1[2] = 13;
                    a1[1] <<= a1[2]; // 0x184861d030000, 溢出0xdd030000
                    a1[1] ^= a1[9];
                    a1[1] ^= a1[4];
                    a1[1] ^= a1[5]; // 0x1848a3933e818, 溢出0xf935e818
                    a1[9] = a1[1]; // 0x1848a3933e818, 溢出0xf935e818
                    a1[3] = 32;
                    a1[1] *= a1[3]; // 0x309147267d0300, 溢出0x26bd0300
                    a1[4] = a1[1]; // 0x309147267d0300, 溢出0x26bd0300
                    a1[1] ^= a1[9]; // 0x3115cd1f4eeb18, 溢出0xdf88eb18
                    a1[2] = 17;
                    a1[1] >>= a1[2]; // 0x188ae68fa7, 溢出0xffffefc4
                    a1[5] = a1[1];
                    a1[1] = a1[5]; // 0x188ae68fa7, 溢出0xffffefc4
                    a1[1] ^= a1[4];
                    a1[1] ^= a1[9]; // 0x3115d595a864bf, 溢出0x207704dc
                    a1[2] = 13;
                    a1[1] <<= a1[2]; // 0x622bab2b50c97e000, 溢出0xe09b8000
                    a1[1] ^= a1[9];
                    a1[1] ^= a1[4];
                    a1[1] ^= a1[5]; // 0x6228ba760993f84bf, 0xc0ec84dc
                    //printf("%x\n", a1[1]);

                    if ( a1[1] == 0xCF1304DC ){
                        printf("%c%c%c%c", i, j, m, n);
                        //printf("%x", i);
                    }
                }
            }
        }
    }

    for(int i=32; i<127; i++){
        for(int j=32; j<127; j++){
            for(int m=32; m<127; m++){
                for(int n=32; n<127; n++){
                    unsigned int a1[10] = {0};

                    a1[1] = i;
                    a1[2] = 24;
                    a1[1] <<= a1[2];
                    a1[9] = a1[1];

                    a1[1] = j;
                    a1[2] = 16;
                    a1[1] <<= a1[2];
                    a1[9] += a1[1];

                    a1[1] = m;
                    a1[2] = 8;
                    a1[1] <<= a1[2];
                    a1[9] += a1[1];

                    a1[1] = n;
                    a1[9] += a1[1];

                    a1[1] = a1[9];
                    a1[3] = 32;
                    a1[1] *= a1[3];
                    a1[4] = a1[1];
                    a1[1] ^= a1[9];
                    a1[2] = 17;
                    a1[1] >>= a1[2];
                    a1[5] = a1[1];
                    a1[1] = a1[5];
                    a1[1] ^= a1[4];
                    a1[1] ^= a1[9];
                    a1[2] = 13;
                    a1[1] <<= a1[2];
                    a1[1] ^= a1[9];
                    a1[1] ^= a1[4];
                    a1[1] ^= a1[5];
                    a1[9] = a1[1];
                    a1[3] = 32;
                    a1[1] *= a1[3];
                    a1[4] = a1[1];
                    a1[1] ^= a1[9];
                    a1[2] = 17;
                    a1[1] >>= a1[2];
                    a1[5] = a1[1];
                    a1[1] = a1[5];
                    a1[1] ^= a1[4];
                    a1[1] ^= a1[9];
                    a1[2] = 13;
                    a1[1] <<= a1[2];
                    a1[1] ^= a1[9];
                    a1[1] ^= a1[4];
                    a1[1] ^= a1[5];
                    if ( 0x283B8E84 == a1[1] ){
                        printf("%c%c%c%c", i, j, m, n);
                    }
                }
            }
        }
    }

    return 0;
}
