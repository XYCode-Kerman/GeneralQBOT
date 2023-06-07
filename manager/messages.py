import flask
import json
from mirai import Mirai
from typing import Union
from utils.token import verify_token
from utils.database import get_col
from utils.logger import get_gq_logger
from flask import make_response, request, Blueprint
from bson.json_util import dumps

messages_blueprint = Blueprint(
    'messages',
    __name__,
    url_prefix='/messages'
)

logger = get_gq_logger()
mirai: Union[Mirai, None] = None

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

# @messages_blueprint.route('/send', methods)
