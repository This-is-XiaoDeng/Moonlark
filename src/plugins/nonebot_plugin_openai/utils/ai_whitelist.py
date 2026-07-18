"""
AI 功能白名单工具函数
管理哪些群聊可以使用 AI 功能（仅针对 QQ 官方 Bot）
"""

from typing import Any

from nonebot.adapters import Bot
from nonebot.adapters.qq import Bot as QQBot
from nonebot.params import Depends
from nonebot_plugin_larkutils import get_group_id as _get_group_id
from nonebot_plugin_orm import get_session
from sqlalchemy import select

from ..models import AIWhitelist


async def is_ai_enabled_for_group(bot: Bot, group_id: str) -> bool:
    """检查指定群聊是否可以使用 AI 功能

    规则：
    1. 群聊在白名单中且已启用 -> True
    2. QQ 官方 Bot 且不在白名单中 -> False
    3. 其他情况 -> True
    """
    async with get_session() as session:
        result = await session.scalar(select(AIWhitelist).where(AIWhitelist.group_id == group_id))
        if result is not None and result.enabled:
            return True
    return not isinstance(bot, QQBot)


async def _check_ai_enabled(bot: Bot, group_id: str = _get_group_id()) -> bool:
    return await is_ai_enabled_for_group(bot, group_id)


def check_ai_enabled() -> Any:
    """检查 AI 功能是否可用（依赖注入）"""
    return Depends(_check_ai_enabled)
