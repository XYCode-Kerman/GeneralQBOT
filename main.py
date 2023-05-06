import shlex
import handlers.tms
import handlers.anti_flippedscreen
import datetime
from configs import config
from handlers import *
from mirai import *
from typing import *

bot = Mirai(qq=config.BOT_QQ, adapter=WebSocketAdapter(verify_key=config.API_VERIFY_KEY, host=config.API_HOST, port=config.API_PORT))


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

    bot.run()
