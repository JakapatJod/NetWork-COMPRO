from socket import *
from chatDatabase import chatRecord
from threading import Thread
import threading
from time import ctime,sleep


class clientHandler(Thread):
    def __init__(self,client,record,address):
        Thread.__init__(self)
        self._client = client
        self._record = record
        self._address = address
    

    def broadCastingMessage(self, activeClient, message):
        if message.startswith('quit'):
            self._record.addMessage(message)  # Add the "quit" message to the chat record
        else:
            for socket in CONNECTIONS_LIST:
                if socket != server and socket != activeClient:
                    try:
                        broadcastMessage = str.encode(message)
                        socket.send(broadcastMessage)
                    except:
                        print(f'Client {self._address} is offline')
                        self.broadCastingMessage(socket, f'Client {self._address} is offline')
                        socket.close()
                        CONNECTIONS_LIST.remove(socket)
    def run(self):
        self._client.send(str.encode('Welcome to the chat room'))
        self._name = bytes.decode(self._client.recv(BUFSIZE))   

        print(ctime(),f'{self._address} {self._name}','Connect Server')
        
        allMessage = self._record.getMessage(0)
        self._client.send(str.encode(allMessage))
        try:
            while True:
                message = bytes.decode(self._client.recv(BUFSIZE))
                if not message:
                    print(ctime(),f' {self._address} {self._name} leave Server')
                    break 
                else:
                    message = self._name+' : ' + message
                    self._record.addMessage(message)
                    
                    threadLock.acquire()
                    self.broadCastingMessage(self._client,message)
                    threadLock.release()
        except ConnectionResetError:
            print(f'Client ({self._address}) forcibly closed the connection')
            
        leave_message = f'{self._name} left from server!!'
        self._record.addMessage(leave_message)
        threadLock.acquire()
        self.broadCastingMessage(self._client, leave_message)
        threadLock.release()
        
        self._client.close()
        CONNECTIONS_LIST.remove(self._client)


HOST = 'localhost'
PORT = 5000
BUFSIZE = 4096
ADDRESS = (HOST, PORT) 
CONNECTIONS_LIST = []
# Creating Threads Synchronization
threadLock = threading.Lock()
record = chatRecord()

server = socket(AF_INET,SOCK_STREAM)
server.bind(ADDRESS)
server.listen(10)

# Add server socket to the list
CONNECTIONS_LIST.append(server)
print('Chat server started on port ' + str(PORT))


while True:

    print('Waiting for connection...')
    client, address = server.accept()

    threadLock.acquire()
    CONNECTIONS_LIST.append(client)
    threadLock.release()
    handler  = clientHandler(client,record,address)

    
    handler.start() 