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
        print(device_info)
        devices.append({
            'id': device_info[0],
            'ip': device_info[-2].split('->')[0],
            'name': device_info[-1],
            'status': status
        })

    return devices
