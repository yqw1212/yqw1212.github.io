#include <stdio.h>

int main(){
    int opcode[550]={ 0xA1, 0xC1, 0x00, 0xB1, 0x77, 0xC2, 0x4A, 0x01, 0x00, 0x00,
                      0xC1, 0x01, 0xB2, 0x77, 0xC2, 0x19, 0x01, 0x00, 0x00, 0xC1,
                      0x02, 0xB4, 0x77, 0xC2, 0xDD, 0x01, 0x00, 0x00, 0xC1, 0x03,
                      0xB3, 0x77, 0xC2, 0x0F, 0x01, 0x00, 0x00, 0xC1, 0x04, 0xB2,
                      0x77, 0xC2, 0x1B, 0x01, 0x00, 0x00, 0xC1, 0x05, 0xB4, 0x77,
                      0xC2, 0x89, 0x01, 0x00, 0x00, 0xC1, 0x06, 0xB1, 0x77, 0xC2,
                      0x19, 0x01, 0x00, 0x00, 0xC1, 0x07, 0xB3, 0x77, 0xC2, 0x54,
                      0x01, 0x00, 0x00, 0xC1, 0x08, 0xB1, 0x77, 0xC2, 0x4F, 0x01,
                      0x00, 0x00, 0xC1, 0x09, 0xB1, 0x77, 0xC2, 0x4E, 0x01, 0x00,
                      0x00, 0xC1, 0x0A, 0xB3, 0x77, 0xC2, 0x55, 0x01, 0x00, 0x00,
                      0xC1, 0x0B, 0xB3, 0x77, 0xC2, 0x56, 0x01, 0x00, 0x00, 0xC1,
                      0x0C, 0xB4, 0x77, 0xC2, 0x8E, 0x00, 0x00, 0x00, 0xC1, 0x0D,
                      0xB2, 0x77, 0xC2, 0x49, 0x00, 0x00, 0x00, 0xC1, 0x0E, 0xB3,
                      0x77, 0xC2, 0x0E, 0x01, 0x00, 0x00, 0xC1, 0x0F, 0xB1, 0x77,
                      0xC2, 0x4B, 0x01, 0x00, 0x00, 0xC1, 0x10, 0xB3, 0x77, 0xC2,
                      0x06, 0x01, 0x00, 0x00, 0xC1, 0x11, 0xB3, 0x77, 0xC2, 0x54,
                      0x01, 0x00, 0x00, 0xC1, 0x12, 0xB2, 0x77, 0xC2, 0x1A, 0x00,
                      0x00, 0x00, 0xC1, 0x13, 0xB1, 0x77, 0xC2, 0x42, 0x01, 0x00,
                      0x00, 0xC1, 0x14, 0xB3, 0x77, 0xC2, 0x53, 0x01, 0x00, 0x00,
                      0xC1, 0x15, 0xB1, 0x77, 0xC2, 0x1F, 0x01, 0x00, 0x00, 0xC1,
                      0x16, 0xB3, 0x77, 0xC2, 0x52, 0x01, 0x00, 0x00, 0xC1, 0x17,
                      0xB4, 0x77, 0xC2, 0xDB, 0x00, 0x00, 0x00, 0xC1, 0x18, 0xB1,
                      0x77, 0xC2, 0x19, 0x01, 0x00, 0x00, 0xC1, 0x19, 0xB4, 0x77,
                      0xC2, 0xD9, 0x00, 0x00, 0x00, 0xC1, 0x1A, 0xB1, 0x77, 0xC2,
                      0x19, 0x01, 0x00, 0x00, 0xC1, 0x1B, 0xB3, 0x77, 0xC2, 0x55,
                      0x01, 0x00, 0x00, 0xC1, 0x1C, 0xB2, 0x77, 0xC2, 0x19, 0x00,
                      0x00, 0x00, 0xC1, 0x1D, 0xB3, 0x77, 0xC2, 0x00, 0x01, 0x00,
                      0x00, 0xC1, 0x1E, 0xB1, 0x77, 0xC2, 0x4B, 0x01, 0x00, 0x00,
                      0xC1, 0x1F, 0xB2, 0x77, 0xC2, 0x1E, 0x00, 0x00, 0x00, 0xC1,
                      0x20, 0x80, 0x02, 0x18, 0x00, 0x00, 0x00, 0x23, 0x10, 0xC1,
                      0x21, 0x80, 0x02, 0x10, 0x00, 0x00, 0x00, 0x23, 0xF7, 0xC1,
                      0x22, 0x80, 0x02, 0x08, 0x00, 0x00, 0x00, 0x23, 0xF7, 0xC1,
                      0x23, 0xF7, 0xFE, 0x80, 0x02, 0x05, 0x00, 0x00, 0x00, 0x22,
                      0x77, 0x10, 0x80, 0x02, 0x07, 0x00, 0x00, 0x00, 0x23, 0x80,
                      0x02, 0x23, 0x77, 0xF1, 0x98, 0x31, 0x77, 0x10, 0x80, 0x02,
                      0x18, 0x00, 0x00, 0x00, 0x23, 0x80, 0x02, 0x20, 0xB9, 0xE4,
                      0x35, 0x31, 0x77, 0x10, 0x80, 0x02, 0x12, 0x00, 0x00, 0x00,
                      0x22, 0x77, 0xA0, 0xC1, 0x24, 0x80, 0x02, 0x18, 0x00, 0x00,
                      0x00, 0x23, 0x10, 0xC1, 0x25, 0x80, 0x02, 0x10, 0x00, 0x00,
                      0x00, 0x23, 0xF7, 0xC1, 0x26, 0x80, 0x02, 0x08, 0x00, 0x00,
                      0x00, 0x23, 0xF7, 0xC1, 0x27, 0xF7, 0xFE, 0x32, 0x20, 0x43,
                      0x33, 0x77, 0x80, 0x02, 0x11, 0x00, 0x00, 0x00, 0x22, 0x35,
                      0x37, 0x38, 0x77, 0x80, 0x02, 0x0D, 0x00, 0x00, 0x00, 0x23,
                      0x77, 0x38, 0x39, 0x10, 0x32, 0x20, 0x43, 0x33, 0x77, 0x80,
                      0x02, 0x11, 0x00, 0x00, 0x00, 0x22, 0x35, 0x37, 0x38, 0x77,
                      0x80, 0x02, 0x0D, 0x00, 0x00, 0x00, 0x23, 0x77, 0x38, 0x39,
                      0xC7, 0xC1, 0x28, 0x80, 0x02, 0x18, 0x00, 0x00, 0x00, 0x23,
                      0x10, 0xC1, 0x29, 0x80, 0x02, 0x10, 0x00, 0x00, 0x00, 0x23,
                      0xF7, 0xC1, 0x2A, 0x80, 0x02, 0x08, 0x00, 0x00, 0x00, 0x23,
                      0xF7, 0xC1, 0x2B, 0xF7, 0xFE, 0x32, 0x20, 0x43, 0x33, 0x77,
                      0x80, 0x02, 0x11, 0x00, 0x00, 0x00, 0x22, 0x35, 0x37, 0x38,
                      0x77, 0x80, 0x02, 0x0D, 0x00, 0x00, 0x00, 0x23, 0x77, 0x38,
                      0x39, 0x10, 0x32, 0x20, 0x43, 0x33, 0x77, 0x80, 0x02, 0x11,
                      0x00, 0x00, 0x00, 0x22, 0x35, 0x37, 0x38, 0x77, 0x80, 0x02,
                      0x0D, 0x00, 0x00, 0x00, 0x23, 0x77, 0x38, 0x39, 0xC8, 0x99 };
    int i = 0, a1[8] = {0};
    while ( 1 ){
        if ( opcode[i] == 0x71 ){
          //a1[6] = opcode[i+1];
          printf("a1[6] = %d\n", opcode[i+1]);
          i += 5;
        }
        if ( opcode[i] == 0x41 ){
          //a1[1] += a1[2];
          printf("a1[1] += a1[2]\n");
          ++i;
        }
        if ( opcode[i] == 0x42 ){
          //a1[1] -= a1[4];
          printf("a1[1] -= a1[4]\n");
          ++i;
        }
        if ( opcode[i] == 0x43 ){
          //a1[1] *= a1[3];
          printf("a1[1] *= a1[3]\n");
          ++i;
        }
        if ( opcode[i] == 0x37 ){
          //a1[1] = a1[5]
          printf("a1[1] = a1[5]\n");
          ++i;
        }
        if ( opcode[i] == 0x38 ){
          //a1[1] ^= a1[4]
          printf("a1[1] ^= a1[4]\n");
          ++i;
        }
        if ( opcode[i] == 0x39 ){
          //a1[1] ^= a1[5];
          printf("a1[1] ^= a1[5]\n");
          ++i;
        }
        if ( opcode[i] == 0x35 ){
          //a1[5] = a1[1];
          printf("a1[5] = a1[1]\n");
          ++i;
        }
        if ( opcode[i] == 0xF7 ){
          //a1[9] += a1[1]
          printf("a1[9] += a1[1]\n");
          ++i;
        }
        if ( opcode[i] == 0x44 ){
          //a1[1] /= a1[5];
          printf("a1[1] /= a1[5]\n");
          ++i;
        }
        if ( opcode[i] == 0x80 ){
          //a1[sub_804875F(a1, 1) = *(a1[8] + 2);
          //printf("a1[sub_804875F(a1, 1)] = %d\n", opcode[i+2]);
          printf("a1[%d] = %d\n", opcode[i+1], opcode[i+2]);
          i += 6;
        }
        if ( opcode[i] == 0x77 ){
          //a1[1] ^= a1[9];
          printf("a1[1] ^= a1[9]\n");
          ++i;
        }
        if ( opcode[i] == 0x53 ){
          //putchar(a1[3]);
          printf("putchar(a1[3])\n");
          i += 2;
        }
        if ( opcode[i] == 0x22 ){
          //a1[1] >>= a1[2];
          printf("a1[1] >>= a1[2]\n");
          ++i;
        }
        if ( opcode[i] == 0x23 ){
          //a1[1] <<= a1[2];
          printf("a1[1] <<= a1[2]\n");
          ++i;
        }
        if ( opcode[i] == 0x99 )
          break;
        if ( opcode[i] == 0x76 ){
          //a1[3] = a1[6];
          printf("a1[3] = a1[6]\n");
          //a1[6] = 4;
          printf("a1[6] = 4\n");
          i += 5;
        }
        if ( opcode[i] == 0x54 ){
          //a1[3] = getchar();
          printf("a1[3] = getchar()\n");
          i += 2;
        }
        if ( opcode[i] == 0x30 ){
          //a1[1] |= a1[2];
          printf("a1[1] |= a1[2]\n");
          ++i;
        }
        if ( opcode[i] == 0x31 ){
          //a1[1] &= a1[2];
          printf("a1[1] &= a1[2]\n");
          ++i;
        }
        if ( opcode[i] == 0x32 ){
          //a1[3] = opcode[i+1];
          printf("a1[3] = %d\n", opcode[i+1]);
          i += 2;
        }
        if ( opcode[i] == 9 ){
          //a1[1] = 0x6FEBF967;
          printf("a1[1] = 0x6FEBF967\n");
          ++i;
        }
        if ( opcode[i] == 0x10 ){
          //a1[9] = a1[1];
          printf("a1[9] = a1[1]\n");
          ++i;
        }
        if ( opcode[i] == 0x33 ){
          //a1[4] = a1[1];
          printf("a1[4] = a1[1]\n");
          ++i;
        }
        if ( opcode[i] == 0x34 ){
          //a1[2] = opcode[i+1];
          printf("a1[2] = &d\n", opcode[i+1]);
          i += 2;
        }
        if ( opcode[i] == 0xFE ){
          //a1[1] = a1[9];
          printf("a1[1] = a1[9]\n");
          ++i;
        }
        if ( opcode[i] == 0x11 ){
          //printf(\"%x\\n\", a1[1])
          printf("printf(\"%x\\n\", a1[1])\n");
          ++i;
        }
        if ( opcode[i] == 0xA0 ){
          //if ( a1[1] != 0x6FEBF967 )
          printf("if( a1[1] != 0x6FEBF967 )\n");
          printf("    exit(0)\n");
            //exit(0);
          ++i;
        }
        if ( opcode[i] == 0xA1 ){
          //read(0, s, 0x2Cu);
          printf("read(0, s, 0x2Cu)\n");
          printf("if ( strlen(s) != 0x2C )\n");
          //if ( strlen(s) != 0x2C )
          printf("    exit(0)\n");
            //exit(0);
          ++i;
        }
        if ( opcode[i] == 0xB1 ){
          //a1[9] = dword_804B080[0];
          printf("a1[9] = dword_804B080[0]\n");
          ++i;
        }
        if ( opcode[i] == 0xB2 ){
          //a1[9] = dword_804B084;
          printf("a1[9] = dword_804B084\n");
          ++i;
        }
        /*
        if ( opcode[i] == 0xA4 ){
          dword_804B084[opcode[i+1]] = a1[1];
          i += 4;
        }
        */
        if ( opcode[i] == 0xB3 ){
          //a1[9] = dword_804B088;
          printf("a1[9] = dword_804B088\n");
          ++i;
        }
        if ( opcode[i] == 0xB4 ){
          //a1[9] = dword_804B08C;
          printf("a1[9] = dword_804B08C\n");
          ++i;
        }
        if ( opcode[i] == 0xC1 ){
          //a1[1] = s[opcode[i+1]];
          printf("a1[1] = s[%d]\n", opcode[i+1]);
          i += 2;
        }
        if ( opcode[i] == 0xC7 ){
          //if ( 0x0CF1304DC != a1[1] )
          printf("if ( 0x0CF1304DC != a1[1] )\n");
          printf("    exit(0)\n");
            //exit(0);
          ++i;
        }
        if ( opcode[i] == 0xC8 ){
          //if ( 0x283B8E84 != a1[1] )
          printf("if ( 0x283B8E84 != a1[1] )\n");
          printf("    exit(0)\n");
            //exit(0);
          ++i;
        }
        if ( opcode[i] == 0xC2 ){
          //if ( opcode[i+1] != a1[1] )
          printf("if ( %d != a1[1] )\n", opcode[i+1]);
          printf("    exit(0)\n");
            //exit(0);
          i += 5;
        }
    }
    return 0;
}
