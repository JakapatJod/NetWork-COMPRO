import paramiko
import threading
import os.path
import subprocess
import time
import sys
import re

#Checking IP Address file and content validity
def ip_is_valid():
    check = False
    global ip_list

    while True:
        # Prompting user for input
        print('\n--------------------------------------\n')
        ip_file = input('# Enter IP file name and extension: ')
        print('\n--------------------------------------\n')

        # Changing exception message
        try:
            # Open user selected file for reading (IP address file)
            selected_ip_file = open(ip_file,'r')

            # Starting from the beginning of the file
            selected_ip_file.seek(0)
            
            # Reading each line (IP address) in the file
            ip_list = selected_ip_file.readlines()

            # Closing the file
            selected_ip_file.close()
        
        except FileNotFoundError as e:
            print('=== Found Python Traceback Cause: -->',e)
            print('\n=== File %s does not exits! Please check and try again!\n'%ip_file)
        
        # Checking octets
        try:
            for ip in ip_list:
                a = ip.rsplit().split('.')

                if (len(a) == 4) and (1 <= int(a[0]) <= 223) and (int(a[0]) !=127) and (int(a[0]) !=169) or int(a[1] != 254) and (0 <= int(a[1]) <= 255
                and 0 <= int(a[2]) <= 255 and 0 <= int(a[3]) <= 255):
                    print('The current IP Address to verify: ',a)
                    check = True
                    continue
                else:
                    print('The current IP address to verify: ',a)
                    print('\n There was an INVALID IP address! Please check and try again!\n')
                    check = False
                    break
        except NameError:
            continue

        # Evaluating the 'check' flag
        if check == False:
            print('Go to While loop\n')
            continue
        elif check == True:
            print("\nAll IP Address in 'ssh-ip.txt' file are valid")
            break

        # Checking IP reachability
        print("\n* Checking IP reachability. Please wait...\n")

        check2 = False

        while True:
            for ip in ip_list:
                ping_reply = subprocess.call(['ping','-n','-c','2','-W','1',ip])

                if ping_reply == 0:
                    check2 = True
                    continue

                elif ping_reply == 2:
                    print('\n*No response from device %s'%ip)
                    check2 = False
                    break
                else:
                    print('\n* Ping to the following device has FAILED: ',ip)
                    check2 = False
                    break

            # Evaluating the 'check' flag
            if check2 == False:
                print('* Please re-check IP address list or device.\n')
                ip_is_valid()
            
            elif check2 == True:
                print('\n* All devices are reachable. Waiting for username/password file....\n')
                break
# Checking user file validity
def user_is_valid():
    global user_file

    while True:
        print('\n========================================\n')
        ip_file = input('# Enter user/pass file name and extension: ')
        print('\n========================================\n')

        # Changing output messages
        if os.path.isfile(user_file) == True:
            print('\n* Username/password file has been validated. Waiting for command file...')
            break

        else:
            print('\n* File %s does not exist! Please check and try again!\n' % user_file)
            continue
