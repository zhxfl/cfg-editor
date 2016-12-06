import copy
import Config


g_sImageConv = "image_conv"
g_sImagePool = "image_pool"
g_sSoftmax = "softmax"
g_sLossCe = "loss_ce"

_g_dImageConv = {
"type" : "image_conv",
"name" : "conv1",
"inputs" : [],
"convAlgoType" : "auto",
"convGradAlgoType" : "auto",
"convDiffAlgoType" : "auto",
"width": 32,
"height" : 32,
"inputMaps" : 3,
"outputMaps" : 96,
"filterHeight" : 3,
"filterWidth" : 3,
"strideHeight" : 1,
"strideWidth" : 1,
"paddingHeight" : 1,
"paddingWidth" : 1,
"hasBias" : True,
"learnRate" : 0.0000025,
"momentum" : 0.9,
"initMean" : 0,
"initStdv" : 0.1
}

_g_dImagePool = {
"type": "image_pool",
"name": "pool1_2",
"inputs": [],
"poolingType": "avgPooling",
"width": 6,
"height": 6,
"winHeight": 6,
"winWidth": 6,
"strideHeight": 6,
"strideWidth": 6,
"inputMaps ": 100
}

_g_dSoftmax = {
"type" : "softmax",
"name" : "softmax1",
"inputs" : [],
"inDim":20,
"outDim":20
}

_g_dLossCe = {
"type" : "loss_ce",
"name" : "loss2",
"inputs" : [],
"label" : "label-data1",
"cost-type" : "err",
"inDim" : 100,
"outDim" : 100
}

g_dLayerCfg= {
    g_sSoftmax : _g_dSoftmax,
    g_sImageConv : _g_dImageConv,
    g_sImagePool : _g_dImagePool,
    g_sLossCe :_g_dLossCe 
}

g_lLayerTypeList = [
    g_sSoftmax, g_sImageConv, g_sImagePool, g_sLossCe]

def getLayerCfg(layer_name):
    if g_dLayerCfg.has_key(layer_name) == True:
        dKeys = copy.deepcopy(g_dLayerCfg[layer_name])
        dKeys["outputs"] = []
        if layer_name == g_sSoftmax:
            layerObj = Config.SoftmaxLayer("")
            layerObj.m_dKeys = dKeys
            return layerObj
        elif layer_name == g_sLossCe:
            layerObj = Config.LossCeLayer("")
            layerObj.m_dKeys = dKeys
            return layerObj
        elif layer_name == g_sImageConv:
            layerObj = Config.ConvLayer("")
            layerObj.m_dKeys = dKeys
            return layerObj
        elif layer_name == g_sImagePool:
            layerObj = Config.PoolingLayer("")
            layerObj.m_dKeys = dKeys
            return layerObj
    else:
        assert False
