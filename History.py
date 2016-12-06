#coding: utf-8
import copy
g_lStack = []
_g_nIdx = -1

def push(dLayer):
    global _g_nIdx
    global g_lStack
    if len(g_lStack) > 1000:
        del g_lStack[0]

    g_lStack.append(copy.deepcopy(dLayer))
    _g_nIdx = len(g_lStack) - 1
    print 'push history', 'stack size', len(g_lStack)

def back(dLayer):
    """ 
        @ 后退
    """
    global _g_nIdx
    global g_lStack

    print "history back g_nIdx = ", _g_nIdx
    if _g_nIdx >= 0:
        lRet = copy.deepcopy(g_lStack[_g_nIdx])
        _g_nIdx = _g_nIdx - 1
        return lRet
    else:
        return dLayer

def forward(dLayer):
    """
        @ 前进
    """
    global _g_nIdx
    global g_lStack

    print "history forward g_nIdx", _g_nIdx
    if _g_nIdx + 1 < len(g_lStack):
        _g_nIdx = _g_nIdx + 1
        lRet = copy.deepcopy(g_lStack[_g_nIdx])
        return lRet
    else:
        return dLayer
