
# 控制台测试用
# import sys
# sys.path.append(r'D:\CityU_CS\CS5483_DataMining\TextClassification')
# import os
# os.chdir(r'D:\CityU_CS\CS5483_DataMining\TextClassification\src')

import pickle
import pandas as pd
import Dataset.DataLoader as dl
from Dataset.segmentation import loadSegmentedData
from Dataset.embedding import trainEmbedding
from Dataset.embedding import loadEmbedding
from src.NetworkTrainer import Trainer
from src.Network import SimpleClasifier
from src.Network import DeeperClassifier
import torch
from Dataset.DataLoader import TextDataLoader

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
# shortcut
# td = dl.TextData(model,df)
# f = open('dataset.pkl','bw')
# pickle.dump(td,f)
f = open('dataset.pkl','br')
td = pickle.load(f)
# print(len(td))

# 参数
para = {
    'num_epoch': 50, # 代数
    'batch_size': 5000,
    'lr': 0.005, # learning rate
    'categoryNums':3, # 3个类
    'useGPU':True, # 开启GPU模式
    'saveEveryEpochs':10, # 每多少代保存一次模型
    'willDecay':True, # 学习率是否衰减
    'learningDecay':0.5,
    'decayWhen':10 # 每三十代decay
}

# 训练简单的神经网络分类器
# net = SimpleClasifier(50,25,3).cuda()
net = DeeperClassifier([50,120,60,30,15],3).cuda()

# 使用SGD优化器 传入网络参数与学习率lr
optimizer = torch.optim.Adam(net.parameters(),lr=para['lr'],)

# 损失函数 交叉熵
lossFunc = torch.nn.CrossEntropyLoss()

# 获取 训练 测试集合
train,test = TextDataLoader(td,para['batch_size'])

# 训练器
trainer = Trainer(net,optimizer,lossFunc,train,test,para)

trainer.train()
trainer.test()


