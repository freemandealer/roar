#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 安装 Python 依赖
pip3 install -r requirements.txt

# 创建配置目录
sudo mkdir -p /etc/command-notifier
sudo cp config.ini.template /etc/command-notifier/config.ini

# 安装服务器程序
sudo cp "$SCRIPT_DIR/src/server/notification_server.py" /usr/local/bin/command-notifier-server
sudo chmod +x /usr/local/bin/command-notifier-server

# 安装并启动系统服务
sudo cp "$SCRIPT_DIR/linux/command-notifier.service" /etc/systemd/system/
# 替换服务文件中的用户名
sudo sed -i "s/YOUR_USERNAME/$USER/" /etc/systemd/system/command-notifier.service

# 重新加载 systemd 配置
sudo systemctl daemon-reload
sudo systemctl enable command-notifier
sudo systemctl start command-notifier

echo "Server installation complete!"
echo "Check status with: sudo systemctl status command-notifier" 