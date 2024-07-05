#!/bin/bash

export XDG_RUNTIME_DIR=/run/user/1000

echo "activating python env"
source /home/amizan8653/.venv/bin/activate

echo "running python script"
/home/amizan8653/.venv/bin/python /home/amizan8653/Desktop/git_repos/infrared-remote-project/RemoteControl.py

echo "script terminated... this shouldn't happen"
