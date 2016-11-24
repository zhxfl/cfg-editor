#coding: utf-8
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Geometry
import BaseShape
import math
import Editor
import copy
import History
import AnimationFactory

class PaintWidget(QWidget):
    """
        @画板
    """
    def __init__(self):
        QWidget.__init__(self)
        self.m_curShapeCode = -1 #记录当前是划线模式还是画矩形模式
        self.m_shape = None
        self.m_perm = True
        self.m_lShape = []
        self.m_curAction = None #画线或者画矩形回调句柄
        self.m_chooseShape = None: #被选中的图元ID
        self.m_prePoint = QPoint()
        self.m_curPoint = QPoint()
        self.setFocusPolicy(Qt.ClickFocus) #??
        self.m_bMoving = False
        self.m_AnimationObj = AnimationFactory.Animation()
        #ActionObj = AnimationFactory.EllipseMoveAction(QPoint(1,1), QPoint(1600, 800), self.AfterAction)
        #self.m_AnimationObj.Push(ActionObj)
        self.m_dTips = {}

    def SetCurrentShape(self, s, action):
        self.m_curAction = action
        if s != self.m_curShapeCode:
            self.m_curShapeCode = s

    def GetSpacePoint(self):
        nX = 0
        nY = 0
        for shape in self.m_lShape:
            if shape.m_start.x() > nX:
                nX = shape.m_start.x()
            if shape.m_end.x() > nX:
                nX = shape.m_end.x()
            if shape.m_start.y() > nY:
                nY = shape.m_start.y()
            if shape.m_end.y() > nY:
                nY = shape.m_start.y()
        print 'GetSpacePoint',QPoint(nX, nY)
        return QPoint(nX, nY)

    def AddComment(self):
        for shape in self.m_lShape:
            if shape.isLine():
                if len(shape.m_lCondition) > 0 and shape.m_nCommentId == -1:
                    #算出最合適的start點
                    CommentObj = BaseShape.Comment(self.GetSpacePoint(), shape)
                    self.m_lShape.append(CommentObj)
                    shape.m_nCommentId = CommentObj.m_nId
        #刪除非法的注釋
        while self.CheckErrorCommment() != -1:
            for i in range(len(self.m_lShape)):
                if self.m_lShape[i].isLine():
                    if len(self.m_lShape[i].m_lCondition) == 0 and self.m_lShape[i].m_nCommentId != -1:
                        self.RemoveComment(self.m_lShape[i].m_nCommentId)
                        break

    def RemoveComment(self, nId):
        for i in range(len(self.m_lShape)):
            if self.m_lShape[i].m_nId == nId:
                del self.m_lShape[i]
                return

        for shape in  self.m_lShape:
            if shape.isLine():
                if shape.m_nCommentId == nId:
                    shape.m_nCommentId = -1

    def CheckErrorCommment(self):
        for shape in self.m_lShape:
            if shape.isLine():
                if len(shape.m_lCondition) == 0 and shape.m_nCommentId != -1:
                    return shape.m_nCommentId
        return -1

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(Qt.white)
        painter.drawRect(0, 0, self.width(), self.height())
        self.AddComment()
        #self.m_AnimationObj.Update(painter)
        for shape in self.m_lShape:
            shape.paint(painter)
        if self.m_shape != None:
            self.m_shape.paint(painter)
        #AnimationFactory.AnimationSingleton().Update()

    def Update(self):
        """
            @每50ms更新一次
        """
        self.update()
        QTimer.singleShot(50, self.Update)

    def AfterAction(self):
        print 'after action'

    def mouseDoubleClickEvent(self, event):
        #鼠标双击操作，弹出属性框编辑
        if self.m_chooseShape != None:
            if self.m_chooseShape.isRect() == True:
                editor = Editor.RectEditor(self.m_chooseShape)
                editor.exec_()
                print 'Double click ',self.m_chooseShape.GetStateDescribe()
            elif self.m_chooseShape.isLine() == True:
                editor = Editor.LineEditor(self.m_chooseShape)
                editor.exec_()
                print 'Double click ',self.m_chooseShape.GetStateDescribe()

    def PressChooseShape(self, event):
        if self.m_chooseShape != None:
            self.m_chooseShape.setColor(False)
            self.m_chooseShape.m_curConner = - 1
            self.m_chooseShape = None
            self.update()
        for shape in self.m_lShape:
            if shape.isRect() == True:
                if self.inRect(event.pos(), shape):
                    self.m_bMoving = True
                    print 'choose Rect', shape.m_nId
                    self.m_chooseShape = shape
                    self.m_chooseShape.setColor(True)
                    self.update()
                    return
            elif shape.isLine() == True and shape.isRing() == False:
                #求出点到直线的距离
                p1 = Geometry.PointToLineInterPoint(shape.m_start, shape.m_end, event.pos())
                p2 = event.pos()
                x1 = p1.x() - p2.x()
                y1 = p1.y() - p2.y()
                len = math.sqrt( 1.0 * x1 * x1 + y1 * y1)
                if len <= 3 and self.inRect(p1, shape):
                    self.m_bMoving = True
                    print 'choose Line', shape.m_nId
                    self.m_chooseShape = shape
                    self.m_chooseShape.setColor(True)
                    self.update()
                    return
            elif shape.isLine() == True and shape.isRing() == True:
                print 'choose Ring', shape.m_nId
                startPoint = QPoint(shape.m_start.x() + (shape.m_end.x() - shape.m_start.x()) / 4, shape.m_start.y())
                startPoint += QPoint(0.0, (shape.m_start.y() - shape.m_end.y()) / 2)
                end = QPoint(shape.m_start.x() + (shape.m_end.x() - shape.m_start.x()) / 4 * 3, shape.m_start.y())
                tmp = BaseShape.Rect()
                tmp.m_start = startPoint
                tmp.m_end = end
                if self.inRect(event.pos(), tmp):
                    self.m_bMoving = True
                    self.m_chooseShape = shape
                    self.m_chooseShape.setColor(True)
                    self.update()
                    return
            elif shape.isDiamond() == True:
                if self.inRect(event.pos(), shape):
                    self.m_bMoving = True
                    print 'choose Diamond', shape.m_nId
                    self.m_chooseShape = shape
                    self.m_chooseShape.setColor(True)
                    self.update()
                    return
            elif shape.isComment() == True:
                if shape.InComment(event.pos()):
                    self.m_bMoving = True
                    print 'choose Comment', shape.m_nId
                    self.m_chooseShape = shape
                    self.m_chooseShape.setColor(True)
                    self.update()
                    return

    def mousePressEvent(self, event):
        print 'press'
        self.m_prePoint = event.pos()
        #已经有被选中的矩形或线条，判断是是否需要编辑
        if self.m_chooseShape != None:
            if self.m_chooseShape.getCorner(event.pos()) != -1:
                    return

        #没有画图任务，这里触发一个选中操作
        if self.m_curShapeCode == -1:
            self.PressChooseShape(event)
            print 'choose shape code',self.m_curShapeCode
            return

        #新建线条
        if self.m_curShapeCode == BaseShape.BaseShape.s_Line:
            self.m_shape = BaseShape.Line()
        #新建矩形
        elif self.m_curShapeCode == BaseShape.BaseShape.s_Rect:
            self.m_shape = BaseShape.Rect()

        self.m_perm = False
        self.m_shape.setStart(event.pos())
        self.m_shape.setEnd(event.pos())
        if self.m_chooseShape != None:
            self.m_chooseShape.setColor(False)
            self.m_chooseShape = None

    def MoveReShape(self, event):
        if self.m_chooseShape.isRect() == True:
            self.m_curPoint = event.pos()
            if self.m_chooseShape.CanReshap(self.m_curPoint - self.m_prePoint):
                #先对线进行移动
                for shape in self.m_lShape:
                    if shape.isLine() == True:
                        shape.followRect(self.m_chooseShape, self.m_curPoint - self.m_prePoint)
                #重新画矩形
                self.m_chooseShape.reShape(self.m_curPoint - self.m_prePoint)
            self.m_prePoint = self.m_curPoint

        elif self.m_chooseShape.isLine() == True:
            if self.m_chooseShape.hasCorner() != -1:
                self.m_curPoint = event.pos()
                self.m_chooseShape.reShape(self.m_curPoint - self.m_prePoint)
                self.m_prePoint = self.m_curPoint

        elif self.m_chooseShape.isDiamond() == True:
            if self.m_chooseShape.hasCorner() != -1:
                self.m_curPoint = event.pos()
                if self.m_chooseShape.CanReshap(self.m_curPoint - self.m_prePoint):
                    self.m_chooseShape.reShape(self.m_curPoint - self.m_prePoint)
                    self.m_prePoint = self.m_curPoint
                    for shape in self.m_lShape:
                        if shape.isLine() == True:
                            shape.FollowDiamond(self.m_chooseShape)
        self.update()

    def mouseMoveEvent(self, event):
        """
            @鼠标拖动事件回调
        """
        if self.m_chooseShape != None and self.m_chooseShape.hasCorner() != -1:
            self.MoveReShape(event)
            return

        #处理被选中的物体的拖动，这里线是不能被拖动的
        DeltaMoveObj = QPoint()
        if self.m_chooseShape != None and self.m_chooseShape.isRect() == True:
            if self.m_bMoving == True:
                self.m_bMoving = False
                self.m_chooseShape.setColor(False)
                History.Push(self.m_lShape)
                self.m_chooseShape.setColor(True)

            self.m_curPoint = event.pos()
            DeltaMoveObj = self.m_curPoint - self.m_prePoint
            self.m_chooseShape.move(DeltaMoveObj)
            #所有线段检查是否和这个矩形有关系，如果有，移动
            for shape in self.m_lShape:
                if shape.isLine() == True:
                    shape.move(DeltaMoveObj, self.m_chooseShape.m_nId)
            self.m_prePoint = self.m_curPoint
            self.update()
            return

        if self.m_shape and self.m_perm == False:
            self.m_shape.setEnd(event.pos())
            self.update()
            return

    def keyPressEvent(self, event):
        """
            @键盘回调函数
        """
        #删除矩形或者线条
        if event.key() == Qt.Key_Delete:
            if self.m_chooseShape !=None:
                self.m_chooseShape.setColor(False)
                print 'key delete'
                History.Push(self.m_lShape)
                if self.m_chooseShape.isRect() or self.m_chooseShape.isDiamond():
                    self.RemoveRect(self.m_chooseShape.m_nId)
                elif self.m_chooseShape.isLine():
                    self.RemoveLine(self.m_chooseShape.m_nId)
            self.m_chooseShape = None
            self.update()
        #ctrl + z 回退错误修改
        elif event.modifiers() == (Qt.ControlModifier) and event.key() == Qt.Key_Z:
            self.m_lShape = History.Pop(self.m_lShape)
            self.update()
            if self.m_chooseShape == True:
                self.m_chooseShape.setColor(False)
                self.m_chooseShape = None
                self.m_shape = None
                self.m_perm = True
            if self.m_curAction != None:
                self.m_curAction.setChecked(False)
            self.m_curAction = None
            self.m_curShapeCode = -1
        #ctrl + r 前进
        elif event.modifiers() == (Qt.ControlModifier) and event.key() == Qt.Key_R:
            assert False

    def RemoveLine(self, nId):
        nCommentId = 0
        for i in range(len(self.m_lShape)):
            if self.m_lShape[i].m_nId == nId:
                nCommentId = self.m_lShape[i].m_nCommentId
                del self.m_lShape[i]
                break
        for i in range(len(self.m_lShape)):
            if self.m_lShape[i].m_nId == nCommentId:
                del self.m_lShape[i]
                break

    def RemoveRect(self, nId):
        for i in range(len(self.m_lShape)):
            if self.m_lShape[i].m_nId == nId:
                del self.m_lShape[i]
                break
        self.RemoveErrorLine(nId)

    def RemoveErrorLine(self, nId):
        while True:
            flag = self.CheckErrorLine(nId);
            if flag == -1:
                break;
            else:
                self.RemoveLine(self.m_lShape[flag].m_nId)

    def CheckErrorLine(self, nId):
        for i in range(len(self.m_lShape)):
            if self.m_lShape[i].m_left == nId or self.m_lShape[i].m_right == nId:
                return i
        return -1

    #重新編輯圖元結束
    def ReleaseReshape(self, event):
        History.Push(self.m_lShape)
        if self.m_chooseShape.isRect() == True or self.m_chooseShape.isDiamond() == True:
            self.m_chooseShape.m_curConner = -1
        elif self.m_chooseShape.isLine() == True:
            self.m_curPoint = event.pos()
            self.m_chooseShape.reShape(self.m_curPoint - self.m_prePoint)
            self.m_prePoint = self.m_curPoint
            for i in range(len(self.m_lShape)):
                if self.m_lShape[i] == self.m_chooseShape:
                    del self.m_lShape[i]
                    break
            self.m_shape = self.m_chooseShape
            self.m_chooseShape.m_curConner = -1
            self.m_curShapeCode = BaseShape.BaseShape.s_Line
            self.ReleaseCreate(event)

    #創建新的圖元
    def ReleaseCreate(self, event):
        #如果是直线，需要判断前后是否落在两个方框内
        History.Push(self.m_lShape)
        if self.m_shape.isLine():
            if self.checkLineLegal() == True:
                self.m_lShape.append(self.m_shape)
        elif self.m_shape.isRect():
            x1 = self.m_shape.m_start.x() - self.m_shape.m_end.x()
            y1 = self.m_shape.m_start.x() - self.m_shape.m_end.y()
            if math.fabs(x1) > 10 and math.fabs(y1) > 10:
                self.m_lShape.append(self.m_shape)
        elif self.m_shape.isDiamond():
            x1 = self.m_shape.m_start.x() - self.m_shape.m_end.x()
            y1 = self.m_shape.m_start.x() - self.m_shape.m_end.y()
            if math.fabs(x1) > 10 and math.fabs(y1) > 10:
                self.m_lShape.append(self.m_shape)

        self.m_perm = True
        self.m_shape = None
        if self.m_curAction != None:
            self.m_curAction.setChecked(False)
        self.m_curAction = None
        self.m_curShapeCode = -1
        self.update()


    def mouseReleaseEvent(self, event):
        if self.m_chooseShape != None and self.m_chooseShape.hasCorner() != -1:
            self.ReleaseReshape(event)
            return

        if self.m_curShapeCode != -1:
            self.ReleaseCreate(event)
            return

    #线段的起点和终点必须在矩形的内部
    def checkLineLegal(self):
        flag1 = -1
        flag2 = -1
        for i in range(len(self.m_lShape)):
            if self.m_lShape[i].isLine():
                continue;
            if self.m_lShape[i].isRect():
                if self.m_lShape[i].InRect(self.m_shape.m_start):
                    flag1 = i
                if self.m_lShape[i].InRect(self.m_shape.m_end):
                    flag2 = i
            if self.m_lShape[i].isDiamond():
                if self.m_lShape[i].InDiamond(self.m_shape.m_start):
                    flag1 = i
                if self.m_lShape[i].InDiamond(self.m_shape.m_end):
                    flag2 = i

        if flag1 != -1 and flag2 != -1:
            #重複的邊
            for ShapeObj in self.m_lShape:
                    if ShapeObj.isLine():
                        if ShapeObj.m_left ==  self.m_lShape[flag1].m_nId and ShapeObj.m_right ==  self.m_lShape[flag2].m_nId:
                            return False
            #非環
            if flag1 != flag2:
                start = QPoint()
                if self.m_lShape[flag1].isRect():
                    start = self.GetRectVLineInterPoint(self.m_lShape[flag1], self.m_shape.m_start, self.m_shape.m_end)
                elif self.m_lShape[flag1].isDiamond():
                    start = self.m_lShape[flag1].GetInterPoint(self.m_shape.m_start)

                end = QPoint()
                if self.m_lShape[flag2].isRect():
                    end = self.GetRectVLineInterPoint(self.m_lShape[flag2], self.m_shape.m_start, self.m_shape.m_end)
                elif self.m_lShape[flag2].isDiamond():
                    end = self.m_lShape[flag2].GetInterPoint(self.m_shape.m_end)

                if start == None:
                    start = copy.deepcopy(self.m_shape.m_start)
                if end == None:
                    end = copy.deepcopy(self.m_shape.m_end)

                self.m_shape.m_start = start
                self.m_shape.m_end = end
                self.m_shape.m_left = self.m_lShape[flag1].m_nId
                self.m_shape.m_right = self.m_lShape[flag2].m_nId
                return True
            #環
            else:
                #菱形不能有環
                if self.m_lShape[flag1].isDiamond():
                    return False
                self.m_shape.m_start = copy.deepcopy(self.m_lShape[flag1].m_start)
                self.m_shape.m_end = copy.deepcopy(self.m_lShape[flag1].m_end)
                self.m_shape.m_left = copy.deepcopy(self.m_lShape[flag1].m_nId)
                self.m_shape.m_right = copy.deepcopy(self.m_lShape[flag1].m_nId)
                return True
        else:
            return False

    #判断一个点是否在矩形中
    def inRect(self, point, rect):
        x = point.x()
        y = point.y()
        flag1 = False
        flag2 = False
        if  rect.m_start.x() <= x and x <= rect.m_end.x():
            flag1 = True
        if  rect.m_end.x() <= x and x <= rect.m_start.x():
            flag1 = True
        if  rect.m_start.y() <= y and y <= rect.m_end.y():
            flag2 = True
        if  rect.m_end.y() <= y and y <= rect.m_start.y():
            flag2 = True
        if flag1 == True and flag2 == True:
            return True
        else:
            return False

    def GetRectVLineInterPoint(self, rect, p1, p2):
        a1 = QPoint(rect.m_start.x(), rect.m_end.y())
        a2 = QPoint(rect.m_end.x(), rect.m_start.y())
        a3 = rect.m_start
        a4 = rect.m_end

        if Geometry.IsSegmentIntersect(a3, a1, p1, p2):
            return Geometry.InterPoint(a3, a1, p1, p2)
        elif Geometry.IsSegmentIntersect(a3, a2, p1, p2):
            return Geometry.InterPoint(a3, a2, p1, p2)
        elif Geometry.IsSegmentIntersect(a4, a1, p1, p2):
            return Geometry.InterPoint(a4, a1, p1, p2)
        elif Geometry.IsSegmentIntersect(a4, a2, p1, p2):
            return Geometry.InterPoint(a4, a2, p1, p2)
