import shlex
import handlers.tms
import handlers.anti_flippedscreen
import handlers.join_group
import datetime
import jwt
from configs import config
from handlers import *
from mirai import *
from mirai.models.events import MemberJoinRequestEvent
from typing import *
import traceback
import pymongo

bot = Mirai(qq=config.BOT_QQ, adapter=WebSocketAdapter(verify_key=config.API_VERIFY_KEY, host=config.API_HOST, port=config.API_PORT))

mongo = pymongo.MongoClient(config.DATABASE_IP, config.DATABASE_PORT)

if config.DATABASE_NAME not in [x['name'] for x in mongo.list_databases()]:
    print(config.DATABASE_NAME, "doesn't exists, will create")

db = mongo[config.DATABASE_NAME]

if '__main__' == __name__:
    @bot.on(GroupMessage)
    async def group_message(event: GroupMessage):
        if event.group.id in config.GROUP:
            # 反不良信息
            await handlers.anti_flippedscreen.anti_fc(event, bot)

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

    bot.run()
