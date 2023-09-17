import poplib
from email.message import EmailMessage

server = "192.168.182.128"
user = "jakapat"
passwd = "jakapat12"

server = poplib.POP3(server)
server.user(user)
server.pass_(passwd)

msgNum = len(server.list()[1])

for i in range(msgNum):
    for msg in server.retr(i+1)[1]:
        print(msg.decode('utf-8', errors='ignore'))
