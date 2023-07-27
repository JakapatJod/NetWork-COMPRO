import socket
# Echo Client program

HOST = '10.4.15.120'                       # Symbolic name meaning all availble interface
PORT = 8000                    # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(b'Hello , world')
    data = s.recv(1024)
print('Received', repr(data))