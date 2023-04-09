# 开发时间: 2023/4/5
from flask import Flask, jsonify, request
import openai
import json
import jsonpath
from flask import Flask
from flask_cors import CORS
import os
from pyairtable import Table

api_key = 'keyeiDgcTmA161KLa'
table = Table(api_key, 'appAr3TiyzS3bFg8J', 'UID=0001')

app = Flask(__name__)
CORS(app)

openai.api_key = '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'

@app.route('/api/chatgpt', methods=['GET', 'POST'])
def chatgpt():
    if request.method == 'GET':
        question = request.args.get('question')
        context = request.args.get('context')
        prompt_type = request.args.get('prompt_type')
        userQuestion = request.args.get('userQuestion')
    else:
        data = request.get_json()
        question = data['question']
        prompt_type = data['prompt_type']
        userQuestion = data['userQuestion']
        context = data.get('context', {})
    print(prompt_type,userQuestion,question)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # model="gpt-4",
        messages=[
            {"role": "assistant", "content":question}
        ]
    )
    res = ''.join(jsonpath.jsonpath(json.loads(str(completion)), '$..content'))
    answer = res
    context = question + res
    response = {
        'answer': answer,
        'context': context
    }
    table.batch_create([{'Uid': 1, 'Chat_topic': prompt_type, 'Questions': userQuestion, 'GPT_Answer': res}])
    return jsonify(response)



@app.route('/api/get_chat_history', methods=['GET', 'POST'])
def get_chat_history():
    data = table.all()
    new_data = []
    for d in data:
        if 'Questions' in d['fields'] and 'GPT_Answer' in d['fields']:
            new_d = {'Uid': d['fields']['Uid'], 'Date': d['fields']['Date'], 'Chat_topic': d['fields']['Chat_topic'], 'Questions': d['fields']['Questions'], 'GPT_Answer': d['fields']['GPT_Answer']}
            new_data.append(new_d)
    return new_data








if __name__ == '__main__':
    app.run(debug=True)
# 开发时间: 2023/4/5
# -*- coding:utf-8 -*-
