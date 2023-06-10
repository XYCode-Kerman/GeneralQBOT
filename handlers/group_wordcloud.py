import wordcloud
import datetime
import base64
import jieba
import nltk
from utils.database import get_col
from utils.logger import get_gq_logger
from mirai import Mirai, GroupMessage, Image, Plain
from io import BytesIO
from typing import List

logger = get_gq_logger()

def gen_messages(group: int) -> List[str]:
    message_col = get_col('message')
    messages = list(message_col.find({
        'group.id': group
    }))
    
    messages_plain: List[str] = [
        message['message']
        for message in messages
    ]
    
    messages_plain = [
        message.replace('\[.*\]|\..*|@.*', '').replace(' ', '')
        for message in messages_plain
    ]
    
    return messages_plain

def gen_words(messages: List[str]) -> List[str]:
    # 中文分词
    words = [
        jieba.lcut(message)
        for message in messages
    ]
    
    little_words = []
    
    for word in words:
        for little_word in word:
            if little_word not in ['.', '@', '[', ']']:
                little_words.append(little_word)
    
    return little_words

def gen_wordcloud(group: int):
    seq_text = ' '.join(gen_words(gen_messages(group)))
    
    wc = wordcloud.WordCloud(
        './resources/XiaolaiSC-Regular.ttf',
        1980,
        1080,
        min_font_size=4,
        background_color='white'
    )
    
    wc_image = wc.generate(seq_text).to_image()
    wc_image.save(f'./images/wordclouds/{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.png', 'PNG')
    
    # 转换为 base64
    buffer = BytesIO()
    wc_image.save(buffer, format='png')
    buffer.seek(0)
    wc_image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    
    return wc_image_base64

async def handle_message(event: GroupMessage, bot: Mirai, command: List[str]):
    del command[0]
    
    group = event.group.id
    
    wc_b64 = gen_wordcloud(group)
    
    await bot.send(event, [
        Plain(f'词云图生成日期：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}   目标群：{group}'),
        Image(base64=wc_b64)
    ])