# TextClassification
亚文化文本分类,采集网络上的亚文化群体的评论、言论进行学习分类
目前采集了: 狗粉丝，蛤丝，淫梦厨，

# 须知
## 小数据集
下载下来后 在根目录创建一个 resources 文件 把下载的 weibo分词压缩包解压到里面:
https://drive.google.com/open?id=1IUiukBpiv43nTFxCRa2ovJ5ence0G-VL

这里有一个现成训练好的embedding model 放到src里面:
https://drive.google.com/open?id=1EAiWlBCVIa_5GMHZJJ37N8vIIg0wPv13

## 3.15 更新
所有数据集及模型已通过git-lfs上传。git pull后即可食用。

# 表现
## 小数据集
2019.3.13 word2vec + MLP(50->25->3) 86.3%
