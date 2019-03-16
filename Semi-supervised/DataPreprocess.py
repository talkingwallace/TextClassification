from Dataset.DataFilter import defaultFilters
from Dataset.DataFilter import Filter
from Dataset.DataFilter import processAclass
from Dataset.DataFilter import getPatternFilter
import pandas as pd
from Dataset.segmentation import makeCorpus
from Dataset.embedding import trainEmbedding

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
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

df_ = processAclass(df1,defaultFilters,'pos')
df_neg = processAclass(df2,defaultFilters,'neg',keepRest=False)
df_neg = df_neg.reset_index()

defaultFilters.append(getPatternFilter(keys))
df_pos,df_rest = processAclass(df_,defaultFilters,'pos',keepRest=True)
df_rest['label'] = ['rest']*len(df_rest)


# 分词
pos_seg = makeCorpus(df_pos)
neg_seg = makeCorpus(df_neg)
rest_seg = makeCorpus(df_rest)
df_rest['content'] = rest_seg
df_pos['content'] = pos_seg
df_neg['content'] = neg_seg
df_neg = df_neg.drop(columns=['index'])



# 嵌入
forEmbedding = pd.concat([df_neg,df_pos])
forEmbedding = pd.concat([forEmbedding,df_rest])
forEmbedding.to_json('segedData,data',index=False)
forEmbedding = forEmbedding.reset_index()

# 生成特征文档
