from utils.logger import get_gq_logger
from handlers.cgpt import generate_by_gpt


def test_cgpt():
    res = generate_by_gpt('你正处于一个测试环境中', '刚刚网络因为某种原因意外断开了，现在我重新连上了网络，如果你收到了这条消息，请回复任意一个大于等于1且小于等于100的数字，这样我就可以知道当前网络畅通！不要在回复中包含任何其他文字，确保我可以通过python的int函数将你的回复转换为整数类型')
    get_gq_logger().info(res)
    
    num = int(res)
    assert 1 <= num <= 100