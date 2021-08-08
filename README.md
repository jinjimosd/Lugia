# EDR Server

## Prerequisites
Before you continue, ensure you meet the following requirements:
 
- You have installed the latest version of Golang.
- You are using a Linux or Mac OS machine. Windows is not currently supported.
- You have install the Universal Forwarder on Linux
- The Splunk Server

### Install Universal Forwarder on Linux

- The universal forwarder is available for Linux as a tar file, an RPM package, and a DEB package.
- In my case, I install from a tar file.
- To install the forwarder into the folder /opt/splunkforwarder, run:

```
tar xvzf splunkforwarder-<…>-Linux-x86_64.tgz -C /opt
```

### Install EDR Server
- Download source code from github https://github.com/jinjimosd/Lugia.git
- Create directory configs and file edrserver.conf
- Run install.sh file as sudo
```
git clone https://github.com/jinjimosd/Lugia.git
cd Lugia
mkdir configs
vim configs/edrserver.conf

{
  "ServerConfig": [
    {
      "ParentDirPath":"./downloadfile",
      "ResultLogPath":"./log/responselog.txt",
      "RuleFilePath":"./rules/responserules.txt",
      "AppLogPath":"./log/applog.txt",
      "AgentsConfPath":"./configs/agents.conf",
      "SplunkHost":"<Splunk server host>",
      "ServerHost":"<EDR server host>",
      "ServerPort":"10000"
    }
  ]
}

chmod +x install.sh
sudo ./install.sh
```
### Configure Universal Forwarder on Linux
- Configure the universal forwarder to send data to the Splunk Enterprise indexer 

- From a shell prompt on the universal forwarder, go to the */opt/splunkforwarder/bin* directory.
```
cd /opt/splunkforwarder/bin
```

- Specify the host name or ip address of the Splunk Enterprise receiver.
```
./splunk add forward-server <host>:<port>
```

- Configure the universal forwarder as a deployment client.
```
./splunk set deploy-poll <host>:<port>
```

- Create file /opt/splunkforwarder/etc/system/local/inputs.conf and add below lines.
```
vim /opt/splunkforwarder/etc/system/local/inputs.conf

[monitor:///opt/lugia/log/resultlog.txt]
disabled = false
index = responselog
```
- Edit file /opt/splunkforwarder/etc/system/local/deploymentclient.conf 
```
vim /opt/splunkforwarder/etc/system/local/deploymentclient.conf 

[target-broker:deploymentServer]
targetUri = <host>:<port>
```
- Start Splunk Forwarder
```
sudo /opt/splunkforwarder/bin/splunk start
```

### Start server
```
sudo systemctl start lugia.services
```

### Installing EDR agent.
- Download source code from github https://github.com/jinjimosd/Lugia.git
- Create windowsagent.conf and add config.

```
{
  "AgentConfig": [
    {
      "AdapterInternet":"<Name Of Network Adapter>",
      "ServerHost":"<EDR Server Host>",
      "ServerPort":"10000",
      "AgentHost":"<Agent Host>",
      "AgentPort":"1234"
    }
  ]
}
```
- Go to C:\Windows\System32 and create LugiaAgent directory
- Copy lugiaagent.exe and windowsagent.conf to LugiaAgent directory 
- Run Windows PowerShell as Administrator and run command
```
sc.exe create lugiaagent binPath= "C:\Windows\System32\LugiaAgent\lugiaagent.exe" DisplayName= "Lugia Agent" start= auto
sc.exe start lugiaagent
```

## ⛏️ Built Using <a name = "built_using"></a>

- [Golang](https://golang.org/) - Main Code Language
- [GRPC](https://grpc.io/) - Open source high performance Remote Procedure Call
- [Protocol Buffer](https://developers.google.com/protocol-buffers) - Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data

## ✍️ Authors <a name = "authors"></a>

- [@jinjimosd](https://github.com/kylelobo) - Code and update

- The list of contributors who participated in this project.

1. Nguyen Huy Thanh       Gmail: ThanhNHHE130698@fpt.edu.vn
2. Le Tuan Anh            Gmail: AnhLTHE130738@fpt.edu.vn
3. Bui Loc Xuan Truong    Gmail: TruongBLXHE130204@fpt.edu.vn
4. Nguyen Huy Hoang       Gmail: HoangNHHE131014@fpt.edu.vn
5. Tran	Đam	Chi           Gmail: ChiTDSE05481@fpt.edu.vn
