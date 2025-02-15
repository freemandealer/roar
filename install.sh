#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 创建函数定义
FUNCTION_DEF="
# Command output notifier function
notify() {
    if [ \$# -eq 0 ]; then
        cat | python3 \"$SCRIPT_DIR/src/cli/command_watcher.py\"
    else
        \"\$@\" 2>&1 | python3 \"$SCRIPT_DIR/src/cli/command_watcher.py\"
    fi
}
"

# 确定使用的 shell 配置文件
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    # 默认使用 .zshrc
    SHELL_RC="$HOME/.zshrc"
fi

# 检查是否已经安装了函数
if ! grep -q "Command output notifier function" "$SHELL_RC"; then
    echo "$FUNCTION_DEF" >> "$SHELL_RC"
    echo "Function installed successfully in $SHELL_RC"
    echo "Please run: source $SHELL_RC"
else
    echo "Function already installed in $SHELL_RC"
fi

# 安装 Python 依赖
pip install -r requirements.txt

# 使脚本可执行
chmod +x src/cli/command_watcher.py

# 创建服务器启动脚本
cat > start_server.sh << EOL
#!/bin/bash
python3 "$SCRIPT_DIR/src/server/notification_server.py"
EOL

chmod +x start_server.sh

# 创建托盘应用启动脚本
cat > start_tray.sh << EOL
#!/bin/bash
if [ -z "\$1" ]; then
    echo "Usage: ./start_tray.sh http://server-address:5000"
    exit 1
fi
python3 "$SCRIPT_DIR/src/tray/tray_app.py" "\$1"
EOL

chmod +x start_tray.sh

echo "Installation complete!"
echo ""
echo "To start the server (on the server machine), run:"
echo "    ./start_server.sh"
echo ""
echo "To start the tray app (on your local machine), run:"
echo "    ./start_tray.sh http://server-address:5000"
echo "    (Replace server-address with your server's address)"
echo ""
echo "To use the notifier, you can either:"
echo "1. Pipe any command: 'your-command | notify'"
echo "2. Use notify as prefix: 'notify your-command'" 