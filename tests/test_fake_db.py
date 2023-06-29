from configs import config
from utils.logger import get_gq_logger
from utils.database import get_col

def test_mode():
    assert config.TEST_MODE == True

def test_get_col():
    assert config.TEST_MODE == True
    userdata = get_col('userdata')
    
    userdata.find_one({'id': 1234567890})