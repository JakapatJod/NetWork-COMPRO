from flask import Flask, render_template, request, jsonify
from netmiko import ConnectHandler
import re
app = Flask(__name__)

device = {
    'device_type': 'cisco_ios',
    'ip': '10.4.60.146',
    'username': 'cisco',
    'password': 'cisco',
    'port': 22,
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showrun', methods=['POST'])
def show_run():

    return render_template('show_run.html')

@app.route('/get_command', methods=['GET'])
def get_command():
    global device

    net_connect = ConnectHandler(**device)
    net_connect.enable()
    command = request.args.get('show run')  
    net_connect.disconnect()


    return jsonify({'command': command})

if __name__ == '__main__':
    app.run(debug=True)
