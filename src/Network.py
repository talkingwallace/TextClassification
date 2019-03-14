import torch
from torch.nn import functional as F
from torch.nn import Module
import torch.nn.functional as F

class SimpleClasifier(Module):

    def __init__(self,dim,hiddenSize,classNum):
        """
        :param dim: 词向量维度
        :param hiddenSize: 隐藏层节点数
        :param classNum: 类个数
        """
        super(SimpleClasifier, self).__init__()
        self.inputL =  torch.nn.Linear(in_features=dim,out_features=hiddenSize)
        self.hiddenL = torch.nn.Linear(in_features=hiddenSize,out_features=classNum)
        self.softmax = F.softmax
        self.classNum = classNum


    def forward(self, docVec):
        x = F.relu(self.inputL(docVec))
        x = F.relu(self.hiddenL(x))
        out = self.softmax(x)
        return out

class DeeperClassifier(Module): # 加深可就完事啦

    def __init__(self,layerList,classNum):
        """
        :param dim: 词向量维度
        :param hiddenSize: 隐藏层节点数
        :param classNum: 类个数
        """
        super(DeeperClassifier, self).__init__()

        self.Layer = torch.nn.ModuleList()
        for i in range(0,len(layerList)):
            if i+1 == len(layerList):
                break
            self.Layer.append(torch.nn.Linear(in_features=layerList[i],out_features=layerList[i+1]))
        self.Layer.append(torch.nn.Linear(in_features=layerList[-1],out_features=layerList[classNum]))
        self.softmax = F.softmax
        self.classNum = classNum


    def forward(self, x):
        relu = F.relu
        for i in self.Layer:
            x = i(x)
            x = relu(x)
        return x


