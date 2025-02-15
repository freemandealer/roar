#!/usr/bin/env python3
import sys
import requests
import json
from typing import List
import os
import select

SERVER_URL = "http://localhost:5000/notify"

def send_to_server(lines: List[str]):
    try:
        requests.post(SERVER_URL, json={"lines": lines}, timeout=1)
    except Exception:
        pass  # Silently fail to not interfere with the original command

def process_output():
    # 用于存储最后10行
    last_lines = []
    
    # 检查是否有数据可读
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
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
    
    # 如果有收集到输出，发送到服务器
    if last_lines:
        send_to_server(last_lines)

if __name__ == '__main__':
    process_output() 