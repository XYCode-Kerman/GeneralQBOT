"""
* @project       GeneralQBOT
* @author        XYCode <xycode-xyc@outlook.com>
* @date          2023-05-01 23:32:16
* @lastModified  2023-05-14 17:22:05
"""
import shlex
import handlers.tms
import handlers.anti_flippedscreen
import handlers.join_group
import handlers.integral
import handlers.cgpt
import datetime
import jwt
from configs import config
from handlers import *
from mirai import *
from mirai.models.events import MemberJoinRequestEvent
from typing import *
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import traceback
import pymongo
import openai

bot = Mirai(qq=config.BOT_QQ, adapter=WebSocketAdapter(verify_key=config.API_VERIFY_KEY, host=config.API_HOST, port=config.API_PORT))

mongo = pymongo.MongoClient(config.DATABASE_IP, config.DATABASE_PORT)

if config.DATABASE_NAME not in [x['name'] for x in mongo.list_databases()]:
    print(config.DATABASE_NAME, "doesn't exists, will create")

db = mongo[config.DATABASE_NAME]

openai.api_key = config.OPENAI_KEY

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
                    
                    if command[0] == 'test':
                        await test(event, bot, command)
                    elif command[0] == 'math':
                        await math_handle(event, bot, command)
                    elif command[0] == 'hitokoto':
                        await hitokoto(event, bot, command)
                    elif command[0] == 'picture':
                        await picture(event, bot, command)
                    elif command[0] == 'bing':
                        await bing(event, bot, command)
                    elif command[0] == 'breset':
                        await breset(event, bot, command)
                    elif command[0] == 'get_join_key':
                        if event.sender.id not in config.ADMIN_QQ:
                            await bot.send(event, '您无权使用！')
                        else:
                            await handlers.join_group.get_join_key(event, bot, command)
                    elif command[0] == 'integral':
                        await handlers.integral.integral(event, bot, command)
        except Exception as e:
            exc = traceback.format_exc()
            
            content = handlers.cgpt.generate_by_gpt('以下是一个Python语言的报错，请使用幽默且通俗易懂提示用户这个错误。要求表述完整，并为产生这个错误表示深深的歉意，不超过50字', exc)
            
            await bot.send(event, '[趣味日志] ' + content)

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

    # 定时任务
    scheduler = AsyncIOScheduler()
    @scheduler.scheduled_job(config.TIMER_TRIGGER)
    async def timer():
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            temperature=1,
            messages=[
                { 'role': 'system', 'content': f'现在是 20{datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")}' },
                { 'role': 'user', 'content': '写一句不超过 25 字的话，内容不限，结合当前时间提醒用户' }
            ]
        )
        
        content = response.choices[0].message["content"]
        
        for group in config.GROUP:
            await bot.send_group_message(group, '[定时提醒] ' + content)

    @bot.on(Startup)
    async def startup(event: Startup):
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            temperature=1,
            messages=[
                { 'role': 'system', 'content': f'现在是 20{datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")}' },
                { 'role': 'user', 'content': '写一句不超过 25 字的话，你将作为本群的机器人，使用有创意的语言，提醒用户你已经上线' }
            ]
        )
        
        content = response.choices[0].message["content"]
        
        for group in config.GROUP:
            await bot.send_group_message(group, '[趣味日志] ' + content)
            await bot.send_group_message(group, f'[免责声明] 本机器人所有的 [定时提醒] [趣味日志] 均由 OpenAI 公司的 gpt-3.5-turbo 模型生成，本人不对其负有任何责任')
        
        await timer()
        
        scheduler.start()
        
    @bot.on(Shutdown)
    async def shutdown(event: Shutdown):
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            temperature=1,
            messages=[
                { 'role': 'system', 'content': f'现在是 20{datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")}' },
                { 'role': 'user', 'content': '写一句不超过 25 字的话，你将作为本群的机器人，使用有创意的语言，提醒用户你已经下线' }
            ]
        )
        
        content = response.choices[0].message["content"]
        
        for group in config.GROUP:
            await bot.send_group_message(group, '[趣味日志] ' + content)

        scheduler.shutdown(True)

    bot.run()
