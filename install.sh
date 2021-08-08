#!/bin/sh

rm -rf /opt/lugia
rm -rf /etc/systemd/system/lugia.service

mkdir /opt/lugia
mkdir -p /opt/lugia/cmd/edr_manager/
cp ./cmd/edr_manager/main.go /opt/lugia/cmd/edr_manager/

cp -r ./configs /opt/lugia
touch /opt/lugia/configs/agents.conf

mkdir /opt/lugia/downloadfile

mkdir /opt/lugia/log
touch /opt/lugia/log/applog.txt
touch /opt/lugia/log/responselog.txt

mkdir /opt/lugia/pkg
cp -r ./pkg/rpc /opt/lugia/pkg
cp -r ./pkg/server /opt/lugia/pkg

cp -r ./rules /opt/lugia/
cp lugia.service /etc/systemd/system/

cd /opt/lugia
go mod init lugia
go build -o lugia cmd/edr_manager/main.go
cd

systemctl enable lugia.service
systemctl daemon-reload
