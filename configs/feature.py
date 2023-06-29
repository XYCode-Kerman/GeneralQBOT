from enum import Enum, auto

class Features(Enum):
    TencentTMS = '腾讯文本审核'
    LocalAITMS = '本地 AI 文本审核'
    LocalKeywordTMS = '本地关键词文本审核'
    Interview = '面试'
    Startup_Tips = '启动提示'
    RemoteManager = '远程管理（已弃用）'
    Fun_Log = '趣味日志'
    Raw_Log = '原始日志'

# 推荐使用TencentTMS，LocalAI由于数据集不充分，且训练步数较少，不认识某些生词，准确率大概在50%左右
ENABLE_TMS_SERVICER = [Features.TencentTMS]
ENABLED_FEATURE = [Features.Interview, Features.RemoteManager, Features.Fun_Log, Features.Raw_Log]