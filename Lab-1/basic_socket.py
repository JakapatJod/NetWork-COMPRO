import socket

try:
    print("Fully qualified domain name " + socket.getfqdn("8.8.8.8"))
    print("Host name to IP address: " + socket.gethostbyname("www.python.org"))
    print("Get host name of local machine: " + str(socket.gethostbyname_ex("www.python.org")))
    print("Get host name of local machine: "+ socket.gethostbyname())
except Exception as err:
    print("Error: "+str(err))