import socket

host = "10.4.15.120"
port = 5001

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"Hello World to UDP", (host, port))
    data, addr = s.recvfrom(1024)

print("Received response: " + repr(data))