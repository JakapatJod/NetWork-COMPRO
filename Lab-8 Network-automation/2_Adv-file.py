import paramiko
import time

HOST = '192.168.1.122'
user = 'cisco'
password = 'cisco'

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=HOST, username=user, password=password, allow_agent=False,look_for_keys=False)

print('Successful connected to: '+ HOST)

remoter_connection = ssh_client.invoke_shell()
remoter_connection.send('en\n')
remoter_connection.send('show ip int brief\n')
time.sleep(1)

output = remoter_connection.recv(65535)
print(output.decode('ascii'))

ssh_client.close()