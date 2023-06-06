import flask
from flask import Request, Response, request

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