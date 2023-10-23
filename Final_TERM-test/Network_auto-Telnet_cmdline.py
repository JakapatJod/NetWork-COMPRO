import telnetlib

def telnet_connect(ip, username, password):
    try:
        tn = telnetlib.Telnet(ip)
        tn.read_until(b"Username: ")
        tn.write(username.encode('ascii') + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
        return tn
    except Exception as e:
        print("An error occurred: " + str(e))
        return None

def send_command(tn, cmd):
    try:
        tn.write(cmd.encode('ascii') + b"\n")
        output = tn.read_until(b"#", timeout=5)
        return output.decode('ascii')
    except Exception as e:
        print("An error occurred: " + str(e))
        return None

ip = '192.168.1.21'
username = 'cisco'
password = 'cisco'

try:
    tn = telnet_connect(ip, username, password)

    if tn is not None:
        while True:
            try:
                cmd = input("$>")
                if cmd == "leave":
                    break

                if cmd.strip().lower() == "configure terminal":
                    tn.write(b"configure terminal\n")
                    tn.read_until(b"#")
                else:
                    output = send_command(tn, cmd)
                    if output:
                        print(output)
            except KeyboardInterrupt:
                break
    else:
        print("Failed to establish Telnet connection.")

except Exception as err:
    print(f"Error: {str(err)}")

finally:
    try:
        tn.close()
    except NameError:
        pass
