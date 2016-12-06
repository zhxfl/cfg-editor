#coding: utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import math
import Geometry
import copy

class BaseShape(object):
    s_Line = 0
    s_Rect = 1
    s_Diamond = 2
    s_DottedLine = 3
    s_Comment = 4
    s_curId = 0

    def __init__(self):
        self.m_nId = self.s_curId
        BaseShape.s_curId += 1
        self.m_start = object
        self.m_end = object
        self.m_bLine = False
        self.m_bRect = False
        self.m_bDiamond = False
        self.m_bDottedLine = False
        self.m_bComment = False
        self.m_sLayerName = ""

        #是否被选中
        self.m_color = False
        self.m_left = -1
        self.m_right = -1
        self.m_stateId = 0

        self.m_dJson = {}

    def ToJson(self):
        self.m_dJson = {}
        self.m_dJson['m_start'] = [self.m_start.x(), self.m_start.y()]
        self.m_dJson['m_end'] = [self.m_end.x(), self.m_end.y()]
        self.m_dJson['m_bLine'] = [self.m_bLine]
        self.m_dJson['m_bRect'] = [self.m_bRect]
        self.m_dJson['m_bDiamond'] = [self.m_bDiamond]
        self.m_dJson['m_bDottedLine'] = [self.m_bDottedLine]
        self.m_dJson['m_bComment'] = [self.m_bComment]
        self.m_dJson['m_left'] = [self.m_left]
        self.m_dJson['m_right'] = [self.m_right]
        self.m_dJson['m_stateId'] = [self.m_stateId]
        self.m_dJson['m_color'] = [self.m_color]
        return self.m_dJson

    def InitFromJson(self, key, value):
        self.m_nId = int(key)
        self.m_start = QPoint(int(value['m_start'][0]), int(value['m_start'][1]))
        self.m_end = QPoint(int(value['m_end'][0]), int(value['m_end'][1]))
        self.m_bLine = value['m_bLine'][0]
        self.m_bDiamond = value['m_bDiamond'][0]
        self.m_bRect = value['m_bRect'][0]
        self.m_bDottedLine = value['m_bDottedLine'][0]
        self.m_bComment = value['m_bComment'][0]
        self.m_left = int(value['m_left'][0])
        self.m_right = int(value['m_right'][0])
        self.m_stateId = int(value['m_stateId'][0])
        self.m_color = value['m_color'][0]
        return

    def setStart(self, start):
        self.m_start = start

    def setEnd(self, end):
        self.m_end = end

    def SetStateId(self, nId):
        self.m_stateId = nId

    def GetStateId(self):
        return self.m_stateId

    def GetStateDescribe(self):
        if self.m_stateId != -1:
            return BaseShape.s_dState[self.m_stateId]
        else:
            return ''

    def setColor(self, flag):
        self.m_color = flag

    def isLine(self):
        return self.m_bLine

    def isRect(self):
        return self.m_bRect

    def isDiamond(self):
        return self.m_bDiamond

    def isComment(self):
        return self.m_bComment

    def isRing(self):
        if self.m_left != -1 and self.m_right != -1 and self.m_left == self.m_right:
            return True
        else:
            return False

    def isDottedLine(self):
        return self.m_bDottedLine

    def setPainter(self, painter):
        if self.m_color == True:
            pen = QPen()
            pen.setWidth(2)
            pen.setColor(QColor(255,0,0))
            painter.setPen(pen)
        else:
            pen = QPen()
            pen.setWidth(2)
            pen.setColor(QColor(0,0,0))
            painter.setPen(pen)

    def getMid(self):
        return QPoint((self.m_start.x() + self.m_end.x()) / 2,
                      (self.m_start.y() + self.m_end.y()) / 2)

class Line(BaseShape):
    def __init__(self):
        BaseShape.__init__(self)
        self.m_curConner = -1
        self.m_lCondition = []
        self.m_bLine = True
        self.m_nCommentId = -1

    def ToJson(self):
        BaseShape.ToJson(self)
        self.m_dJson['m_lCondition'] = self.m_lCondition
        self.m_dJson['m_nCommentId'] = [self.m_nCommentId]
        return self.m_dJson

    def InitFromJson(self, key, value):
        BaseShape.InitFromJson(self, key, value)
        self.m_lCondition = value['m_lCondition']
        self.m_nCommentId = int(value['m_nCommentId'][0])
        return

    def DrawCustomLine(self, painter, start, end):
        if start.x() == end.x() and start.y() == end.y():
            return
        VectorObj1 = Geometry.ClockWise(start - end, 100)
        VectorObj2 = Geometry.AntiClockWise(start - end, 100)
        if VectorObj1.x() == 0 and VectorObj1.y() == 0:
            return
        if VectorObj2.x() == 0 and VectorObj2.y() == 0:
            return
        #print 'vector_obj', VectorObj1, VectorObj2
        PointObj1 = Geometry.GetPointByVectorAndLegth(VectorObj1, 15)
        PointObj2 = Geometry.GetPointByVectorAndLegth(VectorObj2, 15)
        pathPaint = QPainterPath()
        pathPaint.moveTo(end)
        pathPaint.lineTo(PointObj1 + end)
        painter.drawPath(pathPaint)
        pathPaint.moveTo(end)
        pathPaint.lineTo(PointObj2 + end)
        painter.drawPath(pathPaint)
        #print PointObj1 + end, PointObj2 + end
        return

    def AfterAction(self):
        print 'after action'

    def paint(self, painter):
        self.setPainter(painter)
        self.m_bLine = True
        if self.isRing() == True:
            pathPaint = QPainterPath()
            startPoint = QPoint(self.m_start.x() + (self.m_end.x() - self.m_start.x()) / 4, self.m_start.y())
            end = QPoint(self.m_start.x() + (self.m_end.x() - self.m_start.x()) / 4 * 3, self.m_start.y())
            pathPaint.moveTo(startPoint)
            startPoint += QPoint(0.0, (self.m_start.y() - self.m_end.y()) / 2)
            pathPaint.lineTo(startPoint)
            startPoint += QPoint(end.x() - startPoint.x(), 0)
            pathPaint.lineTo(startPoint)
            pathPaint.lineTo(end)
            painter.drawPath(pathPaint)
            #painter.drawEllipse (end, 5, 5)

            #ellipse = QGraphicsEllipseItem(self.m_start.x(), self.m_start().y, 5, 5)
            #ellipse.paint(painter, QStyleOptionGraphicsItem(), None)
            #QPropertyAnimation
            self.DrawCustomLine(painter, startPoint, end)
        else:
            painter.drawLine(self.m_start, self.m_end)
            self.DrawCustomLine(painter, self.m_start, self.m_end)
            #painter.drawEllipse (self.m_end, 5, 5)

        if self.hasCorner() != -1:
            lPoint = []
            lPoint.append(self.m_start)
            lPoint.append(self.m_end)
            pen = QPen()
            pen.setWidth(2)
            pen.setColor(QColor(0,255,0))
            painter.setPen(pen)
            painter.drawEllipse (lPoint[self.m_curConner], 5, 5)
        #pathPaint.rotate(10)
        #painter.drawPath(pathPaint)

    def GetCondition(self):
        return self.m_lCondition

    def GetCondiction(self, nIndex):
        if len(self.m_lCondition) > nIndex:
            return self.m_lCondition[nIndex]
        else:
            return 0

    def SetCondition(self, lCondiction):
        self.m_lCondition = lCondiction

    def followRect(self, rect, p):
        if self.isRing() and self.m_left == rect.m_nId:
            self.m_start = copy.deepcopy(rect.m_start)
            self.m_end = copy.deepcopy(rect.m_end)
        p1 = QPoint()
        if rect.m_nId == self.m_left:
            p1 = self.m_start - rect.m_start
        elif rect.m_nId == self.m_right:
            p1 = self.m_end - rect.m_start
        else:
            return

        start = copy.deepcopy(rect.m_start)
        end = copy.deepcopy(rect.m_end)
        if rect.m_curConner == 0:
            start += p
        elif rect.m_curConner == 1:
            start += QPoint(p.x(), 0)
            end += QPoint(0, p.y())
        elif rect.m_curConner == 2:
            end += QPoint(p.x(), 0)
            start += QPoint(0, p.y())
        elif rect.m_curConner == 3:
            end += p

        p1 = QPoint(1.0 * p1.x() * math.fabs(end.x() - start.x()) / math.fabs(rect.m_end.x() - rect.m_start.x()) ,1.0 * p1.y() * math.fabs(end.y() - start.y()) / math.fabs(rect.m_end.y() - rect.m_start.y()))
        if rect.m_nId == self.m_left:
            self.m_start = p1 + start
        elif rect.m_nId == self.m_right:
            self.m_end = p1 + start

    def FollowDiamond(self, DiamondObj):
        #跟蹤離他最近的角點
        lMPoint = DiamondObj.GetConnerPoints()
        if DiamondObj.m_nId == self.m_left:
            nLen = len(lMPoint)
            for i in range(nLen):
                nDistance = Geometry.GetDistance(lMPoint[i], self.m_start)
                if nDistance < 10:
                    self.m_start = lMPoint[i]
                    break
        elif DiamondObj.m_nId == self.m_right:
            nLen = len(lMPoint)
            for i in range(nLen):
                nDistance = Geometry.GetDistance(lMPoint[i], self.m_end)
                if nDistance < 10:
                    self.m_end = lMPoint[i]
                    break
        else:
            return

    def getCorner(self, p):
        if self.isRing() == False:
            lPoint = []
            lPoint.append(self.m_start)
            lPoint.append(self.m_end)
            for i in range(len(lPoint)):
                if Geometry.getDistance(lPoint[i], p) <= 10:
                    self.m_curConner = i
                    return i
            self.m_curConner = -1
        else:
            lPoint = []
            startPoint = QPoint(self.m_start.x() + (self.m_end.x() - self.m_start.x()) / 4, self.m_start.y())
            end = QPoint(self.m_start.x() + (self.m_end.x() - self.m_start.x()) / 4 * 3, self.m_start.y())
            lPoint.append(startPoint)
            lPoint.append(end)
            for i in range(len(lPoint)):
                if Geometry.getDistance(lPoint[i], p) <= 10:
                    self.m_curConner = i
                    return i
            self.m_curConner = -1
        return -1

    def hasCorner(self):
        return self.m_curConner

    def reShape(self, p):
        if self.isRing():
            if self.m_curConner == 0:
                self.m_left = -1
            elif self.m_curConner == 1:
                self.m_right = -1
            t1 = QPoint(self.m_start.x() + (self.m_end.x() - self.m_start.x()) / 4, self.m_start.y())
            t2 = QPoint(self.m_start.x() + (self.m_end.x() - self.m_start.x()) / 4 * 3, self.m_start.y())
            self.m_start = t1
            self.m_end = t2
        if self.m_curConner == 0:
            self.m_start += p
        elif self.m_curConner == 1:
            self.m_end += p

    def move(self, p, flag):
        if self.m_left == flag:
            self.m_start += p
        if self.m_right == flag:
            self.m_end += p

class Rect(BaseShape):
    def __init__(self):
        BaseShape.__init__(self)
        self.m_curConner = -1
        self.m_bRect = True

    def GetLabelMaxWidth(self, painter):
        FontObj = QFontMetrics(painter.fontMetrics())
        nCurLen = FontObj.width(self.m_sLayerName)
        self.m_end = self.m_start + QPoint(nCurLen + 20, 20)
        return nCurLen

    def paint(self, painter):
        self.setPainter(painter)
        self.GetLabelMaxWidth(painter)

        painter.drawRoundRect(self.m_start.x(), self.m_start.y(),
                         self.m_end.x() - self.m_start.x(),
                         self.m_end.y() - self.m_start.y())
        painter.drawText(QRect(self.m_start, self.m_end), Qt.AlignCenter,
                self.m_sLayerName)

        if self.hasCorner() != -1:
            lPoint = []
            lPoint.append(self.m_start)
            lPoint.append(QPoint(self.m_start.x(), self.m_end.y()))
            lPoint.append(QPoint(self.m_end.x(), self.m_start.y()))
            lPoint.append(self.m_end)
            pen = QPen()
            pen.setWidth(2)
            pen.setColor(QColor(0,255,0))
            painter.setPen(pen)
            painter.drawEllipse(lPoint[self.m_curConner], 5, 5)

    def move(self, p):
        self.m_start += p
        self.m_end += p

    def getCorner(self, p):
        lPoint = []
        lPoint.append(self.m_start)
        lPoint.append(QPoint(self.m_start.x(), self.m_end.y()))
        lPoint.append(QPoint(self.m_end.x(), self.m_start.y()))
        lPoint.append(self.m_end)

        for i in range(len(lPoint)):
            if Geometry.getDistance(lPoint[i], p) <= 10:
                self.m_curConner = i
                return i
        self.m_curConner = -1
        return -1

    def hasCorner(self):
        return self.m_curConner

    def CanReshap(self, p):
        StartPointObj = copy.deepcopy(self.m_start)
        EndPointObj = copy.deepcopy(self.m_end)
        if self.m_curConner == 0:
            self.m_start += p
        elif self.m_curConner == 1:
            self.m_start += QPoint(p.x(), 0)
            self.m_end += QPoint(0, p.y())
        elif self.m_curConner == 2:
            self.m_end += QPoint(p.x(), 0)
            self.m_start += QPoint(0, p.y())
        elif self.m_curConner == 3:
            self.m_end += p
        OriXLen = math.fabs(StartPointObj.x() - EndPointObj.x())
        OriYLen = math.fabs(StartPointObj.y() - EndPointObj.y())

        NewXLen = math.fabs(self.m_start.x() - self.m_end.x())
        NewYLen = math.fabs(self.m_start.y() - self.m_end.y())
        #总是可以变大
        #出现不合法情况不可以变小
        if NewXLen < 25 or NewYLen < 25:
            if OriXLen > NewXLen or OriYLen > NewYLen:
                self.m_start = StartPointObj
                self.m_end = EndPointObj
                return False
        self.m_start = StartPointObj
        self.m_end = EndPointObj
        return True

    def reShape(self, p):
        if self.m_curConner == 0:
            self.m_start += p
        elif self.m_curConner == 1:
            self.m_start += QPoint(p.x(), 0)
            self.m_end += QPoint(0, p.y())
        elif self.m_curConner == 2:
            self.m_end += QPoint(p.x(), 0)
            self.m_start += QPoint(0, p.y())
        elif self.m_curConner == 3:
            self.m_end += p

    def InRect(self, point):
        x = point.x()
        y = point.y()
        flag1 = False
        flag2 = False
        grap = 5
        if  self.m_start.x() - grap <= x and x <= self.m_end.x() + grap:
            flag1 = True
        if  self.m_end.x() - grap <= x and x <= self.m_start.x() + grap:
            flag1 = True
        if  self.m_start.y() - grap <= y and y <= self.m_end.y() + grap:
            flag2 = True
        if  self.m_end.y() - grap <= y and y <= self.m_start.y() + grap:
            flag2 = True
        if flag1 == True and flag2 == True:
            return True
        else:
            return False

    def GetRectVLineInterPoint(self, p1, p2):
        a1 = QPoint(self.m_start.x(), self.m_end.y())
        a2 = QPoint(self.m_end.x(), self.m_start.y())
        a3 = self.m_start
        a4 = self.m_end

        if Geometry.IsSegmentIntersect(a3, a1, p1, p2):
            return Geometry.InterPoint(a3, a1, p1, p2)
        elif Geometry.IsSegmentIntersect(a3, a2, p1, p2):
            return Geometry.InterPoint(a3, a2, p1, p2)
        elif Geometry.IsSegmentIntersect(a4, a1, p1, p2):
            return Geometry.InterPoint(a4, a1, p1, p2)
        elif Geometry.IsSegmentIntersect(a4, a2, p1, p2):
            return Geometry.InterPoint(a4, a2, p1, p2)

class Diamond(BaseShape):
    def __init__(self):
        BaseShape.__init__(self)
        self.m_curConner = -1
        self.m_bDiamond = True

    def paint(self, painter):
        self.setPainter(painter)

        lPoint = []
        lPoint.append(self.m_start)
        lPoint.append(QPoint(self.m_start.x(), self.m_end.y()))
        lPoint.append(self.m_end)
        lPoint.append(QPoint(self.m_end.x(), self.m_start.y()))

        m1 = Geometry.GetMidPoint(lPoint[0], lPoint[1])
        m2 = Geometry.GetMidPoint(lPoint[1], lPoint[2])
        m3 = Geometry.GetMidPoint(lPoint[2], lPoint[3])
        m4 = Geometry.GetMidPoint(lPoint[3], lPoint[0])

        lMPoint = [m1, m2, m3, m4]
        path = QPainterPath()
        path.moveTo(m1)
        path.lineTo(m2)
        path.lineTo(m3)
        path.lineTo(m4)
        path.lineTo(m1)
        painter.drawPath(path)

        if self.hasCorner() != -1:
            pen = QPen()
            pen.setWidth(2)
            pen.setColor(QColor(0,255,0))
            painter.setPen(pen)
            painter.drawEllipse (lMPoint[self.m_curConner], 5, 5)

    def move(self, p):
        self.m_start += p
        self.m_end += p

    def GetConnerPoints(self):
        lPoint = []
        lPoint.append(self.m_start)
        lPoint.append(QPoint(self.m_start.x(), self.m_end.y()))
        lPoint.append(self.m_end)
        lPoint.append(QPoint(self.m_end.x(), self.m_start.y()))

        m1 = Geometry.GetMidPoint(lPoint[0], lPoint[1])
        m2 = Geometry.GetMidPoint(lPoint[1], lPoint[2])
        m3 = Geometry.GetMidPoint(lPoint[2], lPoint[3])
        m4 = Geometry.GetMidPoint(lPoint[3], lPoint[0])
        lMPoint = [m1, m2, m3, m4]
        return lMPoint

    def getCorner(self, p):
        lMPoint = self.GetConnerPoints()
        self.m_curConner = -1

        for i in range(len(lMPoint)):
            if Geometry.getDistance(lMPoint[i], p) <= 10:
                self.m_curConner = i
                print 'touch diamond conner',i
                return i
        self.m_curConner = -1
        return -1

    def hasCorner(self):
        return self.m_curConner

    def reShape(self, p):
        if self.m_curConner == 0:
            self.m_start += QPoint(p.x(), 0)
        elif self.m_curConner == 1:
            self.m_end += QPoint(0, p.y())
        elif self.m_curConner == 2:
            self.m_end += QPoint(p.x(), 0)
        elif self.m_curConner == 3:
            self.m_start += QPoint(0, p.y())

    def CanReshap(self, p):
        StartPointObj = copy.deepcopy(self.m_start)
        EndPointObj = copy.deepcopy(self.m_end)
        self.reShape(p)
        OriXLen = math.fabs(StartPointObj.x() - EndPointObj.x())
        OriYLen = math.fabs(StartPointObj.y() - EndPointObj.y())
        NewXLen = math.fabs(self.m_start.x() - self.m_end.x())
        NewYLen = math.fabs(self.m_start.y() - self.m_end.y())
        #总是可以变大
        #出现不合法情况不可以变小
        if NewXLen < 25 or NewYLen < 25:
            if OriXLen > NewXLen or OriYLen > NewYLen:
                self.m_start = StartPointObj
                self.m_end = EndPointObj
                print 'diamond can not reshap'
                return False
        self.m_start = StartPointObj
        self.m_end = EndPointObj
        return True

    def InDiamond(self, point):
        x = point.x()
        y = point.y()
        flag1 = False
        flag2 = False
        grap = 5
        if  self.m_start.x() - grap <= x and x <= self.m_end.x() + grap:
            flag1 = True
        if  self.m_end.x() - grap <= x and x <= self.m_start.x() + grap:
            flag1 = True
        if  self.m_start.y() - grap <= y and y <= self.m_end.y() + grap:
            flag2 = True
        if  self.m_end.y() - grap <= y and y <= self.m_start.y() + grap:
            flag2 = True
        if flag1 == True and flag2 == True:
            return True
        else:
            return False

    def GetInterPoint(self, PointObj):
        lMPoint = self.GetConnerPoints()
        nMinLen = 10000000
        nRet = QPoint()
        for MPointObj in lMPoint:
            nLen = Geometry.GetDistance(MPointObj, PointObj)
            if nMinLen > nLen:
                nMinLen = nLen
                nRet = copy.deepcopy(MPointObj)
        return nRet

class DottedLine(BaseShape):
    def __init__(self):
        BaseShape.__init__(self);
        self.m_bDottedLine = True

    def paint(self, painter):
        self.setPainter(painter)
        PenObj = QPen()
        PenObj.setBrush(QBrush(Qt.blue))
        PenObj.setDashPattern([4,2,4,2])
        painter.setPen(PenObj)
        painter.drawLine(self.m_start, self.m_end)

    def Update(self, ShapeObj1, ShapeObj2):
        if ShapeObj1 == None or ShapeObj2 == None:
            return
        if ShapeObj2.isLine():
            tmp = ShapeObj1
            ShapeObj1 = ShapeObj2
            ShapeObj2 = tmp

        if ShapeObj1.isRing() == False:
            self.m_start = Geometry.GetMidPoint(ShapeObj1.m_start, ShapeObj1.m_end)
        else:
            pathPaint = QPainterPath()
            startPoint = QPoint(ShapeObj1.m_start.x() + (ShapeObj1.m_end.x() - ShapeObj1.m_start.x()) / 4, ShapeObj1.m_start.y())
            end = QPoint(ShapeObj1.m_start.x() + (ShapeObj1.m_end.x() - ShapeObj1.m_start.x()) / 4 * 3, ShapeObj1.m_start.y())
            startPoint += QPoint(0.0, (ShapeObj1.m_start.y() - ShapeObj1.m_end.y()) / 2)
            endPoint = startPoint + QPoint(end.x() - startPoint.x(), 0)
            self.m_start = Geometry.GetMidPoint(startPoint, endPoint)

        lMPoint = ShapeObj2.GetConnerPoints()
        nMinLen = 1000000
        nLen = len(lMPoint)
        for i in range(nLen):
            nDis = Geometry.GetDistance(lMPoint[i], self.m_start)
            if nDis < nMinLen:
                nMinLen = nDis
                self.m_end = lMPoint[i]
        return


class Comment(BaseShape):
    def __init__(self, StartPointObj, LineObj):
        BaseShape.__init__(self)
        self.m_curConner = -1
        self.m_bComment = True
        self.m_LineObj = LineObj
        self.m_start = StartPointObj
        self.m_nGrapSize = 5
        self.m_nTextSize = 20
        #算出需要的長寬
        self.m_nWidth = 200
        self.m_nHight = 100
        self.m_end = QPoint(self.m_start.x() + self.m_nWidth, self.m_start.y() + self.m_nHight)
        #計算虛線起始點
        self.m_DottedLine = DottedLine()
        #self.m_DottedLine.Update(self, LineObj)

    def GetLabelMaxWidth(self, painter):
        nLen = len(self.m_LineObj.m_lCondition)
        FontObj = QFontMetrics(painter.fontMetrics())
        nMax = 0
        for i in range(nLen):
            nCurLen = FontObj.width(BaseShape.s_dCondition[self.m_LineObj.m_lCondition[i]])
            if nCurLen > nMax:
                nMax = nCurLen
        return nMax

    def paint(self, painter):
        if self.m_LineObj == None:
            return

        self.setPainter(painter)
        PenObj = QPen()
        PenObj.setBrush(QBrush(Qt.blue))
        painter.setPen(PenObj)

        self.m_nWidth = self.GetLabelMaxWidth(painter) + self.m_nGrapSize * 3
        nGrapSize = self.m_nGrapSize
        nTextSize = self.m_nTextSize
        self.m_nHight = nGrapSize + nTextSize * len(self.m_LineObj.m_lCondition)
        self.m_end = QPoint(self.m_start.x() + self.m_nWidth, self.m_start.y() + self.m_nHight)
        self.m_DottedLine.Update(self, self.m_LineObj)

        lPoint = []
        lPoint.append(self.m_start)
        lPoint.append(QPoint(self.m_end.x() - nGrapSize, self.m_start.y()))
        lPoint.append(QPoint(self.m_end.x(), self.m_start.y() + nGrapSize))
        lPoint.append(QPoint(self.m_end.x() - nGrapSize, self.m_start.y() + nGrapSize))
        lPoint.append(QPoint(self.m_end.x() - nGrapSize, self.m_start.y()))
        lPoint.append(QPoint(self.m_end.x(), self.m_start.y() + nGrapSize))
        lPoint.append(self.m_end)
        lPoint.append(QPoint(self.m_start.x(), self.m_end.y()))
        lPoint.append(self.m_start)

        path = QPainterPath()
        path.moveTo(lPoint[0])
        nLen = len(lPoint)
        for i in range(nLen):
            path.lineTo(lPoint[(i + 1) % (nLen - 1)])
        painter.drawPath(path)

        nGrapSize = self.m_nGrapSize
        nTextSize = self.m_nTextSize
        #填寫文字
        nLen = len(self.m_LineObj.m_lCondition)
        for i in range(nLen):
            painter.drawText(QRect(self.m_start + QPoint(nGrapSize, nGrapSize + nTextSize * i), \
                                   self.m_start + QPoint(self.m_nWidth, nGrapSize + nTextSize * (i + 1)) ), \
                             Qt.AlignLeft, \
                             BaseShape.s_dCondition[self.m_LineObj.m_lCondition[i]])
        #畫虛線
        self.m_DottedLine.Update(self, self.m_LineObj)
        self.m_DottedLine.paint(painter)

    def move(self, p):
        self.m_start += p
        self.m_end += p

    def GetConnerPoints(self):
        lPoint = []
        lPoint.append(self.m_start)
        lPoint.append(QPoint(self.m_start.x(), self.m_end.y()))
        lPoint.append(self.m_end)
        lPoint.append(QPoint(self.m_end.x(), self.m_start.y()))

        m1 = Geometry.GetMidPoint(lPoint[0], lPoint[1])
        m2 = Geometry.GetMidPoint(lPoint[1], lPoint[2])
        m3 = Geometry.GetMidPoint(lPoint[2], lPoint[3])
        m4 = Geometry.GetMidPoint(lPoint[3], lPoint[0])
        lMPoint = [m1, m2, m3, m4]
        return lMPoint

    def getCorner(self, p):
        lPoint = []
        lPoint.append(self.m_start)
        lPoint.append(QPoint(self.m_start.x(), self.m_end.y()))
        lPoint.append(self.m_end)
        lPoint.append(QPoint(self.m_end.x(), self.m_start.y()))

        self.m_curConner = -1

        for i in range(len(lPoint)):
            if Geometry.getDistance(lPoint[i], p) <= 10:
                self.m_curConner = i
                print 'touch diamond conner',i
                return i
        self.m_curConner = -1
        return -1

    def hasCorner(self):
        return self.m_curConner

    def reShape(self, p):
        if self.m_curConner == 0:
            self.m_start += QPoint(p.x(), 0)
        elif self.m_curConner == 1:
            self.m_end += QPoint(0, p.y())
        elif self.m_curConner == 2:
            self.m_end += QPoint(p.x(), 0)
        elif self.m_curConner == 3:
            self.m_start += QPoint(0, p.y())

    def InComment(self, point):
        x = point.x()
        y = point.y()
        flag1 = False
        flag2 = False
        grap = 5
        if  self.m_start.x() - grap <= x and x <= self.m_end.x() + grap:
            flag1 = True
        if  self.m_end.x() - grap <= x and x <= self.m_start.x() + grap:
            flag1 = True
        if  self.m_start.y() - grap <= y and y <= self.m_end.y() + grap:
            flag2 = True
        if  self.m_end.y() - grap <= y and y <= self.m_start.y() + grap:
            flag2 = True
        if flag1 == True and flag2 == True:
            return True
        else:
            return False

    def GetInterPoint(self, PointObj):
        lMPoint = self.GetConnerPoints()
        nMinLen = 10000000
        nRet = QPoint()
        for MPointObj in lMPoint:
            nLen = Geometry.GetDistance(MPointObj, PointObj)
            if nMinLen > nLen:
                nMinLen = nLen
                nRet = copy.deepcopy(MPointObj)
        return nRet
