from flask import Flask, render_template, request, make_response, Markup, send_file
from utils import get_devices
import subprocess as sp
import requests


app = Flask(__name__, template_folder='./templates')

@app.route('/')
def index():
    devices = get_devices()
    content = render_template('devices.html', devices=devices)
    return render_template('index.html', content=Markup(content))

@app.route('/<device_id>/')
def debug(device_id):
    content = requests.get('http://127.0.0.1:5000').text
    return render_template('index.html', content=Markup(content), device_id=device_id)

@app.route('/<device_id>/<endpoint>', methods=['GET', 'POST'])
def status(device_id, endpoint):

    if request.method == 'GET':
        api_response = requests.get(f'http://127.0.0.1:5000/{endpoint}').text
        return api_response
    if request.method == 'POST':
        data = request.form
        api_response = requests.post(f'http://127.0.0.1:5000/{endpoint}', data=data).text
        return api_response

app.run(host='0.0.0.0', port=4000, debug=True)
