import datetime
import os

import requests
from flask import Flask, render_template, request, Markup, flash, redirect, url_for, send_from_directory
from pyaxmlparser import APK
from werkzeug.utils import secure_filename

from utils import get_devices, convert_size

UPLOAD_FOLDER = "./resources/"
ALLOWED_EXTENSIONS = ["js", "apk"]
MAX_FILE_SIZE = 100 * 1024 * 1024

app = Flask(__name__, template_folder='./templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = MAX_FILE_SIZE


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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/scripts')
def frida_script_list():
    columns = ["Frida Scripts", "Size", "Last Modifed"]

    path = os.path.join(os.getcwd(), "resources/frida_scripts")
    files = os.listdir(path)
    scripts = []
    for filename in files:
        file_size = convert_size(os.path.getsize(os.path.join(path, filename)))
        last_modified = str(datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(path, filename))))[:-7]

        script = []
        script.append(filename)
        script.append(file_size)
        script.append(last_modified)

        scripts.append(script)

    return render_template('list.html', columns=columns, len_col=len(columns) + 1, files=scripts,
                           list_name="Frida Script")


@app.route('/apps')
def apk_list():
    columns = ["APK File Name", "Package", "Size", "Version"]

    path = os.path.join(os.getcwd(), "resources/apks")
    files = os.listdir(path)
    apks = []
    for filename in files:
        print("boop", os.path.join(path, filename))
        apkf = APK(os.path.join(path, filename))

        package = apkf.package
        file_size = convert_size(os.path.getsize(os.path.join(path, filename)))
        version = apkf.version_name

        apk = []
        apk.append(filename)
        apk.append(package)
        apk.append(file_size)
        apk.append(version)

        apks.append(apk)

    return render_template('list.html', columns=columns, len_col=len(columns) + 1, files=apks, list_name="APK")


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        extension = file.filename.split('.')[-1]

        if extension == "apk":
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "apks/", filename))
            return redirect(url_for('apk_list'))

        if extension == "js":
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "frida_scripts/", filename))
            return redirect(url_for('frida_script_list'))
        return redirect(request.url)


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
