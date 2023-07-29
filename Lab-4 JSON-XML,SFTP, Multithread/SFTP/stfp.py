import paramiko

hostname = '192.168.123.25'
username = 'watcharachai'
passwd = 'password'
port = 22

try:
    p = paramiko.Transport((hostname,port))
    p.connect(username=username,password=passwd)

    print("[*] Connected to "+ hostname + "via SSH")
    stfp = paramiko.SFTPClient.from_transport(p)
    print("[*] Starting file download")
    stfp.get("/home/watcharachai/text.txt","/Users/watcharachai/Downloads/d.txt")
    print("[*] File download complete")
    print("[*] Starting file upload")
    stfp.put("/Users/watcharachai/Downloads/d.txt","/home/watcharachai/u.txt")
    print("[*] File download complete")
    p.close()
    print("[*] Disconnected from server")

except Exception as err:
    print("[!] "+ str(err))
