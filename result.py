#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from flask import Flask, redirect, url_for, request, render_template, json, Response, jsonify
import test
import re

app = Flask(__name__)


@app.route('/hello/<answer>')
def hello(answer):
    return '%s' % answer

@app.route('/result/', methods=['POST', 'GET'])
@app.route('/')
def result():
    data = {}
    answer = {'answer': 'a'}
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        print(data['question'])
        
        if data['question'] != None:
            print('question')
            a = test.chatbot(data['question'])
            a = re.sub(r'[<>unk/s]{1,100}','',a)
            answer['answer'] = a
            return jsonify(answer)
            # return render_template('result.html', **answer)
        else:
            print('!q')
            return jsonify(answer)
            # return render_template('result.html', **answer)
            # return redirect(url_for('hello', answer=1))

    else:
        print('!post')
        return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)