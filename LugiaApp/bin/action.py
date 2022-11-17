#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
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

def format_Data(data, message, action):
    log = json.loads(data)
    eventdata = ('Time: ' + log['result']['_raw']).split('\n')
    raw = dict(event.replace('=', ': ', 1).replace('\r','').split(': ', 1)
                for event in eventdata)
    if action in ['kill','killtree','suspend'] and raw['EventCode']!='3':
        raw['Type'] = 'Process'
    elif action in ['delete','getfile'] and raw['EventCode'] not in ['12','13','14']:
        raw['Type'] = 'File'
    elif action in ['kill','blockip'] and raw['EventCode']=='3':
        raw['Type'] = 'Network'
    else:
        raw['Type'] = 'Registry'
    raw['Message'] = message
    raw['Action'] = action
    return json.dumps(raw)

@Configuration()
class GenerateHelloCommand(GeneratingCommand):
    recordnumber = Option(require=True, validate=validators.Integer())
    trigger = Option(require=True)
    action = Option(require=True)
    host = Option(require=True)
    def generate(self):
        process = subprocess.Popen(shlex.split("/opt/splunk/bin/./splunk search 'index=windows RecordNumber=" + str(self.recordnumber) +  " host_fqdn=" + str(self.host) + " ' -output json -auth admin:Abcd@123456"), stdout=subprocess.PIPE)
        log = process.stdout.readline().decode()
        raw_data = format_Data(str(log), str(self.trigger), str(self.action))
        send_Data(raw_data)
        yield {'_raw': raw_data}

dispatch(GenerateHelloCommand, sys.argv, sys.stdin, sys.stdout, __name__)
