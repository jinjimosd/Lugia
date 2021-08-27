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
def format_Data(action, rtype, rmessage, raction, rdata):
    raw={}
    # data = json.loads(rdata)
    raw['Action Rule'] = action
    raw['Type'] = rtype
    raw['Message'] = rmessage
    raw['Action'] = raction
    raw['Data'] = rdata
    return json.dumps(raw)

@Configuration()
class GenerateHelloCommand(GeneratingCommand):
    action = Option(require=True)
    rtype = Option(require=True)
    rmessage = Option(require=True)
    raction = Option(require=True)
    rdata = Option(require=True)
    def generate(self):
        if str(self.action)== 'delete':
            f = open('test.txt', 'a')
            f.write(str(self.rdata)+'\n')
            f.close()
            os.system("/opt/splunk/bin/./splunk search 'index=ruleresponse | delete' -auth admin:Abcd@123456 > /dev/null 2>&1")
        raw_data = format_Data(str(self.action), str(self.rtype), str(self.rmessage), str(self.raction), str(self.rdata))
        send_Data(raw_data)
        yield {'_raw': raw_data}

dispatch(GenerateHelloCommand, sys.argv, sys.stdin, sys.stdout, __name__)
