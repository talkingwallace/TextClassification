import torch
# 得到训练测试集合



class Trainer(object):

    def __init__(self, model,optimizer,lostFunc,trainLoader,testLoader,para):
        self.model = model
        self.opt = optimizer
        self.crit = lostFunc
        self.dataLoader = trainLoader
        self.testLoader = testLoader
        self.epochs = para['num_epoch']
        self.useGPU = para['useGPU']
        self.para = para
        self.saveEveryEpochs = para['saveEveryEpochs']
        self.lossLogger = {}
        self.learningDecayRate = para['learningDecay'] # 学习衰减率
        self.willDecay = para['willDecay']
        self.decayWhen = para['decayWhen']
        self.epochsCount = 1


    # 训练一批
    def train_single_batch(self, inputData, labels, batchId):

        # 要转换 float的格式
        inputData = inputData.type(torch.float32)
        # label 要longtensor格式
        labels = labels.type(torch.LongTensor)

        if self.useGPU == True:
            inputData = inputData.cuda()
            labels = labels.cuda()

        self.opt.zero_grad()
        labels_pred = self.model(inputData)
        loss = self.crit(labels_pred, labels)
        loss.backward()
        self.opt.step()
        loss = loss.data.cpu().numpy()
        return loss

    # 训练一代
    def train_an_epoch(self, epoch_id):
        assert hasattr(self, 'model'), '没有网络传入'
        self.model.train()

        for ID,smpl in enumerate(self.dataLoader):

            if self.willDecay == True: #学习率衰减
                if self.epochsCount % self.decayWhen == 0:
                    self.opt.param_groups[0]['lr'] = self.opt.param_groups[0]['lr']*self.learningDecayRate

            loss = self.train_single_batch(smpl[0],smpl[1],ID)
            print('[Training Epoch {}] Batch {}, Loss {}'.format(epoch_id, ID, loss))
            self.lossLogger[ID] = loss



    def train(self):

        for i in range(0,self.epochs):
            self.train_an_epoch(i)
            self.epochsCount += 1
            # if (i+1)%self.saveEveryEpochs == 0:
            #     torch.save(self.model,'epoch_'+str(i)+'_model.pkl')
            #     print('model of epoch'+str(i)+' saved')
        print('训练完成!')

    # 测试网络
    def test(self):

        totalacc = 0
        count = 0
        for ID,testData in enumerate(self.testLoader):
            count += 1
            print('testing batch:'+str(ID))
            inputData = testData[0]
            labels = testData[1]

            # 要转换 float的格式
            inputData = inputData.type(torch.float32)
            # label 要longtensor格式
            labels = labels.type(torch.LongTensor)

            if self.useGPU == True:
                inputData = inputData.cuda()
                labels = labels.cuda()

            labels_pred = self.model(inputData.cuda())
            labels_pred = labels_pred.cpu()
            rsIdx = []
            for i in labels_pred:
                rsIdx.append(int(i.argmax().numpy()))

            rsIdx = torch.Tensor(rsIdx)
            rsIdx = rsIdx.type(torch.LongTensor)
            labels = labels.cpu()
            acc = rsIdx.eq(labels).float().mean()
            print('acc:',acc)
            totalacc = totalacc + acc.numpy()

        print('avg acc:')
        print(totalacc/count)

        return totalacc/count