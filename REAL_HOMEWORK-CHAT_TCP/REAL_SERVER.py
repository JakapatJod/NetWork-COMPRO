import socket
import threading
import datetime
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

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
        print(Fore.GREEN+f"[STATUS] {ip_client}:{client_address[1]} connected as {username} in {room} at {get_time}"+Style.RESET_ALL)
        
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    print(Fore.RED+f"[STATUS] {client_address} disconnected from room {room}"+Style.RESET_ALL)
                    break

                if message.lower() == "leave":
                    print(Fore.YELLOW+f"[STATUS] {username} IP {client_address} has been left the room {room} at {time}"+Style.RESET_ALL)
                    self.send_to_room(Fore.YELLOW+f"{username} has been left the room at {time}"+Style.RESET_ALL, room)
                    self.send_to_room("")
                    self.remove_client(client_socket, room)
                    self.handle_client(client_socket, client_address, username, room)
                

                if message.lower() == "exit":
                    print(Fore.RED+f"[STATUS] {username} IP {client_address} has been left the program at {time}"+Style.RESET_ALL)
                    self.send_to_room(Fore.RED+f"{username} has been left the program at {time}"+Style.RESET_ALL, room)
                    self.remove_client(client_socket, room)
                    self.send_to_client(Fore.RED+"You has been exit the chat."+Style.RESET_ALL, client_socket)
                    client_socket.close()
                    return

                for client, r in self.rooms[room]:
                    if client != client_socket:
                        try:
                            client.send(f"{username} : {message}".encode('utf-8'))
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

            self.send_to_room(Fore.GREEN+f"{username} has joined "+Style.RESET_ALL, room)

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address, username, room))
            client_thread.start()

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.main()