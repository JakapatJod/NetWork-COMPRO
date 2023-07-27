import socket

host = "10.4.15.120"
port = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(b"Hello World TEACHER BOY")
    data = s.recv(1024)

print("Received response: "+ repr(data))