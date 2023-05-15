"""
* @project       GeneralQBOT
* @author        XYCode <xycode-xyc@outlook.com>
* @date          1970-01-01 08:00:00
* @lastModified  2023-05-15 12:52:15
"""
import random
import pymongo
from configs import config
from mirai import *
from mirai_extensions.trigger import GroupMessageFilter, FriendMessageFilter, Trigger, InterruptControl
from typing import *
from typing_extensions import *

mongo = pymongo.MongoClient(config.DATABASE_IP, config.DATABASE_PORT)

if config.DATABASE_NAME not in [x['name'] for x in mongo.list_databases()]:
    print(config.DATABASE_NAME, "doesn't exists, will create")

db = mongo[config.DATABASE_NAME]

__all__ = ['guess_numbers']

def add_integral(integral: int, id: int):
    userdata = db['userdata']
    
    userdata.update_one(
        {
            'id': id
        },
        {
            '$inc': {
                'integral': integral
            }
        }
    )

async def guess_numbers(event: GroupMessage, bot: Mirai, command: List[str]):
    await bot.send(event, f'让我们开始猜一个 0-100 之间的数字吧！')
    
    inc = InterruptControl(bot)
    number = random.randint(0, 100)
    
    @GroupMessageFilter(group_member=event.sender)
    def waiter(event_new: GroupMessage):
        message = str(event_new.message_chain)
        
        try:
            input_number = int(message)
        except ValueError:
            return None
        
        return input_number
    
    while True:
        input_number = await inc.wait(waiter, 60)
        
        if input_number is None:
            await bot.send(event, '超时了')
            break
        
        if input_number > number:
            await bot.send(event, '猜大了')
        elif input_number < number:
            await bot.send(event, '猜小了')
        elif input_number == number:
            await bot.send(event, '猜对了')
            await bot.send(event, '我们将为您增加 5 积分')
            
            add_integral(5, event.sender.id)
            
            await bot.send(event, '积分增加完成')
            
            break