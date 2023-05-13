"""
* @project       GeneralQBOT
* @author        XYCode <xycode-xyc@outlook.com>
* @date          2023-05-03 08:34:29
* @lastModified  2023-05-13 18:39:23
"""
import json
import base64
from typing import *
import configs.config as config
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tms.v20201229 import tms_client, models

def tencent_moderation(text: str) -> Dict[str, Union[bool, models.TextModerationResponse]]:
    cred = credential.Credential(config.QCLOUD_SECRET_ID, config.QCLOUD_SECRET_KEY)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "tms.tencentcloudapi.com"
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = tms_client.TmsClient(cred, "ap-beijing", clientProfile)

    req = models.TextModerationRequest()
    params = {
        "Content": base64.b64encode(text.encode('utf-8')).decode('utf-8')
    }
    req.from_json_string(json.dumps(params))

    resp = client.TextModeration(req)
    
    return {
        'bad': resp.Suggestion == 'Pass',
        'resp': resp
    }

__all__ = ['tencent_moderation']
