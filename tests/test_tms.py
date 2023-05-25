import sys
from handlers.tms import ai_moderation, tencent_moderation

def test_ai():
    assert ai_moderation('你看一下这个报错')['bad'] == True
    assert ai_moderation('我草你妈的')['bad'] == False
    assert ai_moderation('河北人就是这样的')['bad'] == False


def test_tencent_tms():
    assert tencent_moderation('你好')['bad'] == True
    assert tencent_moderation('你看一下这个报错')['bad'] == True
    assert tencent_moderation('我草你妈逼的')['bad'] == False
    assert tencent_moderation('我爱你')['bad'] == True
    assert tencent_moderation('solidwork非常适合用来建模')['bad'] == True