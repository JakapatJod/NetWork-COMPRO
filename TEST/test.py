from flask import Flask, request, render_template, redirect, url_for
from netmiko import ConnectHandler

app = Flask(__name__)
app.secret_key = 'SeCreT_Key'
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.21',
    'username': 'cisco',
    'password': 'cisco'
}
current_output = "" 

@app.route('/')
def index():
    return render_template('command.html', output=current_output)  

@app.route('/execute', methods=['POST'])
def execute_command():
    global device
    global current_output  

    if not device:
        return "No device"

    try:
        command = request.form.get('command')

        net_connect = ConnectHandler(**device)
        net_connect.config_mode()

        if command == 'exit':
            net_connect.send_command("exit")
            net_connect.enable()

        elif command == 'config terminal':
            net_connect.send_command("exit")
            net_connect.config_mode()

        output = net_connect.send_command_timing(command)

        print(output)

        return render_template('command.html', output=output)  

    except Exception as err:
        print(f"Error: {str(err)}")

if __name__ == '__main__':
    app.run(debug=True)
