from socket import *

s = socket(AF_INET,SOCK_DGRAM) # Create datagram socket

s.bind(("",10000)) # ระบุเลข port 

while True:
    data , addr = s.recvfrom(maxsize) # รอ message

    resp = "Get off my lawn!"
    s.sendto(resp,addr)         # Send reponse
    
    # ไม่มีการ เชื่อมต่อกัน NO ' Connection '
    # เป็นการส่ง และ รับ ของ packet