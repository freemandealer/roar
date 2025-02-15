#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: ./start_tray.sh http://server-address:5000"
    exit 1
fi
python3 "/Users/zhangzhengyu01/project/roar/src/tray/tray_app.py" "$1"
