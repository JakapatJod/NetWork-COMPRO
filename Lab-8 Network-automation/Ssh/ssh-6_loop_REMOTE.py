from netmiko import ConnectHandler

device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.21',
    'username': 'cisco',
    'password': 'cisco',
    'port': 22,
}

try:
    net_connect = ConnectHandler(**device)
    net_connect.enable()  

    while True:
        try:
            cmd = input("$>")
            if cmd == "exit":
                break

            # Send the command and set the expected prompt
            if cmd.strip().lower() == "configure terminal":
                output = net_connect.config_mode()
            else:
                output = net_connect.send_command_timing(cmd)

            # Print the output
            print(output)
        except KeyboardInterrupt:
            break
        except Exception as err:
            print(f"Error: {str(err)}")

except Exception as err:
    print(f"Error: {str(err)}")

finally:
    try:
        # Exit configuration mode if needed before disconnecting
        if net_connect.check_config_mode():
            net_connect.exit_config_mode()

        net_connect.disconnect()
    except NameError:
        pass
