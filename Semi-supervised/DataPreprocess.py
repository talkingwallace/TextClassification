from Dataset.DataFilter import defaultFilters
from Dataset.DataFilter import Filter
from Dataset.DataFilter import processAclass
from Dataset.DataFilter import getPatternFilter
import pandas as pd
from Dataset.segmentation import makeCorpus
from Dataset.embedding import trainEmbedding
from Dataset.DataLoader import TextData
from gensim.models import Word2Vec
from Dataset.segmentation import getSegFunc
import pandas as pd
from src.ClassicMethod import runAndTestRF
from src.ClassicMethod import runAndTestKnn
import numpy as np


# 通过训练来不停的筛选新样本
class Trainer():

    def __init__(self,df,trainFrac = 0.9):
        self.pos = df[df['label'] == 'pos'].copy()
        self.rest = df[df['label'] == 'rest'].copy()
        self.neg = df[df['label'] == 'neg'].copy()
        self.labelToIndex = {'neg':0,'pos':1,'rest':2}
        self.pos['label'] = [1]*len(self.pos)
        self.neg['label'] = [0]*len(self.neg)
        self.rest['label'] = [2]*len(self.rest)
        self.frac = trainFrac

    def trainOnPos(self,trainFunc):
        """
        传入一个训练函数 返回一个classfier
        :return:
        """
        train_pos = self.pos.sample(frac=self.frac)
        test_pos = self.pos.drop(train_pos.index)
        train_neg = self.neg.sample(frac=self.frac)
        # test_neg = self.neg.drop(train_neg.index)
        train = pd.concat([train_pos,train_neg])
        test = test_pos
        classifier = trainFunc((list(train['vec']),list(train['label'])),(list(test['vec']),list(test['label'])))
        return classifier,test_pos

    def getNewSamples(self,classifier):
        X = self.rest['vec']
        predictions = classifier.predict(X)
        print(predictions)


file1 = 'jojo.csv'
file2 =  'other.csv'

# load keys
f = open('jojo.txt')
k = f.read()
k = k.replace('\n','')
key = k.split('##')
keys = []
for i in key:
    if len(i) == 0:
        continue
    keys.append(i.split(' '))

# 过滤
# df1 = pd.read_csv(file1)
# df2 = pd.read_csv(file2)
#
# df_ = processAclass(df1,defaultFilters,'pos')
# df_neg = processAclass(df2,defaultFilters,'neg',keepRest=False)
# df_neg = df_neg.reset_index()
#
# defaultFilters.append(getPatternFilter(keys))
# df_pos,df_rest = processAclass(df_,defaultFilters,'pos',keepRest=True)
# df_rest['label'] = ['rest']*len(df_rest)


# 分词
# pos_seg = makeCorpus(df_pos)
# neg_seg = makeCorpus(df_neg)
# rest_seg = makeCorpus(df_rest)
# df_rest['content'] = rest_seg
# df_pos['content'] = pos_seg
# df_neg['content'] = neg_seg
# df_neg = df_neg.drop(columns=['index'])

# 嵌入
# forEmbedding = pd.concat([df_neg,df_pos])
# forEmbedding = pd.concat([forEmbedding,df_rest])
# forEmbedding.to_json('segedData.data',index=False)
# forEmbedding = forEmbedding.reset_index()

# forEmbedding = pd.read_json(r'segData.json')
# model = trainEmbedding(forEmbedding,)
#
# # 生成特征文档
# td = TextData(model,forEmbedding)

import pickle
# f = open('dataset.pkl','bw')
# pickle.dump(td,f)
# f.close()

def mannuallyTest(target,model,classifier):
    seg = getSegFunc()
    s = seg.cut(target)
    vec = np.zeros(model.vector_size)
    count = 0
    for i in s:
        try:
            vec += model[i]
            count += 1
        except:
            print(i,' not in vocab')
    vec = vec/count
    return classifier.predict([vec])

f = open('dataset.pkl','br')
td = pickle.load(f)
trainer = Trainer(td.segData,trainFrac=0.9)
neigh,test_pos = trainer.trainOnPos(runAndTestRF)

print('making prediction')
predict = neigh.predict(list(trainer.rest['vec']))
trainer.rest['predict'] = predict


# from src.Visualize import TsneVisualize
# x1 = trainer.pos.sample(3000)
# x2 = trainer.neg.sample(6000)
# x = pd.concat([x1,x2])
# TsneVisualize(list(x['vec']),list(x['label']),)