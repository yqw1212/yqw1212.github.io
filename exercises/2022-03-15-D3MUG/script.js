function hooktest () {
    let i = 0;
    var d3mug = Module.findBaseAddress("libd3mug.so");
    Interceptor.attach(d3mug.add(0x0000780), {
        onEnter: function (args) {
            var real_time = arr[i++];
            args[0] = new NativePointer(real_time);
        },
        onLeave: function (arg) {
            console.log(hexdump(d3mug.add(0x0000000000002D18).readPointer()));
            return arg;
        }
    });

}

setImmediate(function () {
    setTimeout(hooktest, 100);
})