"""
* @project       GeneralQBOT
* @author        XYCode-Kerman <xycode-xyc@outlook.com>
* @date          1970-01-01 08:00:00
* @lastModified  2023-05-15 13:05:15
"""
import requests
import asyncio
import base64
from configs import config
from utils.logger import get_gq_logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from mirai import *
from typing_extensions import *
from typing import *

logger = get_gq_logger()
__all__ = ['Listener', 'PixivListener']

class Listener(object):
    def __init__(self, type: str, api_url: str, trigger_rate: CronTrigger, scheduler: AsyncIOScheduler, bot: Mirai) -> None:
        self.type = type
        self.api_url = api_url
        self.trigger_rate = trigger_rate
        self.bot = bot
        
        self.scheduler = scheduler
        self.scheduler.add_job(self.checker, self.trigger_rate)
    
    def stop(self):
        self.scheduler.remove_job(self.checker)
    
    async def checker(self):
        pass


class PixivListener(Listener):
    def __init__(self, type: enumerate(['user', 'tag']), api_url: str, name: str, trigger_rate: CronTrigger, scheduler: AsyncIOScheduler, bot: Mirai) -> None:
        super().__init__(type, api_url, trigger_rate, scheduler, bot)

        self.name = name
        self.old = 3554724
    
    async def checker(self):
        if self.type == 'user':
            logger.debug('Checking user: %s' % self.name)
            await self.user_checker()
        elif self.type == 'tag':
            logger.debug('Checking tag: %s' % self.name)
            await self.tag_checker()
        else:
            logger.warning('Unknown type: %s' % self.type)
    
    async def user_checker(self):
        pass
    
    async def tag_checker(self):
        req = requests.get(f'https://www.pixiv.net/ajax/search/artworks/{self.name}?word=background&order=date_d&mode=all&p=1&s_mode=s_tag&type=all&lang=zh&version=15184bdd760e9ec16c72845f60ba1ae1e4f05054',
            {
                'Referer': 'https://www.pixiv.net/'
            }
        )
        
        data = req.json()
        total = data['body']['illustManga']['total']
        
        if self.old != total and self.old is not None:
            logger.info(f'New pixiv artwork found! Total: {total}  Old: {self.old}  Tag: {self.name}')
            
            for group in config.GROUP:
                await self.bot.send_group_message(group, f'{self.name} 上有新的作品, 作品名称：{data["body"]["illustManga"]["data"][0]["title"]}')
                await self.bot.send_group_message(group, f'请等待机器人下载图片缩略图')
            
            # download image
            url = data["body"]["illustManga"]["data"][0]["url"]
            image = requests.get(url, headers={
                'Referer': 'https://www.pixiv.net/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
                'Sec-Ch-Ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                'Sec-Ch-Platform': '"Windows"',
                'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
            })
            
            # Use base64 to encode the image
            image_b64 = base64.b64encode(image.content).decode('utf-8')
            
            for group in config.GROUP:
                await self.bot.send_group_message(group, [Image(base64=image_b64)])
        
        self.old = total