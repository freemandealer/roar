# Command Output Notifier

这是一个 Mac 平台的命令输出通知工具，它能够捕获任何命令的最后 10 行输出，并通过系统通知的方式提醒你。该工具由三个部分组成：

1. CLI 工具：无缝捕获命令输出
2. 通知服务器：转发通知
3. Mac 托盘应用：显示系统通知和输出结果

## 安装

1. 运行安装脚本：
```bash
./install.sh
```

2. 加载 shell 配置（必需步骤）：
```bash
source ~/.zshrc  # 如果你使用 zsh
# 或
source ~/.bashrc  # 如果你使用 bash
```

安装脚本会：
- 安装所需的 Python 依赖
- 添加 `notify` 命令到你的 shell 配置
- 创建服务启动脚本

### 故障排除

如果遇到 "command not found: notify" 错误，请尝试以下步骤：

1. 确认安装脚本已经运行成功
2. 运行相应的 source 命令：
   ```bash
   source ~/.zshrc  # 对于 zsh 用户
   # 或
   source ~/.bashrc  # 对于 bash 用户
   ```
3. 检查你的 shell 配置文件（~/.zshrc 或 ~/.bashrc）是否包含 notify 函数
4. 如果以上步骤都不解决问题，尝试重新运行安装脚本

## 启动服务

首次使用或重启电脑后，需要启动后台服务：
```bash
./start_services.sh
```

如果服务已在运行，该脚本会自动停止旧的服务并启动新的服务。

## 使用方法

你可以用两种方式使用这个工具：

1. 作为管道使用：
```bash
your-command | notify
```
例如：
```bash
ls -la | notify
```

2. 作为命令前缀使用：
```bash
notify your-command
```
例如：
```bash
notify ls -la
```

这两种方式都不会影响原始命令的正常输出和交互。

## 功能特点

- 无缝集成到终端工作流程中
- 不影响原始命令的输出和交互
- 捕获任何命令的最后 10 行输出
- 通过系统通知提醒命令执行完成
- 点击托盘图标可以查看最近的输出
- 输出结果以格式化的 HTML 页面显示
- 支持所有类型的命令，包括交互式命令
- 即使通知服务未运行也不会影响原始命令

## 系统要求

- macOS
- Python 3.6+
- 必要的 Python 包（见 requirements.txt） 