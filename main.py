"""
* @project       GeneralQBOT
* @author        XYCode <xycode-xyc@outlook.com>
* @date          2023-05-01 23:32:16
* @lastModified  2023-05-15 22:37:07
"""
import shlex
import multiprocessing
import manager
import handlers.tms
import handlers.group_wordcloud
import handlers.anti_flippedscreen
import handlers.interview
import handlers.join_group
import handlers.integral
import handlers.games.guess_numbers
import handlers.cgpt
import handlers.pixiv.listener
import handlers.pixiv.manager
import handlers.ai_features.fake_lovers
import datetime
import jwt
import threading
from configs import config, feature
from handlers import *
from mirai import *
from mirai.models.events import MemberJoinRequestEvent
from typing import *
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import traceback
import pymongo
import openai
from utils.logger import get_gq_logger

bot = Mirai(qq=config.BOT_QQ, adapter=WebSocketAdapter(
    verify_key=config.API_VERIFY_KEY, host=config.API_HOST, port=config.API_PORT))

mongo = pymongo.MongoClient(config.DATABASE_IP, config.DATABASE_PORT)
logger = get_gq_logger()

if config.DATABASE_NAME not in [x['name'] for x in mongo.list_databases()]:
    print(config.DATABASE_NAME, "doesn't exists, will create")

db = mongo[config.DATABASE_NAME]

openai.api_key = config.OPENAI_KEY

listening = []

if '__main__' == __name__:
    def member_check(event: GroupMessage):
        usercol = db['userdata']

        data = usercol.find({
            'id': event.sender.id
        })

        data = [
            x['id']
            for x in data
        ]

        if event.sender.id not in data:
            usercol.insert_one({
                'id': event.sender.id,
                'name': event.sender.member_name,
                'integral': 0,
                'last_checkin': datetime.datetime.now()
            })

    @bot.on(GroupMessage)
    async def group_message(event: GroupMessage):
        try:
            if event.group.id in config.GROUP:
                # 反不良信息
                await handlers.anti_flippedscreen.anti_fc(event, bot)

                # 自动注册
                member_check(event)

                # 判断是否为机器人指令
                if str(event.message_chain).startswith(config.STARTS_WITH):
                    # 解析
                    message = str(event.message_chain)[1:]
                    print(message)
                    command = shlex.split(message)

                    if command[0] == 'test' or command[0] == '测试':
                        await test(event, bot, command)
                    elif command[0] == 'math' or command[0] == '数学':
                        await math_handle(event, bot, command)
                    elif command[0] == 'hitokoto' or command[0] == '一言':
                        await hitokoto(event, bot, command)
                    elif command[0] == 'picture' or command[0] == '图片':
                        await picture(event, bot, command)
                    elif command[0] == 'bing' or command[0] == '必应':
                        await bing(event, bot, command)
                    elif command[0] == 'breset' or command[0] == '重置':
                        await breset(event, bot, command)
                    elif command[0] == 'integral' or command[0] == '积分':
                        await handlers.integral.integral(event, bot, command)
                    elif command[0] == 'game' or command[0] == '游戏':
                        if command[1] == 'guess_numbers' or command[1] == '猜数字':
                            await handlers.games.guess_numbers.guess_numbers(event, bot, command)
                    elif command[0] == 'pixiv' or command[0] == 'P站':
                        await handlers.pixiv.manager.manager(event, bot, command)
                    elif command[0] == 'wordcloud' or command[0] == '词云':
                        await handlers.group_wordcloud.handle_message(event, bot, command)
        
                # 判断是否为管理员指令
                if str(event.message_chain).startswith(config.ADMIN_COMMAND_STARTS_WITH):
                    if event.sender.id in config.ADMIN_QQ:
                        # 解析
                        message = str(event.message_chain)[1:]
                        print(message)
                        command = shlex.split(message)
                        
                        if command[0] == 'start_interview':
                            await handlers.interview.start_a_interview(event, bot, command)
                        elif command[0] == 'get_join_key':
                            await handlers.join_group.get_join_key(event, bot, command)
                    else:
                        await bot.send(event, '您无权使用！')
        except Exception as e:
            exc = traceback.format_exc()

            if feature.Features.Fun_Log in feature.ENABLED_FEATURE:
                content = await handlers.cgpt.generate_by_gpt('以下是一个Python语言的报错，请使用幽默且通俗易懂提示用户这个错误。要求表述完整，并为产生这个错误表示深深的歉意，不超过50字', exc)

                await bot.send(event, '[趣味日志] ' + content)
            
            if feature.Features.Raw_Log in feature.ENABLED_FEATURE:
                await bot.send(event, '[原始日志] ' + exc)

            logger.error(exc)

    @bot.on(MemberJoinRequestEvent)
    async def member_join_request(event: MemberJoinRequestEvent):
        decoded = {}
        inp = event.message.split('\n')[-1].replace('答案：', '')
        print(inp)
        data: dict = db['join_keys'].find_one({'key': inp})

        if data is None:
            await bot.decline(event, '不符合要求的 token！请重新申请！')
            return

        target: int = data.get('target', None)
        exp_time: datetime.datetime = decoded.get('exp_time', None)

        # if exp_time < datetime.datetime.now():
        #     await bot.decline(event, 'token 过期，请找管理员重新获取！')
        # elif target != event.from_id:
        #     await bot.decline(event, '你正在盗用他人的 token，禁止加入本群！')
        #     for admin in config.ADMIN_QQ:
        #         await bot.send_friend_message(admin, f'{event.from_id} 正在盗用 token 以加入 {event.group_id}')
        # else:
        await bot.allow(event, '欢迎进入本群！')
        print('allowed')

    @bot.on(FriendMessage)
    async def friend_message(event: FriendMessage):
        command = event.message_chain.__str__()
        if command.startswith(config.STARTS_WITH):
            command = shlex.split(command[1:])
        
            if command[0] == 'fake_lover':
                await handlers.ai_features.fake_lovers.handler(event, bot, command)

    # 定时任务
    scheduler = AsyncIOScheduler()

    @scheduler.scheduled_job(config.TIMER_TRIGGER)
    async def timer():
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            temperature=1,
            messages=[
                {'role': 'system', 'content': f'现在是 20{datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")}'},
                {'role': 'user', 'content': '写一句不超过 25 字的话，内容不限，结合当前时间提醒用户'}
            ]
        )

        content = response.choices[0].message["content"]

        for group in config.GROUP:
            await bot.send_group_message(group, '[定时提醒] ' + content)

    async def start_listeners():
        listeners = db['listeners']
        listeners = list(listeners.find({}))

        global listening

        # when listeners col isn't exists
        if len(listeners) == 0:
            listeners = [
                {
                    'target': 'test_only',
                    'type': 'test_only',
                    'name': 'test_only',
                    'trigger_rate': '* * * * *'
                }
            ]

            for listener in listeners:
                db['listeners'].insert_one(listener)

        for listener in listeners:
            if listener['target'] == 'pixiv':
                listener = handlers.pixiv.listener.PixivListener(
                    type=listener['type'],
                    api_url='test',
                    name=listener['name'],
                    scheduler=scheduler,
                    bot=bot,
                    trigger_rate=CronTrigger.from_crontab(
                        listener['trigger_rate'])
                )

                listening.append(listener)
            else:
                logger.warning(f'未知的监听器类型：{listener["target"]}')

    async def restart_listeners():
        # stop all listeners
        for listener in listening:
            listener.stop()
            listening.remove(listener)

        # start all listeners
        await start_listeners()

    @bot.on(Startup)
    async def startup(event: Startup):
        if feature.Features.Startup_Tips in feature.ENABLED_FEATURE:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                temperature=1,
                messages=[
                    {'role': 'system', 'content': f'现在是 20{datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")}'},
                    {'role': 'user', 'content': '写一句不超过 25 字的话，你将作为本群的机器人，使用有创意的语言，提醒用户你已经上线'}
                ]
            )

            content = response.choices[0].message["content"]

            for group in config.GROUP:
                try:
                    await bot.send_group_message(group, '[趣味日志] ' + content)
                    await bot.send_group_message(group, f'[免责声明] 本机器人所有的 [定时提醒] [趣味日志] 均由 OpenAI 公司的 gpt-3.5-turbo 模型生成，本人不对其负有任何责任')
                except:
                    logger.error(f'发送启动消息失败：{group}')
                    logger.error(traceback.format_exc())

        # pixiv_listener = handlers.pixiv.listener.PixivListener('tag', 'test', 'girl', CronTrigger(minute='*', second=30), scheduler, bot)
        await start_listeners()
        
        if feature.Features.RemoteManager in feature.ENABLED_FEATURE:
            logger.info('Flask server starting')
            logger.error('远程管理系统已被弃用')
            logger.info('Skip to start flask server, because it is out of date')
            # flask = multiprocessing.Process(target=manager.run, daemon=True, args=(bot, config.REMOTE_MANAGER_HOST, config.REMOTE_MANAGER_PORT, config.REMOTE_MANAGER_DEBUG, ))
            # flask.start()
            # logger.info('Flask server started')
        else:
            logger.info('Skip to start Flask server, because it is disabled')

        scheduler.start()

    @bot.on(Shutdown)
    async def shutdown(event: Shutdown):
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            temperature=1,
            messages=[
                {'role': 'system', 'content': f'现在是 20{datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")}'},
                {'role': 'user', 'content': '写一句不超过 25 字的话，你将作为本群的机器人，使用有创意的语言，提醒用户你已经下线'}
            ]
        )

        content = response.choices[0].message["content"]

        for group in config.GROUP:
            await bot.send_group_message(group, '[趣味日志] ' + content)

        scheduler.shutdown(True)

    bot.run()
