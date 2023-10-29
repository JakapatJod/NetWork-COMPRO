from flask import Flask, render_template, request, redirect, url_for
from netmiko import ConnectHandler
import re
import os


app = Flask(__name__)
app.secret_key = 'SeCreT_Key'
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024 # 300MB

devices_4 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.21',
    'username': 'cisco',
    'password': 'cisco'
}

devices_5 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.171',
    'username': 'cisco',
    'password': 'cisco'
}

all_dev = [devices_4,devices_5]

@app.route('/')
def index():
    global all_dev
    results = []

    for device in all_dev:
        netconect = ConnectHandler(**device)
        netconect.enable()   # enable mode
        config_command = ['do show ip int bri'] 
        output = netconect.send_config_set(config_command)

        results.append(output)

        print(results) 
        netconect.disconnect()

    return render_template('index.html',results=results)


@app.route('/Hostname',methods=['GET','POST'])
def Hostname():
    global devices_4
    netconect = ConnectHandler(**devices_4)
    netconect.enable()   # enable mode
    
    New_hostnameDevice = request.form.get(f'hostname')

    config_command = [f'hostname {New_hostnameDevice} '] 
    output = netconect.send_config_set(config_command)

    print(output) 
    netconect.disconnect()

    return render_template('Hostname.html',output=output)

@app.route('/config_ip', methods=['GET','POST'])
def config_ip():
    global devices_4

    net_connect = ConnectHandler(**devices_4)
    net_connect.enable()

    config_commands = ['exit', 'show ip interface brief']
    output = net_connect.send_config_set(config_commands)

    lines = output.splitlines()
    interface_list = []

    for line in lines:
        match = re.match(r'^([A-Za-z]+\d+/\d+/\d+|[A-Za-z]+\d+/\d+|[A-Za-z]+\d+)', line)
        if match:
            interface = match.group(1)
            if not re.match(r'^(SW|Router|R|Switch)', interface, re.IGNORECASE):
                interface_list.append(interface)
                
    print(interface_list)
    # print(interface)

    interface_name = request.form.get('interface')
    new_ip = request.form.get('new_ip')
    new_subnet = request.form.get('new_subnetmask')
    noswitchport = request.form.get('noswitchport')

    print(f'Interface Name: {interface_name}')

    if interface_name and new_ip:
        config_commands = [
            f'interface {interface_name}',
            f'ip address {new_ip} {new_subnet}',
            'no shutdown',
            'end',
            'show ip interface brief'
        ]
        if noswitchport == 'yes': 
            config_commands.insert(2, 'no sw')

        output = net_connect.send_config_set(config_commands)

    net_connect.disconnect()

    return render_template('config_ip.html', output=output, interface_list=interface_list)


uploads_directory = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(uploads_directory):
    os.makedirs(uploads_directory)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    results = []

    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            file_path = os.path.join(uploads_directory, uploaded_file.filename)
            uploaded_file.save(file_path)

            with open(file_path, 'r') as file:
                file_contents = file.read()

            devices_to_configure = all_dev

            for device in devices_to_configure:
                net_connect = ConnectHandler(**device)
                net_connect.enable()
                config_command = file_contents.split('\n')
                output = net_connect.send_config_set(config_command)
                results.append(output)

                net_connect.disconnect()

            os.remove(file_path)

            return render_template('upload_result.html', results=results)

    return render_template('upload.html')


# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         uploaded_file = request.files['file']
#         if uploaded_file:
#             file_path = os.path.join(uploads_directory, uploaded_file.filename)
#             uploaded_file.save(file_path)

#             with open(file_path, 'r') as file:
#                 file_contents = file.read()

#             net_connect = ConnectHandler(**devices_4)
#             net_connect.enable()
#             config_command = file_contents.split('\n')
#             output = net_connect.send_config_set(config_command)
#             net_connect.disconnect()

#             # Remove the uploaded file
#             os.remove(file_path)

#             return render_template('upload_result.html', output=output)

#     return render_template('upload.html')




if __name__ == '__main__':
    app.run(debug=True)