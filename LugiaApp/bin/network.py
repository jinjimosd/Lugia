import socket
import subprocess
import shlex
import os,sys
import time
import json
from splunklib.searchcommands import dispatch, GeneratingCommand, Configuration, Option, validators

def send_Data(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('10.184.0.4', 10000)
    sock.connect(server_address)
    try:
        sock.sendall(bytes(data, encoding='utf-8'))
    finally:
        sock.close()

def format_Data(action, host):
    raw={}
    # data = json.loads(rdata)
    raw['Action'] = action
    raw['ComputerName'] = host
    return json.dumps(raw)

@Configuration()
class GenerateHelloCommand(GeneratingCommand):
    action = Option(require=True)
    host = Option(require=True)
    def generate(self):
        raw_data = format_Data(str(self.action), str(self.host))
        send_Data(raw_data)
        yield {'_raw': raw_data}

dispatch(GenerateHelloCommand, sys.argv, sys.stdin, sys.stdout, __name__)
