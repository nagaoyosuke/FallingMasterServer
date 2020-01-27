import requests

response = requests.post('http://localhost:8000/post', data='{"state":"ScoreAppend", "unity":"True", "mode":"dani", "name":"client2", "score":"10"}')
print(response.status_code)    # HTTPのステータスコード取得
print(response.text)    # レスポンスのHTMLを文字列で取得