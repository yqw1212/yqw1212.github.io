#include <stdio.h>
#include <stdlib.h>

int s;

void op(int sig, int par, int index){
    switch(sig){
        case 0x22:{
            //qword_6030C8[qword_6030C8[0x13]] = a2;
            //qword_6030C8[0x13]++;

            if(index == 0){
                printf("qword_6030C8[qword_6030C8[0x13]] = %d;\n", par);
                printf("qword_6030C8[0x13]++;\n");
            }else{
                printf("qword_6030C8[qword_6030C8[0x13]] = qword_6030C8[0x%x];\n", index);
                printf("qword_6030C8[0x13]++;\n");
            }
            break;
        }
        case 0x23:{
            //qword_6030C8[0x13]--;
            //a2 = qword_6030C8[qword_6030C8[0x13]];

            printf("qword_6030C8[0x13]--;\n");
            printf("qword_6030C8[0x%x] = qword_6030C8[qword_6030C8[0x13]];\n", index);
            break;
        }
        case 0x24:{
            //qword_6030C8[0x10] += qword_6030C8[0x11];

            printf("qword_6030C8[0x10] += qword_6030C8[0x11];\n");
            break;
        }
        case 0x25:{
            //a2 += s;


            printf("qword_6030C8[0x%d] += %d;\n", index, s);
            break;
        }
        case 0x26:{
            //qword_6030C8[0x10] -= qword_6030C8[0x11];

            printf("qword_6030C8[0x10] -= qword_6030C8[0x11];\n");
            break;
        }
        case 0x27:{
            //a2 -= s1[0x4F];

            printf("qword_6030C8[0x%x] -= %d;\n", index, s);
            break;
        }
        case 0x28:{
            //qword_6030C8[0x10] ^= qword_6030C8[0x11];

            printf("qword_6030C8[0x10] ^= qword_6030C8[0x11];\n");
            break;
        }
        case 0x29:{
            //qword_6030C8[0x15] = qword_6030C8[0x10] == qword_6030C8[0x11];

            printf("qword_6030C8[0x15] = qword_6030C8[0x10] == qword_6030C8[0x11];\n");
            break;
        }
        case 0x2A:{
            //qword_6030C8[qword_6030C8[0x13]] = qword_6030C8[0x14];
            //qword_6030C8[0x13]++;
            //qword_6030C8[0x14] = s1[0x4F];

            printf("qword_6030C8[qword_6030C8[0x13]] = qword_6030C8[0x14];\n");
            printf("qword_6030C8[0x13]++;\n");
            printf("qword_6030C8[0x14] = %d;\n", s);
            break;
        }
        case 0x2B:{
            //qword_6030C8[0x13]--;
            //qword_6030C8[0x14] = qword_6030C8[qword_6030C8[0x13];

            printf("qword_6030C8[0x13]--;\n");
            printf("qword_6030C8[0x14] = qword_6030C8[qword_6030C8[0x13];\n");
            break;
        }
        case 0x2C:{
            //qword_6030C8[0x14] = s1[0x4F];

            printf("qword_6030C8[0x14] = %d;\n", s);
            break;
        }
        case 0x2D:{
            //if ( qword_6030C8[0x15] )
            //    qword_6030C8[0x14] = s1[0x4F];

            printf("if ( qword_6030C8[0x15] )\n");
            printf("    qword_6030C8[0x14] = %d;\n", s);
            break;
        }
        case 0x2E:{
            //qword_6030C8[qword_6030C8[0x13]] = qword_6030C8[8][qword_6030C8[0x12]];

            printf("qword_6030C8[qword_6030C8[0x13]] = qword_6030C8[8][qword_6030C8[0x12]];\n");
            break;
        }
        case 0x2F:{
            //qword_6030C8[0x13]--;
            //qword_6030C8[8][qword_6030C8[0x12]] = qword_6030C8[qword_6030C8[0x13];

            printf("qword_6030C8[0x13]--;\n");
            printf("qword_6030C8[8][qword_6030C8[0x12]] = qword_6030C8[qword_6030C8[0x13];\n");
            break;
        }
    }
}

int main(){
    int opcode[87] = {17, 52, 0, 42, 5, 16, 20, 9, 23, 0, 36, 5, 3, 17, 29, 6, 0, 0, 5, 3, 17, 64, 6, 0, 72, 5, 17, 29, 23, 14, 1, 21, 4, 15, 1, 22, 2, 0, 0, 4, 3, 5, 16, 20, 50, 5, 9, 2, 19, 29, 5, 18, 21, 4, 16, 20, 61, 10, 1, 19, 52, 3, 4, 18, 14, 1, 21, 4, 7, 1, 22, 2, 0, 0, 4, 3, 5, 16, 20, 85, 5, 9, 1, 19, 64, 5, 18};
    int qword_6030C8[100] = {};

    //for(int i=0; opcode[i]!=0x17; i++){
    for(int i=0; i<87; i++){
        int opc = opcode[i];
        switch(opc){
            case 0:
            case 8:
            case 9:
            case 0xA:
            case 0xC:
            case 0xD:
            case 0xE:
            case 0x11:
            case 0x13:
            case 0x14:{
                s = opcode[++i];
                break;
            }
            default:
                break;
        }
        switch(opc){
            case 0:
                op(0x22, s, 0);
                break;
            case 1:
                op(0x22, qword_6030C8[0x10], 0x10);
                break;
            case 2:
                op(0x22, qword_6030C8[0x11], 0x11);
                break;
            case 3:
                op(0x22, qword_6030C8[0x12], 0x12);
                break;
            case 4:
                op(0x23, qword_6030C8[0x10], 0x10);
                break;
            case 5:
                op(0x23, qword_6030C8[0x11], 0x11);
                break;
            case 6:
                op(0x23, qword_6030C8[0x12], 0x12);
                break;
            case 7:
                op(0x24, 0, 0);
                break;
            case 8:
                op(0x25, qword_6030C8[0x10], 0x10);
                break;
            case 9:
                op(0x25, qword_6030C8[0x11], 0x11);
                break;
            case 0xA:
                op(0x25, qword_6030C8[0x12], 0x12);
                break;
            case 0xB:
                op(0x26, 0, 0);
                break;
            case 0xC:
                op(0x27, qword_6030C8[0x10], 0x10);
                break;
            case 0xD:
                op(0x27, qword_6030C8[0x11], 0x11);
                break;
            case 0xE:
                op(0x27, qword_6030C8[0x12], 0x12);
                break;
            case 0xF:
                op(0x28, 0, 0);
                break;
            case 0x10:
                op(0x29, 0, 0);
                break;
            case 0x11:
                op(0x2A, 0, 0);
                break;
            case 0x12:
                op(0x2B, 0, 0);
                break;
            case 0x13:
                op(0x2C, 0, 0);
                break;
            case 0x14:
                op(0x2D, 0, 0);
                break;
            case 0x15:
                op(0x2E, 0, 0);
                break;
            case 0x16:
                op(0x2F, 0, 0);
                break;
            default:
                op(2, 0, 0);
                break;
        }
    }

    char result[42] = {0xA3, 0xD8, 0xAC, 0xA9, 0xA8, 0xD6, 0xA6, 0xCD, 0xD0, 0xD5,
                       0xF7, 0xB7, 0x9C, 0xB3, 0x31, 0x2D, 0x40, 0x5B, 0x4B, 0x3A,
                       0xFD, 0x57, 0x42, 0x5F, 0x58, 0x52, 0x54, 0x1B, 0x0C, 0x78,
                       0x39, 0x2D, 0xD9, 0x3D, 0x35, 0x1F, 0x09, 0x41, 0x40, 0x47,
                       0x42, 0x11};
    for(int i=41; i>=0; i--){
        result[i] = result[i] ^ (72 + 2*(41-i));
        //printf("%d ", result[i]);
    }

    for(int i=41; i>=0; i--){
        result[i] -= (41-i);
        //printf("%d ", result[i]);
    }

    for(int i=41; i>=0; i--){
        result[i] ^= 36 + (2*(41-i));
    }
    for(int i=0; i<42; i++){
        printf("%c", result[i]);
    }

    return 0;
}
