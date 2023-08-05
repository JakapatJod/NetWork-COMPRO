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

exiting = False

def receive_messages():
    global exiting  
    while not exiting:  
        receiveMessage = bytes.decode(server.recv(BUFSIZE))
        if not receiveMessage:
            print('Server disconnected')
            break
        print(receiveMessage)

receive_thread = Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

try:
    while True:
        sendMessage = input('')
        if sendMessage == 'quit':
            leave_message = f'{name} left from server!!'
            server.send(str.encode(leave_message))
            print('You have left the server.')
            exiting = True  
            break
        server.send(str.encode(sendMessage))
except KeyboardInterrupt:
    print('You have left the server (Ctrl+C)')
    leave_message = f'{name} left from server!!'
    server.send(str.encode(leave_message))
    exiting = True  

receive_thread.join()  
server.close()
