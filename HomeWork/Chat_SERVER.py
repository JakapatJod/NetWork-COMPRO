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
    

    def broadCastingMessage(self, activeClient ,message):
        for socket in CONNECTIONS_LIST:
            if socket != server and socket != activeClient:
                try:
                    broadcastMessage = str.encode(message)
                    socket.send(broadcastMessage)
                except:
                    print('Client (%s) is offline'% self._address)
                    broadCastingMessage(socket,('Client (%s) is offline'%self._address))
                    socket.close()
                    CONNECTIONS_LIST.remove(socket)
    def run(self):
        self._client.send(str.encode('Welcome to the chat room'))
        self._name = bytes.decode(self._client.recv(BUFSIZE))        

        allMessage = self._record.getMessage(0)
        self._client.send(str.encode(allMessage))
        while True:
            message = bytes.decode(self._client.recv(BUFSIZE))
            if not message:
                print('Client disconnected')
                self._client.close()
                CONNECTIONS_LIST.remove(self._client)
            else:
                message = self._name+' : ' + message
                self._record.addMessage(message)
                
                threadLock.acquire()
                self.broadCastingMessage(self._client,message)
                threadLock.release()

def displayChatRecord(record):
    while True:
        sleep(10)  
        print("\n===== Chat Record =====")
        allMessages = record.getMessage(0)
        print(allMessages)
        print("=======================\n")

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

display_thread = Thread(target=displayChatRecord, args=(record,))
display_thread.daemon = True 
display_thread.start()

while True:
    print('Waiting for connection...')
    client, address = server.accept()
    print(' ...Connnected from : ',address )

    threadLock.acquire()
    CONNECTIONS_LIST.append(client)
    # Release CONNECTIONS_LIST
    threadLock.release()
    handler  = clientHandler(client,record,address)

    handler.start() 