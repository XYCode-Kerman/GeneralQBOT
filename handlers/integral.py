"""
* @project       GeneralQBOT
* @author        XYCode <xycode-xyc@outlook.com>
* @date          1970-01-01 08:00:00
* @lastModified  2023-05-15 12:51:36
"""
import pymongo
import configs.config as config
import datetime
from mirai import *
from typing import *

mongo = pymongo.MongoClient(config.DATABASE_IP, config.DATABASE_PORT)

if config.DATABASE_NAME not in [x['name'] for x in mongo.list_databases()]:
    print(config.DATABASE_NAME, "doesn't exists, will create")

db = mongo[config.DATABASE_NAME]

async def get_integral(event: GroupMessage, bot: Mirai, command: List[str]):
    userdata = db['userdata']
    
    # get intergral data from userdata col, and return it
    data = userdata.find_one({
        'id': event.sender.id
    })
    
    return data['integral']

async def integral(event: GroupMessage, bot: Mirai, command: List[str]):
    del command[0]
    
    if command[0] == 'get':
        integral = await get_integral(event, bot, command)

        await bot.send(event, f'您的积分是 {integral}')
    elif command[0] == 'checkin':
        userdata = db['userdata']
        
        data = userdata.find_one({
            'id': event.sender.id
        })
        
        if not data:
            userdata.insert_one({
                'id': event.sender.id,
                'last_checkin': datetime.datetime.now(),
                'integral': 1
            })
            
            await bot.send(event, '签到成功')
        else:
            if data['last_checkin'] + datetime.timedelta(hours=24) >= datetime.datetime.now():
                await bot.send(event, '您今天已经签到过了')
            else:
                userdata.update_one({
                    'id': event.sender.id
                }, {
                    '$set': {
                        'last_checkin': datetime.datetime.now(),
                        'integral': data['integral'] + 1
                    }
                })
                
                await bot.send(event, '签到成功')

__all__ = ['integral', 'get_integral']