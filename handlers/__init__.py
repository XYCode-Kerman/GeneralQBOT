"""
* @project       GeneralQBOT
* @author        XYCode <xycode-xyc@outlook.com>
* @date          2023-05-03 08:34:23
* @lastModified  2023-05-15 12:53:02
"""
import math
import base64
import requests
import pathlib
from configs.config import *
import configs.pictures as pic
import random as rd
import numpy as np
from math import *
from numpy import *
from typing import *
from mirai import *
from EdgeGPT import Chatbot, ConversationStyle

bing_bot = Chatbot(cookie_path=COOKIE_PATH)
count_prompt = 0

__all__ = ['test', 'math_handle', 'hitokoto', 'picture', 'breset', 'bing']

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

async def picture(event: Union[GroupMessage, FriendMessage], bot: Mirai, command: List[str]):
    images = [
        x
        for x in pic.IMAGE_DIR.iterdir()
        if x.is_file()
    ]
    
    image: pathlib.Path = rd.choice(images)
    
    with open(image, 'rb') as f:
        data = f.read()
        b64_data = base64.b64encode(data).decode('utf-8')
    
    await bot.send(event, [
        Plain(f'这是来自 {image.name.replace(".png", "").replace(".jpg", "")} 的图片'),
        Image(base64=b64_data)
    ])

async def breset(event: Union[GroupMessage, FriendMessage], bot: Mirai, command: List[str]):
    global count_prompt, bing_bot
    
    await bing_bot.reset()
    count_prompt = 0
    await bot.send(event, '机器人超过对话次数限制，所有记忆内容已被重置！')

async def bing(event: Union[GroupMessage, FriendMessage], bot: Mirai, command: List[str]):
    global bing_bot, count_prompt
    
    del command[0]
    prompt = ' '.join(command)
    temp_message_id = []
    
    if count_prompt >= 20:
        await breset(event, bot, command)
    
    count_prompt += 1
    
    if ASYNC_RESPONSE:
        try:
            async for res in bing_bot.ask_stream(prompt=prompt, conversation_style=ConversationStyle.creative):
                try:
                    msgs = res[1]['item']['messages']
                    chat = [
                        msg['text']
                        for msg in msgs
                        if msg['author'] == 'bot'
                    ]
                    
                    sugrep = [
                        f"{msgs[1]['suggestedResponses'].index(rsp) + 1}. {rsp['text']}"
                        for rsp in msgs[1]['suggestedResponses']
                    ]
                    
                    chat.append('建议回答：')
                    chat.extend(sugrep)
                    
                    chat = '\n'.join(chat)
                except:
                    chat = res[1]
                
                if chat.__len__() % ASYNC_SEND_CHAR == 0 and chat.__len__() >= 1:
                    if temp_message_id.__len__() >= 1:
                        print(temp_message_id[-1])
                    temp_message_id.append(await bot.send(event, chat))
        except Exception:
            await breset(event, bot, command)
    else:
        temp_message_id.append(await bot.send(event, '正在咨询 New Bing'))
        
        res = bing_bot.ask_stream(prompt=prompt, conversation_style=ConversationStyle.creative)
        msgs = res[1]['item']['messages']
        chat = [
            msg['text']
            for msg in msgs
            if msg['author'] == 'bot'
        ]
        
        sugrep = [
            f"{msgs[1]['suggestedResponses'].index(rsp) + 1}. {rsp['text']}"
            for rsp in msgs[1]['suggestedResponses']
        ]
        
        chat.append('建议回答：')
        chat.extend(sugrep)
        
        chat = '\n'.join(chat)
    
    chat += f'\n对话次数：{count_prompt} / 20'
    
    for id in temp_message_id:
        await bot.recall(target=event.group.id, messageId=id)
    await bot.send(event, chat)