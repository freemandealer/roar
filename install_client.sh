#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 安装 Python 依赖
pip3 install -r requirements.txt

# 创建配置目录
mkdir -p ~/.config/command-notifier
cp config.ini.template ~/.config/command-notifier/config.ini

# 安装 CLI 工具
sudo cp "$SCRIPT_DIR/src/cli/command_watcher.py" /usr/local/bin/command-notifier-cli
sudo chmod +x /usr/local/bin/command-notifier-cli

# 添加 shell 函数
FUNCTION_DEF="
# Command output notifier function
notify() {
    if [ \$# -eq 0 ]; then
        cat | command-notifier-cli
    else
        \"\$@\" 2>&1 | command-notifier-cli
    fi
}
"

# 确定使用的 shell 配置文件
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    SHELL_RC="$HOME/.zshrc"
fi

# 检查是否已经安装了函数
if ! grep -q "Command output notifier function" "$SHELL_RC"; then
    echo "$FUNCTION_DEF" >> "$SHELL_RC"
    echo "Function installed in $SHELL_RC"
fi

# 如果是 Mac，安装托盘应用
if [[ "$OSTYPE" == "darwin"* ]]; then
    # 安装托盘应用
    sudo cp "$SCRIPT_DIR/src/tray/tray_app.py" /usr/local/bin/command-notifier-tray
    sudo chmod +x /usr/local/bin/command-notifier-tray
    
    # 安装启动项
    cp "$SCRIPT_DIR/mac/com.command-notifier.tray.plist" ~/Library/LaunchAgents/
    launchctl load ~/Library/LaunchAgents/com.command-notifier.tray.plist
    launchctl start com.command-notifier.tray
fi

echo "Installation complete!"
echo "Please edit ~/.config/command-notifier/config.ini to set your server URL"
echo "Then run: source $SHELL_RC" 