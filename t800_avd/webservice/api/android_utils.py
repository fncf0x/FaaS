import subprocess as sp
import os
import base64


def screenshot():
    sp.run(['adb shell screencap -p > /tmp/screen.png && convert /tmp/screen.png -resize 480x480 /tmp/screen_.png && rm /tmp/screen.png'], shell=True, stdout=sp.PIPE).stdout

def get_b64_screen():
    screenshot()
    image_binary = open('/tmp/screen_.png', 'rb').read()
    b64_image = base64.b64encode(image_binary).decode()
    return b64_image

def android_shell_cmd(cmd):
    p = sp.run([f'adb shell \'{cmd}\''], shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout = p.stdout
    stderr = p.stderr
    return stdout.decode(), stderr.decode()

def shell_cmd(cmd):
    p = sp.run([cmd], shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout = p.stdout
    stderr = p.stderr
    return stdout.decode(), stderr.decode()

def get_info():
    os, _ = android_shell_cmd("getprop ro.build.version.release")
    api_lvl, _ = android_shell_cmd("getprop ro.build.version.sdk")
    arch, _ = android_shell_cmd("getprop ro.product.cpu.abi")
    cpu_info, _ = android_shell_cmd("cat /proc/cpuinfo")
    uname, _ = android_shell_cmd("uname -a")
    _storage, _ = android_shell_cmd('df -h /sdcard/ | tr -s " " ":" | cut -d: -f2,3,4,5 | tail -1')
    storage = _storage.split(":")
    return [{
        "api": api_lvl,
        "os": os,
        "arch": arch,
        "cpuinfo": cpu_info,
        "uname": uname,
        "storage": storage
    }]

def get_device_info():
    d_info = {}

    container_id, _ = shell_cmd('cat /etc/hostname')
    uptime, _ = android_shell_cmd('uptime | tr -s " " "|" | cut -d "|" -f4 | tr -d ","')
    d_info['id'] = container_id
    d_info['uptime'] = uptime
    return d_info

def get_apps():
    stdout = sp.run([f'adb shell pm list packages'], shell=True, stdout=sp.PIPE).stdout
    apps = [v.replace('package:', '') for v in stdout.decode().split('\n') if 'com.android' not in v]
    return apps[:-1]


def get_hooks():
    hooks = os.scandir('/hooks')
    return [hook.name for hook in hooks]
