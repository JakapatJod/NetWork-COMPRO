import socket
import threading


def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print( "Connection to server lost.")
                break
            print(message)
            
        except Exception as error:
            print( f"Error: {error}")
            break

def main():
    server_ip = 'localhost'
    server_port = 80

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, server_port))
    except Exception as error:
        print( f"Error connecting to the server: {error}")
        return

    NAME = input("Enter your username: ")

    while True:
        print("")
        print("You can create a room or type 'exit' to quit")
        print("")

        room = input("Enter the room name: ")

        if room.lower() == "exit":
            client.send(room.encode('utf-8'))
            print( "You have exited the server.")
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
                print( "You have exited the chat.")
                receive_thread.join()
                client.close()
                return
            elif message.lower() == "leave":
                client.send(message.encode('utf-8'))
                print(f"{NAME} left the chat")
                client.close()
                receive_thread.join()
                main()
                return
            else:
                print(f"{room} - {NAME} sent message: {message}")
                client.send(message.encode('utf-8'))

if __name__ == "__main__":
    main()
