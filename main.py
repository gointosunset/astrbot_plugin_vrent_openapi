from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api import AstrBotConfig
import aiohttp
import re
from urllib.parse import urljoin


@register("openapi", "gointosunset", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        # logger.info(self.config)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command("dd")
    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def dd(self, event: AstrMessageEvent):
        """处理 /dd 指令，调用退款API"""
        message_str = event.message_str  # 用户发的纯文本消息字符串
        parts = message_str.strip().split()
        if len(parts) < 2:
            yield event.plain_result("格式错误。正确格式：/dd 单号")
            return

        tno = parts[1]
        logger.info(f"解析参数: tno={tno}")

        # 构建请求数据
        payload = {"tno": tno}

        # 检查配置
        base_url = getattr(self.config, "Base_Url", None)
        if not base_url:
            yield event.plain_result("/dd 插件尚未配置，请先完成配置")
            return

        path = "/j2ee/merctx/openapi/robotic/dd"
        full_url = urljoin(base_url, path)
        headers = {"Content-Type": "application/json"}

        # 可选添加 Token
        apikey = getattr(self.config, "X-API-Key", None)
        if apikey:
            headers["X-API-Key"] = f"{apikey}"

        logger.info(f"发送请求到 {full_url}, payload={payload}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    full_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"API响应: {result}")
                        if result.get("code") == 200:
                            yield event.plain_result(result.get("message", "操作成功"))
                        else:
                            yield event.plain_result(
                                f"API返回错误：{result.get('message', '未知错误')}"
                            )
                    else:
                        yield event.plain_result(f"HTTP错误 {response.status}")
        except aiohttp.ClientError as e:
            yield event.plain_result(f"网络请求失败：{str(e)}")
        except Exception as e:
            yield event.plain_result(f"处理失败：{str(e)}")

    @filter.command("tk")
    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def tk(self, event: AstrMessageEvent):
        """处理 /tk 指令，调用退款API"""
        message_str = event.message_str  # 用户发的纯文本消息字符串
        parts = message_str.strip().split()
        if len(parts) < 4:
            yield event.plain_result("格式错误。正确格式：/tk 单号 金额 原因")
            return

        tno = parts[1]
        amount_str = parts[2]
        reason = " ".join(parts[3:])

        # 提取金额数字
        amount_match = re.search(r"\d+", amount_str)
        if not amount_match:
            yield event.plain_result("金额格式错误，请包含数字")
            return
        amount = int(amount_match.group())
        logger.info(f"解析参数: tno={tno}, amount={amount}, reason={reason}")

        # 构建请求数据
        payload = {"tno": tno, "amount": amount, "reason": reason}

        # 检查配置
        base_url = getattr(self.config, "Base_Url", None)
        if not base_url:
            yield event.plain_result("/tk 插件尚未配置，请先完成配置")
            return

        path = "/j2ee/merctx/openapi/robotic/dd"
        full_url = urljoin(base_url, path)
        headers = {"Content-Type": "application/json"}

        # 可选添加 Token
        apikey = getattr(self.config, "X-API-Key", None)
        if apikey:
            headers["X-API-Key"] = f"{apikey}"

        logger.info(f"发送请求到 {full_url}, payload={payload}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    full_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"API响应: {result}")
                        if result.get("code") == 200:
                            yield event.plain_result(result.get("message", "操作成功"))
                        else:
                            yield event.plain_result(
                                f"API返回错误：{result.get('message', '未知错误')}"
                            )
                    else:
                        yield event.plain_result(f"HTTP错误 {response.status}")
        except aiohttp.ClientError as e:
            yield event.plain_result(f"网络请求失败：{str(e)}")
        except Exception as e:
            yield event.plain_result(f"处理失败：{str(e)}")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
