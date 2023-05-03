import math
import numpy as np
from math import *
from numpy import *
from typing import *
from mirai import *

async def test(event: Union[GroupMessage, FriendMessage], bot: Mirai, command: List[str]):
    await bot.send(event, [Plain('这是一个测试，出现这条消息，说明机器人已经在工作了！')])
    
async def math_handle(event: GroupMessage, bot: Mirai, command: List[str]):
    del command[0]
    result = str(
        eval(''.join(command))
    )
    
    await bot.send(event, f'{" ".join(command)[0:5]}... 的计算结果为：{result}')
