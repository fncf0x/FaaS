from flask import Flask, render_template, request, make_response, Markup
import subprocess as sp
import logging
from android_utils import *
from utils import check_page_name, safe_cmd, make_args
import re


logging.basicConfig(filename='/flask.log',level=logging.DEBUG)
app = Flask(__name__, template_folder='./templates')

@app.route('/')
def index():
    device_info = get_device_info()
    default_page = render_template(
        'device.html',
        uptime=device_info['uptime'],
        device_id=device_info['id'],
        img_b64=get_b64_screen(),
        display=Markup(render_template('./views/info.html', infos=get_info())))
    return default_page


@app.route('/page', methods=['GET', 'POST'])
def page():
    page_name = request.form.get('name')
    if page_name:
        if not check_page_name(page_name):
            return "Error"
        path = f'views/{page_name}.html'
        return {
            "info": render_template(path, infos=get_info()),
            "apps": render_template(path, apps=get_apps()),
            "hooks": render_template(path, hooks=get_hooks()),
            "shell": render_template(path, stdout='')
            }.get(page_name, 'Error')
    return 'Error'


@app.route('/exec_frida_function', methods=['GET', 'POST'])
def exec_frida_function():
    app_name = request.args.get('app_name')
    init_script = request.args.get('init_script')
    class_name = request.args.get('class_name')
    func_name = request.args.get('func_name')
    func_args = request.args.get('func_args')
    func_args = make_args(func_args)
    frida_func(app_name, init_script, func_name, func_args)
    return (
        f'name: {app_name}<br>'
        f'init_script: {init_script}<br>'
        f'class: {class_name}<br>'
        f'function: {func_name}<br>'
        f'args: {func_args}<br>')


@app.route('/exec_frida_script', methods=['GET', 'POST'])
def exec_frida_script():
    app_name = request.args.get('app_name')
    script_name = request.args.get('script_name')
    args = request.args.get('args')
    args = make_args(args)
    code, msg = frida_script(app_name, script_name, args)
    if not code:
        return json.dumps({
            'code': 1,
            'msg': msg})
    else:
        return json.dumps({
            'code': 0,
            'msg': json.loads(msg)})


@app.route('/install_apk', methods=['GET', 'POST'])
def install():
    apk_name = request.args.get('apk_name')
    apks = get_apks()
    if not apks:
        return 'No apks uploaded yet'
    if apk_name not in apks:
        return 'Apk not found'
    return install_apk(apk_name)


@app.route('/cmd', methods=['GET', 'POST'])
def cmd():
    cmd = request.form.get('cmd')
    if cmd:
        cmd = safe_cmd(cmd)
        stdout, stderr = android_shell_cmd(cmd)
        if stdout:
            return stdout
        else:
            return stderr
    return 'Error'


@app.route('/getScreen')
def get_screen():
    b64_screen = get_b64_screen()
    return f"<img src='data:image/png;base64,{b64_screen}' height=100%>"


app.run(host='0.0.0.0', debug=True)
