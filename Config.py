#coding: utf-8
import pdb
class BaseLayer(object):
    s_sName = 'name'
    def __init__(self, sContext):
        """
            @sContext 待解析的字符串
        """
        #public
        self.m_dKeys = {}
        lLine = sContext.split("\n")
        #建立字典
        for sLine in lLine:
            if sLine.find("=") != -1:
                sLine = sLine.replace(' ', '')
                sLine = sLine.replace('\n', '')
                sSplit = sLine.split('=')
                assert len(sSplit) == 2
                self.m_dKeys[sSplit[0]] = sSplit[1]
        print self.m_dKeys

    def GetName(self):
        return self.m_dKeys[BaseLayer.s_sName]

class ConvLayer(BaseLayer):
    #静态成员变量
    s_sType = 'type'
    s_sInputs = 'inputs'
    s_sConvAlgoType = 'convAlgoType'
    s_sConvDiffAlgoType = 'sConvDiffAlgoType'
    s_sWidth= 'width'
    s_sHeight = "height"
    s_sInputMaps = "inputMaps"
    s_sOutputMaps = "outputMaps"
    s_sFilterHeight = "filterHeight"
    s_sFilterWidth = "filterWidth"
    s_sStrideHeight = "strideHeight"
    s_sStrideWidth = "strideWidth"
    s_sPaddingHeight = "paddingHeight"
    s_sPaddingWidth = "paddingWidth"
    s_sHasBias = "hasBias"
    s_sLearnRate = "learnRate"
    s_sMomentum = "momentum"
    s_sInitMean = "initMean"
    s_sInitStdv = "initStdv"

class PoolingLayer(BaseLayer):
    #静态成员变量
    s_sType = "type"
    s_sInputs = "inputs"
    s_sPoolingTyp = "poolingType"
    s_sWidth = "width"
    s_sHeight = "height"
    s_sWinWidth = "winWidth"
    s_sWinHeight = "winHeight"
    s_sStrideHeight = "strideHeight"
    s_sStrideWidth = "strideWidth"
    s_sInputMaps = "inputMaps"

class SoftmaxLayer(BaseLayer):
    s_sType = "type"
    s_sInputs = "inputs"
    s_sInDim = "inDim"
    s_sOutDim = "outDim"

class LossCeLayer(BaseLayer):
    s_sType = "type"
    s_sInputs = "inputs"
    s_sLabel = "label"
    s_sCostType = "cost-type"
    s_sInDim = "inDim"
    s_sOutDim = "outDim"

class Config(object):
    def __init__(self, sPath):
        #private
        self._m_sPath = sPath
        self._m_lBlock = []
        self._m_sRemain = ""
        #public 
        self.m_dLayers = {}

#public
    def Read(self):
        """
            @读取配置表
            @将每层的信息分块，保存在_m_lBlock中
            @将剩余的信息保存在_m_sRemain中
        """
        fileObj = open(self._m_sPath)
        sContext = fileObj.read();
        sContext = self._RemoveSpace(sContext)
        #根据[layer][end]划分块，每块对齐参数进行解析
        nStartIdx = sContext.find("[Layer]")
        while nStartIdx != -1:
            nEndIdx = sContext.find("[end]")
            sBlock = sContext[nStartIdx : nEndIdx]
            sContext = sContext[0 : nStartIdx] + sContext[nEndIdx + 1: ] 
            nStartIdx = sContext.find("[Layer]")
            self._m_lBlock.append(sBlock)
        self._m_sRemain = sContext
        #解析配置表，建立树形图
        self._BuildLayerMap()

#private
    def _RemoveSpace(self, sContext):
        """
           @移除sContext的中多余的空格换行
           @不留空格
           @头不留换行
           @中间不会重复换行
        """
        sContext = sContext.replace(' ', '')
        lContext = sContext.split('\n')
        lRet = ""
        for sLine in lContext:
            if sLine.find("#") == -1:
                lRet = lRet + sLine + "\n"
        return lRet[0 : -1]


    def _BuildLayerMap(self):
        """
            @解析每个层，并且建立树形图
        """
        for sBlock in self._m_lBlock:
            if sBlock.find("image_conv") != -1:
                convLayerObj = ConvLayer(sBlock)
                sName = convLayerObj.GetName()
                self.m_dLayers[sName] = convLayerObj
            elif sBlock.find("image_pool") != -1:
                poolingLayerObj = PoolingLayer(sBlock)
                sName = poolingLayerObj.GetName()
                self.m_dLayers[sName] = poolingLayerObj
            elif sBlock.find("softmax") != -1:
                softmaxLayerObj = SoftmaxLayer(sBlock)
                sName = softmaxLayerObj.GetName()
                self.m_dLayers[sName] = softmaxLayerObj
            elif sBlock.find("loss_ce") != -1:
                lossCeLayerObj = LossCeLayer(sBlock)
                sName = lossCeLayerObj.GetName()
                self.m_dLayers[sName] = lossCeLayerObj
            else:
                print u"这个类型没有支持"
                assert false

        #建立每个layer的outputs便于后面BFS遍历
        for (sName, layerObj) in self.m_dLayers.items():
            lInputs = layerObj.GetInputs()
            for sInputName in lInputs:
                if self.m_dLayers.has_key(sInputName):
                    self.m_dLayers[sInputName].AppendOutput(sName)

        print self.m_dLayers

#if __name__ == "__main__":
#    cfgObj = Config("./image_train.cfg")
#    cfgObj.Read()

