from flask import Flask, request, render_template, redirect, url_for
from netmiko import ConnectHandler

app = Flask(__name__)

device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.21',
    'username': 'cisco',
    'password': 'cisco',
    'port': 22,
}

net_connect = ConnectHandler(**device)
net_connect.enable()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/command-page')
def command_page():
    return render_template('command-page.html')

@app.route('/command', methods=['POST'])
def execute_command():
    try:
        cmd = request.form['command']
        if cmd.strip().lower() == "configure terminal":
            output = net_connect.config_mode()
        else:
            output = net_connect.send_command_timing(cmd)
        return output
    except Exception as err:
        return f"Error: {str(err)}"

if __name__ == '__main__':
    app.run()
