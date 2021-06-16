import subprocess as sp


T800_BIN = '/home/jack/dataimpact/t800/t800_avd/'

def get_status(device_id):
    p = sp.run(f"docker logs --tail 13 {device_id}", shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    raw_output = p.stdout.decode()
    if any(t in raw_output for t in ['* Running', 'HTTP']):
        return 'running'
    return 'booting'
    
def get_images():
    images = []

    p = sp.run("docker images | grep -Ei '^t800_'|tr -s ' ' '|'", shell=True, stdout=sp.PIPE)
    raw_output = p.stdout.decode()
    _images = raw_output.split('\n')[:-1]
    for image in _images:
        image_info = image.split('|')
        images.append({"name": image_info[0].replace('t800_', ''), "id": image_info[2]})
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
    devices_info = dict([(d['id'],d) for d in devices_list])
    return devices_list, devices_ids, devices_info

def run_device(device_id):
    p = sp.run(f"docker ps -a | grep '{device_id}'|tr -s ' ' '|'", shell=True, stdout=sp.PIPE)
    raw_output = p.stdout.decode()
    name = raw_output.split('|')[-1].strip().split('_')
    arch = name[0]
    api = name[1]
    tag = name[2]
    p = sp.Popen([f"EPWD={T800_BIN} {T800_BIN}t800 run {arch} {api} {tag}"], shell=True, stdout=sp.PIPE, stderr=sp.PIPE, close_fds=True)

def stop_device(device_id):
    sp.run(f"docker stop {device_id}", shell=True, stdout=sp.PIPE)

def remove_device(device_id):
    p = sp.run(f"docker ps -a | grep '{device_id}'|tr -s ' ' '|'", shell=True, stdout=sp.PIPE)
    raw_output = p.stdout.decode()
    name = raw_output.split('|')[-1].strip().split('_')
    arch = name[0]
    api = name[1]
    tag = name[2]
    sp.run(f"EPWD={T800_BIN} {T800_BIN}t800 remove {arch} {api} {tag}", shell=True, stdout=sp.PIPE, stderr=sp.PIPE)

def add_new_device(image):
    info = image.strip().split('_')
    arch = info[2]
    api = info[1]
    sp.run(f"EPWD={T800_BIN} {T800_BIN}t800 add {arch} {api} ", shell=True, stdout=sp.PIPE, stderr=sp.PIPE)