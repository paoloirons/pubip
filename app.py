from flask import Flask, render_template, request
import requests
import ipaddress

app = Flask(__name__)

def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    return response.json()['ip']

def calculate_subnet(ip, subnet):
    network = ipaddress.ip_network(f"{ip}/{subnet}", strict=False)
    return {
        'network': str(network.network_address),
        'broadcast': str(network.broadcast_address),
        'netmask': str(network.netmask),
        'hosts': list(network.hosts())
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    public_ip = get_public_ip()
    subnet_info = None
    if request.method == 'POST':
        ip = request.form['ip']
        subnet = request.form['subnet']
        subnet_info = calculate_subnet(ip, subnet)
    return render_template('index.html', public_ip=public_ip, subnet_info=subnet_info)

if __name__ == '__main__':
    app.run(debug=True)
