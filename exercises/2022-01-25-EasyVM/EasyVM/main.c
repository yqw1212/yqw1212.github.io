#include <stdio.h>
#include <stdlib.h>

int main(){

    int op[31] = {0xCA, 0x00, 0x00, 0x00, 0x00, 0xCB, 0x00, 0x00, 0x00, 0x00,
                  0xCC, 0xCF, 0xC9, 0xEE, 0x00, 0x00, 0x00, 0xCF, 0xD1, 0xD3,
                  0x01, 0xFE, 0xC2, 0xD2, 0x39, 0x00, 0x00, 0x00, 0xD4, 0xEC,
                  0xFF};
    int op_point=0;

    int data[57] = {0xBE, 0x36, 0xAC, 0x27, 0x99, 0x4F, 0xDE, 0x44, 0xEE, 0x5F,
                    0xDA, 0x0B, 0xB5, 0x17, 0xB8, 0x68, 0xC2, 0x4E, 0x9C, 0x4A,
                    0xE1, 0x43, 0xF0, 0x22, 0x8A, 0x3B, 0x88, 0x5B, 0xE5, 0x54,
                    0xFF, 0x68, 0xD5, 0x67, 0xD4, 0x06, 0xAD, 0x0B, 0xD8, 0x50,
                    0xF9, 0x58, 0xE0, 0x6F, 0xC5, 0x4A, 0xFD, 0x2F, 0x84, 0x36,
                    0x85, 0x52, 0xFB, 0x73, 0xD7, 0x0D, 0xE3};

    int _this[9] = {0};


    int a5[57] = {80, 102, 116, 0};

    _this[1] = op[op_point];

    while ( 2 ){
        printf("%x\n", _this[1]);
        switch ( _this[1] ){
            case 0xC0:
                // sub_4013B0

                ++_this[2];

                _this[1] = op[++op_point];
                continue;
            case 0xC1:
                // sub_4013C0
                ++_this[3];

                _this[1] = op[++op_point];
                continue;
            case 0xC2:
                // sub_4013D0
                printf("++_this[4];\n");

                ++_this[4];

                _this[1] = op[++op_point];
                continue;
            case 0xC3:
                // sub_4013E0
                _this[2] = _this[3];

                _this[1] = op[++op_point];
                continue;
            case 0xC4:
                // sub_4013F0
                _this[2] = _this[4];

                _this[1] = op[++op_point];
                continue;
            case 0xC5:
                // sub_401400
                _this[3] = _this[2];

                _this[1] = op[++op_point];
                continue;
            case 0xC6:
                // sub_401410
                _this[3] = _this[4];

                _this[1] = op[++op_point];
                continue;
            case 0xC7:
                // sub_401420
                _this[4] = _this[2];

                _this[1] = op[++op_point];
                continue;
            case 0xC8:
                // sub_401430
                _this[4] = _this[3];

                _this[1] = op[++op_point];
                continue;
            case 0xC9:
                // sub_401440
                printf("_this[2] = %d\n", op[op_point+1]);

                _this[2] = op[op_point+1];

                _this[1] = op[op_point+5];
                op_point += 5;
                continue;
            case 0xCA:
                // sub_401450
                printf("_this[3] = %d\n", op[op_point+1]);

                _this[3] = op[op_point+1];

                _this[1] = op[op_point+5];
                op_point += 5;
                continue;
            case 0xCB:
                // sub_401460
                printf("_this[4] = %d\n", op[op_point+1]);

                _this[4] = op[op_point+1];

                _this[1] = op[op_point+5];
                op_point += 5;
                continue;
            case 0xCC:
                // sub_401470
                printf("_this[2] = a5[%d]\n", _this[4]);

                _this[2] = a5[_this[4]];

                _this[1] = op[++op_point];
                continue;
            case 0xCD:
                // sub_401490
                _this[3] = a5[_this[4]];

                _this[1] = op[++op_point];
                continue;
            case 0xCE:
                // sub_4014B0
                _this[2] ^= _this[3];

                _this[1] = op[++op_point];
                continue;
            case 0xCF:
                // sub_4014D0
                printf("_this[3] ^= _this[2]\n");

                _this[3] ^= _this[2];

                _this[1] = op[++op_point];
                continue;
            case 0xD0:
                // sub_4014F0
                // 和data比较
                if ( _this[2] == data[_this[4]] ){
                    _this[5] = 1;
                }else{
                    if ( _this[2] >= data[_this[4]] ){
                        _this[5] = 2;
                    }else{
                        _this[5] = 0;
                    }
                }
                _this[1] = op[++op_point];
                continue;
            case 0xD1:
                // sub_401540
                // 和data比较
//                printf("%d,", _this[3]);
                if ( _this[3] == data[_this[4]] ){
                    _this[5] = 1;
                    printf("_this[5] = 1;\n");
                }else{
                    if ( _this[3] >= data[_this[4]] ){
                        _this[5] = 2;
                        printf("_this[5] = 2\n");
                    }else{
                        _this[5] = 0;
                        printf("_this[5] = 0");
                    }
                }
                _this[1] = op[++op_point];
                continue;
            case 0xD2:
                // sub_401590

                // 0x39(57)
                if ( _this[4] == op[op_point+1] ){
                    _this[5] = 1;
                }else{
                    if ( _this[4] >= op[op_point+1] )
                        _this[5] = 2;
                    else
                        _this[5] = 0;
                }
                _this[1] = op[op_point+5];
                op_point+=5;
                continue;
            case 0xD3:
                // sub_4015D0
                if ( _this[5] == 1 ){
                    _this[1] = op[op_point + op[op_point + 1]+2];
                    op_point += (op[op_point + 1]+2);
                }else{
                    _this[1] = op[op_point+2];
                    op_point += 2;
                }
                continue;
            case 0xD4:
                // sub_4015F0
                if ( !_this[5] ){
                    printf("%d\n", (op_point + op[op_point + 1]+2)&0xff);

                    _this[1] = op[(op_point + op[op_point + 1]+2) & 0xff] ;
//                    op_point += (op[op_point+1]+2);
                    op_point = (op_point + op[op_point+1]+2) & 0xff;
                }else{
                    _this[1] = op[op_point+2];
                    op_point += 2;
                }
                continue;
            case 0xFE:
                return 0;
            case 0xFF:
                return 1;
            default:
                return 0;
        }
    }

    return 0;
}
