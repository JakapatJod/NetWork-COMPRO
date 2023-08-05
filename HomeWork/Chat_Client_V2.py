import socket
import threading

username = input('Choose a Username: ')

HOST = 'localhost'
PORT = 5000
BUFSIZE = 4096
ADDRESS = (HOST, PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(username.encode('ascii'))
            else:
                print(message)
        except:
            print('An error occurred!')
            client.close()
            break

def write():
    while True:
        message = f'{username}: {input("")}'
        client.send(message.encode('ascii'))
    
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()