contract Contract {
    function main() {

        var var0 = msg.value;
    
        var0 = msg.data[0x00:0x20] >> 0xe0;
    
        if (0x6ca5b5b0 > var0) {
            if (var0 == 0x0bcbbd21) {
                // Dispatch table entry for r2()
                var var1 = 0x00dc;
                var var2 = r2();
                var temp0 = memory[0x40:0x60];
                memory[temp0:temp0 + 0x20] = var2;
                var temp1 = memory[0x40:0x60];
                return memory[temp1:temp1 + (temp0 + 0x20) - temp1];
            } else if (var0 == 0x343943bd) {
                // Dispatch table entry for 0x343943bd (unknown)
                var1 = 0x00fa;
                var2 = func_02F2();
                var temp2 = memory[0x40:0x60];
                memory[temp2:temp2 + 0x20] = var2;
                var temp3 = memory[0x40:0x60];
                return memory[temp3:temp3 + (temp2 + 0x20) - temp3];
            } else if (var0 == 0x4ff13571) {
                // Dispatch table entry for x2()
                var1 = 0x0118;
                var2 = x2();
                var temp4 = memory[0x40:0x60];
                memory[temp4:temp4 + 0x20] = var2;
                var temp5 = memory[0x40:0x60];
                return memory[temp5:temp5 + (temp4 + 0x20) - temp5];
            } else if (var0 == 0x56b15fe3) {
                // Dispatch table entry for feistel(uint256,uint256,uint256)
                var1 = 0x016e;
                var2 = 0x04;
                var var3 = msg.data.length - var2;
            
                feistel(var2, var3);
                stop();
            } else if (var0 == 0x5e031f4a) {
                // Dispatch table entry for setr2(uint256)
                var1 = 0x019c;
                var2 = 0x04;
                var3 = msg.data.length - var2;
            
                setr2(var2, var3);
                stop();
            } else if (var0 == 0x6c3ce676) {
                // Dispatch table entry for setr3(uint256)
                var1 = 0x01ca;
                var2 = 0x04;
                var3 = msg.data.length - var2;
            
                setr3(var2, var3);
                stop();
            } else { revert(memory[0x00:0x00]); }
        } else if (0x8bf6e410 > var0) {
            if (var0 == 0x6ca5b5b0) {
                // Dispatch table entry for r1()
                var1 = 0x01d4;
                var2 = r1();
                var temp6 = memory[0x40:0x60];
                memory[temp6:temp6 + 0x20] = var2;
                var temp7 = memory[0x40:0x60];
                return memory[temp7:temp7 + (temp6 + 0x20) - temp7];
            } else if (var0 == 0x7059c7e0) {
                // Dispatch table entry for setr1(uint256)
                var1 = 0x0216;
                var2 = 0x04;
                var3 = msg.data.length - var2;
            
                setr1(var2, var3);
                stop();
            } else if (var0 == 0x890eba68) {
                // Dispatch table entry for flag()
                var1 = 0x0220;
                var2 = flag();
                var temp8 = memory[0x40:0x60];
                memory[temp8:temp8 + 0x20] = var2;
                var temp9 = memory[0x40:0x60];
                return memory[temp9:temp9 + (temp8 + 0x20) - temp9];
            }
        } else if (var0 == 0x8bf6e410) {
            // Dispatch table entry for 0x8bf6e410 (unknown)
            var1 = 0x023e;
            var2 = func_0440();
            var temp10 = memory[0x40:0x60];
            memory[temp10:temp10 + 0x20] = var2;
            var temp11 = memory[0x40:0x60];
            return memory[temp11:temp11 + (temp10 + 0x20) - temp11];
        } else if (var0 == 0xa3b78873) {
            // Dispatch table entry for 0xa3b78873 (unknown)
            var1 = 0x025c;
            var2 = func_0446();
            var temp12 = memory[0x40:0x60];
            memory[temp12:temp12 + 0x20] = var2;
            var temp13 = memory[0x40:0x60];
            return memory[temp13:temp13 + (temp12 + 0x20) - temp13];
        } else if (var0 == 0xa7ba732e) {
            // Dispatch table entry for setflag(uint256)
            var1 = 0x029e;
            var2 = 0x04;
            var3 = msg.data.length - var2;
        
            setflag(var2, var3);
            stop();
        } else if (var0 == 0xc4ee5c77) {
            // Dispatch table entry for calcx(uint256,uint256,uint256,uint256)
            var1 = 0x02ea;
            var2 = 0x04;
            var3 = msg.data.length - var2;
        
            calcx(var2, var3);
            stop();
        }
    }
    
    function feistel(var arg0, var arg1) {
        var temp0 = arg0;
        var temp1 = temp0 + 0x20;
        arg0 = msg.data[temp0:temp0 + 0x20];
        arg1 = msg.data[temp1:temp1 + 0x20];
        var var0 = msg.data[temp1 + 0x20:temp1 + 0x20 + 0x20];
        var temp2 = storage[0x04] & 0x2aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;
        var temp3 = arg0;
        var temp4 = temp2 ~ (storage[0x04] & 0x555555555555555555555555555555555555) ~ temp3;
        var temp5 = arg1;
        var temp6 = temp4 ~ temp2 ~ temp5;
        var temp7 = var0;
        storage[0x04] = temp6 ~ temp6 ~ temp4 ~ temp7;
        var temp8 = storage[0x05] & 0x2aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;
        var temp9 = temp8 ~ (storage[0x05] & 0x555555555555555555555555555555555555) ~ temp3;
        var temp10 = temp9 ~ temp8 ~ temp5;
        storage[0x05] = temp10 ~ temp10 ~ temp9 ~ temp7;
        var temp11 = storage[0x06] & 0x2aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;
        var temp12 = temp11 ~ (storage[0x06] & 0x555555555555555555555555555555555555) ~ temp3;
        var temp13 = temp12 ~ temp11 ~ temp5;
        storage[0x06] = temp13 ~ temp13 ~ temp12 ~ temp7;
    }
    
    function setr2(var arg0, var arg1) {
        arg0 = msg.data[arg0:arg0 + 0x20];
        arg1 = arg0;
        var var0 = storage[0x00];
    
        if (!arg1) { assert(); }
    
        storage[0x02] = var0 % arg1;
    }
    
    function setr3(var arg0, var arg1) {
        arg0 = msg.data[arg0:arg0 + 0x20];
        arg1 = arg0;
        var var0 = storage[0x00];
    
        if (!arg1) { assert(); }
    
        storage[0x03] = var0 % arg1;
    }
    
    function setr1(var arg0, var arg1) {
        arg0 = msg.data[arg0:arg0 + 0x20];
        arg1 = arg0;
        var var0 = storage[0x00];
    
        storage[0x01] = var0 % arg1;
    }
    
    function setflag(var arg0, var arg1) {
        arg0 = msg.data[arg0:arg0 + 0x20];
        storage[0x00] = arg0;
    }
    
    function calcx(var arg0, var arg1) {
        var temp0 = arg0;
        var temp1 = temp0 + 0x20;
        arg0 = msg.data[temp0:temp0 + 0x20];
        var temp2 = temp1 + 0x20;
        arg1 = msg.data[temp1:temp1 + 0x20];
        var var0 = msg.data[temp2:temp2 + 0x20];
        var var1 = msg.data[temp2 + 0x20:temp2 + 0x20 + 0x20];
    
        if (arg0 == 0x01) {
            storage[0x04] = storage[0x01] * arg1 + storage[0x02] * var0 + storage[0x03] * var1;
            return;
        } else if (arg0 != 0x02) {
            storage[0x06] = storage[0x01] * arg1 + storage[0x02] * var0 + storage[0x03] * var1;
            return;
        } else {
            storage[0x05] = storage[0x01] * arg1 + storage[0x02] * var0 + storage[0x03] * var1;
            return;
        }
    }
    
    function r2() returns (var r0) { return storage[0x02]; }
    
    function func_02F2() returns (var r0) { return storage[0x04]; }
    
    function x2() returns (var r0) { return storage[0x05]; }
    
    function r1() returns (var r0) { return storage[0x01]; }
    
    function flag() returns (var r0) { return storage[0x00]; }
    
    function func_0440() returns (var r0) { return storage[0x03]; }
    
    function func_0446() returns (var r0) { return storage[0x06]; }
}