"""
* @project       GeneralQBOT
* @author        XYCode <xycode-xyc@outlook.com>
* @date          2023-05-05 12:54:04
* @lastModified  2023-05-15 12:53:43
"""
import datetime
import mirai.exceptions
import json
from utils import logger, database, message_chain
from handlers import tms
from configs import config, feature
from mirai import *
from mirai.models.message import FlashImage, File, Voice, Quote, Poke
from typing import *

message_rate: Dict[datetime.datetime, Dict[int, int]] = {}
log = logger.get_gq_logger()
test_mode = False

__all__ = ['save_message', 'anti_fc']


async def save_message(event: GroupMessage, bot: Mirai, blocked=False, reason=None):
    if test_mode:
        return 'In Test Mode'
    
    message = database.get_col('message')
    
    message.insert_one(
        {
            'message': event.message_chain.__str__(),
            'message_chain': message_chain.message_chain_to_list(event.message_chain),
            'sender': {
                'id': event.sender.id,
                'name': event.sender.member_name,
                'join_time': event.sender.join_timestamp
            },
            'group': {
                'id': event.group.id,
                'name': event.group.name
            },
            'block': {
                'blocked': blocked,
                'reason': reason
            },
            'send_time': datetime.datetime.now().timestamp(),
            'receiver': {
                'id': bot.qq,
                'is_admin': await bot.is_admin(event.group)
            }
        }
    )


async def check_fc(event: GroupMessage, bot: Mirai, test: bool = False):
    global test_mode
    test_mode = test
    
    date = datetime.datetime.now()
    date = datetime.datetime.fromtimestamp(
        int(date.timestamp()) + (30 - int(date.timestamp()) % 30)
    )

    blocked = False
    reason = None

    print('anti fc', message_rate)

    if date not in message_rate.keys():
        message_rate[date] = {}

    if event.sender.id not in message_rate[date].keys():
        message_rate[date][event.sender.id] = 0

    message_rate[date][event.sender.id] += 1

    if message_rate[date][event.sender.id] > config.ALERT_MESSAGE_RATE:
        if not test:
            await bot.send(event, [
                At(target=event.sender.id),
                Plain(
                    f'你发送的消息超过了管理员设置的 {config.ALERT_MESSAGE_RATE} 条消息每分钟，现在对您进行警告！\n如果您的消息发送速率超过了 {config.MAX_MESSAGE_RATE}，本群将对您禁言 {config.IF_OVER_MAX_MESSAGE_RATE_MUTE_SECONDS / 60} 分钟！')
            ])

        blocked = True
        reason = '警告！超过频率限制'

    if message_rate[date][event.sender.id] > config.MAX_MESSAGE_RATE:
        if not test:
            await bot.send(event, [
                At(target=event.sender.id),
                Plain(
                    f'您发送的消息超过了管理员设置的 {config.MAX_MESSAGE_RATE} 条消息每分钟，现在根据管理员的规定对您禁言 {config.IF_OVER_MAX_MESSAGE_RATE_MUTE_SECONDS / 60} 分钟')
            ])

            await bot.mute(event.group.id, event.sender.id, config.IF_OVER_MAX_MESSAGE_RATE_MUTE_SECONDS)

        blocked = True
        reason = '撤回+禁言！超过频率限制'

    return blocked, reason


async def anti_tms(event: GroupMessage, bot: Mirai):
    if feature.ENABLE_TMS_SERVICER.__len__() > 1:
        log.warning('Do not use more than one TMS Servicer!')

    if feature.Features.TencentTMS in feature.ENABLE_TMS_SERVICER:
        mod = tms.tencent_moderation(str(event.message_chain))
    elif feature.Features.LocalAITMS in feature.ENABLE_TMS_SERVICER:
        mod = tms.ai_moderation(str(event.message_chain))
    else:
        log.error('Cannot find any TMS Servicer!')

    if not mod['bad']:
        blocked = True
        # reason = json.loads(mod['resp'].to_json_string())
        reason = None

        await bot.send(event, [
            Plain('您的聊天记录违反了本群规定，现已被撤回！\n'),
            Plain('根据您的违规情况，我们认为您应该被禁言 {} 分钟'.format(
                mod['resp'].Score / 100 * 10))
        ])

        try:
            await bot.recall(messageId=event.message_chain.message_id, target=event.group.id)
            await bot.mute(event.group.id, event.sender.id, mod['resp'].Score / 100 * 10 * 60)
        except mirai.exceptions.ApiError:
            pass


async def anti_fc(event: GroupMessage, bot: Mirai):
    blocked, reason = await check_fc(event, bot)

    if blocked:
        await bot.send(event, [
            At(target=event.sender.id),
            Plain(f'您发送消息过于频繁，现在对您进行处理，原因：{reason}')
        ])

    await anti_tms(event, bot)

    await save_message(event, bot, blocked, reason)
