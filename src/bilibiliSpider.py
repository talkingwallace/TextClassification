import requests
import json
from bs4 import BeautifulSoup as bs
from os import path
import re

filePath = path.dirname(__file__)
import time
import pickle
import sys

# query url 查询用的link
qURL = r'https://search.bilibili.com/all?keyword='

# 要筛掉前排的弱智评论关键词
simakeywords = ['前', '留', '复兴', '来了', '*']

# 关键词和页数
para = {
    'ly': [['淋语', 2], ['淋淋', 2]],
    'ym': [['先辈', 8], ['真夏夜', 5]],
    'liuxue': [['六学', 2]],  #
    'goufensi': [['孙笑川', 4], ['带带大师兄', 10], ['抽象圣经', 2], ],
    'jojo': [['jojo', 5]],  #
    'other': [['中国', 2], ['城市', 3], ['日本 中国', 2], ['数据可视化', 2], ]
}
# quin 类 自己收集的
quin = [15870645, 29651746, 17206858, 16650632, 17154202, 42533046, 8732054]
# zhuxue类 自己收集的
zhexue = [42123157, 44283479, 30769568, 35582226]


# 按关键词获取av号
def getAVnumByKws(key, pages=5):
    def extractAVNum(soup):
        l = soup.find_all('a', class_='title')
        avs = []
        for i in l:
            try:
                avstr = re.search('(av)(.+)(\?)', i['href']).group().replace('?', '')
                avint = avstr.replace('av', '')
                avs.append(avint)
            except:
                print(i)
        return avs

    avs = []
    pageNum = pages
    for i in range(1, pageNum + 1):
        resp = requests.get(qURL + key + '&page=' + str(i))
        soup = bs(resp.text)
        avNum = extractAVNum(soup)
        avs += avNum
    return avs


# 根据av号爬取bilibili评论
def getAllCommentList(item):
    info_list = []
    url = "http://api.bilibili.com/x/reply?type=1&oid=" + str(item) + "&pn=1&nohot=1&sort=0"
    r = requests.get(url)
    numtext = r.text
    # print(numtext)
    try:
        json_text = json.loads(numtext)
        commentsNum = json_text["data"]["page"]["count"]
        page = commentsNum // 20 + 1
        print('page: ' + str(page))
        for n in range(1, page):
            url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=" + str(n) + "&type=1&oid=" + str(
                item) + "&sort=1&nohot=1"
            req = requests.get(url)
            text = req.text
            json_text_list = json.loads(text)
            for i in json_text_list["data"]["replies"]:
                info_list.append(i["content"]["message"])
            if 0.24 < n / page < 0.26:
                print('{0}, about 25% replies of this video finished'.format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            if 0.49 < n / page < 0.51:
                print('{0}, about 50% replies of this video finished'.format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            if 0.74 < n / page < 0.76:
                print('{0}, about 75% replies of this video finished'.format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            # print(str(n) + '/' + str(page) + ' page finished')
            time.sleep(2)
    except:
        time.sleep(2)
        print('no comment')
        return []
    return info_list


# 根据上面的参数获取av 号
def getAvList():
    avList = {}
    avList['quin'] = quin
    avList['zhexue'] = zhexue
    for i in para:
        avNum = []
        print('collecting query result:', i)
        for k in para[i]:
            avNum += getAVnumByKws(k[0], pages=k[1])
        avList[i] = avNum
    return avList


# 按av号收集评论
def collectReview(avList, classList):
    # rs = {}
    for i in classList:
        tmp = {}
        print('processing class:', i)
        print(str(len(avList[i])) + ' videos in ' + i)
        count = 0
        for k in avList[i]:
            print('avid:', k)
            reviews = getAllCommentList(k)
            print(str(len(reviews)) + ' reviews in avid: ' + str(k))
            tmp[k] = reviews
            count += 1
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ', ' + str(count) + '/' + str(len(avList[i])) + ' video of ' + i + ' finished')
        # rs[i] = tmp
        pickle.dump(tmp, open(i + '.pkl', 'bw'))
        print('processed class:', i)
    # return rs


# 获取参数
print(sys.argv)
targetList = sys.argv[1].split(',')
# outputname = sys.argv[2]
print('going to collect classes:', targetList)

# 收集av号
avList = getAvList()

print(len(avList), 'class collected')
totalNum = 0
for i in avList:
    totalNum += len(avList[i])
print('in total:', totalNum, ' videos')

# 根据av号收集评论

# ly,liuxue,other part1
# zhexue,quin,goufensi part2
# ym,jojo part3
collectReview(avList, targetList)
# result = collectReview(avList, targetList)
#
# pickle.dump(result, open(outputname + '.pkl', 'bw'))
