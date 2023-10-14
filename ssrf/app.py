import re
import json
import urllib.parse
import requests
import copy

def request(method, url, headers, data):

    if url.find("http") != 0 and url.find("https") != 0:
        url = 'http://' + url

    if method == "GET":
        res = requests.get(url=url, headers=headers)
    elif method == "POST":
        if 'Content-type' in headers and "application/json" in headers['Content-type']:
            res = requests.post(url=url, headers=headers, json=data)
        else:
            res = requests.post(url=url, headers=headers, data=data)

    print("Response data : ", res.text)

class Packet:
    def __init__(self, file_path):
        self.file_path = file_path
        self.method = None
        self.path = None
        self.version = None
        self.headers = {}
        self.body = None
        self.data = {}
        self.parse_packet()

    def data_to_dict(self):
        
        if self.method == "POST":

            # Handle JSON data
            if self.headers.get('Content-Type') and "application/json" in self.headers['Content-Type']:
                self.data = json.loads(self.body)

            # Handle XML data
            elif self.headers.get('Content-Type') and "application/xml" in self.headers['Content-Type']:
                self.data = {'__xml__': self.body}

            # Handle FORM data
            else:
                for arg in self.body.split("&"):
                    regex = re.compile('(.*)=(.*)')
                    for name, value in regex.findall(arg):
                        name = urllib.parse.unquote(name)
                        value = urllib.parse.unquote(value)
                        self.data[name] = value

    def parse_packet(self):
        try:
            with open(self.file_path, 'r') as file:
                packet_data = file.read()

                # HTTP 요청은 첫 줄에 시작하며, 첫 번째 단어는 메서드, 두 번째는 경로, 세 번째는 버전입니다.
                request_line = packet_data.split('\n')[0]
                self.method, self.path, self.version = re.split(r'\s+', request_line)

                # 헤더와 바디를 나누기 위해 빈 줄을 찾습니다.
                
                headers , self.body = re.split(r'\n\n', packet_data, 1) if '\n\n' in packet_data else (packet_data, '')

                # 헤더를 파싱하여 딕셔너리로 만듭니다.
                header_lines = headers.split('\n')[1:]
                self.headers = {line.split(': ')[0]: line.split(': ')[1] for line in header_lines if ': ' in line}

                # 데이터를 딕셔너리로 변환
                self.data_to_dict()

        except FileNotFoundError:
            print(f"Error: File not found at {self.file_path}")
        except Exception as e:
            print(f"Error reading file: {e}")

# 파일 경로를 입력하여 Packet 인스턴스 생성

file_path = input()
packet_instance = Packet(file_path)

# 결과 출력
print("Parsed HTTP Request:")
print(f"Method: {packet_instance.method}")
print(f"Path: {packet_instance.path}")
print(f"HTTP Version: {packet_instance.version}")
print("Headers:")
for key, value in packet_instance.headers.items():
    print(f"  {key}: {value}")
print(f"Body:\n{packet_instance.body}")
print("Data: ", packet_instance.data)

ssrf_data = []

for key in packet_instance.data.keys():
    sub = packet_instance.data.copy()
    sub[key] = '127.0.0.1'
    ssrf_data.append(sub)

print(ssrf_data)

for data in ssrf_data:
    request(packet_instance.method, packet_instance.headers['Host'], packet_instance.headers, data)


