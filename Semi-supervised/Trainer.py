# 在此训练

# 通过训练来不停的筛选新样本
class Trainer():

    def __init__(self,df):
        self.pos = df[df['label'] == 'pos'].reset_index()
        self.rest = df[df['label'] == 'rest'].reset_index()
        self.neg = df[df['label'] == 'neg'].reset_index()
        self.labelToIndex = {'neg':0,'pos':1,'rest':2}
        self.pos['label'] = [1]*len(self.pos)
        self.neg['label'] = [0]*len(self.neg)
        self.rest['label'] = [2]*len(self.rest)

    def trainOnPos(self,trainFunc):
        """
        传入一个训练函数 返回一个classfier
        :return:
        """
        pass

    def getNewSamples(self,classfier):
        pass