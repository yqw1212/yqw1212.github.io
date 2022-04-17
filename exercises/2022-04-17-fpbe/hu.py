#!/usr/bin/env python3
import os
import re
import time
import string
import hashlib

flag_len = 16
flag_chars = string.digits + string.ascii_letters + '_@#!-+=*$&^()<>?~'

os.system(r"echo 'p:uprobed_function_enter /mnt/hgfs/Shares/datacon2022/re/fpbe/fpbe:0x2316 %ip %ax' > /sys/kernel/debug/tracing/uprobe_events")
os.system(r"echo 'r:uprobed_function_exit /mnt/hgfs/Shares/datacon2022/re/fpbe/fpbe:0x2316 %ip %ax' >> /sys/kernel/debug/tracing/uprobe_events")
os.system(r"echo 1 > /sys/kernel/debug/tracing/events/uprobes/enable")

flag = ['0' for _ in range(flag_len)]
for i in range(flag_len):
    sub_times = []
    for ch in flag_chars:
        flag[i] = ch
        payload = './fpbe "{}" > /dev/null'.format(''.join(flag))
        os.system(payload)
        time_stamp = str(time.time())
        temp_file = hashlib.md5(time_stamp.encode()).hexdigest()
        os.system('tail -n 2 /sys/kernel/debug/tracing/trace > {}'.format(temp_file))
        with open(temp_file, 'r') as f:
            res = f.readlines()
            uprobed_function_enter = eval(res[0][35:46])
            uprobed_function_exit = eval(res[1][35:46])
            # print(uprobed_function_enter, uprobed_function_exit)
            sub_times.append(uprobed_function_exit - uprobed_function_enter)
        os.system('rm {}'.format(temp_file))
    idx = sub_times.index(max(sub_times))
    flag[i] = flag_chars[idx]

os.system(r"echo 0 > /sys/kernel/debug/tracing/events/uprobes/enable")
os.system(r"echo > /sys/kernel/debug/tracing/uprobe_events")

print('HFCTF{' + ''.join(flag) + '}')
