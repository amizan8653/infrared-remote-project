#!/bin/bash

sudo cp remote-control.service /etc/systemd/system/remote-control.service 
sudo systemctl daemon-reload 
sudo systemctl enable remote-control
sudo systemctl start remote-control
