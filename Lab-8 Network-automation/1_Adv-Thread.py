import threading
from queue import Queue
from getpass import getpass
from netmiko import ConnectHandler

# Define username and password to login to all routers with
USER = 'cisco'
PASSWORD = 'cisco'

# Define router IPs, you could also make a dictionary imported from a CSV file, or create a list from a text of hostnames
routers = ['192.168.1.122','192.168.1.123','192.168.1.124']

def ssh_session(router,output_q):
    # Place what you want each thread to do here, for example connect to SSH , run a command , get output
    output_dict = {}
    hostname = router
    router = {'device_type':'cisco_ios','ip':router,'username': USER,'password':PASSWORD,'verbose':False}
    ssh_session = ConnectHandler(**router)
    output = ssh_session.send_command('show version')
    output_dict[hostname] = output
    output_q.put(output_dict)

if __name__ == '__main__':
    output_q = Queue()

    # Start thread for each router in router list
    for router in routers:
        my_thread = threading.Thread(target=ssh_session, args=(router, output_q))
        my_thread.start()
    
    # Wait for all threads to complete
    main_thread = threading.currentThread()
    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            some_thread.join()

    # Retrieve everything off the queue - l is the router IP, v is output
    # You could also write this to a file , or create a file for each router
    
    while not output_q.empty():
        my_dict = output_q.get()
        for k, val in my_dict.items():
            print(k)
            print(val)