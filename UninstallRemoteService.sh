#!/bin/bash

sudo systemctl stop remote-control
sudo systemctl disable remote-control
sudo rm /etc/systemd/system/remote-control
sudo rm /etc/systemd/system/remote-control # and symlinks that might be related
sudo rm /usr/lib/systemd/system/remote-control 
sudo rm /usr/lib/systemd/system/remote-control # and symlinks that might be related
sudo systemctl daemon-reload
sudo systemctl reset-failed
