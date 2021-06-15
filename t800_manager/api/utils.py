import math
import subprocess as sp


def get_devices():
    devices = []

    p = sp.run("docker ps -a | grep 'Android_'|tr -s ' ' '|'", shell=True, stdout=sp.PIPE)
    raw_output = p.stdout.decode()

    _devices = raw_output.split('\n')[:-1]
    for device in _devices:
        status = 'running'
        if 'Exited' in device:
            status = 'stopped'
        device_info = device.split('|')
        ip = device_info[-2].split('->')[0]
        if status == 'stopped':
            ip = 'Not listening'
        devices.append({
            'id': device_info[0],
            'ip': ip,
            'name': device_info[-1],
            'status': status
        })

    return devices


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
