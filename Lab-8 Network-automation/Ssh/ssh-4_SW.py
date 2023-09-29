from netmiko import ConnectHandler

device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.21',
    'username': 'cisco',
    'password': 'cisco',
}

# เชื่อมต่อ SSH ไปยังอุปกรณ์
try:
    net_connect = ConnectHandler(**device)
    net_connect.enable()  # เข้าสู่โหมด enable

    # ส่งคำสั่งการกำหนดค่า
    config_commands = ['exit','show run']
    output = net_connect.send_config_set(config_commands)

    # ออกจากอุปกรณ์ SSH
    net_connect.disconnect()

    print(output) # print output

except Exception as e:
    print(f"เกิดข้อผิดพลาด: {str(e)}")