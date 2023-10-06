from flask import Flask, render_template, request, jsonify
from netmiko import ConnectHandler
import re
app = Flask(__name__)

device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.21',
    'username': 'cisco',
    'password': 'cisco',
    'port': 22,
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configure_interface', methods=['GET','POST'])
def configure_interface():
    global device
    try:
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
        print(interface_list)

        interface_name = request.form.get('interface')
        mode = request.form.get('mode')
        vlan_id = request.form.get('vlan_id')
        switchport = request.form.get('switchport')

        # trunk_encapsulation  = request.form.get('trunk_encapsulation')

        access_vlan = request.form.get('access_vlan')


        net_connect = ConnectHandler(**device)
        net_connect.enable()
        if interface_name and mode:

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

            # if trunk_encapsulation == 'yes': 
            #     config_commands.insert(2, 'switchport trunk encapsulation dot1q')

            if mode == 'access':
                config_commands.insert(3,f'switchport access vlan {vlan_id}')

            if access_vlan:  
                config_commands.insert(3, f'switchport trunk allow vlan {access_vlan}') 

            output = net_connect.send_config_set(config_commands)
        net_connect.disconnect()

        return render_template('configure_interface.html', output=output, interface_list=interface_list)

    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"
    
@app.route('/re_sw', methods=['GET','POST'])
def re_sw():
    global device
    try:
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
        print(interface_list)

        interface_name = request.form.get('interface')
        mode = request.form.get('mode')
        re_vlan_id = request.form.get('re_vlan_id')
        re_switchport = request.form.get('re_switchport')

        # trunk_encapsulation  = request.form.get('trunk_encapsulation')

        re_access_vlan = request.form.get('re_access_vlan')

        net_connect = ConnectHandler(**device)
        net_connect.enable()
        if interface_name and mode:

            config_commands = [
                f'interface {interface_name}',
                'no switchport trunk encapsulation dot1q',
                f'no switchport mode {mode}',
                'end',
                'show vlan brief',
                'show interface trunk'
            ]
            if re_switchport == 'yes': 
                config_commands.insert(1, 'no sw')

            # if trunk_encapsulation == 'yes': 
            #     config_commands.insert(2, 'switchport trunk encapsulation dot1q')

            if mode == 'access':
                config_commands.insert(3,f'no switchport access vlan {re_vlan_id}')

            if re_access_vlan:  
                config_commands.insert(3, f'no switchport trunk allow vlan {re_access_vlan}') 

            output = net_connect.send_config_set(config_commands)
        net_connect.disconnect()

        return render_template('configure_interface.html', output=output, interface_list=interface_list)

    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
