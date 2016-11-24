#coding: utf-8
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Geometry
class EllipseMoveAction(object):
    def __init__(self, StartQPointObj, EndQPointObj, CallBackFuntion):
        self.m_StartQPointObj = StartQPointObj
        self.m_EndQPointObj = EndQPointObj
        #算出单位向量
        self.m_UnitVectorObj = Geometry.GetUnitVector(EndQPointObj - StartQPointObj)
        self.m_CallBackFuntion = CallBackFuntion
        return

    def IsFinish(self):
        nLen = Geometry.GetDistance(self.m_StartQPointObj, self.m_EndQPointObj)
        if nLen < 5:
            self.m_CallBackFuntion()
            print 'is finish'
            return True
        else:
            return False

    def Move(self):
        if self.IsFinish() == True:
            return
        nStep = 30
        self.m_StartQPointObj += nStep * self.m_UnitVectorObj

    def paint(self,painter):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(0,255,0))
        painter.setPen(pen)
        painter.drawEllipse(self.m_StartQPointObj, 5, 5)
        return

class Animation(object):
    def __init__(self):
        self.m_lAction = []

    def Push(self, ActionObj):
        self.m_lAction.append(ActionObj)

    def Remove(self, ActionObj):
        nLen = len(self.m_lAction)
        for i in range(nLen):
            if self.m_lAction[i] == ActionObj:
                del self.m_lAction[i]
                return

    def Update(self, painter):
        for ActionObj in self.m_lAction:
            ActionObj.Move()
            ActionObj.paint(painter)
        lTmp = []
        for ActionObj in self.m_lAction:
            if ActionObj.IsFinish() == False:
                lTmp.append(ActionObj)
        self.m_lAction = lTmp
        #QTimer.singleShot(100, self.Update)






