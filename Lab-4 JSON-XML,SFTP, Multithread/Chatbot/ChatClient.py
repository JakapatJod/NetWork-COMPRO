# Chat client for a multi-client chat room
from socket import *

HOST = 'localhost'
PORT = 5000
BUFSIZE  = 4096
ADDRESS = (HOST,PORT) # (127.0.0.1 , 50000)

server = socket(AF_INET,SOCK_STREAM)
server.connect(ADDRESS)
messageFromServer = bytes.decode(server.recv(BUFSIZE))
print(messageFromServer)
name = input('Enter you name: ')
userName = str.encode(name)
server.send(userName)

while True:
    receiveMessage = bytes.decode(server.recv(BUFSIZE))
    if not receiveMessage:
        print('Server disconnected')
        break

    print(receiveMessage)
    SendMessage = input('> ')
    if not SendMessage:
        print('Server disconnected')
        break
    server.send(str.encode(SendMessage))
server.close()