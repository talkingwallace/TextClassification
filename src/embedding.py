from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec # 记录 callback 用
# # 分词
# df = dl.loadSmallSmplData()
# rs = sg.makeCorpus(df)
#
# with open('segSmpl.pkl', 'wb') as f:
#     pickle.dump(rs,f)
# #
# # 保存分词结果
# df['content'] = rs
# df.to_json('segSmpl.json')

from os import path
filePath = path.dirname(__file__)

class EpochLogger(CallbackAny2Vec):
     '''Callback to log information about training'''

     def __init__(self):
        self.epoch = 0

     def on_epoch_begin(self, model):
         print("Epoch #{} start".format(self.epoch))

     def on_epoch_end(self, model):
        print("Epoch #{} end".format(self.epoch))
        self.epoch += 1

def trainEmbedding(df,contentIndex = 'content',min_count = 1, iter = 30, window = 2, size = 50, workers = 8, savePath = 'embedding.model'): # 分词好的
    sentences = list(df[contentIndex])
    model = Word2Vec(sentences, min_count=min_count, iter=iter, window=window, size=size, workers=workers, )
    model.save(filePath+'\\'+savePath)
    return model

def loadEmbedding(defaultName = 'embedding.model'):
    return Word2Vec.load(filePath+'\\'+defaultName)