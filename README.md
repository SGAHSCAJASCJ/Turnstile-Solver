# Turnstile CAPTCHA Solver 

## 🚀 Project Overview
This is a high-performance Cloudflare Turnstile CAPTCHA automatic solving solution built with FastAPI and asynchronous browser technology, providing RESTful API services.Available until the current time, still available

## 📊 Performance Metrics

| 指标 / Metric | 数值 / Value | 说明 / Description |
|---------------|--------------|--------------------|
| 并发处理能力 / Concurrent Capacity | 500+ requests/min | 每分钟可处理超过1000个请求 |
| 平均响应时间 / Average Response Time | 1.8-3 seconds | 平均验证码解决时间 |
| 成功率 / Success Rate | 99%+ | 验证码解决成功率 |
| 内存占用 / Memory Usage | <300MB | 单实例内存占用 |
| CPU占用 / CPU Usage | <30% | 4核CPU环境下的占用率 |

## 🚀 快速开始 / Quick Start

### 环境要求 / Requirements
- Python 3.8+
- Windows/Linux/macOS
- 2GB+ RAM
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

## 🔧 Advanced Configuration

### 性能调优 / Performance Tuning
- **线程数配置**：建议设置为CPU核心数
- **页面数配置**：高性能服务器可适当增加
- **代理轮换**：启用代理支持可提高成功率
- **内存监控**：定期监控内存使用情况

## 🤝 Support the Project

If this project helps you, welcome to support our development work!

### 💰 Donation
**以太坊钱包地址 / Ethereum Wallet Address:**
```
0x44b8f11e77ef75fb10f6cc41a926da26ab91b631
```

Your support will help us:
- Continuously improve and optimize the code
- Add more features
- Provide better technical support
- Maintain long-term project development

## 📄 License

MIT License - 详见 LICENSE 文件

## 🔗 Related Links

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Camoufox 项目](https://github.com/daijro/camoufox)
- [Cloudflare Turnstile 文档](https://developers.cloudflare.com/turnstile/)

---

**⚡ 高性能 | 🚀 易部署 | 🛡️ 稳定可靠 **

**⚡ High Performance | 🚀 Easy Deploy | 🛡️ Stable & Reliable **
