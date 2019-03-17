import pkuseg  # 分词包
from os import path
import pandas as pd
import multiprocessing
from multiprocessing import Process, Pool, Lock, Manager
from multiprocessing.dummy import Pool as ThreadPool
import datetime

filePath = path.dirname(__file__)
user_dict = ['_____', ]


def getSegFunc():
    return pkuseg.pkuseg(model_name=filePath + r'/../resources/weibo_seg', user_dict=user_dict)


def wordCut(seg, item, count):
    print(count)
    return seg.cut(item)


def makeCorpus(df, contentIndex='content'):
    """
    分词并且产生一个文集（corpus),corpus由许多文档组成(这里是单条评论)
    :return:
    """
    starttime = datetime.datetime.now()
    l = list(df[contentIndex])
    seg = getSegFunc()
    rs = []
    rs_tmp = []
    count = 0
    pool = ThreadPool(multiprocessing.cpu_count() - 1)
    for i in l:
        rs_tmp.append(pool.apply_async(func=wordCut, args=(seg, i, count)))
        # print(count)
        # rs.append(seg.cut(i))
        count += 1
    pool.close()
    pool.join()
    for i in rs_tmp:
        if i.get() is not None:
            rs.append(i.get())
    endtime = datetime.datetime.now()
    print("Time used of makeCorpus for {0} data: {1}s.".format(str(count), str((endtime - starttime).seconds)))
    return rs


def loadSegmentedData():
    df = pd.read_json(filePath + r'\\' + r'segSmpl.json')
    return df


def loadRawData():
    pass


if __name__ == '__main__':
    df = pd.read_csv(filePath + "/RawData/Mr_quin.csv")
    makeCorpus(df=df, contentIndex='comment_cont')