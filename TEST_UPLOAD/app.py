from flask import Flask, request, render_template, redirect, url_for
from netmiko import ConnectHandler

app = Flask(__name__)
app.secret_key = 'SeCreT_Key'
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.21',
    'username': 'cisco',
    'password': 'cisco'
}

@app.route('/')
def index():
    return render_template('command.html')  

@app.route('/upload', methods=['POST'])
def upload_file():
    global device

    try:

        if not device:
            return "No device"
        
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        
        if file.filename == '':
            return "No selected file"
        
        # อ่านคำสั่งจากไฟล์ที่อัปโหลด
        commands = file.read().decode('utf-8').splitlines()
        for i in device:
            net_connect = ConnectHandler(**device)
            output = net_connect.send_config_set(commands)

        return render_template('command.html', output=output)  



    except Exception as err:
        print(f"Error: {str(err)}")

if __name__ == '__main__':
    app.run(debug=True)

   