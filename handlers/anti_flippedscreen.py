import datetime
from configs import config
from mirai import *
from typing import *

message_rate: Dict[datetime.datetime, Dict[int, int]] = {}

async def anti_fc(event: GroupMessage, bot: Mirai):
    date = datetime.datetime.now()
    date = datetime.datetime.fromtimestamp(
        int(date.timestamp()) + (30 - int(date.timestamp()) % 30)
    )
    
    print('anti fc', message_rate)
    
    if date not in message_rate.keys():
        message_rate[date] = {}
    
    if event.sender.id not in message_rate[date].keys():
        message_rate[date][event.sender.id] = 0
    
    message_rate[date][event.sender.id] += 1
    
    if message_rate[date][event.sender.id] > config.ALERT_MESSAGE_RATE:
        await bot.send(event, [
            At(target=event.sender.id),
            Plain(f'你发送的消息超过了管理员设置的 {config.ALERT_MESSAGE_RATE} 条消息每分钟，现在对您进行警告！\n如果您的消息发送速率超过了 {config.MAX_MESSAGE_RATE}，本群将对您禁言 {config.IF_OVER_MAX_MESSAGE_RATE_MUTE_SECONDS / 60} 分钟！')
        ])
    
    if message_rate[date][event.sender.id] > config.MAX_MESSAGE_RATE:
        await bot.send(event, [
            At(target=event.sender.id),
            Plain(f'您发送的消息超过了管理员设置的 {config.MAX_MESSAGE_RATE} 条消息每分钟，现在根据管理员的规定对您禁言 {config.IF_OVER_MAX_MESSAGE_RATE_MUTE_SECONDS / 60} 分钟')
        ])
        
        await bot.mute(event.group.id, event.sender.id, config.IF_OVER_MAX_MESSAGE_RATE_MUTE_SECONDS)