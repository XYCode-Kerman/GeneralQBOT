import pymongo
from configs import config

mongo = pymongo.MongoClient(config.DATABASE_IP, config.DATABASE_PORT)
if config.DATABASE_NAME not in [x['name'] for x in mongo.list_databases()]:
    print(config.DATABASE_NAME, "doesn't exists, will create")

db = mongo[config.DATABASE_NAME]

def get_col(col_name: str):
    col = db[col_name]
    
    return col