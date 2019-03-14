# 使用PCA或者TSNE可视化高维数据
from sklearn.manifold import TSNE
import seaborn as sns
from seaborn import scatterplot
import pandas as pd
import matplotlib.pyplot as plt

def TsneVisualize(x,y,dim = 2):

    df = pd.DataFrame()
    x_ = TSNE(n_components=2).fit_transform(x)
    df['x1'] = x_[:,0]
    df['x2'] = x_[:,1]
    df['y'] = y
    ax = sns.scatterplot(x="x1", y="x2",hue='y',data=df)
    plt.show()
    return x_,y

def dataSetToList(dataset):
    """
    把dataset转成两个list 一个是特征 一个是标签
    :return: 2 list
    """
    features = []
    labels = []
    for i in dataset:
        features.append(list(i[0]))
        labels.append(i[1])

    return features,labels

from Dataset.DataLoader import splitDataset
import pickle
f = open('dataset.pkl','br')
td = pickle.load(f)
train,_ = splitDataset(dataset=td)
f,l = dataSetToList(train)
TsneVisualize(f[0:5000],l[0:5000])