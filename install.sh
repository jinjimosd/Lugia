#!/bin/sh

rm -rf /opt/lugia
rm -rf /etc/systemd/system/lugia.service

mkdir /opt/lugia

cp -r ./configs /opt/lugia
cp lugia /opt/lugia
chmod +x /opt/lugia/lugia

touch /opt/lugia/configs/agents.conf

mkdir /opt/lugia/downloadfile

mkdir /opt/lugia/log
touch /opt/lugia/log/applog.txt
touch /opt/lugia/log/responselog.txt

cp -r ./rules /opt/lugia/
cp lugia.service /etc/systemd/system/

systemctl enable lugia.service
systemctl daemon-reload
