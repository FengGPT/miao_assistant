# 开发时间: 2023/4/5
# -*- coding:utf-8 -*-
# coding=utf-8
import sys
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app)


def get_tts_url(TEXT):
    # content= input('输入要转的内容')
    IS_PY3 = sys.version_info.major == 3
    if IS_PY3:
        from urllib.request import urlopen
        from urllib.request import Request
        from urllib.error import URLError
        from urllib.parse import urlencode
        from urllib.parse import quote_plus
    else:
        import urllib2
        from urllib import quote_plus
        from urllib2 import urlopen
        from urllib2 import Request
        from urllib2 import URLError
        from urllib import urlencode

    API_KEY = 'tVbSSQNOifM5OB3hhMovAyeP'
    SECRET_KEY = 'AVyb3EaZkBifHlWDTQylVfDZkGSAQxGj'

    # TEXT = content

    # 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
    # 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
    PER = 4
    # 语速，取值0-15，默认为5中语速
    SPD = 5
    # 音调，取值0-15，默认为5中语调
    PIT = 5
    # 音量，取值0-9，默认为5中音量
    VOL = 5
    # 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
    AUE = 3

    CUID = "123456PYTHON"

    TTS_URL = 'http://tsn.baidu.com/text2audio'


    class DemoError(Exception):
        pass


    """  TOKEN start """

    TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'
    SCOPE = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选


    def fetch_token():
        # print("fetch token begin")
        params = {'grant_type': 'client_credentials',
                  'client_id': API_KEY,
                  'client_secret': SECRET_KEY}
        post_data = urlencode(params)
        if (IS_PY3):
            post_data = post_data.encode('utf-8')
        req = Request(TOKEN_URL, post_data)
        try:
            f = urlopen(req, timeout=5)
            result_str = f.read()
        except URLError as err:
            # print('token http response http code : ' + str(err.code))
            result_str = err.read()
        if (IS_PY3):
            result_str = result_str.decode()

        # print(result_str)
        result = json.loads(result_str)
        # print(result)
        if ('access_token' in result.keys() and 'scope' in result.keys()):
            if not SCOPE in result['scope'].split(' '):
                raise DemoError('scope is not correct')
            # print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
            return result['access_token']
        else:
            raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


    """  TOKEN end """

    if __name__ == '__main__':
        token = fetch_token()
        tex = quote_plus(TEXT)  # 此处TEXT需要两次urlencode
        print(tex)
        params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': CUID,
                  'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

        data = urlencode(params)
        Browser_link = TTS_URL + '?' + data
        print(Browser_link)
        return (Browser_link)


@app.route('/api/v1/get_tts_url', methods=['GET', 'POST'])
@cross_origin()
def api_get_tts_url():
    if request.method == 'GET':
        text = request.args.get('text')
    elif request.method == 'POST':
        text = request.form.get('text')
    else:
        return jsonify({"error": "Invalid request method"}), 400

    if text is None:
        return jsonify({"error": "No 'text' parameter provided"}), 400

    try:
        url = get_tts_url(text)
        return jsonify({"url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

