import telnetlib

username = 'cisco'
password = 'cisco'

for n in range (170,172):
    IP = "10.4.15." + str(n)

    tn = telnetlib.Telnet(IP)

    tn.read_until(b'Username: ')
    tn.write(username.encode('ascii') + b'\n')

    if password:
        tn.read_until(b'Password: ')
        tn.write(password.encode('ascii') + b'\n')

    tn.write(b'enable \n')
    tn.write(b'conf t \n')

    for n in range(2,10):
        tn.write(b'vlan ' + str(n).encode('ascii') + b'\n')
        tn.write(b'name Python_VLAN_' + str(n).encode('ascii') + b'\n')
    
    tn.write(b'end \n')
    tn.write(b'exit \n')

    print(tn.read_all().decode('ascii'))