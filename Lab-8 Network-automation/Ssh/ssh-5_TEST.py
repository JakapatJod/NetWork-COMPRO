from netmiko import ConnectHandler

def connect_to_device(ip, username, password):
    device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password,
    }

    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        return net_connect
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {str(e)}")
        return None

def find_and_configure_port(net_connect, port_name, new_ip, mask):
    try:
        # ส่งคำสั่ง show interfaces status
        output = net_connect.send_command('show interfaces status')

        # ค้นหาชื่อพอร์ต
        if port_name in output:
            print(f"พอร์ต {port_name} พร้อมใช้งาน")

            # ส่งคำสั่งการกำหนดค่า IP
            config_commands = [
                f'configure terminal',
                f'interface {port_name}',
                f'ip address {new_ip} {mask}',
                'no shutdown',
                'exit',
                'exit',
            ]
            output = net_connect.send_config_set(config_commands)
            print(f"ทำการกำหนดค่า IP สำเร็จ")
        else:
            print(f"ไม่พบข้อมูลสำหรับพอร์ต {port_name}")

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {str(e)}")

def main():
    ip = '192.168.1.21'
    username = 'cisco'
    password = 'cisco'
    port_name = 'GigabitEthernet0/2'  # แก้ตามที่ต้องการ
    new_ip = '192.168.1.100'
    mask = '255.255.255.0'

    net_connect = connect_to_device(ip, username, password)
    if net_connect:
        find_and_configure_port(net_connect, port_name, new_ip, mask)
        net_connect.disconnect()

if __name__ == "__main__":
    main()
