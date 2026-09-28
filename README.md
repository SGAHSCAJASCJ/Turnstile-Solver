# Turnstile CAPTCHA Solver

## Quick Start


### Environmental Requirements


- Python 3.8+
- Windows / Linux / macOS
- 1 GB RAM

### Install

```bash
pip install fastapi uvicorn camoufox loguru
python -m camoufox fetch
```

### Config

edit `api_server.py`：

```python
headless = True 
thread = 2      
page_count = 1   

host = "0.0.0.0"
port = 8000
```

### Start

```bash
python api_server.py
```

## API

### Submit task

```http
GET /turnstile?url=https://example.com&sitekey=0x4AAAAAAA...
```

```json
{
  "task_id": "uuid-string",
  "status": "accepted"
}
```

### Search Results

```http
GET /result?id=task_id
```

```json
{
  "status": "success",
  "elapsed_time": 3.245,
  "value": "turnstile-response-token"
}
```

**High Performance · Easy to Deploy · Stable and Reliable**

Need a faster, enterprise-grade protocol-level solution? Contact me on Telegram at @Lu_mingfeihuizhang to purchase the source code or lease the API.
