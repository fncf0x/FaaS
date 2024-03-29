import math
import subprocess as sp

FAAS_BIN = '/home/jack/dataimpact/faas/faas_avd/'


def get_status(device_id):
    p = sp.run(f"docker logs --tail 6 {device_id}", shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    raw_output = p.stdout.decode()
    if any(t in raw_output for t in ['* Running', 'HTTP']):
        return 'running'
    return 'booting'


def get_images():
    images = []

    p = sp.run("docker images | grep -Ei '^faas_'|tr -s ' ' '|'", shell=True, stdout=sp.PIPE)
    raw_output = p.stdout.decode()
    _images = raw_output.split('\n')[:-1]
    for image in _images:
        image_info = image.split('|')
        images.append({"name": image_info[0].replace('faas_', ''), "id": image_info[2]})
    return images


def get_devices(all_devices=True):
    devices = []

    p = sp.run("docker ps | grep 'android_'|tr -s ' ' '|'", shell=True, stdout=sp.PIPE)
    if all_devices:
        p = sp.run("docker ps -a | grep 'android_'|tr -s ' ' '|'", shell=True, stdout=sp.PIPE)
    raw_output = p.stdout.decode()

    _devices = raw_output.split('\n')[:-1]
    for device in _devices:
        device_info = device.split('|')
        status = ''
        ip = 'Not listening'
        device_id = device_info[0]
        device_name = device_info[1]
        if any(t in device for t in ['Exited', 'Created']):
            status = 'stopped'
            ip = 'Not listening'
        else:
            status = get_status(device_id)
            ip = device_info[-2].split('->')[0]
        devices.append({
            'id': device_id,
            'ip': ip,
            'name': device_name,
            'status': status
        })

    return devices


def refresh_devices(all_devices=True):
    devices_list = get_devices(all_devices)
    devices_ids = [d['id'] for d in devices_list]
    devices_info = dict([(d['id'], d) for d in devices_list])
    return devices_list, devices_ids, devices_info


def run_device(device_id):
    p = sp.run(f"docker ps -a | grep '{device_id}'|tr -s ' ' '|'", shell=True, stdout=sp.PIPE)
    raw_output = p.stdout.decode()
    name = raw_output.split('|')[-1].strip().split('_')
    arch = name[0]
    api = name[1]
    tag = name[2]
    p = sp.Popen([f"EPWD={FAAS_BIN} {FAAS_BIN}faas run {arch} {api} {tag}"], shell=True, stdout=sp.PIPE, stderr=sp.PIPE,
                 close_fds=True)


def stop_device(device_id):
    sp.run(f"docker stop {device_id}", shell=True, stdout=sp.PIPE)


def remove_device(device_id):
    p = sp.run(f"docker ps -a | grep '{device_id}'|tr -s ' ' '|'", shell=True, stdout=sp.PIPE)
    raw_output = p.stdout.decode()
    name = raw_output.split('|')[-1].strip().split('_')
    arch = name[0]
    api = name[1]
    tag = name[2]
    sp.run(f"EPWD={FAAS_BIN} {FAAS_BIN}faas remove {arch} {api} {tag}", shell=True, stdout=sp.PIPE, stderr=sp.PIPE)


def add_new_device(image):
    info = image.strip().split('_')
    arch = info[2]
    api = info[1]
    sp.run(f"EPWD={FAAS_BIN} {FAAS_BIN}faas add {arch} {api} ", shell=True, stdout=sp.PIPE, stderr=sp.PIPE)


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
