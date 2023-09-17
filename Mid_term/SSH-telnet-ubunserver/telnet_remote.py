import getpass
import telnetlib

HOST = "192.168.182.128"
user = input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b'login: ')
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b'Password: ')
    tn.write(password.encode('ascii') + b"\n")

while True:
    s = input('Enter command: ')
    tn.write(f'{s}\n'.encode('ascii'))
    output = tn.read_very_eager()
    print(output.decode('utf-8', errors='ignore'))
