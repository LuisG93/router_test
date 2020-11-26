from flask import request, make_response
from flask import Blueprint
from paramiko import SSHClient, AutoAddPolicy
import time
from utils import validate_request

router = Blueprint("index", __name__)

@router.route('/', methods=['GET'])
def index():
    return make_response({"message": "WELCOME"})

@router.route('/update_router', methods=['POST'])
@validate_request({
    "routers": {"type": "list", "required":True, 'schema': {'type': 'dict', "schema": {
        "ip": {"type": "string"},
        "port": {"type": "integer"},
        "user": {"type": "string"},
        "password": {"type": "string"},
        "interface": {"type": "string"},
    }}},
    "bandwidh": {"type": "integer", "required":True},
})
def update_router():
    for router in request.json["routers"]:
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(router["ip"], router["port"], router["user"], router["password"])
        ssh_command = ssh.invoke_shell()
        ssh_command.send("configure terminal\n")
        ssh_command.send("interface {}\n".format(router["interface"]))
        time.sleep(5)
        output = ssh_command.recv(5000)
        print(output)
        ssh_command.send("bandwidth {}\n".format(request.json["bandwidh"]))
        time.sleep(5)
        output = ssh_command.recv(5000)
        print(output)
        ssh_command.send("no shutdown\n")
        time.sleep(5)
        output = ssh_command.recv(5000)
        print(output)
        ssh_command.send("exit\n")
        ssh_command.send("exit\n")
        time.sleep(5)
        output = ssh_command.recv(5000)
        print(output)
        #ssh_command.send("copy running-config startup-config\n")
        ssh.close()
    return make_response({"message": "complete"})
    
    
    
"""
GigabitEthernet1
router: csr-1000v
ip 200.4.144.3
puerto:50081
usuario: cisco
password: cisco
"""