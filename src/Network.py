import torch
from torch.nn import functional as F
from torch.nn import Module

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
        out = self.softmax(self.hiddenL(self.inputL(docVec)))
        return out


