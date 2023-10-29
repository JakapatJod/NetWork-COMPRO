from flask import Flask, render_template, request, jsonify
from netmiko import ConnectHandler

app = Flask(__name__)

device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.171',
    'username': 'cisco',
    'password': 'cisco',
    'port': 22,
}

net_connect = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_command', methods=['POST'])
def send_command():
    global net_connect 

    if not net_connect or not net_connect.is_alive():  # Check if the connection is active
        try:
            net_connect = ConnectHandler(**device)
            net_connect.enable()
        except Exception as e:
            return jsonify({'output': f'Error connecting: {str(e)}'})

    cmd = request.form['command']
    if cmd.strip().lower() == "configure terminal":
        output = net_connect.config_mode()
    else:
        output = net_connect.send_command_timing(cmd)

    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
