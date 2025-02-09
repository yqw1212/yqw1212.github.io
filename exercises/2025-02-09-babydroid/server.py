#!/usr/bin/env python3
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import random
import shlex
import string
import subprocess
import sys
import time
import base64
import requests
import uuid
from hashlib import *
import zipfile
import signal
import traceback

random_hex = lambda x: ''.join([random.choice('0123456789abcdef') for _ in range(x)])
difficulty = 6
ADB_PORT = int(random.random() * 60000 + 5000)
EMULATOR_PORT = ADB_PORT + 1
EXPLOIT_TIME_SECS = 30
APK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app-debug.apk")
FLAG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flag")
HOME = "/home/user"
VULER = "com.bytectf.babydroid"
ATTACKER = "com.bytectf.pwnbabydroid"

ENV = {}
ENV.update(os.environ)
ENV.update({
    "ANDROID_ADB_SERVER_PORT": "{}".format(ADB_PORT),
    "ANDROID_SERIAL": "emulator-{}".format(EMULATOR_PORT),
    "ANDROID_SDK_ROOT": "/opt/android/sdk",
    "ANDROID_SDK_HOME": HOME,
    "ANDROID_PREFS_ROOT": HOME,
    "ANDROID_EMULATOR_HOME": HOME + "/.android",
    "ANDROID_AVD_HOME": HOME + "/.android/avd",
    "JAVA_HOME": "/usr/lib/jvm/java-11-openjdk-amd64",
    "PATH": "/opt/android/sdk/cmdline-tools/latest/bin:/opt/android/sdk/emulator:/opt/android/sdk/platform-tools:/bin:/usr/bin:" + os.environ.get("PATH", "")
})

def print_to_user(message):
    print(message)
    sys.stdout.flush()

def download_file(url):
    try:
        download_dir = "download"
        if not os.path.isdir(download_dir):
            os.mkdir(download_dir)
        tmp_file = os.path.join(download_dir, time.strftime("%m-%d-%H:%M:%S", time.localtime())+str(uuid.uuid4())+'.apk')
        f = requests.get(url)
        if len(f.content) > 5*1024*1024: # Limit size 5M
            return None
        with open(tmp_file, 'wb') as fp:
            fp.write(f.content)
        return tmp_file
    except:
        return None

def proof_of_work():
    prefix = random_hex(6)
    print_to_user(f'Question: sha256(("{prefix}"+"xxxx").encode()).hexdigest().startswith("{difficulty*"0"}")')
    print_to_user(f'Please enter xxxx to satisfy the above conditions:')
    proof = sys.stdin.readline().strip()
    return sha256((prefix+proof).encode()).hexdigest().startswith(difficulty*"0") == True

def check_apk(path):
    return True

def setup_emulator():
    subprocess.call(
        "avdmanager" +
        " create avd" +
        " --name 'pixel_xl_api_30'" +
        " --abi 'google_apis/x86_64'" +
        " --package 'system-images;android-30;google_apis;x86_64'" +
        " --device pixel_xl" +
        " --force" +
        " > /dev/null 2> /dev/null" + 
        "",
        env=ENV,
        close_fds=True,
        shell=True)

    return subprocess.Popen(
        "emulator" +
        " -avd pixel_xl_api_30" +
        " -no-cache" +
        " -no-snapstorage" +
        " -no-snapshot-save" +
        " -no-snapshot-load" +
        " -no-audio" +
        " -no-window" +
        " -no-snapshot" +
        " -no-boot-anim" +
        " -wipe-data" +
        " -accel on" +
        " -netdelay none" +
        " -no-sim" +
        " -netspeed full" +
        " -delay-adb" +
        " -port {}".format(EMULATOR_PORT) +
        " > /dev/null 2> /dev/null " +
        "",
        env=ENV,
        close_fds=True,
        shell=True,
        preexec_fn=os.setsid)

def adb(args, capture_output=True):
    return subprocess.run(
        "adb {} 2> /dev/null".format(" ".join(args)),
        env=ENV,
        shell=True,
        close_fds=True,
        capture_output=capture_output).stdout

def adb_install(apk):
    adb(["install", apk])

def adb_activity(activity, extras=None, wait=False):
    args = ["shell", "am", "start"]
    if wait:
        args += ["-W"]
    args += ["-n", activity]
    if extras:
        for key in extras:
            args += ["-e", key, extras[key]]
    adb(args)

def adb_broadcast(action, receiver, extras=None):
    args = ["shell", "su", "root", "am", "broadcast", "-W", "-a", action, "-n", receiver]
    if extras:
        for key in extras:
            args += ["-e", key, extras[key]]
    adb(args)

print_to_user(r"""
 ____              __               ____                         __     
/\  _`\           /\ \             /\  _`\                __    /\ \    
\ \ \L\ \     __  \ \ \____  __  __\ \ \/\ \  _ __   ___ /\_\   \_\ \   
 \ \  _ <'  /'__`\ \ \ '__`\/\ \/\ \\ \ \ \ \/\`'__\/ __`\/\ \  /'_` \  
  \ \ \L\ \/\ \L\.\_\ \ \L\ \ \ \_\ \\ \ \_\ \ \ \//\ \L\ \ \ \/\ \L\ \ 
   \ \____/\ \__/.\_\\ \_,__/\/`____ \\ \____/\ \_\\ \____/\ \_\ \___,_\
    \/___/  \/__/\/_/ \/___/  `/___/> \\/___/  \/_/ \/___/  \/_/\/__,_ /
                                 /\___/                                 
                                 \/__/                                  
""")

if not proof_of_work():
    print_to_user("Please proof of work again, exit...\n")
    exit(-1)

print_to_user("Please enter your apk url:")
url = sys.stdin.readline().strip()
EXP_FILE = download_file(url)
if not check_apk(EXP_FILE):
    print_to_user("Invalid apk file.\n")
    exit(-1)

print_to_user("Preparing android emulator. This may takes about 2 minutes...\n")
emulator = setup_emulator()
adb(["wait-for-device"])

adb_install(APK_FILE)
adb_activity(f"{VULER}/.MainActivity", wait=True)
with open(FLAG_FILE, "r") as f:
    adb_broadcast(f"com.bytectf.SET_FLAG", f"{VULER}/.FlagReceiver", extras={"flag": f.read()})

time.sleep(3)
adb_install(EXP_FILE)
adb_activity(f"{ATTACKER}/.MainActivity")

print_to_user("Launching! Let your apk fly for a while...\n")
time.sleep(EXPLOIT_TIME_SECS)


try:
    os.killpg(os.getpgid(emulator.pid), signal.SIGTERM)
except:
    traceback.print_exc()