import flask
import json
from mirai import Mirai, MessageChain
from typing import Union, Literal
from utils.token import verify_token
from utils.database import get_col
from utils.logger import get_gq_logger
from flask import make_response, request, Blueprint
from bson.json_util import dumps, loads

messages_blueprint = Blueprint(
    'messages',
    __name__,
    url_prefix='/messages'
)

logger = get_gq_logger()
mirai: Mirai = None

@messages_blueprint.route('/list', methods=['GET'])
def list_messages():
    if verify_token(request.cookies.get('token', '')) == False:
        return {
            'status': 403,
            'message': 'forbidden'
        }, 403
    
    messages = get_col('message')
    data = messages.find({})
    data = dumps(data)
    data = json.loads(data)
    
    return data, 200

@messages_blueprint.route('/send', methods=['POST'])
async def send_message():
    global mirai
    
    if verify_token(request.cookies.get('token', '')) == False:
        return {
            'status': 403,
            'message': 'forbidden'
        }, 403
    
    target = request.get_json().get('target', '')
    target_type: Literal['group', 'friend'] = request.get_json().get('target_type', '')
    message_chain = request.get_json().get('message_chain', [])

    # 判断请求是否正确
    if target == '' or target_type == '' or message_chain == []:
        return {
            'status': 400,
            'message': 'bad request'
        }, 400
    else:
        message_chain = MessageChain(message_chain)
        
        if target_type == 'group':
            await mirai.send_group_message(int(target), message_chain)

            return {
                'status': 200,
                'message_chain': message_chain.dict()
            }, 200
        elif target_type == 'friend':
            await mirai.send_friend_message(int(target), message_chain)

            return {
                'status': 200,
                'message_chain': message_chain.dict()
            }, 200
        else:
            return {
                'status': 400,
                'message': 'bad request'
            }, 400
