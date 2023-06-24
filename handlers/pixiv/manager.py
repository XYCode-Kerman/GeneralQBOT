"""
* @project       GeneralQBOT
* @author        XYCode-Kerman <xycode-xyc@outlook.com>
* @date          1970-01-01 08:00:00
* @lastModified  2023-05-15 23:01:26
"""
import datetime
from handlers.pixiv.searcher import PixivSearcher
from utils.database import get_col
from utils.logger import get_gq_logger
from configs import config
from mirai import *
from mirai_extensions.trigger import GroupMessageFilter
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
    # if len(command) < 2:
    #     await bot.send(event, '参数不足')
        
    #     return False
    
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
    # 对应P站搜索功能
    elif command[0] == 'search':
        searcher = PixivSearcher(event, bot, list(range(100)))
        await bot.send(event, '请输入你需要搜索的tag：')

        @GroupMessageFilter(group_member=event.sender)
        def waiter(event_new: GroupMessage):
            return str(event_new.message_chain)
        
        tag = await searcher.inc.wait(waiter, 60)
        
        if tag is None:
            await bot.send(event, '输入超时')
        else:
            aliases = await searcher.get_aliases(tag)
            await bot.send(event, aliases)
            await bot.send(event, '我们建议您在候选词中选一个，并且建议通过复制的形式输入，否则有可能导致搜索不到结果（P站祖传异能）')
        
        tag = await searcher.inc.wait(waiter, 60)
        
        if tag is None:
            await bot.send(event, '输入超时')
        else:
            result = await searcher.search_by_word(tag)
            await bot.send(event, result)
    else:
        logger.error(f"Unknown command {command[0]}")
        await bot.send(event, '未知命令')
        
        return False
    
    # use bot.emit send listeners_updated event
    if updated:
        logger.info('send gq_listeners_updated event')
    
        await bot.send(event, '操作完成，所有操作都会在下一次启动时生效')