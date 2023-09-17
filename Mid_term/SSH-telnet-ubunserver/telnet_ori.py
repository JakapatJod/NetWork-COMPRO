import getpass
import telnetlib

HOST = "192.168.182.128"
user = input("Enter you remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b'login: ')
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b'Password: ')
    tn.write(password.encode('ascii') + b"\n")


tn.write(b'ls\n')
tn.write(b'mkdir TEST2\n')
tn.write(b'exit\n')

print(tn.read_all().decode('ascii'))