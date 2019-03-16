# 经典的方法 如KNN 随机森林 AdaBoost SVM blablabla

import pickle
from Dataset.DataLoader import splitDataset

# KNN
from sklearn.neighbors import KNeighborsClassifier

# Random Forest
from sklearn.ensemble import RandomForestClassifier

import numpy as np
# 加载小数据集
# f = open('dataset.pkl','br')
# td = pickle.load(f)
# train,test = splitDataset(td)

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

# KNN
def runAndTestKnn(train,test,n_neighbor = 6,speedUp = 'kd_tree',workers=-1,verbose = False,runTest = True):

    print('start training')
    neigh = KNeighborsClassifier(n_neighbors=n_neighbor,algorithm=speedUp,n_jobs=workers)
    f,l = dataSetToList(train)
    neigh.fit(f,l)
    tst_f,tst_l = dataSetToList(test)
    print('testing.....')

    if runTest == True:
        accs = []
        for i in range(0, 10):
            if verbose == True:
                print('testing batch:', i)
            acc = neigh.score(tst_f[i * 100:(i + 1) * 100], tst_l[i * 100:(i + 1) * 100])
            if verbose == True:
                print('acc of current batch', acc)
            accs.append(acc)
        if verbose == True:
            print('acc of KNN:', np.mean(accs))
        print(np.mean(accs))
    return neigh


# Random Forest
def runAndTestRF(train,test,runTest = True):
    print('start building RF')
    f, l = dataSetToList(train)
    t_f, t_l = dataSetToList(test)
    print('start traning......')
    forest = RandomForestClassifier(n_jobs=8,n_estimators=200,)
    forest.fit(f,l)
    if runTest == True:
        print('start testing.......')
        acc = forest.score(t_f, t_l)
        print(acc)
    return forest

# # test best para
# for i in range(1,15):
#     print(runAndTestKnn(train,test,n_neighbor=i))
# forest = runAndTestRF(train,test)