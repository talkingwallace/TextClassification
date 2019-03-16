import requests
from bs4 import BeautifulSoup
import json

text = '我给你最后的爱是手放开'  # 需要转换的文本

payload = {'q': text}
headers = {"Content-Type": "application/x-www-form-urlencoded"}
result = requests.post(url='http://www.fzlft.com/', headers=headers, data=payload).text
soup = BeautifulSoup(result, "lxml")
res_list = soup.find_all(name='textarea')
for item in res_list:
    print(item.text)

