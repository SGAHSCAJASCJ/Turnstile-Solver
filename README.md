# Turnstile CAPTCHA Solver


## 🚀 快速开始 / Quick Start

### 环境要求 / Requirements
- Python 3.8+
- Windows/Linux/macOS
- 1GB+ RAM
- 稳定的网络连接

### 安装依赖 / Install Dependencies
```bash
pip install fastapi uvicorn camoufox loguru
python -m camoufox fetch
```

### 配置文件 / Configuration
edit `api_server.py` 文件：
```python
# 以无头模式运行浏览器 / Run browser in headless mode
headless = True

# 浏览器实例数量(线程数) / Number of browser instances (threads)
thread = 2

# 每个浏览器实例的页面数量 / Pages per browser instance
page_count = 1


# 绑定主机 / Bind host
host = "0.0.0.0"

# 绑定端口 / Bind port
port = 8000
```


### 启动服务 / Start Service
```bash
python api_server.py
```

## 📖 API文档 / API Documentation

### 提交验证码任务 / Submit CAPTCHA Task
```http
GET /turnstile?url=https://example.com&sitekey=0x4AAAAAAA...
```

**响应 / Response:**
```json
{
  "task_id": "uuid-string",
  "status": "accepted"
}
```

### 获取解决结果 / Get Solution Result
```http
GET /result?id=task_id
```

**响应 / Response:**
```json
{
  "status": "success",
  "elapsed_time": 3.245,
  "value": "turnstile-response-token"
}
```


**⚡ 高性能 | 🚀 易部署 | 🛡️ 稳定可靠 **
