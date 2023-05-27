import datetime
import base64
import configs.config as config
from utils.logger import get_gq_logger
from handlers.cgpt import generate_by_gpt, generate_by_gpt_for_interview
from mirai import Mirai, GroupMessage, FriendMessage
from mirai_extensions.trigger import Trigger, GroupMessageFilter, FriendMessageFilter, InterruptControl
from typing import List, Dict

interview: Dict[int, Dict[str, List[str]]] = {}
logger = get_gq_logger()


async def generate_by_chatgpt_for_a_interviewer(target: int):
    messages = config.INTERVIEW_TIPS_FOR_GPT
    
    messages.extend([
        {'role': 'user', 'content': message}
        for message in interview[target]['messages']
    ])

    messages.extend(
        [
            {'role': 'assistant', 'content': message2}
            for message2 in interview[target]['messages_of_interview_officer']
        ]
    )

    generated = await generate_by_gpt_for_interview(
        messages
    )

    logger.info(f'在对 {target} 面试时的 GPT 回复：{generated}')

    return generated


async def chat_with_interviewer(bot: Mirai, target: int, inc: InterruptControl):
    if target in interview.keys():
        await bot.send_friend_message(target, '您的面试官为 OpenAI 公司的 ChatGPT（gpt-3.5-turbo） 模型，开发者及使用者不能保证 GPT-3.5-Turbo 生成的内容是安全的，所以我们对该模型生成的内容不负有任何责任！')
        await bot.send_friend_message(target, '面试开始，请您如实回答面试官的提问！你有120秒的时间用于思考如何回答面试官的问题！回答超时则判定为不通过！')

        while True:
            @FriendMessageFilter(friend=target)
            def waiter(event_new: FriendMessage):
                logger.info(f'面试者 {target} 输入：{str(event_new.message_chain)}')
                return str(event_new.message_chain)

            answer = await inc.wait(waiter, 120)
            
            interview[target]['messages'].append(answer)

            generated = await generate_by_chatgpt_for_a_interviewer(target)
            await bot.send_friend_message(target, generated)
            
            interview[target]['messages_of_interview_officer'].append(
                    generated)
            
            logger.info(answer)

            if answer is None:
                await bot.send_friend_message(target, '您没有回答，面试结束！您被判定为不通过')
                # remove the interviewer
                interview.pop(target)

                return 'deny'
            elif generated == '.allow':
                await bot.send_friend_message(target, '您通过了面试！')
                # remove the interviewer
                interview.pop(target)

                for qq in config.ADMIN_QQ:
                    await bot.send_friend_message(
                        qq,
                        f"""{target}: 通过了面试。
                        时间：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        面试官：ChatGPT（gpt-3.5-turbo）
                        面试官的最后一条消息：{generated}
                        """
                    )

                return 'allow'
            elif generated == '.deny':
                await bot.send_friend_message(target, '您没有通过面试！')
                # remove the interviewer
                interview.pop(target)

                return 'deny'
            else:

                continue
    else:
        logger.warning('传入了一个不存在的面试对象')

# 此函数用于启动一场面试（管理者指定）
# 命令格式如下：/start_interview <对象QQ号（必须事先添加本机器人）>


async def start_a_interview(event: GroupMessage, bot: Mirai, command: List[str]):
    inc = InterruptControl(bot, priority=14)

    del command[0]
    if command.__len__() == 0:
        await bot.send(event, '请指定对象QQ号')
    else:
        try:
            target = int(command[0])

            # 判断他是否已添加本机器人
            if target in await bot.friend_list():
                await bot.send(event, '请先添加本机器人')

            if target in interview:
                await bot.send(event, '该对象已在面试中')
            else:
                interview[target] = {
                    'interviewee': target,
                    'interviewer': event.sender.id,
                    'messages': [],
                    'messages_of_interview_officer': [],
                    'status': 'interviewing'
                }
                await bot.send(event, '面试已开始')

                if await chat_with_interviewer(bot, target, inc) == 'allow':
                    await bot.send(event, f'{target}: 面试通过')
                else:
                    await bot.send(event, f'{target}: 面试不通过')
        except ValueError:
            await bot.send(event, '对象QQ号格式错误')
