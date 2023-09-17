import socket
import threading
from colorama import init as colorama_init
from colorama import Fore, Style

def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(Fore.RED + "Connection to server lost." + Style.RESET_ALL)
                break
            print(message)
        except Exception as error:
            print(Fore.RED + f"Error: {error}" + Style.RESET_ALL)
            break

def main():
    colorama_init(autoreset=True)
    server_ip = 'localhost'
    server_port = 80

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, server_port))
    except Exception as error:
        print(Fore.RED + f"Error connecting to the server: {error}" + Style.RESET_ALL)
        return

    NAME = input("Enter your username: ")

    while True:
        print("")
        print("You can create a room or type 'exit' to quit")
        print("")

        room = input("Enter the room name: ")

        if room.lower() == "exit":
            client.send(room.encode('utf-8'))
            print(Fore.RED + "You have exited the server." + Style.RESET_ALL)
            client.close()
            break

        print("")
        print("You can create a room or type 'leave' to leave room")
        print("")

        client.send(NAME.encode('utf-8'))
        client.send(room.encode('utf-8'))

        receive_thread = threading.Thread(target=receive_message, args=(client,))
        receive_thread.start()

        while True:
            message = input("")

            if message.lower() == "exit":
                client.send(message.encode('utf-8'))
                print(Fore.RED + "You have exited the chat." + Style.RESET_ALL)
                receive_thread.join()
                client.close()
                return
            elif message.lower() == "leave":
                client.send(message.encode('utf-8'))
                print(Fore.YELLOW + f"{NAME} left the chat" + Style.RESET_ALL)
                client.close()
                receive_thread.join()
                main()
                return
            else:
                print(Fore.GREEN + f"{room} - {NAME} sent message: {message}" + Style.RESET_ALL)
                client.send(message.encode('utf-8'))

if __name__ == "__main__":
    main()
