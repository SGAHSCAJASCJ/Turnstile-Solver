安装Camoufox：
python -m camoufox fetch

运行脚本（检查脚本以获得更好的设置）：
python api_solver.py

解决旋转门
  GET /turnstile?url=https://example.com&sitekey=0x4AAAAAAA
请求参数：
范围	类型	描述	必需的
url	str	包含验证码的目标 URL。（例如https://example.com）	是的
sitekey	str	需要解决的 CAPTCHA 的站点密钥。（例如0x4AAAAAAA）	是的
action	str	验证码解决过程中触发的操作，例如login
cdata	str	可用于附加 CAPTCHA 参数的自定义数据。
回复：
如果请求成功接收，服务器将响应task_idCAPTCHA 解决任务：

{"task_id":"743291b4-b74b-467b-8b3c-afa1e611f999","status":"accepted"}

获取结果
  GET /result?id=743291b4-b74b-467b-8b3c-afa1e611f999

如果验证码成功解决，服务器将响应以下信息：
{"status":"success",
 "elapsed_time":3.042,
 "value":"0.OEpQGl_Y.......9b14a8cf5dfc2"
}
