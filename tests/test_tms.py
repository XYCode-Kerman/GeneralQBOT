import sys
sys.path.append('.')
sys.path.append('..')
from handlers.tms import ai_moderation, tencent_moderation

def test_ai():
    # assert ai_moderation('你好')['bad'] == True
    assert ai_moderation('你看一下这个报错')['bad'] == True
    assert ai_moderation('我草你妈的')['bad'] == False
    assert ai_moderation('河北人就是这样的')['bad'] == False