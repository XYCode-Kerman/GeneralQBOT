import flask
import jwt
from datetime import timedelta, datetime
from flask import Request, Response, request
from configs import config

app = flask.Flask(__name__)

@app.route('/ping')
async def ping():
    return {
        'status': 200,
        'ping': 'pong',
        'client': {
            'args': request.args.to_dict(),
            'method': request.method,
            'cookies': request.cookies
        }
    }

@app.route('/auth/login', methods=['POST'])
async def auth_login():
    if request.is_json:
        username = request.get_json().get('username')
        password = request.get_json().get('password')
        
        if username == config.REMOTE_MANAGER_ADMIN_NAME and password == config.REMOTE_MANAGER_ADMIN_PASSWORD:
            return {
                'status': 200,
                'message': 'success',
                'token': jwt.encode({
                    'username': username,
                    'password': password,
                    'expires':  datetime.now() + timedelta(days=1) 
                }, config.JWT_KEY)
            }, 200
        else:
            return {
                'status': 403,
                'message': 'wrong password'
            }, 403
    else:
        return {
            'status': 400,
            'message': 'request is not json'
        }, 400