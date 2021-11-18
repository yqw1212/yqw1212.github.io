auto addr_start = 0x4117A0;//函数起始地址
auto addr_end = 0x411E58;//函数结束地址
auto i=0, j=0;
for(i=addr_start; i<addr_end; i++){
    if(Dword(i)==0x1E8){
        for(j=0; j<6; j++,i++){
            PatchByte(i, 0x90);
        }
        i=i+4;
        for(j=0; j<3; j++,i++){
            PatchByte(i, 0x90);
        }
        i=i+10;
        for(j=0; j<3; j++,i++){
            PatchByte(i, 0x90);
        }
        i=i+5;
        for(j=0; j<1; j++,i++){
            PatchByte(i, 0x90);
        }
        i=i+3;
        for(j=0; j<2; j++,i++){
            PatchByte(i, 0x90);
        }
        i--;
    }
}