import math
import requests
import numpy as np
from math import *
from numpy import *
from typing import *
from mirai import *

async def test(event: Union[GroupMessage, FriendMessage], bot: Mirai, command: List[str]):
    await bot.send(event, [Plain('这是一个测试，出现这条消息，说明机器人已经在工作了！')])
    
async def math_handle(event: GroupMessage, bot: Mirai, command: List[str]):
    del command[0]
    print(command[0])
    result = str(
        eval(command[0])
    )
    
    await bot.send(event, f'{" ".join(command)[0:5]}... 的计算结果为：{result}')

async def hitokoto(event: GroupMessage, bot: Mirai, command: List[str]):
    del command[0]
    
    command.append(0)
    command.append(30)
    
    type_nl = command[0]
    min_length = int(command[1])
    max_length = int(command[2])
    
    tmp1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
    tmp2 = ['动画', '漫画', '游戏', '文学', '原创', '来自网络', '其他', '影视', '诗词', '网易云', '哲学', '抖机灵']
    nl2hitokoto = {}
    for key, value in zip(tmp2, tmp1):
        nl2hitokoto[key] = value

    req = requests.get(f'https://v1.hitokoto.cn?c={nl2hitokoto[type_nl]}&min_length={min_length}&max_length={max_length}')
    data = req.json()
    
    await bot.send(event, f'{data["hitokoto"]}\n——  {data["from_who"]}《{data["from"]}》')
