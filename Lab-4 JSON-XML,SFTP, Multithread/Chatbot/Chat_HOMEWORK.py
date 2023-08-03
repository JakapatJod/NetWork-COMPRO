from socket import *
from threading import Thread

HOST = 'localhost'
PORT = 5000
BUFSIZE = 4096
ADDRESS = (HOST, PORT)

server = socket(AF_INET, SOCK_STREAM)
server.connect(ADDRESS)

messageFromServer = bytes.decode(server.recv(BUFSIZE))
print(messageFromServer)

name = input('Enter your name: ')
userName = str.encode(name)
server.send(userName)

def receive_messages():
    while True:
        receiveMessage = bytes.decode(server.recv(BUFSIZE))
        if not receiveMessage:
            print('Server disconnected')
            break
        print(receiveMessage)

receive_thread = Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

while True:
    sendMessage = input('> ')
    if not sendMessage:
        print('Server disconnected')
        break
    server.send(str.encode(sendMessage))

server.close()