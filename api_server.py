import time
import uuid
import asyncio
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from camoufox import DefaultAddons
from camoufox.async_api import AsyncCamoufox
import uvicorn
class TurnstileAPIServer:
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>body's solver</title>
        <script src="https://challenges.cloudflare.com/turnstile/v0/api.js?onload=onloadTurnstileCallback" async="" defer=""></script>
    </head>
    <body>
        <!-- cf turnstile -->
        <p id="ip-display"></p>
    </body>
    </html>
    """

    def __init__(self, headless: bool,  thread: int, page_count: int, proxy_support: bool):
        self.app = FastAPI()
        self.headless = headless
        self.thread_count = thread
        self.page_count = page_count
        self.proxy_support = proxy_support
        self.page_pool = asyncio.Queue()
        # 浏览器启动参数配置
        self.browser_args = [
            "--no-sandbox",  # 关闭沙箱，部分环境必要
            "--disable-setuid-sandbox",  # 配合 no-sandbox
        ]
        self.camoufox = None  # Camoufox实例
        self.results = {}  # 任务结果存储
        self.proxies = []  # 代理列表
        self.max_task_num = self.thread_count * self.page_count
        self.current_task_num = 0
        # 注册启动和关闭事件
        self.app.add_event_handler("startup", self._startup)
        self.app.add_event_handler("shutdown", self._shutdown)
        self.app.get("/turnstile")(self.process_turnstile)
        self.app.get("/result")(self.get_result)

    async def _cleanup_results(self):
        """定期清理过期结果"""
        while True:
            await asyncio.sleep(3600)  # 每小时清理
            expired = [
                tid for tid, res in self.results.items()
                if isinstance(res, dict) and res.get("status") == "error"
                   and time.time() - res.get("start_time", 0) > 3600
            ]
            for tid in expired:
                self.results.pop(tid, None)
                logger.debug(f"清理过期任务: {tid}")

    async def _periodic_cleanup(self, interval_minutes: int = 60):
        """定期逐个清理并重建页面，避免任务阻塞"""
        while True:
            await asyncio.sleep(interval_minutes * 60)
            logger.info("开始逐个清理页面缓存和上下文")

            total = self.max_task_num
            success = 0
            for _ in range(total):
                try:
                    # 尝试从池子中取出一个页面（说明它此刻空闲）
                    page, context= await self.page_pool.get()
                    try:
                        await page.close()
                    except:
                        pass
                    try:
                        await context.close()
                    except Exception as e:
                        logger.warning(f"清理页面时出错: {e}")

                    context = await self._create_context_with_proxy()
                    page = await context.new_page()
                    await self.page_pool.put((page, context))
                    success += 1
                    await asyncio.sleep(1.5)  # 等待片刻，避免连锁冲击
                except Exception as e:
                    logger.warning(f"清理重建页面失败: {e}")
                    continue
            logger.success(f"定期清理完成，共处理 {success}/{total} 个页面")

    async def _startup(self) -> None:
        """Initialize the browser and page pool on startup."""
        logger.info("开始初始化浏览器")
        try:
            await self._initialize_browser()
        except Exception as e:
            logger.error(f"浏览器初始化失败: {str(e)}")
            raise

    async def _shutdown(self) -> None:
        """关闭时清理所有浏览器资源"""
        logger.info("开始清理浏览器资源")
        try:
            await self.browser.close()
        except Exception as e:
            logger.warning(f"关闭浏览器时异常: {e}")
        logger.success("所有浏览器资源已清理")

    async def _create_context_with_proxy(self ,proxy:str=None):
        """根据代理创建浏览器上下文"""
        if not proxy:
            return await self.browser.new_context()

        parts = proxy.split(':')
        if len(parts) == 3:
            return await self.browser.new_context(proxy={"server": proxy})
        elif len(parts) == 5:
            # 格式: scheme:ip:port:username:password
            proxy_scheme, proxy_ip, proxy_port, proxy_user, proxy_pass = parts
            return await self.browser.new_context(
                proxy={
                    "server": f"{proxy_scheme}://{proxy_ip}:{proxy_port}",
                    "username": proxy_user,
                    "password": proxy_pass
                }
            )
        else:
            logger.warning(f"无效的代理格式: {proxy}，使用无代理上下文")
            return await self.browser.new_context()

    async def _initialize_browser(self):
        self.camoufox = AsyncCamoufox(
            headless=self.headless,
            exclude_addons=[DefaultAddons.UBO],
            args=self.browser_args
        )
        self.browser = await self.camoufox.start()

        # 创建页面池
        for _ in range(self.thread_count):
            context = await self._create_context_with_proxy()
            for _ in range(self.page_count):
                page = await context.new_page()
                await self.page_pool.put((page, context))

        logger.success(f"页面池初始化完成，包含 {self.page_pool.qsize()} 个页面")
        asyncio.create_task(self._cleanup_results())  # 清理任务结果
        asyncio.create_task(self._periodic_cleanup())  # 定期清理页面缓存和上下文

    async def _solve_turnstile(self, task_id: str, url: str, sitekey: str, action: str = None, cdata: str = None):
        """使用页面池中的页面解决 Turnstile 验证码"""
        start_time = time.time()
        page, context = await self.page_pool.get()
        try:
            url_with_slash = url + "/" if not url.endswith("/") else url
            turnstile_div = (f'<div class="cf-turnstile" style="background: white;" data-sitekey="{sitekey}"' +
                             (f' data-action="{action}"' if action else '') +
                             (f' data-cdata="{cdata}"' if cdata else '') + '></div>')
            page_data = self.HTML_TEMPLATE.replace("<!-- cf turnstile -->", turnstile_div)
            await page.route(url_with_slash, lambda route: route.fulfill(body=page_data, status=200))
            await page.goto(url_with_slash)
            await page.eval_on_selector("//div[@class='cf-turnstile']", "el => el.style.width = '70px'")

            # 尝试解决验证码，最多30次尝试
            for attempt in range(30):
                try:
                    # 检查验证码响应值
                    turnstile_check = await page.input_value("[name=cf-turnstile-response]", timeout=400)
                    if turnstile_check == "":
                        # 如果响应为空，点击验证码元素触发验证
                        await page.locator("//div[@class='cf-turnstile']").click(timeout=400)
                        await asyncio.sleep(0.2)
                    else:
                        # 验证码解决成功
                        elapsed_time = round(time.time() - start_time, 3)
                        self.results[task_id] = {
                            "status": 'success',
                            "elapsed_time": elapsed_time,
                            "value": turnstile_check
                        }
                        logger.info(f"验证码解决成功，任务ID: {task_id}，耗时: {elapsed_time}秒")
                        break
                except Exception as e:
                    # 单次尝试失败，继续下一次尝试
                    logger.debug(f"验证码尝试 {attempt + 1} 失败: {e}")

            # 如果所有尝试都失败，标记为错误
            if self.results.get(task_id) == {"status": "process", "message": 'solving captcha'}:
                elapsed_time = round(time.time() - start_time, 3)
                self.results[task_id] = {
                    "status": "error",
                    "elapsed_time": elapsed_time,
                    "value": "captcha_fail"
                }
                logger.warning(f"验证码解决失败，任务ID: {task_id}，耗时: {elapsed_time}秒")

        except Exception as e:
            # 处理异常情况
            elapsed_time = round(time.time() - start_time, 3)
            self.results[task_id] = {
                "status": "error",
                "elapsed_time": elapsed_time,
                "value": "captcha_fail"
            }
            logger.error(f"验证码求解异常，任务ID: {task_id}: {e}")
        finally:
            # 减少当前任务计数并将页面返回池中
            self.current_task_num -= 1
            await self.page_pool.put((page, context))

    async def process_turnstile(self, url: str = Query(...), sitekey: str = Query(...), action: str = Query(None),
                                cdata: str = Query(None)):
        """处理 /turnstile 端点请求"""
        # 参数验证
        if not url or not sitekey:
            raise HTTPException(
                status_code=400,
                detail={"status": "error", "error": "必须提供 'url' 和 'sitekey' 参数"}
            )

        # 检查服务器负载
        if self.current_task_num >= self.max_task_num:
            logger.warning(f"服务器负载已满，当前任务数: {self.current_task_num}/{self.max_task_num}")
            return JSONResponse(
                content={"status": "error", "error": "服务器已达到最大性能，请稍后重试"},
                status_code=429
            )

        # 生成唯一任务ID
        task_id = str(uuid.uuid4())
        logger.info(f"接收新任务，task_id: {task_id}, url: {url}, sitekey: {sitekey}")

        # 初始化任务状态
        self.results[task_id] = {
            "status": "process",
            "message": 'solving captcha',
            "start_time": time.time()
        }

        try:
            # 创建异步任务处理验证码
            asyncio.create_task(
                self._solve_turnstile(
                    task_id=task_id,
                    url=url,
                    sitekey=sitekey,
                    action=action,
                    cdata=cdata
                )
            )
            self.current_task_num += 1
            return JSONResponse(
                content={"task_id": task_id, "status": "accepted"},
                status_code=202
            )
        except Exception as e:
            logger.error(f"处理请求时发生意外错误: {str(e)}")
            # 清理失败的任务
            self.results.pop(task_id, None)
            return JSONResponse(
                content={"status": "error", "message": f"服务器内部错误: {str(e)}"},
                status_code=500
            )

    async def get_result(self, task_id: str = Query(..., alias="id")):
        """返回验证码解决结果"""
        # 参数验证
        if not task_id:
            return JSONResponse(
                content={"status": "error", "message": "缺少task_id参数"},
                status_code=400
            )

        # 检查任务是否存在
        if task_id not in self.results:
            return JSONResponse(
                content={"status": "error", "message": "无效的task_id或任务已过期"},
                status_code=404
            )

        result = self.results[task_id]

        # 检查任务是否仍在处理中
        if result.get("status") == "process":
            # 检查任务是否超时（超过5分钟）
            start_time = result.get("start_time", time.time())
            if time.time() - start_time > 300:  # 5分钟超时
                self.results[task_id] = {
                    "status": "error",
                    "elapsed_time": round(time.time() - start_time, 3),
                    "value": "timeout",
                    "message": "任务超时"
                }
                result = self.results[task_id]
            else:
                # 任务仍在处理中，返回处理状态
                return JSONResponse(content=result, status_code=202)

        # 任务已完成，返回结果并清理
        result = self.results.pop(task_id)

        # 根据结果状态设置HTTP状态码
        if result.get("status") == "success":
            status_code = 200
        elif result.get("value") == "timeout":
            status_code = 408  # Request Timeout
        elif "captcha_fail" in result.get("value", ""):
            status_code = 422  # Unprocessable Entity
        else:
            status_code = 500  # Internal Server Error

        return JSONResponse(content=result, status_code=status_code)
def create_app(headless: bool, thread: int, page_count: int,proxy_support: bool) -> FastAPI:
    server = TurnstileAPIServer(headless=headless,thread=thread, page_count=page_count, proxy_support=proxy_support)
    return server.app

if __name__ == '__main__':
    headless = True
    # 浏览器实例数量(线程数，最大不要超过cpu核心数)
    thread = 2
    # 每个浏览器实例的页面数量(高性能cpu勿动)
    page_count = 1
    # 是否启用代理支持
    proxy_support = False
    # 绑定主机
    host = "0.0.0.0"
    # 绑定端口
    port = 8000
    app = create_app(headless=headless,thread=thread,page_count=page_count, proxy_support=proxy_support)
    uvicorn.run(app, host=host, port=port)
