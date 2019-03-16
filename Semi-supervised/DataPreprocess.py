from Dataset.DataFilter import defaultFilters
from Dataset.DataFilter import Filter
from Dataset.DataFilter import processAclass
from Dataset.DataFilter import getPatternFilter
import pandas as pd

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
defaultFilters.append(getPatternFilter(keys))
df_pos,df_neg = processAclass(df1,defaultFilters,'pos',keepRest=True)
df_neg['label'] = ['neg']*len(df_neg)
tmp = processAclass(df2,defaultFilters,'neg',keepRest=False)
df_neg = pd.concat([df_neg,tmp])
df_neg = df_neg.reset_index()
# 分词


# 嵌入


# 生成特征文档