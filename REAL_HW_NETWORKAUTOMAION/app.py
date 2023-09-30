from flask import Flask, request, session, redirect, url_for, render_template, flash , request
from netmiko import ConnectHandler
import re # import regex

app = Flask(__name__)
app.secret_key = 'SeCreT_Key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')

# ================================= # การใส่ ssh เข้าสู่ตัวเครื่อง

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        ip = request.form['ipaddress']
        username = request.form['username']
        password = request.form['password']

        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password
        }

        session['device'] = device

        return redirect("command")
    
    if 'device' not in session:
        flash('no device')
    
    return render_template('login.html')

# =====================================================


# =========================================== เปิดตัวหน้า command

@app.route('/command')
def command():
    return render_template('command.html')

# =====================================================


# ===================================================== หน้าโชว์ running config 
@app.route('/showrun', methods=['POST'])
def show_run():
    device = session.get('device')

    if not device:
        return "no device"

    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        config_commands = ['exit', 'show run']
        output = net_connect.send_config_set(config_commands)

        net_connect.disconnect()

        return render_template('show_result.html', output=output)

    except Exception as e:
        return f"error: {str(e)}"
# =====================================================

# ===================================================== หน้าโชว์ show ip interface brief
@app.route('/showipinterface', methods=['GET', 'POST'])
def show_ip_interface():
    device = session.get('device')

    if not device:
        return "no device"

    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        config_commands = ['exit', 'show ip interface brief']
        output = net_connect.send_config_set(config_commands)

        net_connect.disconnect()

        return render_template('show_result.html', output=output)

    except Exception as e:
        return f"error: {str(e)}"
# =====================================================

# ===================================================== เปลี่ยนชื่อ device hostname
@app.route('/device_name', methods=['POST'])
def device_name():
    device = session.get('device')
    if not device:
        return "no device"
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        device_name = request.form.get('device-name')

        # คำสั่งการกำหนดค่า VLAN
        config_commands = [
            f'hostname {device_name}',
            'exit'
        ]

        output = net_connect.send_config_set(config_commands)

        net_connect.disconnect()

        return render_template('show_result.html', output=output)

    except Exception as e:
        return f"error: {str(e)}"
# =====================================================


# ===================================================== show VLAN
@app.route('/showvlan', methods=['POST'])
def show_vlan():
    device = session.get('device')

    if not device:
        return "no device"

    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        config_commands = ['exit', 'show vlan']
        output = net_connect.send_config_set(config_commands)

        net_connect.disconnect()

        return render_template('show_result.html', output=output)

    except Exception as e:
        return f"error: {str(e)}"
    
# =====================================================



# ===================================================== config vlan
@app.route('/configure_vlan', methods=['POST'])
def configure_vlan():
    device = session.get('device')
    if not device:
        return "no device"
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        vlan_id = request.form.get('vlan_id')
        vlan_name = request.form.get('vlan_name')

        # คำสั่งการกำหนดค่า VLAN
        config_commands = [
            f'vlan {vlan_id}',
            f'name {vlan_name}',
            'end', 'show vlan'
        ]

        output = net_connect.send_config_set(config_commands)

        net_connect.disconnect()

        return render_template('configure_vlan.html', output=output)

    except Exception as e:
        return f"error: {str(e)}"
# =====================================================



# ===================================================== หน้าใช้ คำสั่ง no VLAN
@app.route('/delete_vlan', methods=['POST'])
def delete_vlan():

    device = session.get('device')

    if not device:
        return "no device"

    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        vlan_id_to_delete = request.form.get('vlan_id_to_delete')

        config_commands = [
            f'no vlan {vlan_id_to_delete}','end', 'show vlan'
        ]

        output = net_connect.send_config_set(config_commands)

        net_connect.disconnect()

        return render_template('configure_vlan.html', output=output)

    except Exception as e:
        return f"error: {str(e)}"
# =====================================================




# ===================================================== หน้าใช้ insert ip address

@app.route('/interface_port', methods=['GET', 'POST'])
def interface_port():
    device = session.get('device')

    if not device:
        return "no device"


    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        config_commands = ['exit', 'show ip interface brief']
        output = net_connect.send_config_set(config_commands)

        lines = output.splitlines()
        interface_list = []

        for line in lines: 
            match = re.match(r'^([A-Za-z]+\d+/\d+/\d+|[A-Za-z]+\d+/\d+|[A-Za-z]+\d+)', line) # นำ regex มาเพื่อคัดหาคำ ว่า Interface จากทั้งหมดของ show ip interface brief 
            if match:
                interface = match.group(1)
                if not re.match(r'^(SW|Router|R|Switch)', interface, re.IGNORECASE):
                    interface_list.append(interface)

        print(interface_list)
        interface_name = request.form.get('interface')
        new_ip = request.form.get('new_ip')
        new_subnet = request.form.get('new_subnetmask')


        print(f'Interface Name: {interface_name}')

        if interface_name and new_ip:   
            config_commands = [
                f'interface {interface_name}',
                'no sw',
                f'ip address {new_ip} {new_subnet}','no shutdown',
                'end','show ip interface brief'
            ]
            output = net_connect.send_config_set(config_commands)
        net_connect.disconnect()

        return render_template('interface_port.html', output=output, interface_list=interface_list)

    except Exception as e:
        return f"error: {str(e)}"
    
# ===================================================== remove ip address

@app.route('/remove_port', methods=['GET', 'POST'])
def remove_port():
    device = session.get('device')

    if not device:
        return "no device"


    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        config_commands = ['exit', 'show ip interface brief']
        output = net_connect.send_config_set(config_commands)

        lines = output.splitlines()
        interface_list = []

        for line in lines: 
            match = re.match(r'^([A-Za-z]+\d+/\d+/\d+|[A-Za-z]+\d+/\d+|[A-Za-z]+\d+)', line) # นำ regex มาเพื่อคัดหาคำ ว่า Interface จากทั้งหมดของ show ip interface brief 
            if match:
                interface = match.group(1)
                if not re.match(r'^(SW|Router|R|Switch)', interface, re.IGNORECASE):
                    interface_list.append(interface)

        print(interface_list)
        interface_name = request.form.get('interface')
        re_ip = request.form.get('remove_ip')
        re_subnet = request.form.get('remove_subnetmask')


        print(f'Interface Name: {interface_name}')

        if interface_name and re_ip:   
            config_commands = [
                f'interface {interface_name}',
                f'no ip address {re_ip} {re_subnet}','shutdown','sw',
                'end','show ip interface brief'
            ]
            output = net_connect.send_config_set(config_commands)
        net_connect.disconnect()

        return render_template('interface_port.html', output=output, interface_list=interface_list)

    except Exception as e:
        return f"error: {str(e)}"


# ===================================================== การทำ ip route กับ ลบ ip route
@app.route('/ip_route', methods=['POST'])
def ip_route():
    device = session.get('device')

    if not device:
        return "no device"

    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        ip_network = request.form.get('ip_network')
        subnetmask = request.form.get('subnetmask')
        next_hop = request.form.get('next_hop')

        add_routing = request.form.get('add_routing')  

        config_commands = [f'ip route {ip_network} {subnetmask} {next_hop}','exit', 'show ip route'] # array
        if add_routing == 'yes': # ถ้าติ๊กถูกจะเพิ่มคำ ip routing
            config_commands.insert(1, 'ip routing')




        output = net_connect.send_config_set(config_commands)

        net_connect.disconnect()

        return render_template('ip_routing.html', output=output )

    except Exception as e:
        return f"error: {str(e)}"
    
# ===================================================== ตำสั่งลบ ip route

@app.route('/removeiproute', methods=['POST'])
def remove_route():
    device = session.get('device')

    if not device:
        return "no device"

    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        ip_network = request.form.get('ip_network')
        subnetmask = request.form.get('subnetmask')
        next_hop = request.form.get('next_hop')

        add_routing = request.form.get('add_routing')  

        remove_commands = [f'no ip route {ip_network} {subnetmask} {next_hop}','exit', 'show ip route']
        if add_routing == 'yes': # ถ้าติ๊กถูกจะทำการลบคำ ip routing
            remove_commands.insert(1, 'no ip routing')


        output = net_connect.send_config_set(remove_commands)

        net_connect.disconnect()

        return render_template('ip_routing.html', output=output )

    except Exception as e:
        return f"error: {str(e)}"
    


if __name__ == '__main__':
    app.run(debug=True)