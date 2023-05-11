from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Mirai Api HTTP
API_VERIFY_KEY = ''
API_HOST = '192.168.2.221'
API_PORT = 5700

# admin
ADMIN_QQ = []

# bot
BOT_QQ = 0
GROUP = []
STARTS_WITH = '.'
MAX_MESSAGE_RATE = 10
ALERT_MESSAGE_RATE = 5
IF_OVER_MAX_MESSAGE_RATE_MUTE_SECONDS = 60

TIMER_TRIGGER = CronTrigger(hour='*', minute=5)

# Tencent Cloud
QCLOUD_SECRET_ID = ''
QCLOUD_SECRET_KEY = ''

# DATABASE
DATABASE_TYPE = 'mongodb'   # Only have mongodb
DATABASE_IP = ''
DATABASE_PORT = 0
DATABASE_NAME = ''

# BING SETTINGS
COOKIE_PATH = ''
ASYNC_RESPONSE = True
ASYNC_SEND_CHAR = 5

# Secret Things
JWT_KEY = 'qwertyuiooasdfgthyjukwadfgfssdrfthgfggghfvyrbdekarghfyehausdefgaeruwhgahyefguhadgifhaghrurjghgruhfaeijowOIHASDFGA45GE78GA1ERG78GAE456EW8AWEE841789ger456789g456fds156'
OPENAI_KEY = ''