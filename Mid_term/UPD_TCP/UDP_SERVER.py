import socket

host = "127.0.0.1"
port = 8081

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((host, port))
    print("UDP server is listening on {}:{}".format(host, port))
    while True:
        data, addr = s.recvfrom(1024)
        if not data:
            break
        print("Received data from client at {}:{}".format(addr[0], addr[1]))
        s.sendto(data, addr)
