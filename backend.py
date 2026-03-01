from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import re

app = Flask(__name__)
CORS(app)

@app.route('/api/test', methods=['GET'])
def test_network():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # 使用 curl 命令获取网络性能指标
        cmd = [
            'curl', '-w', 
            '%{time_namelookup},%{time_connect},%{time_appconnect},%{time_starttransfer},%{time_total}',
            '-o', '/dev/null', '-s',
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return jsonify({'error': 'Failed to test network performance'}), 500
        
        # 解析 curl 输出
        metrics = result.stdout.strip().split(',')
        if len(metrics) != 5:
            return jsonify({'error': 'Invalid curl output'}), 500
        
        # 转换为毫秒并构建响应
        response = {
            'dns_time': float(metrics[0]) * 1000,      # DNS 解析时间
            'tcp_time': (float(metrics[1]) - float(metrics[0])) * 1000,  # TCP 连接时间
            'ssl_time': (float(metrics[2]) - float(metrics[1])) * 1000,  # SSL 连接时间
            'first_byte_time': (float(metrics[3]) - float(metrics[2])) * 1000,  # 首包响应时间
            'total_time': float(metrics[4]) * 1000    # 整体耗时
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)