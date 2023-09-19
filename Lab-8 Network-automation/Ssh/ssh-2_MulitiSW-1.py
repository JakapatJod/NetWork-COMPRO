from netmiko import ConnectHandler

SW4 = {
    'device_type':'cisco_ios',
    'ip':'192.168.1.120',
    'username':'cisco',
    'password':'cisco'
}

SW5 = {
    'device_type':'cisco_ios',
    'ip':'192.168.1.121',
    'username':'cisco',
    'password':'cisco'
}

all_devices =  [SW4,SW5]

for devices in all_devices:
    net_connect = ConnectHandler(**devices)
    for n in range(2,10):
        print(b'Creating VLAN ' + str(n).encode('ascii'))
        config_command = ['vlan' + str(n),'name Python_VLAN ' + str(n)]
        output = net_connect.send_config_set(config_command)
        print(output)