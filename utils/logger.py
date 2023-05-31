"""
* @project       GeneralQBOT
* @author        XYCode-Kerman <xycode-xyc@outlook.com>
* @date          1970-01-01 08:00:00
* @lastModified  2023-05-15 22:46:21
"""
import logging
import datetime

logger = logging.getLogger('GeneralQBOT')

logging.basicConfig(
    filename=f'./logs/{datetime.datetime.now().timestamp()}.log',
    filemode='w'
)

logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(pathname)s] [line:%(lineno)d] %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def get_gq_logger() -> logging.Logger:
    return logger