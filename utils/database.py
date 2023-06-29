from typing import Any
import pymongo
from utils.logger import get_gq_logger
from configs import config

logger = get_gq_logger()

if config.TEST_MODE:
    # 虚假的 mongodb 数据库对象
    class Db:
        def __init__(self):
            self.message = []
        
        def __getattr__(self, __name: str) -> Any:
            def any_func(*args, **kwargs):
                logger.info(f'Executed {__name} in test mode\nargs: {args}\nkwargs: {kwargs}')
                
                self.message.append(
                    {
                        'name': __name,
                        'args': args,
                        'kwargs': kwargs
                    }
                )
            
            return any_func

        def __getitem__(self, __name: str) -> Any:
            logger.info(f'Executed __getitem__ in test mode\n__name: {__name}')
            return Db()
    
    db = Db()
else:
    mongo = pymongo.MongoClient(config.DATABASE_IP, config.DATABASE_PORT)
    if config.DATABASE_NAME not in [x['name'] for x in mongo.list_databases()]:
        print(config.DATABASE_NAME, "doesn't exists, will create")

    db = mongo[config.DATABASE_NAME]

def get_col(col_name: str):
    col = db[col_name]
    
    return col