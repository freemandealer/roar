#!/usr/bin/env python3
import sys
import requests
import json
from typing import List
import os
import select
import configparser
from pathlib import Path

def load_config():
    config = configparser.ConfigParser()
    
    # 查找配置文件
    config_paths = [
        Path.home() / '.config/command-notifier/config.ini',  # 用户配置
        Path('/etc/command-notifier/config.ini'),  # 系统配置
        Path(__file__).parent.parent.parent / 'config.ini'  # 项目目录配置
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            config.read(str(config_path))
            return config['server']['url']
    
    # 如果没有找到配置文件，使用默认值
    return "http://localhost:5000/notify"

SERVER_URL = load_config()
print(SERVER_URL)

def send_to_server(lines: List[str]):
    try:
        requests.post(SERVER_URL + "/notify", json={"lines": lines}, timeout=1)
    except Exception:
        pass  # Silently fail to not interfere with the original command

def process_output():
    # 用于存储最后10行
    last_lines = []
    has_output = False
    
    # 检查是否有数据可读
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        has_output = True
        line = sys.stdin.readline()
        if not line:
            break
            
        # 输出到标准输出，保持原始命令的输出
        sys.stdout.write(line)
        sys.stdout.flush()
        
        # 保存最后10行
        last_lines.append(line.rstrip())
        if len(last_lines) > 10:
            last_lines.pop(0)
    
    # 无论是否有输出，都发送通知
    if has_output:
        send_to_server(last_lines)
    else:
        send_to_server(["(无输出)"])

if __name__ == '__main__':
    process_output() 