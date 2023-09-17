import socket
import threading
import datetime

class ChatServer:
    def __init__(self):
        self.rooms = {}

    def receive_message(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(message)
                print("")
            except Exception as e:
                
                break
            finally:
                client_socket.close()

    def remove_client(self, client_socket, room):
        for client, r in self.rooms[room]:
            if client == client_socket:
                self.rooms[room].remove((client, r))
                break

    def send_to_room(self, message, room):
        for client, r in self.rooms[room]:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                self.remove_client(client, r)

    def send_to_client(self, message, client_socket):
        try:
            client_socket.send(message.encode('utf-8'))
            client_socket.close()
        except:
            client_socket.close()

    def handle_client(self, client_socket, client_address, username, room):
        ip_client = client_address[0]
        get_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[STATUS] {ip_client}:{client_address[1]} connected as {username} in {room} at {get_time}")
        
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    print(f"[STATUS] {client_address} disconnected from room {room}")
                    break

                if message.lower() == "leave":
                    print(f"[STATUS] {username} IP {client_address} has been left the room {room} at {time}")
                    self.send_to_room(+f"{username} has been left the room at {time}", room)
                    self.send_to_room("")
                    self.remove_client(client_socket, room)
                    self.handle_client(client_socket, client_address, username, room)
                

                if message.lower() == "exit":
                    print(f"[STATUS] {username} IP {client_address} has been left the program at {time}")
                    self.send_to_room(f"{username} has been left the program at {time}")
                    self.remove_client(client_socket, room)
                    self.send_to_client("You has been exit the chat.", client_socket)
                    client_socket.close()
                    return

                for client, r in self.rooms[room]:
                    if client != client_socket:
                        try:
                            client.send(f"{username} : {message}".encode('utf-8'))
                            print(f"[SERVER LOG] {username} to {r} : {message}" )  # โชว์ Log คุยกันระหว่าง client กับ client

                        except:
                            client.close()
                            self.remove_client(client, r)
                        
            except:
                break

        client_socket.close()

    def main(self):
        HOST = 'localhost'
        PORT = 80

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[STATUS] Wait connecting......")

        while True:
            client_socket, client_address = server.accept()
            username = client_socket.recv(1024).decode('utf-8')
            room = client_socket.recv(1024).decode('utf-8')

            username = f"{room} - {username}"

            if room not in self.rooms:
                self.rooms[room] = []

            self.rooms[room].append((client_socket, room))

            self.send_to_room(f"{username} has joined ", room)

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address, username, room))
            client_thread.start()

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.main()