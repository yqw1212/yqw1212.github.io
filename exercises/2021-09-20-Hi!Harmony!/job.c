#include <stdio.h>

int main(){
    int data[22] = {0x48, 0x41, 0x52, 0x4d, 0x4f, 0x4e, 0x59, 0x44, 0x52, 0x45, 0x41,
                    0x4d, 0x49, 0x54, 0x50, 0x4f, 0x53, 0x53, 0x49, 0x42, 0x4c, 0x45};
    for(int i=0; i<22; i++){
        if(data[i] < 0x5b){
            data[i] = (data[i] + '\x03' - 'A')%26 + 'A';
        }else {
            data[i] = 'A' + (data[i]-0x57)%0x1a;
        }
        printf("%c", data[i]);
    }
    return 0;
}
