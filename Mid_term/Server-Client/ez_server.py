import socket
import threading

clients = []  # เก็บเคลียนต์ที่เชื่อมต่อเข้ามา

def handle_client(client_socket, username):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                remove_client(client_socket)
                break
            message_with_username = f"{username}: {message}"  # เพิ่มชื่อผู้ใช้งานในข้อความ
            print(message_with_username)
            broadcast(message_with_username)
        except:
            remove_client(client_socket)
            break

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))  # ส่งข้อความไปยังแต่ละ client
        except:
            continue

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # สร้าง socket สำหรับการเชื่อมต่อ
    server_socket.bind((host, port))  # ผูก socket กับที่อยู่และพอร์ต
    server_socket.listen(5)  # รอการเชื่อมต่อ
    print("Chat server listening on {}:{}".format(host, port))

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print("Connection established with {}:{}".format(addr[0], addr[1]))

        client_socket.send("Enter your username: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        print(f"{addr[0]}:{addr[1]} chose the username: {username}")
        
        client_handler = threading.Thread(target=handle_client, args=(client_socket, username))
        client_handler.start()

if __name__ == "__main__":
    main()