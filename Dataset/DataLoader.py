import pandas as pd
from torch.utils.data import Dataset
import numpy as np

# 路径测试用
# import sys
# sys.path.append(r'D:\CityU_CS\CS5483_DataMining\TextClassification')
# import os
# os.chdir(r'D:\CityU_CS\CS5483_DataMining\TextClassification\Dataset')

from os import path
filePath = path.dirname(__file__)

def loadSmallSmplData():
    """
    加载小样本数据集
    :return:
    """
    try:
        return pd.read_csv(filePath+r'/smallData.csv')
    except:
        print('cant find smallData.csv')
        return None


class TextData(Dataset):


    """
    初始化
    :param w2vModel: 词向量look up table
    :param segData: pandas dataframe 已经分好词的dataframe
    :param labelIndex: segData里文本类的column
    """
    def __init__(self,w2vModel,segData,labelIndex = 'label',contentLabel = 'content'):

        self.w2vModel = w2vModel
        self.segData = segData
        self.labelIndex = labelIndex
        self.contentLabel = contentLabel
        self.dim = w2vModel.layer1_size # 词向量维度
        lbls = list(segData.groupby(labelIndex).count().index)
        lookUp = {}

        # 把label转换成数字
        count = 0
        for i in lbls:
            lookUp[i] = count
            count+=1
        self.classes = lookUp
        rs = self.generateDocFeature()
        self.segData['vec'] = rs
        self.data = [i for i in zip(list(self.segData['vec']),list(self.segData[labelIndex]))]

    def generateDocFeature(self):
        """
        给每个文本生成一个学习用的特征向量
        :return:
        """
        rs = []
        content = list(self.segData[self.contentLabel])
        smplNum = 0
        for i in content:
            print('smplNum:',smplNum)
            vec = np.zeros(self.dim)
            count = 1
            for k in i:
                count+=1
                vec += self.w2vModel[k]
            rs.append(vec/count)
            smplNum += 1
        return rs

    def __getitem__(self,index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def getTextContent(self,index):
        return self.segData.loc[index]

