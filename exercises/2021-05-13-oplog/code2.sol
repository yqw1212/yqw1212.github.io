contract disassembler {

    uint256 public r2;

    uint256 public x1;

    uint256 public x2;

    function feistel( uint256 arg0,uint256 arg1,uint256 arg2) public return ()
    {
        x1 = (x1 & 0x2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA) ^ (x1 & 0x555555555555555555555555555555555555) ^ arg0 ^ arg2;
        x2 = (x2 & 0x2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA) ^ (x2 & 0x555555555555555555555555555555555555) ^ arg0 ^ arg2;
        x3 = (x3 & 0x2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA) ^ (x3 & 0x555555555555555555555555555555555555) ^ arg0 ^ arg2;
        return();
    }

    function setr2( uint256 arg0) public return ()
    {
        r2 = MOD(flag,arg0);
        return();
    }

    function setr3( uint256 arg0) public return ()
    {
        r3 = MOD(flag,arg0);
        return();
    }

    uint256 public r1;

    function setr1( uint256 arg0) public return ()
    {
        r1 = MOD(flag,arg0);
        return();
    }

    uint256 public flag;

    uint256 public r3;

    uint256 public x3;

    function setflag( uint256 arg0) public return ()
    {
        flag = arg0;
        return();
    }

    function calcx( uint256 arg0,uint256 arg1,uint256 arg2,uint256 arg3) public return ()
    {
        if ((arg0 == 0x1)) 
        {
            x1 = (((r1 * arg1) + (r2 * arg2)) + (r3 * arg3));
        }
        else if ((arg0 == 0x2)) 
        {
            x2 = (((r1 * arg1) + (r2 * arg2)) + (r3 * arg3));
        }
        else
        {
            x3 = (((r1 * arg1) + (r2 * arg2)) + (r3 * arg3));
        }
        return();
    }

    function main() public return ()
    {
        var0 = msg.value;
        
        var0 = SHR(0xE0,msg.data(0x0));
        if ((0x6CA5B5B0 > SHR(0xE0,msg.data(0x0)))) 
        {

            //ISSUE:COMMENT: Function r2()
            if ((0xBCBBD21 == var0)) 
            {
                var2 = r2();
                mstore(0x80,var2);
                RETURN(0x80,0x20);
            }

            //ISSUE:COMMENT: Function FUNC_343943BD()
            else if ((0x343943BD == var0)) 
            {
                var2 = FUNC_343943BD();
                mstore(0x80,var2);
                RETURN(0x80,0x20);
            }

            //ISSUE:COMMENT: Function x2()
            else if ((0x4FF13571 == var0)) 
            {
                var2 = x2();
                mstore(0x80,var2);
                RETURN(0x80,0x20);
            }

            //ISSUE:COMMENT: Function feistel()
            else if ((0x56B15FE3 == var0)) 
            {
                var3 = (msg.data.length - 0x4);
                feistel(msg.data(0x4),msg.data(0x24),msg.data(0x44));
                stop();
            }

            //ISSUE:COMMENT: Function setr2()
            else if ((0x5E031F4A == var0)) 
            {
                var3 = (msg.data.length - 0x4);
                setr2(msg.data(0x4));
                stop();
            }

            //ISSUE:COMMENT: Function setr3()
            else if ((0x6C3CE676 == var0)) 
            {
                var3 = (msg.data.length - 0x4);
                setr3(msg.data(0x4));
                stop();
            }
            else
            {
                goto label_000000CF;
            }
        }
        else if ((0x8BF6E410 > var0)) 
        {

            //ISSUE:COMMENT: Function r1()
            if ((0x6CA5B5B0 == var0)) 
            {
                var2 = r1();
                mstore(0x80,var2);
                RETURN(0x80,0x20);
            }

            //ISSUE:COMMENT: Function setr1()
            else if ((0x7059C7E0 == var0)) 
            {
                var3 = (msg.data.length - 0x4);
                setr1(msg.data(0x4));
                stop();
            }

            //ISSUE:COMMENT: Function FUNC_890EBA68()
            else if ((0x890EBA68 == var0)) 
            {
                var2 = FUNC_890EBA68();
                mstore(0x80,var2);
                RETURN(0x80,0x20);
            }
            else
            {
                goto label_000000CF;
            }
        }

        //ISSUE:COMMENT: Function FUNC_8BF6E410()
        else if ((0x8BF6E410 == var0)) 
        {
            var2 = FUNC_8BF6E410();
            mstore(0x80,var2);
            RETURN(0x80,0x20);
        }

        //ISSUE:COMMENT: Function FUNC_A3B78873()
        else if ((0xA3B78873 == var0)) 
        {
            var2 = FUNC_A3B78873();
            mstore(0x80,var2);
            RETURN(0x80,0x20);
        }

        //ISSUE:COMMENT: Function setflag()
        else if ((0xA7BA732E == var0)) 
        {
            var3 = (msg.data.length - 0x4);
            require((0x20 < (msg.data.length - 0x4)));
            setflag(msg.data(0x4));
            stop();
        }

        //ISSUE:COMMENT: Function calcx()
        else if ((0xC4EE5C77 == var0)) 
        {
            var3 = (msg.data.length - 0x4);
            calcx(msg.data(0x4),msg.data(0x24),msg.data(0x44),msg.data(0x64));
            stop();
        }
        else
        {
            goto label_000000CF;
        }
    }

}