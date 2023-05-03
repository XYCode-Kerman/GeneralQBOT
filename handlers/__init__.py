from typing import *
from mirai import *


async def test(event: Union[GroupMessage, FriendMessage], bot: Mirai):
    await bot.send(event, [Plain('这是一个测试，出现这条消息，说明机器人已经在工作了！')])
