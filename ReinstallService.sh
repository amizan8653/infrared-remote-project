#!/bin/bash

# kill and remove
sudo systemctl stop remote-control
sudo systemctl disable remote-control
sudo rm /etc/systemd/system/remote-control
sudo rm /etc/systemd/system/remote-control # and symlinks that might be related
sudo rm /usr/lib/systemd/system/remote-control 
sudo rm /usr/lib/systemd/system/remote-control # and symlinks that might be related
sudo systemctl daemon-reload
sudo systemctl reset-failed


# reinstall and start again
sudo cp remote-control.service /etc/systemd/system/remote-control.service 
sudo systemctl daemon-reload 
sudo systemctl enable remote-control
sudo systemctl start remote-control
