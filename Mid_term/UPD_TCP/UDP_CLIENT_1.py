import socket

host = "127.0.0.1"
port = 8000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"Hello World to UDP", (host, port))
    data, addr = s.recvfrom(1024)

print("Received response: " + repr(data))