# Echo Client program
import socket
import sys

HOST = '10.4.15.120'               # The remote host
PORT = 8000                        # The same port as used by the server
s = None
for res in socket.getaddrinfo(HOST,PORT,socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0 ,socket.AI_PASSIVE):
    af,socktype , proto , canonname , sa = res
    try:
        s = socket.socket(af,socktype,proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.connect(sa) # เชื่อมต่อกับ เซิฟเวอร์
    except: 
        s.close()
        s = None
        continue
    break
if s is None:
    print('Could not open socket')
    sys.exit(1)
with s:
    s.sendall(b'Hello, world')
    s.sendall(b'Hello, python')

    data = s.recv(1024)
 
print('Received',repr(data))
