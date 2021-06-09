from flask import Flask, render_template, request, make_response, Markup
import subprocess as sp
from android_utils import get_b64_screen, android_shell_cmd, get_apps, get_hooks, get_info, get_device_info
from utils import check_page_name, safe_cmd


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


@app.route('/run_hook')
def run_hook():
    return 'run hook'


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
