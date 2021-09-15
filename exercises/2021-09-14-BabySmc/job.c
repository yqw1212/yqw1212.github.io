#include <stdio.h>

int main(){
    unsigned char ida_chars[] ={228, 196, 231, 199, 230, 198, 225, 193, 224, 192,
                                227, 195, 226, 194, 237, 205, 236, 204, 239, 207,
                                238, 206, 233, 201, 232, 200, 235, 203, 234, 202,
                                245, 213, 244, 212, 247, 215, 246, 214, 241, 209,
                                240, 208, 243, 211, 242, 210, 253, 221, 252, 220,
                                255, 223, 149, 156, 157, 146, 147, 144, 145, 150,
                                151, 148, 138, 142};
    unsigned char result[56] = {"H>oQn6aqLr{DH6odhdm0dMe`MBo?lRglHtGPOdobDlknejmGI|ghDb<4"};
    char xor[4] = {0xA6, 0xA3, 0xA9, 0xAC};
    for(int i=0; i<56; i++){
        result[i] ^= xor[i%4];
    }

    char right[65] = {"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"};
    int flag[56] = {}, point=0;

    for(int i=0; i<56; i++){
        for(int j=0; j<64; j++){
            if(ida_chars[j] == result[i]){
                flag[point++] = right[j];
                break;
            }
        }
    }
    /*
    for(int i=0; i<56; i++){
        printf("%d ", result[i]);
    }
    */
    for(int i=0; i<56; i++){
        printf("%c", flag[i]);
    }
    return 0;
}
