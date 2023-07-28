import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost',1234))
sock.setblocking(0) # คือ Non_Blocking

data = 'footbar\n' * 10 *1024 *1024 # 70 MB of data
sent = sock.send(data.encode())  # ต้องแปลงเป็น encode

assert sent == len(data),'%s != %s' (sent,len(data))