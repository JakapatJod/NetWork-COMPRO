import socket
import threading

host = "127.0.0.1"
port = 8000

def handle_client(data, addr, server_socket):
    print("Received '{}' from client at {}:{}".format(data.decode('utf-8'), addr[0], addr[1])) # โชว์ข้อความ
    server_socket.sendto(data, addr)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        print("UDP server is listening on {}:{}".format(host, port))
        
        while True:
            data, addr = s.recvfrom(1024)
            if not data:
                break
            
            client_thread = threading.Thread(target=handle_client, args=(data, addr, s))
            client_thread.start()

if __name__ == "__main__":
    main()
