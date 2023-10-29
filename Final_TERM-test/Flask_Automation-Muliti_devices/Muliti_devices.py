from flask import Flask, render_template, request
from netmiko import ConnectHandler
import re

app = Flask(__name__)
app.secret_key = 'SeCreT_Key'
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024 # 300MB

devices_4 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.21',
    'username': 'cisco',
    'password': 'cisco',
    'port':'22'
}

devices_5 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.22',
    'username': 'cisco',
    'password': 'cisco',
    'port':'22'
}

devices_6 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.23',
    'username': 'cisco',
    'password': 'cisco',
    'port':'22',

}

all_devices = [devices_4, devices_5, devices_6]



@app.route('/')
def index():
    return render_template('index.html')


# -------------------------------------------------------------------------------- show ip int bri

@app.route('/show_int', methods=['GET', 'POST'])
def show_int():
    global all_devices
    results = []

    for device in all_devices:
        net_connect = ConnectHandler(**device)
        config_commands = ['do show ip int bri ']
        output = net_connect.send_config_set(config_commands)
        results.append(output)

    return render_template('show_output.html', results=results)

# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- Config VLAN


@app.route('/config_vlan', methods=['GET', 'POST'])
def config_vlan():
    global all_devices
    results = []

    for device in all_devices:
        net_connect = ConnectHandler(**device)
        vlan_id = request.form.get('vlan_id')
        vlan_name = request.form.get('vlan_name')
        config_commands = [
            f'vlan {vlan_id}',
            f'name {vlan_name}',
            'end', 'show vlan'
        ]
        output = net_connect.send_config_set(config_commands)
        
        results.append(output)


    return render_template('config_vlan.html', results=results)

# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- Config ip 

interface_lists = {}  

def get_interface_list(device):
    net_connect = ConnectHandler(**device)
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

    net_connect.disconnect()

    return interface_list

for device in all_devices:
    interface_lists[device['ip']] = get_interface_list(device)

@app.route('/configure_ip', methods=['GET', 'POST'])
def configure_ip():
    global all_devices
    results = []

    if request.method == 'POST':
        for device in all_devices:
            net_connect = ConnectHandler(
                device_type=device['device_type'],
                ip=device['ip'],
                username=device['username'],
                password=device['password'])
            
            net_connect.enable()

            device_ip = device['ip']

            interface_name = request.form.get(f'interface_')
            new_ip = request.form.get(f'new_ip_{device_ip}')
            new_subnet = request.form.get(f'new_subnetmask_{device_ip}')
            noswitchport = request.form.get(f'noswitchport_{device_ip}')

            config_commands = [
                f'interface {interface_name}',
                f'ip address {new_ip} {new_subnet}',
                'no shutdown',
                'end',
                'show ip interface brief']
            
            if noswitchport == 'yes':
                config_commands.insert(1, 'no switchport')

            output = net_connect.send_config_set(config_commands)
            results.append(output)
            net_connect.disconnect()

            print(output)

    return render_template('configure_ip.html', results=results, all_devices=all_devices, interface_lists=interface_lists)

# --------------------------------------------------------------------------------



# --------------------------------------------------------------------------------

@app.route('/configure_mode', methods=['GET', 'POST'])
def configure_mode():
    global all_devices , interface_lists
    results = []

    if request.method == 'POST':
        for device in all_devices:
            net_connect = ConnectHandler(
                device_type=device['device_type'],
                ip=device['ip'],
                username=device['username'],
                password=device['password'])
            
            net_connect.enable()

            interface_name = request.form.get(f'interface_')
            mode = request.form.get('mode')
            vlan_id = request.form.get('vlan_id')
            switchport = request.form.get('switchport')

            access_vlan = request.form.get('access_vlan')
            config_commands = [
                f'interface {interface_name}',
                'switchport trunk encapsulation dot1q',
                f'switchport mode {mode}',
                'end',
                'show vlan brief',
                'show interface trunk'
            ]
            if switchport == 'yes': 
                config_commands.insert(1, 'sw')


            if mode == 'access':
                config_commands.insert(3,f'switchport access vlan {vlan_id}')

            if access_vlan:  
                config_commands.insert(3, f'switchport trunk allow vlan {access_vlan}') 

            output = net_connect.send_config_set(config_commands)
            results.append(output)
            net_connect.disconnect()

            print(output)

    return render_template('configure_mode.html', results=results, all_devices=all_devices, interface_lists=interface_lists)


if __name__ == '__main__':
    app.run(debug=True)
