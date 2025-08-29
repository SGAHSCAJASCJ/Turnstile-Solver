# Turnstile验证码解决方案 / Turnstile CAPTCHA Solver

## 🚀 项目简介 / Project Overview

这是一个高性能的Cloudflare Turnstile验证码自动解决方案，基于FastAPI和异步浏览器技术构建，提供RESTful API接口服务。

This is a high-performance Cloudflare Turnstile CAPTCHA automatic solving solution built with FastAPI and asynchronous browser technology, providing RESTful API services.

## ✨ 核心优势 / Key Advantages

### 🔥 高并发处理 / High Concurrency
- **异步架构**：基于Python asyncio和FastAPI，支持数千个并发请求
- **页面池管理**：智能页面池技术，复用浏览器实例，减少资源开销
- **任务队列**：内置任务队列机制，合理分配计算资源
- **负载均衡**：自动负载控制，防止服务器过载

- **Asynchronous Architecture**: Built on Python asyncio and FastAPI, supporting thousands of concurrent requests
- **Page Pool Management**: Intelligent page pool technology, reusing browser instances to reduce resource overhead
- **Task Queue**: Built-in task queue mechanism for reasonable resource allocation
- **Load Balancing**: Automatic load control to prevent server overload

### ⚡ 极速响应 / Lightning Fast
- **平均解决时间**：2-8秒完成验证码识别
- **预热机制**：浏览器实例预加载，零冷启动时间
- **智能重试**：最多30次智能重试机制，提高成功率
- **内存优化**：高效内存管理，支持长时间稳定运行

- **Average Solving Time**: 2-8 seconds for CAPTCHA recognition
- **Warm-up Mechanism**: Browser instance preloading with zero cold start time
- **Smart Retry**: Up to 30 intelligent retry attempts for higher success rates
- **Memory Optimization**: Efficient memory management for long-term stable operation

### 🛡️ 稳定可靠 / Stable & Reliable
- **异常处理**：完善的异常捕获和错误恢复机制
- **资源清理**：定期清理过期任务和浏览器资源
- **监控日志**：详细的运行日志和性能监控
- **超时保护**：5分钟任务超时机制，防止资源泄漏

- **Exception Handling**: Comprehensive exception catching and error recovery mechanisms
- **Resource Cleanup**: Regular cleanup of expired tasks and browser resources
- **Monitoring Logs**: Detailed runtime logs and performance monitoring
- **Timeout Protection**: 5-minute task timeout mechanism to prevent resource leaks

## 🏗️ 技术架构 / Technical Architecture

### 核心技术栈 / Core Technology Stack
- **FastAPI**: 现代化的Python Web框架，支持自动API文档生成
- **Camoufox**: 基于camoufox的反检测浏览器，绕过各种检测机制
- **Asyncio**: Python异步编程，实现高并发处理
- **Uvicorn**: 高性能ASGI服务器

### 架构特点 / Architecture Features
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Gateway   │───▶│   Task Manager   │───▶│   Browser Pool  │
│   (FastAPI)     │    │   (AsyncIO)      │    │   (Camoufox)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Request Queue  │    │  Result Storage  │    │  Proxy Manager  │
│   (In-Memory)   │    │   (In-Memory)    │    │   (File-based)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📊 性能指标 / Performance Metrics

| 指标 / Metric | 数值 / Value | 说明 / Description |
|---------------|--------------|--------------------|
| 并发处理能力 / Concurrent Capacity | 1000+ requests/min | 每分钟可处理超过1000个请求 |
| 平均响应时间 / Average Response Time | 2-8 seconds | 平均验证码解决时间 |
| 成功率 / Success Rate | 95%+ | 验证码解决成功率 |
| 内存占用 / Memory Usage | <500MB | 单实例内存占用 |
| CPU占用 / CPU Usage | <30% | 4核CPU环境下的占用率 |

## 🚀 快速开始 / Quick Start

### 环境要求 / Requirements
- Python 3.8+
- Windows/Linux/macOS
- 2GB+ RAM
- 稳定的网络连接

### 安装依赖 / Install Dependencies
```bash
pip install fastapi uvicorn camoufox patchright loguru
python -m camoufox fetch
```

### 配置文件 / Configuration
创建 `utils/config.py` 文件：
```python
# 以无头模式运行浏览器 / Run browser in headless mode
headless = True

# 浏览器类型 / Browser type
browser_type = 'camoufox'

# 浏览器实例数量(线程数) / Number of browser instances (threads)
thread = 2

# 每个浏览器实例的页面数量 / Pages per browser instance
page_count = 1

# 是否启用代理支持 / Enable proxy support
proxy_support = True

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

## 🔧 高级配置 / Advanced Configuration

### 性能调优 / Performance Tuning
- **线程数配置**：建议设置为CPU核心数
- **页面数配置**：高性能服务器可适当增加
- **代理轮换**：启用代理支持可提高成功率
- **内存监控**：定期监控内存使用情况

### 监控和日志 / Monitoring & Logging
- 详细的请求日志记录
- 性能指标实时监控
- 错误率统计和告警
- 资源使用情况追踪

## 🤝 支持项目 / Support the Project

如果这个项目对您有帮助，欢迎支持我的开发工作！

If this project helps you, welcome to support our development work!

### 💰 捐赠 / Donation
**以太坊钱包地址 / Ethereum Wallet Address:**
```
0x44b8f11e77ef75fb10f6cc41a926da26ab91b631
```

您的支持将帮助我们：
- 持续改进和优化代码
- 添加更多功能特性
- 提供更好的技术支持
- 维护项目的长期发展

Your support will help us:
- Continuously improve and optimize the code
- Add more features
- Provide better technical support
- Maintain long-term project development

## 📄 许可证 / License

MIT License - 详见 LICENSE 文件

## 🔗 相关链接 / Related Links

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Camoufox 项目](https://github.com/daijro/camoufox)
- [Cloudflare Turnstile 文档](https://developers.cloudflare.com/turnstile/)

---

**⚡ 高性能 | 🚀 易部署 | 🛡️ 稳定可靠 **

**⚡ High Performance | 🚀 Easy Deploy | 🛡️ Stable & Reliable **
