from flask import Flask, render_template, request, make_response, Markup, send_file
from utils import refresh_devices, get_images, run_device, stop_device, remove_device, add_new_device
import subprocess as sp
import requests


app = Flask(__name__, template_folder='./templates')



@app.route('/')
def index():
    devices_list, _, _ = refresh_devices()
    images = get_images()
    devices_page = render_template('devices_list.html', devices=devices_list)
    content = render_template('devices.html', devices_list=Markup(devices_page), images=images)
    return render_template('index.html', content=Markup(content))

@app.route('/devices')
def devices():
    devices_list, _, _ = refresh_devices()
    content = render_template('devices_list.html', devices=devices_list)
    return Markup(content)

@app.route('/settings/')
def settings():
    return render_template('index.html', content=Markup("<center><font color=red>not implemented yet :^)</font></center>"))

@app.route('/servers/')
def servers():
    return render_template('index.html', content=Markup("<center><font color=red>not implemented yet :^)</font></center>"))

@app.route('/<device_id>/')
def debug(device_id):
    _, devices_ids, devices_info = refresh_devices()
    if device_id not in devices_ids:
        return "<center>No such device</center>"
    avd_port = devices_info[device_id]['ip'].split(':')[1]    
    content = requests.get(f'http://127.0.0.1:{avd_port}').text
    return render_template('index.html', content=Markup(content), device_id=device_id)

@app.route('/<device_id>/<endpoint>', methods=['GET', 'POST'])
def status(device_id, endpoint):
    _, devices_ids, devices_info = refresh_devices()
    if device_id not in devices_ids:
        return "<center>No such device</center>"
    avd_port = devices_info[device_id]['ip'].split(':')[1] 
    if request.method == 'GET':
        api_response = requests.get(f'http://127.0.0.1:{avd_port}/{endpoint}').text
        return api_response
    if request.method == 'POST':
        data = request.form
        api_response = requests.post(f'http://127.0.0.1:{avd_port}/{endpoint}', data=data).text
        return api_response

@app.route('/add_device', methods=['POST'])
def add_device():
    images = [ i['name'] for i in get_images()]
    image = request.form.get('image_name')
    if image not in images:
        return 'error'
    add_new_device(image)
    return 'OK'

@app.route('/delete_device', methods=['POST'])
def delete_device():
    device_id = request.form.get('id')
    _, devices_ids, _ = refresh_devices()
    if device_id not in devices_ids:
        return "error"
    remove_device(device_id)
    return 'OK'

@app.route('/pause_device', methods=['POST'])
def pause_device():
    device_id = request.form.get('id')
    _, devices_ids, _ = refresh_devices(all_devices=False)
    if device_id not in devices_ids:
        return "error"
    stop_device(device_id)
    return 'OK'

@app.route('/start_device', methods=['POST'])
def start_device():
    device_id = request.form.get('id')
    _, devices_ids, _ = refresh_devices()
    if device_id not in devices_ids:
        return "error"
    run_device(device_id)
    return 'OK'


app.run(host='0.0.0.0', port=4000, debug=True)
