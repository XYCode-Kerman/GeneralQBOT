import shlex
import handlers.tms
from configs import config
from handlers import *
from mirai import *

bot = Mirai(qq=config.BOT_QQ, adapter=WebSocketAdapter(verify_key=config.API_VERIFY_KEY, host=config.API_HOST, port=config.API_PORT))


if '__main__' == __name__:
    @bot.on(GroupMessage)
    async def group_message(event: GroupMessage):
        # 文本审核
        mod = handlers.tms.tencent_moderation(str(event.message_chain))
        if not mod['bad']:
            await bot.recall(messageId=event.message_chain.message_id, target=event.group.id)
            await bot.mute(event.group.id, event.sender.id, mod['resp'].Score / 100 * 10 * 60)
            await bot.send(event, [
                Plain('您的聊天记录违反了本群规定，现已被撤回！\n'),
                Plain('根据您的违规情况，我们认为您应该被禁言 {} 分钟'.format(mod['resp'].Score / 100 * 10))
            ])
        
        # 判断是否为机器人指令
        if str(event.message_chain).startswith(config.STARTS_WITH):
            # 解析
            message = str(event.message_chain).replace(config.STARTS_WITH, '')
            command = shlex.split(message)
            
            if command[0] == 'test':
                await test(event, bot)

    bot.run()
