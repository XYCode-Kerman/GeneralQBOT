import requests
from mirai import *
from mirai_extensions.trigger import InterruptControl, GroupMessageFilter
from typing import List

class PixivSearcher(object):
    def __init__(self, event: GroupMessage, bot: Mirai, command: List[str]) -> None:
        self.event = event
        self.bot = bot
        del command[0]
        self.command = command
        
        self.method = command[0]
        self.keyword = command[1]
        self.inc = InterruptControl(bot)
    
    async def search(self):
        if self.method == 'tags':
            aliases = await self.get_aliases(self.keyword)
            await self.bot.send(self.event, aliases)
            
            @GroupMessageFilter(group_member=self.event.sender)
            def waiter(event_new: GroupMessage):
                return str(event_new.message_chain)
            
            word = self.inc.wait(waiter, 60)
            
            if word is None:
                await self.bot.send(self.event, '超时了')
                return None
            else:
                string = await self.search_by_word(word)
                await self.bot.send(self.event, string)
        else:
            return None
    
    async def search_by_word(self, word: str):
        res = requests.get(
            f'https://www.pixiv.net/ajax/search/artworks/{word}',
            headers={
                'Referer': 'https://www.pixiv.net/'
            }
        )
        
        data = res.json()['body']['illustManga']['data']
        strings = []
        
        for illust in data:
            strings.append(
                f'画作id：{illust["id"]}\t标题：{illust["title"]}\t标签：{illust["tags"]}'
            )
        
        return '\n'.join(strings)
    
    async def get_aliases(self, word: str):
        res = requests.get(
            f'https://www.pixiv.net/rpc/cps.php?keyword={word}&lang=zh',
            headers={
                'Referer': 'https://www.pixiv.net/'
            }
        )
        
        data = res.json()['candidates']
        strings = []
        
        strings.append('候选词:')
        
        for tag in data:
            strings.append(f'{tag["tag_name"]}  引用数量：{tag["access_count"]}')
        
        return '\n'.join(strings)
