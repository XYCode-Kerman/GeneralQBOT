"""
* @project       GeneralQBOT
* @author        XYCode-Kerman <xycode-xyc@outlook.com>
* @date          1970-01-01 08:00:00
* @lastModified  2023-05-14 17:12:12
"""
import openai
import configs.config
import datetime

openai.api_key = configs.config.OPENAI_KEY

def generate_by_gpt(tips: str, data: str):
    data = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'system',
                'content': f'现在是北京时间 {datetime.datetime.now()}'
            },
            {
                'role': 'system',
                'content': tips
            },
            {
                'role': 'user',
                'content': data
            }
        ]
    )
    
    return data.choices[0].message["content"]