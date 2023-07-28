import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(('localhost',1234))

data = 'footbar\n' * 10 * 1024 * 1024 # 70 MB of data สร้างความยาวของข้อมูล ---- *1024 *1024 = 80MB ซึ่งมีขนาดเพียงพอสำหรับ 70 MB
encode = data.encode('utf-8') # ต้องแปลงเป็น encode
assert sock.send(encode) == len(encode) # True