import subprocess as sp
import os
import base64
import time
import frida
import json


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

def frida_func(app_name=None, init_script=None, class_name=None, func_name=None, func_args=None):
    pass

def frida_script(app_name=None, script_name=None, args=None):
    success = True
    msg = "Script executed"
    script_path = f"/hooks/{script_name}.js"


    try:
        with open(script_path, 'r') as script_file:
            script = script_file.read()
    except:
        success = False
        msg = 'Script not found'

    apps = get_apps()

    if args:
        script = script.format(*args)
        success = True
        msg = script

    if app_name not in apps:
        success = False
        msg = 'app not installed'    

    if not success:
        return success, msg

    def on_message(message, data):
        if message['type'] == 'send':
            with open(f"/tmp/{script_name}.result", "w") as w:
                w.write(str(message['payload']))

    try:
        try:
            process = frida.get_usb_device().attach(app_name)
        except:
            device = frida.get_device_manager().enumerate_devices()[-1]
            pid = device.spawn(app_name)
            process = device.attach(pid)
            time.sleep(20)
            device.resume(pid)
    except frida.ServerNotRunningError:
        sp.run(['adb shell "/data/local/tmp/updater -l 0.0.0.0 -D &"'], shell=True, stdout=sp.PIPE)

    script = process.create_script(script)
    script.on('message', on_message)
    script.load()
    with open(f"/tmp/{script_name}.result", "r") as w:
                msg = w.read()

    return success, msg

def get_apks():
    stdout = sp.run([f'ls /apk/*.apk'], shell=True, stdout=sp.PIPE).stdout.decode()
    apks = []
    for x in stdout.split('\n')[:-1]:
        apk = x.split('/')[-1]
        apks.append(apk)
    return apks

def install_apk(apk_name):
    stdout = sp.run([f'adb install /apk/{apk_name}'], shell=True, stdout=sp.PIPE).stdout.decode()
    return stdout