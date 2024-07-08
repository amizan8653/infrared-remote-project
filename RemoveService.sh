#!/bin/bash

systemctl stop remote-control
systemctl disable remote-control
rm /etc/systemd/system/remote-control
rm /etc/systemd/system/remote-control # and symlinks that might be related
rm /usr/lib/systemd/system/remote-control 
rm /usr/lib/systemd/system/remote-control # and symlinks that might be related
systemctl daemon-reload
systemctl reset-failed
