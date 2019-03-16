import requests
from bs4 import BeautifulSoup

def toMarsWords(text):

    payload = {'q': text}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    result = requests.post(url='http://www.fzlft.com/', headers=headers, data=payload).text
    soup = BeautifulSoup(result, "html")
    res_list = soup.find_all(name='textarea')
    print(res_list)
    return res_list[2].text
