from flask import request, make_response
from flask import Blueprint
from paramiko import SSHClient, AutoAddPolicy
import time
import re
from utils import validate_request

router = Blueprint("index", __name__)


@router.route('/', methods=['GET'])
def index():
    return make_response({"message": "WELCOME"})


@router.route('/update_router', methods=['POST'])
@validate_request({
    "routers": {"type": "list", "required": True, 'schema': {'type': 'dict', "schema": {
        "ip": {"type": "string", "required": True},
        "port": {"type": "integer", "required": True},
        "user": {"type": "string", "required": True},
        "password": {"type": "string", "required": True},
        "interface": {"type": "string", "required": True},
    }}},
    "bandwidh": {"type": "integer", "required": True},
})
def update_router():
    for router in request.json["routers"]:
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(router["ip"], router["port"], router["user"], router["password"])
        ssh_command = ssh.invoke_shell()
        ssh_command.send("configure terminal\n")
        ssh_command.send("interface {}\n".format(router["interface"]))
        time.sleep(1)
        # output = ssh_command.recv(5000)
        # print(output)
        ssh_command.send("bandwidth {}\n".format(request.json["bandwidh"]))
        time.sleep(1)
        # output = ssh_command.recv(5000)
        # print(output)
        ssh_command.send("no shutdown\n")
        time.sleep(1)
        # output = ssh_command.recv(5000)
        # print(output)
        ssh_command.send("exit\n")
        ssh_command.send("exit\n")
        time.sleep(1)
        # output = ssh_command.recv(5000)
        # print(output)
        # ssh_command.send("copy running-config startup-config\n")
        ssh.close()
    return make_response({"message": "complete"})


@router.route('/get_router', methods=['POST'])
@validate_request({
    "routers": {"type": "list", "required": True, 'schema': {'type': 'dict', "schema": {
        "ip": {"type": "string", "required": True},
        "port": {"type": "integer", "required": True},
        "user": {"type": "string", "required": True},
        "password": {"type": "string", "required": True},
        "interface": {"type": "string", "required": True},
    }}},
    "info": {"type": "list", "required": True, "schema": {
        "type": "string",
        "allowed": ["bandwidth", "address"]
    }}
})
def get_router():
    response = {}
    for router in request.json["routers"]:
        try:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(router["ip"], router["port"],
                        router["user"], router["password"])
        except Exception:
            response[router["ip"]+"_"+router["interface"]] = "Connection error"
            ssh.close()
        else:
            ssh_command = ssh.invoke_shell()
            ssh_command.send("show interface {}\n".format(router["interface"]))
            time.sleep(2)
            output = ssh_command.recv(5000).decode()
            # Validate if interface exist
            if output.find("Invalid input detected at") < 0:
                extract_data = {}
                if "bandwidth" in request.json["info"]:
                    search = re.search(r'BW (.*?), ', output)
                    if search:
                        extract_data["bandwidth"] = search.group(1)
                    else:
                        extract_data["bandwidth"] = "bandwidth not found"
                if "address" in request.json["info"]:
                    search = re.search(r'Internet address is (.*?)\r\n', output)
                    if search:
                        extract_data["address"] = search.group(1)
                    else:
                        extract_data["address"] = "address not found"
                response[router["ip"]+"_"+router["interface"]] = extract_data
            else:
                key = router["ip"]+"_"+router["interface"]
                response[key] = "Interface not found"
            ssh.close()
    return response
