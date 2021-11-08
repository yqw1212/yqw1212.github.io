(module
  (type $type0 (func (param i32) (result i32)))
  (type $type1 (func (result i32)))
  (type $type2 (func (param i32)))
  (type $type3 (func))
  (type $type4 (func (param i32 i32 i32) (result i32)))
  (type $type5 (func (param i32 i64 i32) (result i64)))
  (table $__indirect_function_table (;0;) 1 1 anyfunc)
  (memory $memory (;0;) 256 256)
  (global $global0 (mut i32) (i32.const 5243984))
  (global $global1 (mut i32) (i32.const 0))
  (global $global2 (mut i32) (i32.const 0))
  (export "memory" (memory $memory))
  (export "__wasm_call_ctors" (func $__wasm_call_ctors))
  (export "checkright" (func $checkright))
  (export "__errno_location" (func $__errno_location))
  (export "fflush" (func $fflush))
  (export "stackSave" (func $stackSave))
  (export "stackRestore" (func $stackRestore))
  (export "stackAlloc" (func $stackAlloc))
  (export "emscripten_stack_init" (func $emscripten_stack_init))
  (export "emscripten_stack_get_free" (func $emscripten_stack_get_free))
  (export "emscripten_stack_get_end" (func $emscripten_stack_get_end))
  (export "__indirect_function_table" (table $__indirect_function_table))
  (func $__wasm_call_ctors (;0;)
    call $emscripten_stack_init
  )
  (func $checkright (;1;) (param $var0 i32) (result i32)
    (local $var1 i32) (local $var2 i32) (local $var3 i32) (local $var4 i32) (local $var5 i32) (local $var6 i32) (local $var7 i32) (local $var8 i32) (local $var9 i32) (local $var10 i32) (local $var11 i32) (local $var12 i32) (local $var13 i32) (local $var14 i32) (local $var15 i32) (local $var16 i32) (local $var17 i32) (local $var18 i32) (local $var19 i32) (local $var20 i32) (local $var21 i32) (local $var22 i32) (local $var23 i32) (local $var24 i32) (local $var25 i32) (local $var26 i32) (local $var27 i32) (local $var28 i32) (local $var29 i32) (local $var30 i32) (local $var31 i32) (local $var32 i32) (local $var33 i32) (local $var34 i32) (local $var35 i32) (local $var36 i32) (local $var37 i32) (local $var38 i32) (local $var39 i32) (local $var40 i32) (local $var41 i32) (local $var42 i32) (local $var43 i32) (local $var44 i32) (local $var45 i32) (local $var46 i32) (local $var47 i32) (local $var48 i32) (local $var49 i32) (local $var50 i32) (local $var51 i32) (local $var52 i32) (local $var53 i32) (local $var54 i32) (local $var55 i32) (local $var56 i32) (local $var57 i32) (local $var58 i32) (local $var59 i32) (local $var60 i32) (local $var61 i32) (local $var62 i32) (local $var63 i32) (local $var64 i32) (local $var65 i32) (local $var66 i32) (local $var67 i32) (local $var68 i32) (local $var69 i64) (local $var70 i64) (local $var71 i64) (local $var72 i64) (local $var73 i64) (local $var74 i64) (local $var75 i64)
    global.get $global0
    local.set $var1
    i32.const 96
    local.set $var2
    local.get $var1
    local.get $var2
    i32.sub
    local.set $var3
    local.get $var3
    local.get $var0
    i32.store offset=88
    i32.const 48
    local.set $var4
    local.get $var3
    local.get $var4
    i32.add
    local.set $var5
    local.get $var5
    local.set $var6
    i32.const 24
    local.set $var7
    local.get $var6
    local.get $var7
    i32.add
    local.set $var8
    i32.const 0
    local.set $var9
    local.get $var9
    i32.load16_u offset=1048
    local.set $var10
    local.get $var8
    local.get $var10
    i32.store16
    i32.const 16
    local.set $var11
    local.get $var6
    local.get $var11
    i32.add
    local.set $var12
    local.get $var9
    i64.load offset=1040
    local.set $var69
    local.get $var12
    local.get $var69
    i64.store
    i32.const 8
    local.set $var13
    local.get $var6
    local.get $var13
    i32.add
    local.set $var14
    local.get $var9
    i64.load offset=1032
    local.set $var70
    local.get $var14
    local.get $var70
    i64.store
    local.get $var9
    i64.load offset=1024
    local.set $var71
    local.get $var6
    local.get $var71
    i64.store
    i32.const 33
    local.set $var15
    local.get $var3
    local.get $var15
    i32.add
    local.set $var16
    local.get $var16
    local.set $var17
    i32.const 7
    local.set $var18
    local.get $var17
    local.get $var18
    i32.add
    local.set $var19
    i32.const 0
    local.set $var20
    local.get $var20
    i64.load offset=1057 align=1
    local.set $var72
    local.get $var19
    local.get $var72
    i64.store align=1
    local.get $var20
    i64.load offset=1050 align=1
    local.set $var73
    local.get $var17
    local.get $var73
    i64.store align=1
    i32.const 18
    local.set $var21
    local.get $var3
    local.get $var21
    i32.add
    local.set $var22
    local.get $var22
    local.set $var23
    i32.const 7
    local.set $var24
    local.get $var23
    local.get $var24
    i32.add
    local.set $var25
    i32.const 0
    local.set $var26
    local.get $var26
    i64.load offset=1072 align=1
    local.set $var74
    local.get $var25
    local.get $var74
    i64.store align=1
    local.get $var26
    i64.load offset=1065 align=1
    local.set $var75
    local.get $var23
    local.get $var75
    i64.store align=1
    i32.const 0
    local.set $var27
    local.get $var3
    local.get $var27
    i32.store offset=12
    block $label3
      block $label0
        loop $label4
          local.get $var3
          i32.load offset=12
          local.set $var28
          i32.const 26
          local.set $var29
          local.get $var28
          local.set $var30
          local.get $var29
          local.set $var31
          local.get $var30
          local.get $var31
          i32.lt_s
          local.set $var32
          i32.const 1
          local.set $var33
          local.get $var32
          local.get $var33
          i32.and
          local.set $var34
          local.get $var34
          i32.eqz
          br_if $label0
          local.get $var3
          i32.load offset=12
          local.set $var35
          i32.const 48
          local.set $var36
          local.get $var3
          local.get $var36
          i32.add
          local.set $var37
          local.get $var37
          local.set $var38
          local.get $var38
          local.get $var35
          i32.add
          local.set $var39
          local.get $var39
          i32.load8_u
          local.set $var40
          i32.const 255
          local.set $var41
          local.get $var40
          local.get $var41
          i32.and
          local.set $var42
          local.get $var3
          i32.load offset=88
          local.set $var43
          local.get $var3
          i32.load offset=12
          local.set $var44
          local.get $var43
          local.get $var44
          i32.add
          local.set $var45
          local.get $var45
          i32.load8_u
          local.set $var46
          i32.const 24
          local.set $var47
          local.get $var46
          local.get $var47
          i32.shl
          local.set $var48
          local.get $var48
          local.get $var47
          i32.shr_s
          local.set $var49
          i32.const 1
          local.set $var50
          local.get $var49
          local.get $var50
          i32.shl
          local.set $var51
          local.get $var3
          i32.load offset=12
          local.set $var52
          local.get $var51
          local.get $var52
          i32.xor
          local.set $var53
          local.get $var42
          local.set $var54
          local.get $var53
          local.set $var55
          local.get $var54
          local.get $var55
          i32.eq
          local.set $var56
          i32.const 1
          local.set $var57
          local.get $var56
          local.get $var57
          i32.and
          local.set $var58
          block $label2
            block $label1
              local.get $var58
              i32.eqz
              br_if $label1
              br $label2
            end $label1
            i32.const 18
            local.set $var59
            local.get $var3
            local.get $var59
            i32.add
            local.set $var60
            local.get $var60
            local.set $var61
            local.get $var3
            local.get $var61
            i32.store offset=92
            br $label3
          end $label2
          local.get $var3
          i32.load offset=12
          local.set $var62
          i32.const 1
          local.set $var63
          local.get $var62
          local.get $var63
          i32.add
          local.set $var64
          local.get $var3
          local.get $var64
          i32.store offset=12
          br $label4
        end $label4
        unreachable
      end $label0
      i32.const 33
      local.set $var65
      local.get $var3
      local.get $var65
      i32.add
      local.set $var66
      local.get $var66
      local.set $var67
      local.get $var3
      local.get $var67
      i32.store offset=92
    end $label3
    local.get $var3
    i32.load offset=92
    local.set $var68
    local.get $var68
    return
  )
  (func $stackSave (;2;) (result i32)
    global.get $global0
  )
  (func $stackRestore (;3;) (param $var0 i32)
    local.get $var0
    global.set $global0
  )
  (func $stackAlloc (;4;) (param $var0 i32) (result i32)
    (local $var1 i32) (local $var2 i32)
    global.get $global0
    local.get $var0
    i32.sub
    i32.const -16
    i32.and
    local.tee $var1
    global.set $global0
    local.get $var1
  )
  (func $emscripten_stack_init (;5;)
    i32.const 5243984
    global.set $global2
    i32.const 1100
    i32.const 15
    i32.add
    i32.const -16
    i32.and
    global.set $global1
  )
  (func $emscripten_stack_get_free (;6;) (result i32)
    global.get $global0
    global.get $global1
    i32.sub
  )
  (func $emscripten_stack_get_end (;7;) (result i32)
    global.get $global1
  )
  (func $func8 (param $var0 i32) (result i32)
    i32.const 1
  )
  (func $func9 (param $var0 i32)
  )
  (func $func10 (param $var0 i32)
  )
  (func $func11 (param $var0 i32)
  )
  (func $func12 (result i32)
    i32.const 1080
    call $func10
    i32.const 1088
  )
  (func $func13
    i32.const 1080
    call $func11
  )
  (func $fflush (;14;) (param $var0 i32) (result i32)
    (local $var1 i32) (local $var2 i32)
    block $label2
      block $label0
        local.get $var0
        i32.eqz
        br_if $label0
        block $label1
          local.get $var0
          i32.load offset=76
          i32.const -1
          i32.gt_s
          br_if $label1
          local.get $var0
          call $func15
          return
        end $label1
        local.get $var0
        call $func8
        local.set $var1
        local.get $var0
        call $func15
        local.set $var2
        local.get $var1
        i32.eqz
        br_if $label2
        local.get $var0
        call $func9
        local.get $var2
        return
      end $label0
      i32.const 0
      local.set $var2
      block $label3
        i32.const 0
        i32.load offset=1092
        i32.eqz
        br_if $label3
        i32.const 0
        i32.load offset=1092
        call $fflush
        local.set $var2
      end $label3
      block $label4
        call $func12
        i32.load
        local.tee $var0
        i32.eqz
        br_if $label4
        loop $label8
          i32.const 0
          local.set $var1
          block $label5
            local.get $var0
            i32.load offset=76
            i32.const 0
            i32.lt_s
            br_if $label5
            local.get $var0
            call $func8
            local.set $var1
          end $label5
          block $label6
            local.get $var0
            i32.load offset=20
            local.get $var0
            i32.load offset=28
            i32.le_u
            br_if $label6
            local.get $var0
            call $func15
            local.get $var2
            i32.or
            local.set $var2
          end $label6
          block $label7
            local.get $var1
            i32.eqz
            br_if $label7
            local.get $var0
            call $func9
          end $label7
          local.get $var0
          i32.load offset=56
          local.tee $var0
          br_if $label8
        end $label8
      end $label4
      call $func13
    end $label2
    local.get $var2
  )
  (func $func15 (param $var0 i32) (result i32)
    (local $var1 i32) (local $var2 i32)
    block $label0
      local.get $var0
      i32.load offset=20
      local.get $var0
      i32.load offset=28
      i32.le_u
      br_if $label0
      local.get $var0
      i32.const 0
      i32.const 0
      local.get $var0
      i32.load offset=36
      call_indirect (type $type4)
      drop
      local.get $var0
      i32.load offset=20
      br_if $label0
      i32.const -1
      return
    end $label0
    block $label1
      local.get $var0
      i32.load offset=4
      local.tee $var1
      local.get $var0
      i32.load offset=8
      local.tee $var2
      i32.ge_u
      br_if $label1
      local.get $var0
      local.get $var1
      local.get $var2
      i32.sub
      i64.extend_s/i32
      i32.const 1
      local.get $var0
      i32.load offset=40
      call_indirect (type $type5)
      drop
    end $label1
    local.get $var0
    i32.const 0
    i32.store offset=28
    local.get $var0
    i64.const 0
    i64.store offset=16
    local.get $var0
    i64.const 0
    i64.store offset=4 align=4
    i32.const 0
  )
  (func $__errno_location (;16;) (result i32)
    i32.const 1096
  )
  (data (i32.const 1024)
    "\86\8b\aa\85\ac\89\f0\af\d8i\d6\dd\b2\bfn\e5\ae\99\cc\d5\bc\8b\f2}z\e3You are right!\00You are wrong!\00"
  )
)