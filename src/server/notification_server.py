from flask import Flask, request, jsonify
import json
from typing import List, Deque
from collections import deque
import threading
import time

app = Flask(__name__)

# 存储最近的通知
notifications = deque(maxlen=100)  # 最多保存100条通知
notifications_lock = threading.Lock()

@app.route('/notify', methods=['POST'])
def notify():
    try:
        data = request.get_json()
        if not data or 'lines' not in data:
            return jsonify({"error": "Invalid data format"}), 400
        
        lines: List[str] = data['lines']
        
        # 添加通知到队列
        with notifications_lock:
            notifications.append({
                'timestamp': time.time(),
                'lines': lines
            })
        
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/poll', methods=['GET'])
def poll():
    try:
        # 获取客户端最后收到的通知时间戳
        last_timestamp = float(request.args.get('last_timestamp', 0))
        
        # 获取新通知
        new_notifications = []
        with notifications_lock:
            for notif in notifications:
                if notif['timestamp'] > last_timestamp:
                    new_notifications.append(notif)
        
        # 如果有新通知，立即返回
        if new_notifications:
            return jsonify({
                "notifications": new_notifications,
                "timestamp": time.time()
            })
        
        # 如果没有新通知，等待一段时间
        time.sleep(10)  # 等待10秒
        
        # 再次检查新通知
        new_notifications = []
        with notifications_lock:
            for notif in notifications:
                if notif['timestamp'] > last_timestamp:
                    new_notifications.append(notif)
        
        return jsonify({
            "notifications": new_notifications,
            "timestamp": time.time()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 