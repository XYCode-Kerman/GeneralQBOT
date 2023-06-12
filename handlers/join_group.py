"""
* @project       GeneralQBOT
* @author        XYCode <xycode-xyc@outlook.com>
* @date          2023-05-08 22:37:16
* @lastModified  2023-05-15 12:54:20
"""
import datetime
import jwt
import uuid
from utils import database
from mirai import *
from mirai_extensions.trigger import InterruptControl, Filter, GroupMessageFilter, FriendMessageFilter
from configs import config
from typing import *

__all__ = ['get_join_key']

async def get_join_key(event: Union[GroupMessage, FriendMessage], bot: Mirai, command: List[str]):
    del command[0]
    
    inc = InterruptControl(bot)
    
    # get target member
    t: Union[At, None] = event.message_chain[-1]
    username = None
    if isinstance(t, At):
        username = t.target
        target = t.target
    else:
        try:
            target = int(target)
        except (ValueError, TypeError):
            await bot.send(event, '第二个参数为要给予 join_key 的群成员的 @ 或qq号')
            
            return
        
        username = target
    
    await bot.send(event, f'你确定要给予 {username} 加群的 key 吗？如果确认，请输入 /confirm')
    
    @GroupMessageFilter(group_member=event.sender)
    @FriendMessageFilter(friend=event.sender)
    def confirm_waiter(confirm_event: Union[GroupMessage, FriendMessage]):
        if str(confirm_event.message_chain) == '/confirm':
            return True
        else:
            return False
    
    if await inc.wait(confirm_waiter, 60):
        exp_time: datetime.datetime = datetime.datetime.now() + datetime.timedelta(days=1)
        
        encoded_jwt = uuid.uuid4().__str__()
        database.get_col('join_keys').insert_one({
            'target': target,
            'exp_time': exp_time,
            'key': encoded_jwt
        })
        
        await bot.send(event, str(encoded_jwt))
        await bot.send(event, f'加群时将如上 token 填入请求中即可自动批准！\n请在 24 小时内（即 {exp_time.strftime("%m 月 %d 日 %H:%M:%S")} 前）')