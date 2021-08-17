import subprocess
import socket
import sys
import shlex
import json
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('10.146.0.6', 10000)
while sock.connect_ex(server_address) != 0:
    time.sleep(10)

def format_Data(data):
    log = json.loads(data)
    eventdata = ('Time: ' + log['result']['_raw']).split('\n')
    raw = dict(event.replace('=', ': ', 1).split(': ', 1)
                for event in eventdata)
    return json.dumps(raw)

process = subprocess.Popen(shlex.split("/opt/splunk/bin/./splunk rtsearch 'index=windows' -output json -auth admin:Abcd@123456"), stdout=subprocess.PIPE)
try:
    # Send data
    while True:
        log = process.stdout.readline().decode()
        data = str(log)
        sock.sendall(bytes(format_Data(data) + "\n",encoding='utf-8'))
        time.sleep(0.1)
        print(format_Data(data))
        continue
finally:
   print(sys.stderr, 'closing socket')
   sock.close()  
