#!/bin/sh
USER=`whoami`

rm -rf /opt/lugia
rm -rf /etc/systemd/system/lugia.service

mkdir /opt/lugia

cp -r ./configs /opt/lugia
cp lugia /opt/lugia

touch /opt/lugia/configs/agents.conf

mkdir /opt/lugia/downloadfile

mkdir /opt/lugia/log
touch /opt/lugia/log/applog.txt
touch /opt/lugia/log/responselog.txt

cp -r ./rules /opt/lugia/
cp lugia.service /etc/systemd/system/

cd /opt/lugia
go mod init lugia
go build -o lugia cmd/edr_manager/main.go
cd /opt
chown -R $USER:$USER lugia
cd 

systemctl enable lugia.service
systemctl daemon-reload
