import paramiko

hostname = '192.168.16.128'
username = 'jakapat'
passwd = 'jakapat12'
port = 22 # ssh

try:
    p = paramiko.Transport((hostname,port))
    p.connect(username=username,password=passwd)

    print("[*] Connected to "+ hostname + "via SSH")
    stfp = paramiko.SFTPClient.from_transport(p)
    print("[*] Starting file download")
    stfp.get("/home/jakapat/test.txt","/Users/admin/Downloads/d.txt") # get = download ระบุ path เครื่องคอมตัวเองกับ path ใน linux
    print("[*] File download complete")
    print("[*] Starting file upload")
    stfp.put("/Users/admin/Downloads/d.txt","/home/jakapat/u.txt") # put = upload
    print("[*] File download complete")
    p.close()
    print("[*] Disconnected from server")

except Exception as err:
    print("[!] "+ str(err))
