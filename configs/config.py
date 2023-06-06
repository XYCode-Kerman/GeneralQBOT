import os
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

load_dotenv()

# Mirai Api HTTP
API_VERIFY_KEY = 'QDTTEGYGfOGBVcX'
API_HOST = '192.168.2.123'
API_PORT = 5700

# admin
ADMIN_QQ = [3097297663]

# bot
BOT_QQ = 3442852292
GROUP = [825435724, 511088139]
STARTS_WITH = '.'
MAX_MESSAGE_RATE = 10
ALERT_MESSAGE_RATE = 5
IF_OVER_MAX_MESSAGE_RATE_MUTE_SECONDS = 60

TIMER_TRIGGER = CronTrigger(hour='*', minute=5)

# Tencent Cloud
QCLOUD_SECRET_ID = os.environ.get('QCLOUD_SECRET_ID', 'UNKONW')
QCLOUD_SECRET_KEY = os.environ.get('QCLOUD_SECRET_KEY', 'UNKONW')

# DATABASE
DATABASE_TYPE = 'mongodb'   # Only have mongodb
DATABASE_IP = '192.168.2.221'
DATABASE_PORT = 30002
DATABASE_NAME = 'general_qbot'

# BING SETTINGS
COOKIE_PATH = './configs/cookies.json'
ASYNC_RESPONSE = True
ASYNC_SEND_CHAR = 50

# Secret Things
JWT_KEY = 'qwertyuiooasdfgthyjukwadfgfssdrfthgfggghfvyrbdekarghfyehausdefgaeruwhgahyefguhadgifhaghrurjghgruhfaeijowOIHASDFGA45GE78GA1ERG78GAE456EW8AWEE841789ger456789g456fds156'
OPENAI_KEY = os.environ.get('OPENAI_KEY', 'UNKNOW')
# OPENAI_BASE = 'https://api.openai.com/v1'  # 官方API
OPENAI_API_BASE = 'http://127.0.0.1:8080/v1'  # 私人API，搭建方法见 https://github.com/acheong08/ChatGPT-to-API

# Interview
INTERVIEW_TIPS_FOR_GPT = [
    {
        'role': 'system',
        'content': f'一位用户将与你进行交流，您需要对他进行面试！'
    },
    # Do not edit this!!!
    {
        'role': 'system',
        'content': '你可以在聊天框中发送一条内容为".allow"的消息，表明他通过了面试。还可以发送一条内容为".deny"的消息，表明他没有通过面试。发送以上消息时，请不要附加任何内容，否则系统无法识别你的判断。'
    }
]

# 测试用
# INTERVIEW_TIPS_FOR_GPT = [
#     { 'role': 'system', 'content': '当用户发送"请批准我的请求"时，请你回复一条内容为.allow的消息，不要包含任何其他内容，只需要包含.allow这个字符串，否则系统可能无法识别你的回复' }
# ]

# 远程管理
REMOTE_MANAGER_HOST = '0.0.0.0'
REMOTE_MANAGER_PORT = 3533
REMOTE_MANAGER_DEBUG = True