from socket import *
s = socket(AF_INET,SOCK_DGRAM) # Create datagram socket

msg  = "Hello World"
s.sendto(msg,("server.com",10000)) # Send a message

data , addr = s.recvfrom(maxsize) # wait for a response
# data is returned data -------- , addr is remote address

# concept คือ No ' Connection'
# You just send a data packet