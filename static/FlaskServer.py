import os
import json
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
dsn = 'ここ'

dani_base = ['なし','初段','弐段','参段','四段','伍段','六段','七段','八段','九段','十段','皆伝']

#Webで確認するよう
@app.route('/')
def index():
    r = RankingSubmit()
    d = r[0]
    e = r[1]
    return render_template('index.html',d_1_n=d[0][0],d_1_s=d[0][1],d_2_n=d[1][0],d_2_s=d[1][1],d_3_n=d[2][0],d_3_s=d[2][1],d_4_n=d[3][0],d_4_s=d[3][1],d_5_n=d[4][0],d_5_s=d[4][1],
                            e_1_n=e[0][0],e_1_s=e[0][1],e_2_n=e[1][0],e_2_s=e[1][1],e_3_n=e[2][0],e_3_s=e[2][1],e_4_n=e[3][0],e_4_s=e[3][1],e_5_n=e[4][0],e_5_s=e[4][1])

@app.route('/webpageget', methods=["GET"])
def WebPage_GET():
    r = RankingSubmit()
    d = r[0]
    e = r[1]
    return render_template('index.html',d_1_n=d[0][0],d_1_s=d[0][1],d_2_n=d[1][0],d_2_s=d[1][1],d_3_n=d[2][0],d_3_s=d[2][1],d_4_n=d[3][0],d_4_s=d[3][1],d_5_n=d[4][0],d_5_s=d[4][1],
                            e_1_n=e[0][0],e_1_s=e[0][1],e_2_n=e[1][0],e_2_s=e[1][1],e_3_n=e[2][0],e_3_s=e[2][1],e_4_n=e[3][0],e_4_s=e[3][1],e_5_n=e[4][0],e_5_s=e[4][1])


#ここからはUnityからのやつ
#ランキング反映
@app.route('/post', methods=["POST"])
def do_POST():
    #jsonに変換するために一回文字列に変えてる
    get_data = request.data.decode('utf-8')
    get_data = json.loads(get_data)
    
    if get_data['unity'] != "True":
        print('Other Connection Error')
        return ""

    if get_data['state'] == 'ScoreAppend':
        send_data = ScoreAppend(get_data)
    elif get_data['state'] == 'GetScore':
        send_data = Get_Score(get_data)

    return json.dumps(send_data,ensure_ascii=False)

def ScoreAppend(get_data):
    mode = get_data['mode']
    ranking = RankingCheck(mode,get_data)

    send_data = Get_ScoreAppendJson()
    send_data['state'] = "Info"
    send_data['message'] = "ChangeOK"
    send_data['mode'] = mode
    send_data['ranking'] = str(ranking)

    print('{state}::mode={mode},name={name},score={score},ranking={ranking}'.format(state=get_data['state'],mode=mode,name=get_data['name'],score=get_data['score'],ranking=ranking))
    return send_data

def Get_Score(get_data):
    r = RankingSubmit()
    d = r[0]
    e = r[1]

    base = dict([('name','名無し'), ('score','123')])
    send_data = {"state": "GetScore","dani": [],"endless": []}

    send_data['dani'].append(Get_Best5(d))
    send_data['endless'].append(Get_Best5(e))

    print('{state}::OK'.format(state=send_data['state']))
    return send_data

def Get_Best5(mode):
    base = dict([('name','名無し'), ('score','123')])
    data = []
    count = 0
    for n in mode:
        count += 1
        if count > 5: 
            break
        b = base.copy()
        b['name'] = n[0]
        b['score'] = n[1]
        data.append(b)
        print(b)
    return data

def Get_ScoreAppendJson():
    with open('static/JSON/ScoreAppend.json') as f:
        data = json.load(f)
        return data

def Set_DBPass(p):
    global dsn
    dsn = p

def Get_Connection():
    return psycopg2.connect(dsn)

def RankingSubmit():
    with Get_Connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM dani')
            d = cur.fetchall()
            d.sort(key=lambda x: x[1], reverse=True)
            d = [(i[0],dani_base[i[1]]) for i in d]
            cur.execute('SELECT * FROM endless')
            e = cur.fetchall()
            e.sort(key=lambda x: x[1], reverse=True)
            return (d,e)

def DaniRankCheck(get_data):
    return 12345

def RankingCheck(mode,get_data):
    name = str(get_data['name'])
    score = int(get_data['score'])
    ranking = 100
    with Get_Connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM {mode}'.format(mode=mode))
            rows = cur.fetchall()
            #スコアで並び替え
            rows.sort(key=lambda x: x[1], reverse=True)
            ranking = len([i for i in rows if i[1] > score]) + 1
            cur.execute('INSERT INTO {mode} VALUES ({name}, {score})'.format(mode=mode, name="'"+name+"'", score=score))
    return ranking