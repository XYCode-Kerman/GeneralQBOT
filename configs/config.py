
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import dotenv_values

env = dotenv_values()

# Mirai Api HTTP
API_VERIFY_KEY = 'QDTTEGYGfOGBVcX'
API_HOST = '192.168.2.221'
API_PORT = 5700

# admin
ADMIN_QQ = [3097297663]

# bot
BOT_QQ = 3442852292
GROUP = [825435724]
STARTS_WITH = '.'
MAX_MESSAGE_RATE = 10
ALERT_MESSAGE_RATE = 5
IF_OVER_MAX_MESSAGE_RATE_MUTE_SECONDS = 60

TIMER_TRIGGER = CronTrigger(hour='*', minute=5)

# Tencent Cloud
QCLOUD_SECRET_ID = env.get('QCLOUD_SECRET_ID', 'UNKONW')
QCLOUD_SECRET_KEY = env.get('QCLOUD_SECRET_KEY', 'UNKONW')

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
OPENAI_KEY = env.get('OPENAI_KEY', 'UNKNOW')