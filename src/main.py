
# 控制台测试用
# import sys
# sys.path.append(r'D:\CityU_CS\CS5483_DataMining\TextClassification')
# import os
# os.chdir(r'D:\CityU_CS\CS5483_DataMining\TextClassification\src')

import pickle
import pandas as pd
import Dataset.DataLoader as dl
import src.segmentation as sg
from src.segmentation import loadSegmentedData
from src.embedding import trainEmbedding
from src.embedding import loadEmbedding

# word2vec 词嵌入
import gensim
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec # 记录 callback 用

# # 分词
# df = dl.loadSmallSmplData()
# rs = sg.makeCorpus(df)
#
# #
# # 保存分词结果
# df['content'] = rs
# df.to_json('segSmpl.json')

df = loadSegmentedData()

# print('start word embedding')
# model = trainEmbedding(df)

model = loadEmbedding()
print(len(model.wv.vocab))

# 载入Data接口

td = dl.TextData(model,df)

print(len(td))