---
layout: post
title:  babyharmony(JLCTF2024)
date:   2024-09-12 00:08:01 +0300
image:  2024-09-12-ai.jpg
tags:   [ctf,reverse,harmony]
---

将.hap文件后缀更改为.zip解压后就可以看见.hap的文件结构

记事本打开.abc文件，查找关键代码

```assembly
this.observeComponentCreation((elmtId, isInitialRender) => {
    ViewStackProcessor.StartGetAccessRecordingFor(elmtId);
    Button.createWithLabel(this.button_name);
    Button.onClick(() => {
        this.context.resourceManager.getRawFileContent("bin").then((value) => {
            var c = testNapi.check(this.flag, value);
            if ((c & 0b100) === 0b100) {
                this.result = '系统环境异常';
            }
            else if ((c & 0b10) === 0b10) {
                this.result = 'flag格式错误';
            }
            else if ((c & 0b1) === 0b1) {
                this.result = 'flag错误或系统环境异常';
            }
            else {
                this.result = 'flag正确';
            }
            this.dialogController.open();
        });
    });
    if (!isInitialRender) {
        Button.pop();
    }
    ViewStackProcessor.StopGetAccessRecording();
});
```

check函数用来判断flag，在native层

鸿蒙的Native层方法注册流程，用的是魔改后的Node.js的原生库ffi-napi

`RegisterEntryModule`→`napi_module_register`→`要注册方法的结构体napi_module`

```assembly
typedef struct napi_module {
    int nm_version;
    unsigned int nm_flags;
    void* nm_filename;
    napi_addon_register_func nm_register_func;
    void* nm_modname;
    void* nm_priv;
    void* reserved[4];
} napi_module;
```

ida中查看so文件

RegisterEntryModule

```assembly
__int64 RegisterEntryModule()
{
  return napi_module_register(&unk_8210);
}
```

查看unk_8210

```assembly
.data:0000000000008210 unk_8210        db    1                 ; DATA XREF: RegisterEntryModule↑o
.data:0000000000008211                 db    0
.data:0000000000008212                 db    0
.data:0000000000008213                 db    0
.data:0000000000008214                 db    0
.data:0000000000008215                 db    0
.data:0000000000008216                 db    0
.data:0000000000008217                 db    0
.data:0000000000008218                 db    0
.data:0000000000008219                 db    0
.data:000000000000821A                 db    0
.data:000000000000821B                 db    0
.data:000000000000821C                 db    0
.data:000000000000821D                 db    0
.data:000000000000821E                 db    0
.data:000000000000821F                 db    0
.data:0000000000008220                 dq offset sub_2290
.data:0000000000008228                 dq offset aEntry        ; "entry"
```

查看sub_2290

```assembly
__int64 __fastcall sub_2290(__int64 a1, __int64 a2)
{
  _QWORD v3[37]; // [rsp+0h] [rbp-128h] BYREF

  v3[0x21] = __readfsqword(0x28u);
  memcpy(v3, &off_6E40, 0x100uLL);
  napi_define_properties(a1, a2, 4LL, v3);
  return a2;
}
```

off_6E40储存了所有要注册的方法

```assembly
data.rel.ro:0000000000006E40 off_6E40        dq offset aAdd          ; DATA XREF: sub_2290+23↑o
.data.rel.ro:0000000000006E40                                         ; "add"
.data.rel.ro:0000000000006E48                 align 10h
.data.rel.ro:0000000000006E50                 dq offset sub_2310
.data.rel.ro:0000000000006E58                 align 40h
.data.rel.ro:0000000000006E80                 dq offset aCheck        ; "check"
.data.rel.ro:0000000000006E88                 align 10h
.data.rel.ro:0000000000006E90                 dq offset sub_23D0
.data.rel.ro:0000000000006E98                 align 40h
.data.rel.ro:0000000000006EC0                 dq offset aRegister     ; "register"
.data.rel.ro:0000000000006EC8                 align 10h
.data.rel.ro:0000000000006ED0                 dq offset sub_5760
.data.rel.ro:0000000000006ED8                 align 40h
.data.rel.ro:0000000000006F00                 dq offset aCall         ; "call"
.data.rel.ro:0000000000006F08                 align 10h
.data.rel.ro:0000000000006F10                 dq offset sub_58D0
.data.rel.ro:0000000000006F18                 align 40h
```

因此，找到了check的方法是sub_23D0

### napi_get_typedarray_info

通过调用`napi_get_typedarray_info`函数,获取一个TypedArray对象的详细信息,包括数据类型、长度、数据缓冲区指针以及与之关联的ArrayBuffer对象等。

```assembly
napi_status napi_get_typedarray_info(napi_env env,
                                     napi_value typedarray,
                                     napi_typedarray_type* type,
                                     size_t* length,
                                     void** data,
                                     napi_value* arraybuffer,
                                     size_t* byte_offset);
```

参数含义:

1. `napi_env env`: 当前的N-API执行环境。
2. `napi_value typedarray`: 需要获取信息的TypedArray对象。
3. `napi_typedarray_type* type`: 用于存储TypedArray的数据类型,如`napi_int8_array`、`napi_uint8_array`等。
4. `size_t* length`: 用于存储TypedArray的元素个数。
5. `void** data`: 用于存储TypedArray数据缓冲区的指针。
6. `napi_value* arraybuffer`: 用于存储TypedArray关联的ArrayBuffer对象。
7. `size_t* byte_offset`: 用于存储TypedArray在关联ArrayBuffer中的字节偏移量。

返回值:

`napi_status`: 函数执行的状态,可能的值有:

- `napi_ok`: 函数执行成功。
- `napi_invalid_arg`: 参数无效。
- `napi_object_expected`: `typedarray`参数不是一个TypedArray对象。
- 其他错误码: 表示函数执行过程中出现了其他错误。

### napi_call_function函数和TS的testNapi.register回调函数

```assembly
aboutToAppear() {
    // 注册 testNapi 处理程序，针对不同的 batteryInfo 属性进行比较和返回结果
    // 电池剩余电量差值判断
    testNapi.register(0, (a) => {
        var t = batteryInfo.batterySOC - a;
        var f;
        if (t > 0)
            f = 1;
        else if (t == 0)
            f = 0;
        else
            f = -1;
        return f === 0;
    });
...
    // 直接返回电池温度
    testNapi.register(262, () => {
        return batteryInfo.batteryTemperature;
    });
    // 直接返回电池是否存在
    testNapi.register(263, () => {
        return batteryInfo.isBatteryPresent;
    });
    // 直接返回电池容量等级
    testNapi.register(264, () => {
        return batteryInfo.batteryCapacityLevel;
    });
}
```

这些代码就是在ArkTS源码区注册的回调函数，Native层的`napi_call_function函`数可以通过序号调用这些ArkTs层的代码

Native层的获取回调函数的函数：

```
// 通过bin_i的值获取注册在TS的代码，将注册的方法存放于reg_method_0
napi_get_reference_value(env, *(v29 + 40), &reg_method_0);
// 通过bin_i_or_100的值获取注册在TS的代码，将函数存放在reg_method_1
napi_get_reference_value(env, *(v36 + 40), &reg_method_1);
```

