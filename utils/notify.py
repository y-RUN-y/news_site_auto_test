import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Literal, Optional

import urllib.request
import urllib.error


logger = logging.getLogger(__name__)


class NotifyManager:
    """通知管理器，支持企业微信、钉钉、飞书机器人"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.webhook_url = self.config.get("webhook_url", "")
        self.webhook_type = self.config.get("webhook_type", "wechat").lower()
        self.mentioned_mobile_list = self.config.get("mentioned_mobile_list", [])

    def send(self, message: Dict) -> bool:
        """发送通知"""
        if not self.webhook_url:
            logger.warning("未配置 webhook_url，跳过通知")
            return False

        try:
            if self.webhook_type in ("wechat", "qywx", "企微"):
                return self._send_wechat(message)
            elif self.webhook_type in ("dingtalk", "dingding", "钉钉"):
                return self._send_dingtalk(message)
            elif self.webhook_type in ("lark", "feishu", "飞书"):
                return self._send_lark(message)
            else:
                logger.error(f"不支持的 webhook 类型: {self.webhook_type}")
                return False
        except Exception as e:
            logger.error(f"发送通知失败: {e}")
            return False

    def _send_wechat(self, message: Dict) -> bool:
        """发送企业微信机器人消息"""
        msg = {
            "msgtype": "markdown",
            "markdown": {
                "content": self._format_wechat_content(message),
            },
        }
        if self.mentioned_mobile_list:
            msg["markdown"]["mentioned_mobile_list"] = self.mentioned_mobile_list
        return self._send_webhook(msg)

    def _send_dingtalk(self, message: Dict) -> bool:
        """发送钉钉机器人消息"""
        msg = {
            "msgtype": "markdown",
            "markdown": {
                "title": message.get("title", "CI 通知"),
                "text": self._format_dingtalk_content(message),
            },
        }
        at_mobiles = {"atMobiles": self.mentioned_mobile_list} if self.mentioned_mobile_list else {}
        msg.update(at_mobiles)
        return self._send_webhook(msg)

    def _send_lark(self, message: Dict) -> bool:
        """发送飞书机器人消息"""
        msg = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {"tag": "plain_text", "content": message.get("title", "CI 通知")},
                    "template": "red" if "失败" in message.get("message", "") else "green",
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": self._format_lark_content(message),
                        },
                    }
                ],
            },
        }
        return self._send_webhook(msg)

    def _format_wechat_content(self, message: Dict) -> str:
        """格式化企业微信消息内容"""
        status_emoji = "✅" if "成功" in message.get("message", "") else "❌"
        content = f"### {status_emoji} {message.get('title', 'CI 通知')}\n\n"
        content += f"**项目**: {message.get('project', 'N/A')}\n"
        content += f"**分支**: {message.get('branch', 'N/A')}\n"
        content += f"**提交**: `{message.get('commit', 'N/A')}`\n"
        content += f"**任务**: {message.get('job', 'N/A')}\n"
        content += f"**消息**: {message.get('message', 'N/A')}\n"
        if message.get("url"):
            content += f"**链接**: [查看详情]({message.get('url')})\n"
        content += f"\n> 构建时间: {message.get('time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}"
        return content

    def _format_dingtalk_content(self, message: Dict) -> str:
        """格式化钉钉消息内容"""
        status_emoji = "✅" if "成功" in message.get("message", "") else "❌"
        content = f"### {status_emoji} {message.get('title', 'CI 通知')}\n\n"
        content += f"**项目**: {message.get('project', 'N/A')}\n"
        content += f"**分支**: {message.get('branch', 'N/A')}\n"
        content += f"**提交**: `{message.get('commit', 'N/A')}`\n"
        content += f"**任务**: {message.get('job', 'N/A')}\n"
        content += f"**消息**: {message.get('message', 'N/A')}\n"
        if message.get("url"):
            content += f"**链接**: [查看详情]({message.get('url')})\n"
        return content

    def _format_lark_content(self, message: Dict) -> str:
        """格式化飞书消息内容"""
        status_emoji = "✅" if "成功" in message.get("message", "") else "❌"
        content = f"**{status_emoji} {message.get('title', 'CI 通知')}**\n\n"
        content += f"**项目**: {message.get('project', 'N/A')}\n"
        content += f"**分支**: {message.get('branch', 'N/A')}\n"
        content += f"**提交**: `{message.get('commit', 'N/A')}`\n"
        content += f"**任务**: {message.get('job', 'N/A')}\n"
        content += f"**消息**: {message.get('message', 'N/A')}\n"
        if message.get("url"):
            content += f"**链接**: {message.get('url')}\n"
        return content

    def _send_webhook(self, payload: Dict) -> bool:
        """发送 webhook 请求"""
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode("utf-8"))
                if result.get("errcode") == 0:
                    logger.info("通知发送成功")
                    return True
                else:
                    logger.error(f"通知发送失败: {result}")
                    return False
        except urllib.error.URLError as e:
            logger.error(f"Webhook 请求失败: {e}")
            return False
        except Exception as e:
            logger.error(f"发送通知时发生错误: {e}")
            return False


def create_from_env() -> NotifyManager:
    """从环境变量创建通知管理器"""
    config = {
        "webhook_url": os.environ.get("NOTIFY_WEBHOOK_URL", ""),
        "webhook_type": os.environ.get("NOTIFY_TYPE", "wechat"),
        "mentioned_mobile_list": os.environ.get("MENTIONED_MOBILE", "").split(","),
    }
    return NotifyManager(config)


def notify_build_status(
    status: Literal["success", "failed", "skipped"],
    project: str,
    branch: str,
    commit: str,
    job: str,
    build_url: str,
    message: str = "",
):
    """便捷的通知函数"""
    if not message:
        if status == "success":
            message = "测试通过 ✅"
        elif status == "failed":
            message = "测试失败 ❌"
        else:
            message = "测试跳过 ⏭️"

    notify = create_from_env()
    return notify.send(
        {
            "title": f"CI 构建{status}",
            "project": project,
            "branch": branch,
            "commit": commit,
            "job": job,
            "url": build_url,
            "message": message,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )