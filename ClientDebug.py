import requests

response = requests.post('http://localhost:8000/post', data='{"state":"ScoreAppend", "unity":"True", "mode":"endless", "name":"client2", "score":"950"}')
print(response.status_code)    # HTTPのステータスコード取得
print(response.text)    # レスポンスのHTMLを文字列で取得