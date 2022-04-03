import requests
url = 'https://yunqidi.cn/teacherplatform/v2/lecture/lecture/online/view_lecture?coursewareOnlineId=3bd5b939-c82e-4e79-9f7e-7dd9b6ad5b9d&teacherId=69d4445b-0f67-48ae-803d-be5baaa9db59&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGllbnRJZCI6Inl1bnFpZGkiLCJhcHBUeXBlIjozLCJpc3MiOiJBVVRIX0NFTlRFUiIsInVzZXJUeXBlIjowLCJ0b2tlblR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJ1c2VySWQiOiI2OWQ0NDQ1Yi0wZjY3LTQ4YWUtODAzZC1iZTViYWFhOWRiNTkiLCJpYXQiOjE2NDg1NjA0MzEsIm9yZ0lkIjoiMTlhZjE4MDUtOGRlOC00NTgzLWI1MDctMWZjYmY4MjI5M2U1IiwidXNlcm5hbWUiOiIxODk4MzIwNDYxNSJ9.jNSDS8AlWsiYPN37gYlBU-uZAFNGyCbRnLQJFkqSGBw'
headers ={
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}
res = requests.get(url, headers=headers)
print(res.json())
#
