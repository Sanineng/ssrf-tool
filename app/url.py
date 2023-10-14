import urllib.request
import urllib.error
import sys

# 요청을 보낼 URL
url = 'http://123:123@124'

# GET 요청 보내기
try:
    response = urllib.request.urlopen(url)
    
    # 응답 코드 출력
    print('Response code :', response.code)

    # 응답 내용 출력
    content = response.read()
    print('Response Content:', content.decode('utf-8'))

except urllib.error.URLError as e:
    print('Error occoured:', e)

