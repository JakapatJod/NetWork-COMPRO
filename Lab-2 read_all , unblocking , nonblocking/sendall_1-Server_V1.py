import socket
# Echo server program

HOST = '10.4.15.120'                       # Symbolic name meaning all availble interface
PORT = 50007                    # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by',addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            conn.sendall(data)

