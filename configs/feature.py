from enum import Enum, auto

class Features(Enum):
    TencentTMS = auto()
    LocalAITMS = auto()
    LocalKeywordTMS = auto()
    Interview = auto()
    Startup_Tips = auto()
    RemoteManager = auto()

# 推荐使用TencentTMS，LocalAI由于数据集不充分，且训练步数较少，不认识某些生词，准确率大概在50%左右
ENABLE_TMS_SERVICER = [Features.TencentTMS, Features.LocalAITMS]
ENABLED_FEATURE = [Features.Interview, Features.RemoteManager]