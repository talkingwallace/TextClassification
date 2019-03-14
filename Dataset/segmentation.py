import pkuseg # 分词包
from os import path
import pandas as pd

filePath = path.dirname(__file__)
user_dict = ['_',]

def getSegFunc():
    return pkuseg.pkuseg(model_name= r'../resources/weibo_seg',user_dict=user_dict)

def makeCorpus(df,contentIndex='content'):
    """
    分词并且产生一个文集（corpus),corpus由许多文档组成(这里是单条评论)
    :return:
    """
    l = list(df[contentIndex])
    seg = getSegFunc()
    rs = []
    count = 0
    for i in l:
        print(count)
        rs.append(seg.cut(i))
        count += 1
    return rs


def loadSegmentedData():
    df = pd.read_json(filePath+r'\\'+r'segSmpl.json')
    return df