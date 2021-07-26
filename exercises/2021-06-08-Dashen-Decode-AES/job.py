import frida
import sys

PACKAGE = "com.zj.zjtdctf"

if __name__ == '__main__':
    jscode = open('D:/文档/CTF/Bytectf/Dashen Decode AES/script.js', 'r').read() # 获取js脚本内容
    # get_usb_device获取设备（就是你手机）
    # attach（翻译：链接）我所理解是连接给定包名的app的进程，为什么是我所理解，因为官网没有写
    process = frida.get_usb_device().attach(PACKAGE) # 获取给定包名的app进程
    print(process) # 打印看看是嘛玩意儿
    script = process.create_script(jscode) # 这里是把你的js脚本给塞进了process，源码在这https://github.com/frida/frida-python/blob/master/frida/core.py#L147
    # script.on('message', on_message)
    print('[*] Running CTF')
    script.load() # 加载脚本，https://github.com/frida/frida-python/blob/master/frida/core.py#L191
    sys.stdin.read()