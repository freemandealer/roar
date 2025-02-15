#!/usr/bin/env python3
import rumps
import threading
import webbrowser
import tempfile
import os
import subprocess
import requests
import json
import time
from typing import List, Optional
from urllib.parse import urljoin

def send_notification(title: str, subtitle: str, message: str):
    """使用 osascript 发送 macOS 通知"""
    script = f'''
    display notification "{message}" with title "{title}" subtitle "{subtitle}"
    '''
    subprocess.run(['osascript', '-e', script])

class NotificationPoller(threading.Thread):
    def __init__(self, callback, server_url):
        super().__init__()
        self.callback = callback
        self.server_url = server_url
        self.should_run = True
        self.daemon = True
        self.last_timestamp = 0
        self.session = requests.Session()
    
    def run(self):
        poll_url = urljoin(self.server_url, 'poll')
        
        while self.should_run:
            try:
                # 长轮询请求
                response = self.session.get(
                    poll_url,
                    params={'last_timestamp': self.last_timestamp},
                    timeout=30  # 30秒超时
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.last_timestamp = data.get('timestamp', self.last_timestamp)
                    
                    # 处理所有新通知
                    for notif in data.get('notifications', []):
                        if 'lines' in notif:
                            self.callback(notif['lines'])
                
            except requests.Timeout:
                # 超时是正常的，继续轮询
                continue
            except Exception as e:
                print(f"Polling error: {e}")
                time.sleep(5)  # 出错时等待5秒再重试
    
    def stop(self):
        self.should_run = False

class CommandNotifierApp(rumps.App):
    def __init__(self, server_url):
        super().__init__("📟")
        self.current_lines: Optional[List[str]] = None
        self.menu = ["查看最后的输出"]
        
        # 启动轮询器
        self.poller = NotificationPoller(self.handle_notification, server_url)
        self.poller.start()
    
    def handle_notification(self, lines: List[str]):
        self.current_lines = lines
        # 使用 macOS 原生通知
        send_notification(
            title="命令执行完成",
            subtitle="点击托盘图标查看输出",
            message=f"共 {len(lines)} 行输出"
        )
    
    @rumps.clicked("查看最后的输出")
    def show_output(self, _):
        if not self.current_lines:
            send_notification(
                title="没有输出",
                subtitle="",
                message="当前没有可用的命令输出"
            )
            return
        
        # 创建临时HTML文件来显示输出
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            html_content = """
            <html>
            <head>
                <style>
                    body { 
                        font-family: monospace;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }
                    pre {
                        background-color: white;
                        padding: 15px;
                        border-radius: 5px;
                        border: 1px solid #ddd;
                        white-space: pre-wrap;
                        word-wrap: break-word;
                    }
                </style>
            </head>
            <body>
                <h2>命令输出</h2>
                <pre>%s</pre>
            </body>
            </html>
            """ % '\n'.join(self.current_lines)
            f.write(html_content)
            webbrowser.open('file://' + f.name)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python tray_app.py http://server-address:5000")
        sys.exit(1)
    
    server_url = sys.argv[1]
    CommandNotifierApp(server_url).run() 