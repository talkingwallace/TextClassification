# 对数据进行初步的处理

import pandas as pd
import re
from Dataset.segmentation import getSegFunc
from src.feizhuliuTransfer import  toMarsWords

from os import path
filePath = path.dirname(__file__) # 脚本地址
RawDataPath = filePath+r'/RawData/'
FilterDataPath = filePath+r'/FilteredData/'

class Filter():

    """
    Filter 类对数据进行处理 对传入的数据进行过滤 并打上标签 返回一个dataframe
    filterList 是一个过滤器的函数list，会按顺序调用list中的过滤器，过滤器可以返回字符串或者boolean值，
    过滤过的字符串会传给下一个过滤器；如果返回true，那当前的样本就会整个被放弃 ，返回false则会继续讲当前字符串
    传给下一个过滤器

    self.minLen: 经过过滤器后 少于多少长度会被过滤掉
    self.maxLen: 大于多少长度会被滤掉
    """

    def __init__(self,df,filterList,labelName,minLen = 1,maxLen = 114514):
        """
        df 是一个dataframe
        :param df:
        :param filterList:
        """
        self.df = df
        self.df = self.df.dropna() # 去除空值
        if 'content' in list(df.columns):
            self.contentLabel = 'content'
        else:
            self.contentLabel = 'comment_cont'
        self.filterList = filterList
        self.labelName = labelName
        self.minLen = minLen
        self.maxLen = maxLen

    def runFilter(self):
        contents = list(self.df[self.contentLabel])
        rs = []
        for txt in contents:

            abandon = False

            for filter in self.filterList:
                tmp = filter(txt)
                if tmp == False:
                    abandon = True
                    break
                elif tmp == True:
                    continue
                else:
                    txt = tmp

            if abandon == False and len(txt)>=self.minLen and len(txt)<=self.maxLen:
                rs.append(txt)

        df = pd.DataFrame()
        df['content'] = rs
        df['label'] = [self.labelName] * len(rs)

        return df

def tiebaReplyFilter(target): #过滤贴吧 格式（回复 xxxxx :）还有换行符
    target = re.sub('.*：', "", re.sub(r'.*:', "", target))
    target = target.replace('\n','')
    return target

def weiboReplyFilter(target): #过滤微博的回复 格式 (ID: 回复 @xxxx :)
    s = re.sub('.*:',"",re.sub(r'回复@.*:',"",target)) #可能存在中英两种 ':' '：'
    s = re.sub('.*：', "", re.sub(r'回复@.*：', "", s))
    return re.sub('@.* ',"",s)

def linkDetector(target): #检测是否有网页连接 如果有链接则这个样本就不保存 返回False
    if len(re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',target))>0:
        return False
    else:
        return True

def AtFilter(target):
    if '@' in target:
        return False
    return True


def getAkeywordFilter(keywords, any=False):  # 关键词检测
    """
    :param keywords: 关键词清单
    :param any: any = True, 则含有一个关键词就会被保留; any = False 必须含有所有关键词
    :return: True or False
    """

    def filter(target):
        keys = keywords
        Any = any
        for i in keys:
            if i in target:
                if Any == True:
                    return True
            elif Any == False:
                return False

        if Any == True:
            return False

        return True

    return filter

def loadKeyWords(path,cut=False):
    """
    加载过滤用的关键词
    :param path: 地址
    :return: list
    """
    f = open(path,'r')
    txt = f.read()
    txt = re.sub(u'[,.!，。？?]',"",txt)
    if cut == True:
        seg = getSegFunc()
        return seg.cut(txt)
    return txt.split(' ')

def processAclass(df,filters,labelName,keywords=[],any=True,minLen=2,maxLen=100,):
    """
    :param df: dataframe
    :param filters: 自己定义的过滤器
    :param keywords: 过滤的关键词，如没有给一个[]
    :param any: 是否要含有所有关键词才被保留，如果any=True 有一个关键词就能被保留
    :param minLen: 样本最小长度
    :param maxLen: 样本最大长度
    :param labelName: 标签名
    :return: dataframe
    """

    if len(keywords)>0:
        filters.append(getAkeywordFilter(keywords,any))
    processor = Filter(df, filters, labelName,minLen=minLen, maxLen=maxLen)
    return processor.runFilter()

# 常用过滤器
defaultFilters = [linkDetector,AtFilter,tiebaReplyFilter,]

# # 淋语
# def NoXiXi(target): # 不要嘻嘻哦解解
#     if '嘻' in target:
#         return False
#     elif '[' in target and ']' in target:
#         return False
#     else:
#         return True
# df_ly1 = pd.read_csv(RawDataPath+'linyu.csv')
# df_ly2 = pd.read_csv(RawDataPath+'sanmumu2.csv').drop(columns=['time'])
# df_ly = pd.concat([df_ly1,df_ly2])
# df = processAclass(df_ly,[NoXiXi,linkDetector,AtFilter,tiebaReplyFilter,],'ly',minLen=4)
# df.to_csv(FilterDataPath+'linyu.csv',index=False)

# # 广东话 ok
#df_gdh = pd.read_csv(RawDataPath+'guangdonghua.csv')
# gdkey = getAkeywordFilter(['未','宜','咩','噶','D','唔','嘅','係','系','啲',
#                            '哋','捞','佬','野','嘢','咁','冇','讲','咯','d','边','睇','嚟','屌','冚'],any=True)
#
# GDHFilter = Filter(df_gdh,[linkDetector,AtFilter,tiebaReplyFilter,gdkey],'gdh',minLen=2,maxLen=100)
#
# df = GDHFilter.runFilter()
# df.to_csv(FilterDataPath+'gdh.csv',index=False)

# 六学
# df_lx1 = pd.read_csv(RawDataPath+'liuxue.csv').drop(columns=['time'])
# df_lx2 = pd.read_csv(RawDataPath+'liuxuejia.csv').drop(columns=['time'])
# df_lx = pd.concat([df_lx1,df_lx2])
# kws = loadKeyWords(RawDataPath+r'六学关键词.txt')
# df = processAclass(df_lx,defaultFilters,labelName='liuxue',keywords=kws)
# df.to_csv(FilterDataPath+'liuxue.csv',index=False)df

# 哲♂学
# kws = ['♂','dark','DARK','党','奥义','fantasy','van','VAN','平家','boy'
#        ,'Fa','billiy','比利','熏肉','告诫','shit','茂美','全给党','本格','香蕉','暮','魔男','fa','FA','金阁','银阁','铁阁','see']
# df_zx = pd.read_csv(RawDataPath+'xionggui.csv')
# df = processAclass(df_zx,defaultFilters,labelName='zhexue',keywords=kws)
# df.to_csv(FilterDataPath+r'zhexue.csv')

# 银梦
# def NoManSymbol(target): # no ♂
#     if '♂' in target:
#         return False
#     return True
#
# def ymfilter(target): # 淫梦厨专用
#     rs = re.search('([^,.a-zA-Z]\s){2,100}.', target) # 找 出 打 字 带 空 格 的
#     if rs!= None:
#         target = target.replace(rs.group(),rs.group().replace(' ','_____'))
#     return target
#
# def jingxueFilter(target): # 过滤掉京学相关
#     for i in ['爱慕','拆尼斯','拆你死','拆腻子','某些人自卑','十几个雇佣兵','人的片子','不能强','无罪','吴罪','鉴不鉴','贱不贱','我就怼']:
#         if i in target:
#             return False
#     return True
#
# df_ym1 = pd.read_csv(RawDataPath+'zxydym.csv')
# df_ym2 = pd.read_csv(RawDataPath+'zxyzym.csv')
# df_ym = pd.concat([df_ym1,df_ym2])
# defaultFilters.append(ymfilter)
# defaultFilters.append(jingxueFilter)
# df = processAclass(df_ym,defaultFilters,'ym',minLen=4,keywords=['通商','宽','萨','麦子','十里山路','仲夏夜之梦',
#                                                                 '我年轻时就读过','山路','换肩','宽衣'])

# other 正常人的评论(指以上群体都不是正常人)
# df_mx = pd.read_csv(RawDataPath+'mingxing.csv')
# df_cs = pd.read_csv(RawDataPath+'zhonghuachengshi.csv')
# df = pd.concat([df_cs,df_mx])
# df = processAclass(df,defaultFilters,'other',minLen=8,maxLen=100)
# df.to_csv(FilterDataPath+'other.csv')

#狼粉
# df_lf1 = pd.read_csv(RawDataPath+r'zhangdi.csv')
# df_lf2 = pd.read_csv(RawDataPath+r'zhenggongshe.csv').drop(columns='time')
# df_lf = pd.concat([df_lf1,df_lf2])
# df = processAclass(df_lf,defaultFilters,'mlryj',minLen=5,maxLen=20000)
# df.to_csv(FilterDataPath+'mlryj.csv')

#白学
# df_fzl = pd.read_csv(RawDataPath+'baixue.csv')
# df_2 = pd.read_csv(RawDataPath+'baisexiangbu2.csv')
# df = pd.concat([df_fzl,df_2])
# df = processAclass(df,defaultFilters,'baixue',keywords=['明明','这么熟练','腐朽的声音','碧池','小三','变成这样呢','两件','快乐事情','亲过多少次','也好','我先'],maxLen=50)

# 大秦话
# df1 = pd.read_csv(RawDataPath+'Mr_Quin.csv')
# df1.columns = ['content']
# df2 = pd.read_csv(RawDataPath+'mrquin.csv').drop(columns=['time'])
# df_quin = pd.concat([df1,df2])
# df = processAclass(df_quin,defaultFilters,'quin',keywords=['秦','摸','狗头','黑暗','怕不是','rua','RUA',
#                                                       'CMN','cmn''zaima','勃','歇了','神秘','25','二五','21','22','暗剑','黑楼','缺','惊了','堇','翼'
#                                                            ,'白丝','唯一指定邮箱','梦里','nldg','NLDG','哪来的狗','香香鸡','鸡儿丢人','qnmd','guna','警犬','暗示','狗狗我',
#                                                            ])
# df.to_csv(FilterDataPath+'quin.csv',index=False)
#
# def noHWangandPeitu(target): # 滤掉黄网 评论配图
#     if 'php' in target or '.com' in target or '评论配图' in target:
#         return False
#     return True
# df_sxc = pd.read_csv(RawDataPath+r'sxc.csv')
# df = processAclass(df_sxc,[linkDetector,weiboReplyFilter,AtFilter,noHWangandPeitu],'goufensi',minLen=5)
# df.to_csv(FilterDataPath+'goufensi.csv',index=False)

# 蛤丝
# df_hs = pd.read_csv(RawDataPath+'Sharon.csv')
# kws = loadKeyWords(RawDataPath+'hasi.txt')
# df = processAclass(df_hs,[linkDetector,weiboReplyFilter,AtFilter],'hasi',keywords=kws)

# # 非主流 非主流是他妈手动转换的 我佛啦
# df1 = pd.read_csv(RawDataPath+'feizhuliu.csv')
# df = processAclass(df1,defaultFilters,'fzl',minLen=7)
# df.to_csv(FilterDataPath+'feizhuliu.csv',index=False)