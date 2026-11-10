# 网络性能测试工具（前后端不分离版）

基于 FastAPI 的网络性能测试工具，服务端渲染页面 + 同源 API，单一服务部署。

## 功能特性

- **DNS 请求时间**：测量 DNS 域名解析所需时间
- **TCP 建连时间**：测量 TCP 三次握手建立连接所需时间
- **SSL 建连时间**：测量 SSL/TLS 握手建立安全连接所需时间
- **首包响应时间**：测量从建立连接到收到服务器第一个响应字节的时间
- **整体耗时**：测量从发起请求到收到完整响应的总时间

## 技术栈

- Python 3 + FastAPI + Jinja2（服务端渲染）
- 原生 HTML / CSS / JavaScript（无前端框架、无构建步骤）
- curl（底层网络测试工具）

## 项目结构

```
network_performance_test/
├── app.py                 # FastAPI 应用（页面路由 + API）
├── templates/
│   └── index.html         # 页面模板
├── static/
│   ├── style.css          # 样式（简约风格）
│   └── app.js             # 前端逻辑（原生 JS）
├── requirements.txt       # Python 依赖
└── README.md              # 项目说明
```

## 安装与运行

```bash
pip3 install -r requirements.txt
python3 app.py
```

访问 http://localhost:8000 即可使用。

## API

### GET /api/test?url=<目标网址>

返回 JSON：

```json
{
  "dns_time": 12.3,
  "tcp_time": 30.1,
  "ssl_time": 60.5,
  "first_byte_time": 45.0,
  "total_time": 148.0,
  "ssl_protocol": "TLSv1.3",
  "ssl_cipher": "AES128-GCM-SHA256",
  "server": "nginx"
}
```

各耗时字段单位均为毫秒（ms）；另有 HTTP 状态码/版本、远端地址、重定向、下载大小与速度、内容类型、SSL 证书信息等字段。
