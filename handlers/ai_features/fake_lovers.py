import asyncio
import sys
sys.path.append('./')
import hashlib
from mirai_extensions.trigger import InterruptControl, FriendMessageFilter
from mirai import Mirai, FriendMessage
from enum import Enum, auto
from typing import Literal, List
from handlers.cgpt import generate_by_gpt_for_interview
from utils.logger import get_gq_logger
from utils.database import get_col
import recognizers_text
import recognizers_number_with_unit

logger = get_gq_logger()

class Gender(Enum):
    boyfriend = '男朋友'
    girlfriend = '女朋友'

class CharacterSettings:
    def __init__(self, keywords: List[str], sentences: List[str], age: int = 18, job: str = '无职业', city: str = '上海') -> None:
        self.keywords = keywords
        self.sentences = sentences
        self.age = age
        self.job = job
        self.city = city
    
    def __str__(self) -> str:
        return f"""人物设定：{" ".join(self.keywords)} 并且 {" ".join(self.sentences)}
职业：{self.job}
年龄：{self.age}
所在城市：{self.city}
    """

class Lover(object):
    def __init__(self, gender: Literal[Gender.girlfriend, Gender.boyfriend], character_settings: CharacterSettings, name: str, user_name: str) -> None:
        self.gender = gender
        self.character_settings = character_settings
        self.name = name
        self.user_name = user_name
        self.history = [
            {
                'role': 'system',
                'content': '不要在聊天框内告诉用户我们在玩角色扮演游戏，让用户更有沉浸感。'
            },
            {
                'role': 'system',
                'content': '尽量假扮的更好一点，最好不要让用户发觉。多使用口语化的语言。模拟你们在一个名为QQ的聊天软件中聊天。'
            },
            {
                'role': 'system',
                'content': '你可以使用如下命令执行操作。请注意，请确保你在聊天框内输入的内容是命令并且没有任何附加内容，否则我将会把你的输入作为对话内容展现给用户。\n.exit 退出对话\n.ignore 忽略用户的输入'
            },
            {
                'role': 'user',
                'content': f'接下来我将与你玩一个角色扮演游戏，你扮演我的 {self.gender.value}，你的人物设定是：{self.character_settings}，你的名字是：{name}，我的名字是：{user_name}'
            }
        ]
    
    async def asking(self, prompt: str):
        logger.debug(f'asking: {prompt}')
        self.history.append(
            {
                'role': 'user',
                'content': prompt
            }
        )
        
        response = await generate_by_gpt_for_interview(self.history)

        self.history.append(
            {
                'role': 'assistant',
                'content': response
            }
        )
        
        col = get_col('lovers')
        # 将本次对话的信息附加到数据库中
        col.update_one(
            {
                'name': self.name,
                'user_name': self.user_name
            },
            {
                '$push': {
                    'history': {
                        'role': 'user',
                        'content': prompt
                    }
                }
            }
        )
        
        col.update_one(
            {
                'name': self.name,
                'user_name': self.user_name
            },
            {
                '$push': {
                    'history': {
                        'role': 'assistant',
                        'content': response
                    }
                }
            }
        )

        if '.exit' in response or prompt == '.exit':
            return '今天就聊到这里了，下次再见。'
        elif '.ignore' in response or prompt == '.ignore':
            return await self.asking(prompt)
        
        return response

    def __hash__(self) -> int:
        return int(hashlib.sha512(f'{self.gender}{self.character_settings}{self.history}'.encode('utf-8')).hexdigest().encode('utf-8').hex())

    def save(self):
        col = get_col('lovers')
        col.update_one(
            {
                'name': self.name,
                'user_name': self.user_name
            },
            {
                '$set': {
                    'gender': self.gender.value,
                    'character_settings': {
                        'keywords': self.character_settings.keywords,
                        'sentences': self.character_settings.sentences
                    },
                    'user_name': self.user_name,
                    'name': self.name,
                    'history': self.history
                }
            },
            upsert=True
        )
        
        logger.debug(f'Lover {self.name} saved')
    
    @staticmethod
    def load(name: str, user_name: str):
        col = get_col('lovers')
        data = col.find_one(
            {
                'name': name,
                'user_name': user_name
            }
        )
        
        gender = Gender._value2member_map_[data['gender']]
        character_settings = CharacterSettings(keywords=data['character_settings']['keywords'], sentences=data['character_settings']['sentences'])
        history = data['history']
        name = data['name']
        user_name = data['user_name']

        logger.debug(f'Lover {name} loaded')
        
        return Lover(gender, character_settings, name, user_name)

async def handler(event: FriendMessage, bot: Mirai, command: List[str]):
    del command[0]
    inc = InterruptControl(bot)
    
    @FriendMessageFilter(friend=event.sender.id)
    def waiter(event_new: FriendMessage):
        return str(event_new.message_chain)
    
    if command[0] == 'create':
        await bot.send(event, '请输入ta的性别（男、女）：')
        gender = await inc.wait(waiter, 60)
        if '男' in gender:
            gender = Gender.boyfriend
        elif '女' in gender:
            gender = Gender.girlfriend
        else:
            await bot.send(event, '你没有输入正确的性别！默认设定为女朋友')
            gender = Gender.girlfriend
        
        await bot.send(event, '请输入ta的年龄：')
        age: str = str(await inc.wait(waiter, 60))
        parsed = recognizers_number_with_unit.recognize_age(age, 'zh-cn')
        
        if parsed.__len__() < 1:
            try:
                age = int(age)
            except ValueError:
                await bot.send(event, '你没有输入正确的年龄！')
                return
        else:
            age = int(parsed[0].resolution['value'])
        
        await bot.send(event, '请输入设定（句子）')
        character_settings_sentences = str(await inc.wait(waiter, 60)).split(' ')
        
        await bot.send(event, '请输入设定（关键词）')
        character_settings_keywords = str(await inc.wait(waiter, 60)).split(' ')
        
        await bot.send(event, '请输入他所在的地点')
        city = await inc.wait(waiter, 60)
        
        await bot.send(event, '请输入他的职业')
        job = await inc.wait(waiter, 60)
        
        character_settings = CharacterSettings(keywords=character_settings_keywords, sentences=character_settings_sentences, age=age, job=job, city=city)
        
        await bot.send(event, '请输入ta的名字：')
        name: str = str(await inc.wait(waiter, 60))
        user_name: str = event.sender.nickname
        
        await bot.send(
            event,
f"""
请确认ta的设定：
名字：{name}
你的名字：{user_name}
{character_settings}

输入 .yes 确认，输入 .no 取消
"""
        )
        
        confirm = await inc.wait(waiter, 60)
        if confirm == '.yes':
            lover = Lover(gender, character_settings, name, user_name)
            lover.save()
            await bot.send(event, '已保存')
        else:
            await bot.send(event, '编辑器已退出，请重新编辑')

if '__main__' == __name__:
    settings = CharacterSettings(['温柔', '善良', '友好', '可爱'], ['喜欢吃饭', '喜欢看电影', '喜欢看书'])
    gender = Gender.girlfriend
    lover = Lover(gender, settings, '无姓名', 'XYCode')
    loop = asyncio.get_event_loop()
    
    lover.save()
    del lover
    lover = Lover.load('无姓名', 'XYCode')
    
    while True:
        user = input('user: ')
        
        get_future = asyncio.ensure_future(lover.asking(user))
        loop.run_until_complete(get_future)
        print(get_future.result())
