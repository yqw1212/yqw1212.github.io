#include <stdio.h>

int main(){

    char re1[5] = {'L', 'N', '^', 'd', 'l'};
    char re2[5] = {0x20, 0x35, 0x2d, 0x16, 0x61};
    char re3[5] = {'A', 'F', 'B', 'o', '}'};

    char flag[15] = {0};

    for(int i=0; i<4; i++){
        flag[i*3+0] = (re1[i] ^ 0x80) / 2;
    }
    flag[12] = re1[4];
    for(int i=0; i<4; i++){
        flag[i*3+1] = re2[i] ^ re1[i];
    }
    flag[13] = re2[4];
    for(int i=0; i<4; i++){
        flag[i*3+2] = re3[i] ^ re2[i];
    }
    flag[14] = re3[4];
    for(int i=0; i<15; i++){
        printf("%c", flag[i]);
    }

    return 0;
}
