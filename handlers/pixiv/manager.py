"""
* @project       GeneralQBOT
* @author        XYCode-Kerman <xycode-xyc@outlook.com>
* @date          1970-01-01 08:00:00
* @lastModified  2023-05-15 23:01:26
"""
import datetime
from utils.database import get_col
from utils.logger import get_gq_logger
from configs import config
from mirai import *
from typing import *

logger = get_gq_logger()

listeners = get_col('listeners')

def add_listener(bot: Mirai, command: List[str]):
    target = command[1]
    type = command[2]
    name = command[3]
    
    try:
        trigger_rate = command[4]
    except:
        trigger_rate = '30 * * * *'
    
    if target not in ['pixiv']:
        logger.error(f"Unknown target {target}")
        
        return False
    
    listeners.insert_one({
        'target': target,
        'type': type,
        'name': name,
        'trigger_rate': trigger_rate
    })
    
    return True

def update_listener(bot: Mirai, command: List[str]):
    target = command[1]
    type = command[2]
    name = command[3]
    
    if target not in ['pixiv']:
        logger.error(f"Unknown target {target}")
        
        return False
    
    listeners.update_one({
        'target': target,
        'type': type,
        'name': name
    }, {
        '$set': {
            'target': target,
            'type': type,
            'name': name
        }
    }, upsert=True)
    
def delete_listener(bot: Mirai, command: List[str]):
    target = command[1]
    type = command[2]
    name = command[3]
    
    if target not in ['pixiv']:
        logger.error(f"Unknown target {target}")
        
        return False
    
    listeners.delete_one({
        'target': target,
        'type': type,
        'name': name
    })

def list_listener(bot: Mirai, command: List[str]):
    return list(listeners.find({}))

async def manager(event: GroupMessage, bot: Mirai, command: List[str]):
    if len(command) < 2:
        await bot.send(event, '参数不足')
        
        return False
    
    del command[0]
    
    updated = False
    
    if command[0] == 'add':
        add_listener(bot, command)

        updated = True
    elif command[0] == 'update':
        update_listener(bot, command)

        updated = True
    elif command[0] == 'delete':
        delete_listener(bot, command)

        updated = True
    elif command[0] == 'list':
        listeners = list_listener(bot, command)
        
        strings = ['对象\t类型\t名称']
        
        for listener in listeners:
            strings.append(f"{listener['target']}\t{listener['type']}\t{listener['name']}")
        
        string = '\n'.join(strings)
        
        await bot.send(event, string)
    else:
        logger.error(f"Unknown command {command[0]}")
        await bot.send(event, '未知命令')
        
        return False
    
    # use bot.emit send listeners_updated event
    if updated:
        logger.info('send gq_listeners_updated event')
    
        await bot.send(event, '操作完成，所有操作都会在下一次启动时生效')