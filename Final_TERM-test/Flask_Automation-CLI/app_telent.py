from flask import Flask, request, render_template, redirect, url_for
import telnetlib

app = Flask(__name__)

device_ip = '192.168.1.191'
device_username = 'cisco'
device_password = 'cisco'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/command-page')
def command_page():
    return render_template('command-page.html')

@app.route('/command', methods=['POST'])
def execute_command():
    try:
        cmd = request.form['command']

        tn = telnetlib.Telnet(device_ip)
        tn.read_until(b'Username: ', timeout=5)
        tn.write(device_username.encode('utf-8') + b'\n')
        tn.read_until(b'Password: ', timeout=5)
        tn.write(device_password.encode('utf-8') + b'\n')

        tn.read_until(b'#', timeout=5)
        tn.write(cmd.encode('utf-8') + b'\n')
        output = tn.read_until(b'#', timeout=5).decode('utf-8')

        tn.close()

        return output
    except Exception as err:
        return f"Error: {str(err)}"

if __name__ == '__main__':
    app.run()
