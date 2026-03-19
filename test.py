import time
import requests
from loguru import logger
BASE_URL = "http://localhost:8000"
def cf_get_token(max_retry=5, poll_retry=15):
    for attempt in range(max_retry):
        try:
            resp = requests.get(
                f"{BASE_URL}/turnstile",
                params={
                    "url": "https://www.uvwebs.net/",
                    "sitekey": "0x4AAAAAACFv-L5DLSun-lj9"
                },
                timeout=10
            )
            data = resp.json()
            task_id = data.get("task_id")
            if not task_id:
                logger.error(f"创建任务失败: {data}")
                continue
            logger.debug(f"task_id: {task_id}")
            # 2. 轮询结果
            for _ in range(poll_retry):
                try:
                    time.sleep(1)
                    res = requests.get(
                        f"{BASE_URL}/result",
                        params={"id": task_id},
                        timeout=10
                    )
                    if res.status_code != 200:
                        logger.debug(f"验证码解决中: {res.text}")
                        continue
                    result = res.json()
                    # 关键：判断是否完成
                    if result.get("status") == "success":
                        return result
                    elif result.get("status") == "processing":
                        continue
                    else:
                        logger.error(f"任务异常: {result}")
                        break
                except Exception as e:
                    logger.error(f"轮询异常: {e}")
        except Exception as e:
            logger.error(f"创建任务异常: {e}")
    return None

if __name__ == "__main__":
    print(cf_get_token())