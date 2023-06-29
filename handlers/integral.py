"""
* @project       GeneralQBOT
* @author        XYCode <xycode-xyc@outlook.com>
* @date          1970-01-01 08:00:00
* @lastModified  2023-05-15 12:51:36
"""
import configs.config as config
import datetime
from utils import database
from mirai import *
from typing import *

async def get_integral(event: GroupMessage, bot: Mirai, command: List[str]):
    userdata = database.get_col('userdata')
    
    # get intergral data from userdata col, and return it
    data = userdata.find_one({
        'id': event.sender.id
    })
    
    return data['integral']

async def integral(event: GroupMessage, bot: Mirai, command: List[str]):
    del command[0]
    
    if command[0] == 'get' or command[0] == '获取':
        integral = await get_integral(event, bot, command)

        await bot.send(event, f'您的积分是 {integral}')
    elif command[0] == 'leaderboard' or command[0] == '排行榜':
        userdata = database.get_col('userdata')
        
        data = userdata.find().sort('integral', -1)
        
        # get top 10
        data = list(data)[0:10]
        
        # format
        string = [
            '=== 积分排行榜 ===',
            f'统计时间：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        ]
        
        string.extend([f'{data.index(i) + 1}. {i["name"]} - {i["integral"]}' for i in data if i['integral'] > 0])
        
        await bot.send(event, '\n'.join(string))
    elif command[0] == 'checkin' or command[0] == '签到':
        userdata = database.get_col('userdata')
        
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
    elif command[0] == 'manage' or command[0] == '管理':
        userdata = database.get_col('userdata')
        
        # 检验权限
        if event.sender.id not in config.ADMIN_QQ:
            await bot.send(event, '您没有权限进行此操作')
            return
        
        # 判断
        if command[1] == 'add' or command[1] == '增加':
            if isinstance(event.message_chain[2], At):
                target: int = event.message_chain[2].target
                display: str = event.message_chain[2].display
                group_member = await bot.get_group_member(event.group.id, target)
                
                if group_member:
                    display = group_member.member_name
            else:
                target: int = int(command[1])
                display: str = f'未知：{target}'
            
            score = int(command[3])
            
            # 加上对应的积分
            userdata.update_one({
                'id': target
            }, {
                '$inc': {
                    'integral': score
                },
                '$set': {
                    'name': display,
                    'last_checkin': datetime.datetime.now()
                }
            }, upsert=True)
            
            # 查询当前的积分
            data = userdata.find_one({
                'id': target
            })
            
            await bot.send(event, f'已经给 {display} 增加 {score} 积分')
            await bot.send(event, f'当前积分为 {data["integral"]}')
        elif command[1] == 'reduce' or command[1] == '减少':
            if isinstance(event.message_chain[2], At):
                target: int = event.message_chain[2].target
                display: str = event.message_chain[2].display
            else:
                target: int = int(command[1])
                display: str = f'未知：{target}'
            
            score = int(command[3])
            
            # 减去对应的积分
            userdata.update_one({
                'id': target
            }, {
                '$inc': {
                    'integral': -score
                }
            })
            
            # 查询当前的积分
            data = userdata.find_one({
                'id': target
            })
            
            await bot.send(event, f'已经给 {display} 减少 {score} 积分')
            await bot.send(event, f'当前积分为 {data["integral"]}')
        elif command[1] == 'set' or command[1] == '设置':
            if isinstance(event.message_chain[2], At):
                target: int = event.message_chain[2].target
            else:
                target: int = int(command[1])
            
            display: str = str(event.message_chain[2])
            
            score = int(command[2])
            
            # 设置对应的积分
            userdata.update_one({
                'id': target
            }, {
                '$set': {
                    'integral': score
                }
            })
            
            await bot.send(event, f'已经将 {display} 的积分设置为 {score}')

__all__ = ['integral', 'get_integral']