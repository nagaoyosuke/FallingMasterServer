import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#Webで確認するよう
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webpageget', methods=["GET"])
def WebPage_GET():
    return render_template('index.html',dani_first_name="Unity",dani_first_score="皆伝")

#ここからはUnityからのやつ
#ランキング反映
@app.route('/post', methods=["POST"])
def do_POST():
    #jsonに変換するために一回文字列に変えてる
    get_data = request.data.decode('utf-8')
    get_data = json.loads(get_data)
    
    send_data = GetRankCheckJson()
    send_data['status'] = "True"
    send_data['message'] = "ChangeOK"

    return json.dumps(send_data)

def GetRankCheckJson():
    with open('JSON/RankCheck.json') as f:
        data = json.load(f)
        return data