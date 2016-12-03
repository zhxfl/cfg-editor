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
import Queue
import copy
import pdb

class PaintWidget(QWidget):
    """
        @ 画板
    """
    def __init__(self):
        QWidget.__init__(self)

        self.m_dShape = {} #图元列表
        self.m_dLayers = {} #网络配置的层字典
        self.m_sChooseShapeName = None #被选中的形状的名字，包括矩形和线条
        self.m_prePoint = QPoint() #拖动线段时的坐标
        self.m_curPoint = QPoint() #拖动线条时的坐标
        self.m_editor = None #属性编辑框

        self.setFocusPolicy(Qt.ClickFocus)

    def TransLayersToShape(self):
        """
            @ 将配置表神经网络信息转化成待渲染的图元
        """
        #寻找起点,Layer的inputs不是一个Layer，说明其输入是特征，那么该层就是起点
        setMark = set([])
        queObj = Queue.Queue()
        self.m_dShape = {}
        curPoint = QPoint(100, 20)
        for (sName, layer) in self.m_dLayers.items():
            if self.m_sChooseShapeName == None:
                self.m_sChooseShapeName = sName
            lInputs = layer.GetInputs()
            if len(lInputs) == 0:
                queObj.put(layer.GetName())
                setMark.add(layer.GetName())

                shapeObj = BaseShape.Rect()
                shapeObj.setStart(copy.deepcopy(curPoint))
                curPoint += QPoint(250, 0)
                shapeObj.m_sLayerName = layer.GetName()
                shapeObj.GetLabelMaxWidth(QPainter(self))
                print "begin", sName
                        
                self.m_dShape[sName] = shapeObj
            else:
                for sInputName in lInputs:
                    if not self.m_dLayers.has_key(sInputName) :
                        queObj.put(layer.GetName())
                        setMark.add(layer.GetName())

                        shapeObj = BaseShape.Rect()
                        shapeObj.setStart(copy.deepcopy(curPoint))
                        curPoint += QPoint(250, 0)
                        shapeObj.m_sLayerName = layer.GetName()
                        shapeObj.GetLabelMaxWidth(QPainter(self))

                        self.m_dShape[sName] = shapeObj
                        print "begin", sName
                        break
        
        #BFS遍历m_dLayers,根据层次信息生成坐标
        while not queObj.empty():
            sLayerName = queObj.get()
            lOutputs = self.m_dLayers[sLayerName].GetOutpus()
            curShape = self.m_dShape[sLayerName]
            curPoint = copy.copy(curShape.m_start)
            curPoint += QPoint(0, 40)
            for sOutputLayerName in lOutputs:
                print sLayerName, sOutputLayerName
                #统一计算，让其居中
                if sOutputLayerName not in setMark:
                    #画矩形
                    painter = QPainter(self)
                    shapeObj = BaseShape.Rect()
                    shapeObj.setStart(curPoint)
                    shapeObj.m_sLayerName = sOutputLayerName
                    self.m_dShape[sOutputLayerName] = shapeObj
                    curPoint = QPoint(shapeObj.GetLabelMaxWidth(painter) + 40 + curPoint.x(),
                            curPoint.y())
                    #画线条
                    lineObj = BaseShape.Line()
                    startPoint = self.m_dShape[sLayerName].getMid()
                    endPoint =  self.m_dShape[sOutputLayerName].getMid()
                    startPoint = self.GetRectVLineInterPoint(self.m_dShape[sLayerName], startPoint, endPoint)
                    endPoint = self.GetRectVLineInterPoint(self.m_dShape[sOutputLayerName], startPoint, endPoint)

                    lineObj.setStart(startPoint)
                    lineObj.setEnd(endPoint)
                    lineObj.m_left = sLayerName
                    lineObj.m_right = sOutputLayerName

                    self.m_dShape[sLayerName + sOutputLayerName] = lineObj

                    queObj.put(sOutputLayerName)
                    setMark.add(sOutputLayerName)
                else:
                    #画线条
                    lineObj = BaseShape.Line()
                    startPoint = self.m_dShape[sLayerName].getMid()
                    endPoint =  self.m_dShape[sOutputLayerName].getMid()
                    startPoint = self.GetRectVLineInterPoint(self.m_dShape[sLayerName], startPoint, endPoint)
                    endPoint = self.GetRectVLineInterPoint(self.m_dShape[sOutputLayerName], startPoint, endPoint)

                    lineObj.setStart(startPoint)
                    lineObj.setEnd(endPoint)
                    lineObj.m_left = sLayerName
                    lineObj.m_right = sOutputLayerName

                    self.m_dShape[sLayerName + sOutputLayerName] = lineObj
                    

    def paintEvent(self, event):
        """
            @每帧绘制回调
        """
        painter = QPainter(self)
        painter.setBrush(Qt.white)
        painter.drawRect(0, 0, self.width(), self.height())

        for (sName, shape) in self.m_dShape.items():
            if shape.isLine():
                shape.paint(painter)
        for (sName, shape) in self.m_dShape.items():
            if shape.isRect():
                shape.paint(painter)
        #if self.m_shape != None:
        #    self.m_shape.paint(painter)
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
        """
            @鼠标双击事件回调
            @坐标落在空白处，触发生成一个新的层的逻辑
            @坐标落在矩形内部，触发生成一个新的连接的逻辑
        """
        #走单击的逻辑 
        self.PressChooseShape(event)
        #触发新建连接的逻辑
        if self.m_sChooseShapeName != None and self.m_sChooseShapeName != "":
            shapeObj = self.m_dShape[self.m_sChooseShapeName]
            lineObj = BaseShape.Line()
            lineObj.setStart(event.pos())
            lineObj.setEnd(event.pos())
            lineObj.m_left = self.m_sChooseShapeName
            lineObj.m_curConner = 1
            sName = lineObj.m_left + lineObj.m_left
            self.m_dShape[sName] = lineObj
            self.m_sChooseShapeName = sName
        #触发新建层的逻辑
        else:
            print "not imp"

        #鼠标双击操作，弹出属性框编辑
        # if self.m_chooseShape != None:
        #     if self.m_chooseShape.isRect() == True:
        #         editor = Editor.RectEditor(self.m_chooseShape)
        #         editor.exec_()
        #         print 'Double click ',self.m_chooseShape.GetStateDescribe()
        #     elif self.m_chooseShape.isLine() == True:
        #         editor = Editor.LineEditor(self.m_chooseShape)
        #         editor.exec_()
        #         print 'Double click ',self.m_chooseShape.GetStateDescribe()

    def PressChooseShape(self, event):
        """
            @ 处理单击事件选中的操作
        """
        #取消被选中的颜色
        if self.m_sChooseShapeName != None:
            self.m_dShape[self.m_sChooseShapeName].setColor(False)
            self.m_sChooseShapeName = None
            self.update()

        #判断是否选中
        for (sName, shape) in self.m_dShape.items():
            if shape.isRect() == True:
                if self.inRect(event.pos(), shape):
                    print 'choose Rect', shape.m_nId
                    self.m_sChooseShapeName = sName
                    self.m_dShape[self.m_sChooseShapeName].setColor(True)
                    self.update()
                    self.m_editor.ShowLayerConfig(self.m_dLayers[self.m_sChooseShapeName])
                    return
            elif shape.isLine() == True:
                #求出点到直线的距离
                p1 = Geometry.PointToLineInterPoint(shape.m_start, shape.m_end, event.pos())
                p2 = event.pos()
                x1 = p1.x() - p2.x()
                y1 = p1.y() - p2.y()
                len = math.sqrt( 1.0 * x1 * x1 + y1 * y1)
                if len <= 3 and self.inRect(p1, shape):
                    self.m_bMoving = True
                    print 'choose Line', shape.m_nId
                    self.m_sChooseShapeName = sName
                    self.m_dShape[self.m_sChooseShapeName].setColor(True)
                    self.update()
                    return

    def mousePressEvent(self, event):
        """
            @ 鼠标单击事件
        """
        self.m_prePoint = event.pos()
        #判断是否选中了直线的一端，如果选中了，需要触发编辑功能
        if self.m_sChooseShapeName != None and self.m_sChooseShapeName != "":
            shapeObj = self.m_dShape[self.m_sChooseShapeName]
            if shapeObj.isLine() == True:
                if shapeObj.getCorner(event.pos()) != -1:
                    #启动编辑对m_dLayer的输入输出产生影响
                    self.RemoveLine( self.m_sChooseShapeName )
                    return

        self.PressChooseShape(event)
        return;

    def MoveReShape(self, event):
        if self.m_sChooseShapeName == "":
            return

        shapeObj = self.m_dShape[self.m_sChooseShapeName]
        if shapeObj.isLine() == True:
            if shapeObj.hasCorner() != -1:
                self.m_curPoint = event.pos()
                shapeObj.reShape(self.m_curPoint - self.m_prePoint);
                self.m_prePoint = self.m_curPoint

        self.update()

    def mouseMoveEvent(self, event):
        """
            @鼠标拖动事件回调
        """
        #拖动线条的一端
        if self.m_sChooseShapeName != None and self.m_sChooseShapeName != "":
            shapeObj = self.m_dShape[self.m_sChooseShapeName]
            if shapeObj.hasCorner() != -1:
                self.MoveReShape(event)
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

    def RemoveLine(self, sName):
        """
            @ 移除一个连接 
            @ 清理所有和这个连接有关的层的inputs和outputs
            @ 重新绘制图元
        """
        print "RemoveLine", sName
        if self.m_dShape.has_key(sName) == False:
            return

        shapeObj = self.m_dShape[sName]

        sLeftLayerName = shapeObj.m_left
        sRightLayerName = shapeObj.m_right

        if self.m_dLayers.has_key(sLeftLayerName):
            self.m_dLayers[sLeftLayerName].delOutput(sRightLayerName)
        if self.m_dLayers.has_key(sRightLayerName):
            self.m_dLayers[sRightLayerName].delInput(sLeftLayerName)

    def AddLine(self, sName):
        """
            @ 添加一个链接
            @ 删除对应的层的inputs和outputs
        """
        print "addLine", sName

        if self.m_dShape.has_key(sName) == False:
            return

        shapeObj = self.m_dShape[sName]

        sLeftLayerName = shapeObj.m_left
        sRightLayerName = shapeObj.m_right

        self.m_dLayers[sLeftLayerName].AppendOutput(sRightLayerName)
        self.m_dLayers[sRightLayerName].AppendInput(sLeftLayerName)
        print sLeftLayerName, "append outputs", sRightLayerName
        print sRightLayerName, "append inputs", sLeftLayerName
        

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

    def ReleaseReshape(self, event):
        """
            @重新編輯圖元結束
        """
        if self.m_sChooseShapeName != None and self.m_sChooseShapeName != "" and self.m_dShape[self.m_sChooseShapeName].isLine() == True:
            shapeObj = self.m_dShape[self.m_sChooseShapeName]
            self.m_curPoint = event.pos()
            shapeObj.reShape(self.m_curPoint - self.m_prePoint)
            self.m_prePoint = self.m_curPoint
            
            #检查线段是否合理,不合理就将其删除
            if self.checkLineLegal() == False:
                print "修改线段非法"
                del self.m_dShape[self.m_sChooseShapeName]
                self.m_sChooseShapeName = None
                self.TransLayersToShape()
            else:
                print "修改线段合法"
                self.AddLine(self.m_sChooseShapeName)
                shapeObj = self.m_dShape[self.m_sChooseShapeName]
                del self.m_dShape[self.m_sChooseShapeName]
                self.m_sChooseShapeName = None
                sName = shapeObj.m_left + shapeObj.m_right
                self.m_dShape[sName] = shapeObj
                self.TransLayersToShape()

        self.Update()

    def mouseReleaseEvent(self, event):
        """
            @ 释放鼠标回调函数
        """
        # 编辑线段
        if self.m_sChooseShapeName != None and self.m_sChooseShapeName != "":
            if self.m_dShape.has_key(self.m_sChooseShapeName) == False:
                print "without this key", self.m_sChooseShapeName
                assert False, self.m_sChooseShapeName
            if self.m_dShape[self.m_sChooseShapeName].isLine() and self.m_dShape[self.m_sChooseShapeName].m_curConner != -1:
                self.ReleaseReshape(event)
    
    # 线段的起点和终点必须在矩形的内部
    def checkLineLegal(self):
        if self.m_sChooseShapeName == None or self.m_sChooseShapeName == "":
            return False

        flag1 = ""
        flag2 = ""
        curLineObj = self.m_dShape[self.m_sChooseShapeName]
        if curLineObj.isLine() == False:
            return False

        for (sName, shapeObj) in self.m_dShape.items():
            if shapeObj.isRect() == True:
                if shapeObj.InRect(curLineObj.m_start):
                    flag1 = sName
                if shapeObj.InRect(curLineObj.m_end):
                    flag2 = sName
        #不能画环
        if flag1 == flag2:
            return False

        print "editor", flag1, flag2

        if flag1 != "" and flag2 != "":
            #重複的邊
            for (sName, shapeObj) in self.m_dShape.items():
                if self.m_sChooseShapeName == sName:
                    continue
                if shapeObj.isLine():
                    if shapeObj.m_left == flag1 and shapeObj.m_right == flag2:
                        return False

            #非環
            if flag1 != flag2:
                start = QPoint()
                if self.m_dShape[flag1].isRect():
                    start = self.GetRectVLineInterPoint(self.m_dShape[flag1], curLineObj.m_start, curLineObj.m_end)

                end = QPoint()
                if self.m_dShape[flag2].isRect():
                    end = self.GetRectVLineInterPoint(self.m_dShape[flag2], curLineObj.m_start, curLineObj.m_end)

                if start == None:
                    start = copy.deepcopy(curLineObj.m_start)
                if end == None:
                    end = copy.deepcopy(curLineObj.m_end)

                curLineObj.m_start = start
                curLineObj.m_end = end
                curLineObj.m_left = flag1
                curLineObj.m_right = flag2
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
