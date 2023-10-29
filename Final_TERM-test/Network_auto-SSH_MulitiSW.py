from netmiko import ConnectHandler

SW4 = {
    'device_type':'cisco_ios',
    'ip':'192.168.1.171',
    'username':'cisco',
    'password':'cisco'
}

SW5 = {
    'device_type':'cisco_ios',
    'ip':'192.168.1.172',
    'username':'cisco',
    'password':'cisco'
}

all_devices =  [SW4,SW5]

for devices in all_devices:
    net_connect = ConnectHandler(**devices)
    for n in range(2,10):
        config_command = ['show ip int bri' + str(n),'name Python_VLAN ' + str(n)]
        output = net_connect.send_config_set(config_command)
        print(output)