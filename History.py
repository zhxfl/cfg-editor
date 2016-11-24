#coding: utf-8
import copy
g_lStack = []

def Push(lShape):
    g_lStack.append(copy.deepcopy(lShape))
    print 'push history', 'stack size', len(g_lStack)

def Pop(lShape):
    nLen = len(g_lStack)
    if nLen > 0:
        print 'pop history', 'stack size', len(g_lStack)
        lRet = g_lStack[nLen - 1]
        del g_lStack[nLen - 1]
        return lRet
    else:
        print 'pop history fail', 'stack size is empty'
        Push(lShape)
        return lShape
