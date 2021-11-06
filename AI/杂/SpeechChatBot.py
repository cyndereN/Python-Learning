import os
import time
import requests
from json import loads
import json
from aip import AipSpeech
import time
import contextlib
import random

audio=Config.Config.audio
listen_voice_path=Config.Config.listen_voice_path
ll_voice_paths=Config.Config.all_return_voice



def speak_word(word_text):#说
    cover2mps(word_text)#转换音频
    play_mp3(audio)#播放音频

def cover2mps(word_text):# 这是使用百度的语音合成代码，来合成下面填入 APP_ID 和 API_KEY SECRET_KEY
    APP_ID = Config.Config.APP_ID
    API_KEY = Config.Config.API_KEY
    SECRET_KEY = Config.Config.SECRET_KEY

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    result  = client.synthesis(word_text, 'zh', 1, {
        'vol': 5,"per":4,
    })
    if not isinstance(result, dict):
        with open(audio, 'wb') as f:
            f.write(result)


def play_mp3(filename):#使用 mpg123 播放MP3
    os.system('mpg123 %s' % (filename))

def think(text):#连接图灵api调用聊天模块
    #session=requests.session()
    url = 'http://openapi.tuling123.com/openapi/api/v2'
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": text
            },
            "selfInfo": {
                "location": {
                    "city": "",
                    "province": "",
                    "street": ""
                }
            }
        },
        "userInfo": {
            "apiKey": Config.Config.TU_LING_KEY,
            "userId": "123456lll"
        }
    }
    response = requests.post(url=url, data=json.dumps(data)).json()
    final_result=think_to_text(response)
    return  final_result


def think_to_text(return_result):
    for i in return_result["results"]:
        if i["resultType"] == "text":
            word_text = i["values"]["text"]
            print word_text
            return word_text

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def voice_to_text(filePath):# 使用百度api吧声音传成文字
    APP_ID = Config.Config.APP_ID
    API_KEY = Config.Config.API_KEY
    SECRET_KEY = Config.Config.SECRET_KEY

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    result  = client.asr(get_file_content(filePath), 'wav', 16000, {'dev_pid': 1536,})
    print result["err_msg"]
    if "success" in result["err_msg"]:
        return result["result"][0]
def go_listen():#听
    listen_voice_path = Config.Config.listen_voice_path
    os.system('arecord -f S16_LE -d 3 -r 16000 %s' % (listen_voice_path))


go_listen()#听 
works=voice_to_text(listen_voice_path）#声音转换为 文字
final_result = think(works)#文字传给图灵 进行想
speak_word(final_result)#说，想时候使用百度的语音合成返回，完成一次交互