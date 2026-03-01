# 网络性能测试工具

一个基于 Vue3 + Flask 的网络性能测试工具，用于测量和分析网站的网络性能指标。

## 功能特性

- **DNS 请求时间**：测量 DNS 域名解析所需时间
- **TCP 建连时间**：测量 TCP 三次握手建立连接所需时间
- **SSL 建连时间**：测量 SSL/TLS 握手建立安全连接所需时间
- **首包响应时间**：测量从建立连接到收到服务器第一个响应字节的时间
- **整体耗时**：测量从发起请求到收到完整响应的总时间

## 技术栈

### 前端
- Vue 3
- Vite 4

### 后端
- Python 3
- Flask
- curl（底层网络测试工具）

## 项目结构

```
network_performance_test/
├── src/
│   ├── App.vue          # 主组件
│   └── main.js          # 入口文件
├── backend.py           # 后端服务
├── index.html           # HTML 模板
├── package.json         # 前端依赖配置
├── vite.config.js       # Vite 配置
├── requirements.txt     # Python 依赖
└── README.md            # 项目说明文档
```

## 安装与运行

### 环境要求

- Node.js 16+
- Python 3.7+
- curl 命令行工具

### 安装依赖

#### 前端依赖
```bash
npm install
```

#### 后端依赖
```bash
pip3 install -r requirements.txt
```

### 启动服务

#### 启动后端服务
```bash
python3 backend.py
```
后端服务将在 `http://127.0.0.1:8000` 启动

#### 启动前端服务
```bash
npm run dev
```
前端服务将在 `http://127.0.0.1:3000` 启动

### 访问应用

在浏览器中打开 `http://127.0.0.1:3000` 即可使用

## API 接口

### 测试网络性能

**请求**
```
GET /api/test?url=<url>
```

**参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | string | 是 | 要测试的网址 |

**响应示例**
```json
{
  "dns_time": 12.34,
  "tcp_time": 8.76,
  "ssl_time": 15.67,
  "first_byte_time": 23.45,
  "total_time": 56.78
}
```

**响应字段说明**
| 字段 | 说明 | 单位 |
|------|------|------|
| dns_time | DNS 域名解析时间 | 毫秒 |
| tcp_time | TCP 连接建立时间 | 毫秒 |
| ssl_time | SSL/TLS 握手时间 | 毫秒 |
| first_byte_time | 首包响应时间 | 毫秒 |
| total_time | 整体耗时 | 毫秒 |

## 测试示例

使用 curl 命令测试：
```bash
curl "http://127.0.0.1:8000/api/test?url=https://www.baidu.com"
```

## 注意事项

1. 测试 HTTPS 网站时才会有 SSL 建连时间，HTTP 网站该值为 0
2. 各阶段时间为独立耗时，非累计时间
3. 网络环境不同，测试结果会有差异
4. 建议多次测试取平均值以获得更准确的结果

## License

MIT
