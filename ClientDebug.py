import requests

response = requests.post('http://localhost:8000/post', data='{"key": "bar"}')
print(response.status_code)    # HTTPのステータスコード取得
print(response.text)    # レスポンスのHTMLを文字列で取得
