from handlers.anti_flippedscreen import anti_fc, anti_tms, check_fc
from configs.config import MAX_MESSAGE_RATE, ALERT_MESSAGE_RATE

# generate a test for check_fc
async def test_check_fc():
    # generate a fake event
    class GroupMessage:
        def __init__(self):
            self.sender = GroupMessage.Sender()
            self.group = GroupMessage.Group()
        
        class Sender:
            def __init__(self):
                self.id = 123456
                self.member_name = 'test'
                self.join_timestamp = 1234567890
        
        class Group:
            def __init__(self):
                self.id = 123456
                self.name = 'test'
    
    class Mirai:
        async def send(self, event, msg):
            pass
        
        async def mute(self, group_id, member_id, seconds):
            pass
    
    event = GroupMessage()
    bot = Mirai()
    
    # test check_fc
    blocked, reason = await check_fc(event, bot, True)
    assert blocked == False
    assert reason == None
    
    for i in range(ALERT_MESSAGE_RATE + 1):
        blocked, reason = await check_fc(event, bot, test=True)
        
        if i == ALERT_MESSAGE_RATE:
            assert blocked is True and reason.startswith('警告')
    
    for i in range(MAX_MESSAGE_RATE - ALERT_MESSAGE_RATE + 2):
        blocked, reason = await check_fc(event, bot, test=True)
        
        if i == MAX_MESSAGE_RATE - ALERT_MESSAGE_RATE + 1:
            assert blocked is True and reason.startswith('撤回+禁言')