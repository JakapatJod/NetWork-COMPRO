import socket
import threading

host = "127.0.0.1"
port = 8081

def handle_client(conn, addr):
    print("Client connected: " + str(addr))
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)
    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print("Server started on {}:{}".format(host, port))

    clients = []

    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
        clients.append(client_thread)
        
        if len(clients) >= 2:
            break

    for client_thread in clients:
        client_thread.join()