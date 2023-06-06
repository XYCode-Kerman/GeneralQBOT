"""
* @project       GeneralQBOT
* @author        XYCode <xycode-xyc@outlook.com>
* @date          2023-05-03 08:34:29
* @lastModified  2023-05-14 16:49:03
"""
import json
import base64
import numpy as np
import jieba
from typing import *
import configs.config as config
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tms.v20201229 import tms_client, models

tokenizer = None

def texts_to_seq(texts: list) -> np.ndarray:
    seq = []

    for text in texts:
        try:
            words = jieba.lcut(text)
        except:
            words = ['UNK']

        text_seq = []

        for word in words:
            try:
                text_seq.append(tokenizer.texts_to_sequences([word])[0][0])
            except:
                text_seq.append(0)

        seq.append(text_seq)
        print('processed', text, text_seq)

    return seq

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

def ai_moderation(text: str) -> Dict[str, Union[bool, models.TextModerationResponse]]:
    import tensorflow as tf
    if tokenizer is None:
        tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(open('./models/tms_token.json').read())
    model: tf.keras.models.Sequential = tf.keras.models.load_model('./models/tms.tf')
    
    result = model.predict(texts_to_seq([text]))
    result = result[0][0]
    
    class Resp:
        Score = 0
    
    resp = Resp()
    resp.Score = result * 100
    
    # print(result)
    
    return {
        'bad': not (result > 0.7),
        'resp': resp
    }

__all__ = ['tencent_moderation', 'ai_moderation']
