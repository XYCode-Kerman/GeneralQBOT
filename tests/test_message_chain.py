from mirai import MessageChain
from mirai.models.message import *
from utils.message_chain import message_chain_to_list

def test_message_chain_to_list():
    message_chain_str = []
    message_chain = MessageChain([
        Plain('hello')
    ])
    
    message_chain_str = message_chain_to_list(message_chain)
    
    assert message_chain_str == [
        '[Plain] hello'
    ]