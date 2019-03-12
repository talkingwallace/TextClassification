# 对数据进行初步的处理

import pandas as pd
import re

labels = ['ym','gfs','moha',]

def filter1(target): #过滤贴吧 格式（回复 xxxxx :）
    target = re.sub('.*：',"",re.sub(r'.*:',"",target))
    rs = re.search('([^,.]\s)+.', target) # 找 出 打 字 带 空 格 的
    if rs!= None:
        target = target.replace(rs.group(),rs.group().replace(' ','_'))
    return target


def filter2(target): #过滤微博的回复 格式 (ID: 回复 @xxxx :)
    s = re.sub('.*:',"",re.sub(r'回复@.*:',"",target)) #可能存在中英两种 ':' '：'
    s = re.sub('.*：', "", re.sub(r'回复@.*：', "", s))
    return re.sub('@.* ',"",s)

def linkDetector(target): #检测是否有网页连接
    if len(re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',target))>0:
        return True
    else:
        return False


def makeLabel(contList,label):
    """
    创建带标签的数据集
    :param contList:
    :param label:
    :return:
    """
    df_labelled = pd.DataFrame()
    df_labelled['content'] = contList
    df_labelled['label'] = [label] * len(contList)
    return df_labelled

def preprocessor(df,indexName,filter,detector):

    """
    预处理
    :param df: dataframe
    :param indexName: 内容index
    :param filter: 正则过滤函数
    :param detector: 检测函数
    :return: list
    """
    l = df[indexName]
    rs = []
    for i in l:
        if detector(i) == True or len(i) <= 1:
            continue
        else:
            s = filter(i)
            if len(s)<=1:
                continue
            rs.append(s)

    return rs


def preprocessSmallDataset():
    df_zxydym = pd.read_csv(r'zxydym.csv')
    df_zxyzym = pd.read_csv(r'zxyzym.csv')
    df_Sharon = pd.read_csv(r'Sharon.csv')
    df_sxc = pd.read_csv(r'sxc.csv')

    rs1 = preprocessor(df_zxydym, 'content', filter1, linkDetector)
    rs2 = preprocessor(df_zxyzym, 'content', filter1, linkDetector)
    rs3 = preprocessor(df_Sharon, 'comment_cont', filter2, linkDetector)
    rs4 = preprocessor(df_sxc, 'comment_cont', filter2, linkDetector)

    rs_combine = rs1 + rs2
    df1 = makeLabel(rs_combine, 'ym')
    df2 = makeLabel(rs3, 'mh')
    df3 = makeLabel(rs4, 'sxc')

    df = pd.concat([df1, df2, df3])
    df.to_csv('smallData.csv', index=False)

preprocessSmallDataset()


