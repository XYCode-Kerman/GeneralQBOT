import flask
import json
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

@messages_blueprint.route('/list', methods=['GET'])
def list_messages():
    messages = get_col('message')
    data = messages.find({})
    data = dumps(data)
    data = json.loads(data)
    
    return data, 200
