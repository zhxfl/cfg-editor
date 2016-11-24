#coding: utf-8
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PaintWidget
import BaseShape
import json
import History
import Config


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, windowTitle=u"状态机编辑器")
        self.m_PaintWidget = PaintWidget.PaintWidget()
        self.m_PaintWidget.Update()
        #菜单栏
        FileMemu = self.menuBar().addMenu(u"菜单")
        SaveAction = QAction(u"保存", FileMemu)
        SaveAction.triggered.connect(self.Save)
        ReadAction = QAction(u"读取", FileMemu)
        ReadAction.triggered.connect(self.Read)
        FileMemu.addAction(SaveAction)
        FileMemu.addAction(ReadAction)

        #工具栏
        EditorToolBar = QToolBar()

        #画线
        self.addToolBar(Qt.TopToolBarArea,EditorToolBar)
        self.m_DrawLineAction = QAction("Line", EditorToolBar)
        self.m_DrawLineAction.triggered.connect(self.DrawLineActionTriggered)
        self.m_DrawLineAction.setText(u'线')
        self.m_DrawLineAction.setCheckable(True)
        EditorToolBar.addAction(self.m_DrawLineAction)

        #画矩形
        self.m_DrawRectAction = QAction("Rect", EditorToolBar)
        self.m_DrawRectAction.triggered.connect(self.DrawRectActionTriggered)
        self.m_DrawRectAction.setText(u'矩形')
        self.m_DrawRectAction.setCheckable(True)
        EditorToolBar.addAction(self.m_DrawRectAction)

        #画布
        self.m_PaintWidget.setMinimumSize(2000, 2000)
        Scroll = QScrollArea()
        Scroll.setWidget(self.m_PaintWidget)
        Scroll.setAutoFillBackground(True)
        Scroll.setWidgetResizable(True)
        self.setCentralWidget(Scroll)

    def DrawLineActionTriggered(self):
        """
            @切换到画线模式
        """
        self.m_DrawRectAction.setChecked(False)
        self.m_DrawDiamondAction.setChecked(False)
        self.m_PaintWidget.SetCurrentShape(BaseShape.BaseShape.s_Line, self.m_DrawLineAction)

    def DrawRectActionTriggered(self):
        """
            @切换到画矩形模式
        """
        self.m_DrawLineAction.setChecked(False)
        self.m_DrawDiamondAction.setChecked(False)
        self.m_PaintWidget.SetCurrentShape(BaseShape.BaseShape.s_Rect, self.m_DrawRectAction)

    def Save(self):
        fileDialog = QFileDialog(self)
        fileDialog.setWindowTitle(u'保存状态图')
        fileDialog.setDirectory('.')
        fileDialog.setFilter("Image Files(*.json)")
        path = ''
        if fileDialog.exec_() == QDialog.Accepted:
            path = fileDialog.selectedFiles()[0]
            QMessageBox.information(None, u"路径", u"保存目录为：" + path)
            jsonFile = {}
            for shape in self.m_PaintWidget.m_lShape:
                jsonFile[shape.m_nId] = {}
                jsonFile[shape.m_nId] = shape.ToJson()
            jsonFile['s_curId'] = BaseShape.BaseShape.s_curId
            print json.dumps(jsonFile)
            with open(path, 'w') as outfile:
                json.dump(jsonFile, outfile)
        else:
            QMessageBox.information(None, u"路径", u"你没有选中任何文件")
        print u'保存状态图'

    def BuildNet(self):
        for CommentObj in self.m_PaintWidget.m_lShape:
            if CommentObj.isComment():
                for LineObj in self.m_PaintWidget.m_lShape:
                    if LineObj.isLine():
                        if LineObj.m_nCommentId == CommentObj.m_nId:
                            CommentObj.m_LineObj = LineObj
        print 'build net'

    #读取配置表，抽取配置表信息，建立树形结构
    def Read(self):
        fileDialog = QFileDialog(self)
        fileDialog.setWindowTitle(u'读取状态图')
        fileDialog.setDirectory('.')
        fileDialog.setFilter("Image Files(*.cfg)")
        if fileDialog.exec_() == QDialog.Accepted:
            sPath = fileDialog.selectedFiles()[0]
            QMessageBox.information(None, u"路径", u"读取目录为：" + sPath)
            #插入配置表解析模块
            cfgObj = Config.Config(sPath)
            cfgObj.Read()
            jsonFile = {}
            with open(sPath, 'r') as outfile:
                jsonFile = json.load(outfile)
                print jsonFile
                self.m_PaintWidget.m_lShape = []
                for (key,value) in  jsonFile.items():
                    if key == "s_curId":
                        continue
                    if value['m_bLine'][0] == True:
                        shape = BaseShape.Line()
                    elif value['m_bRect'][0] == True:
                        shape = BaseShape.Rect()

                    shape.InitFromJson(key, value)

                    if shape.m_color == True:
                        self.m_PaintWidget.m_chooseShape = shape
                    self.m_PaintWidget.m_lShape.append(shape)

                BaseShape.BaseShape.s_curId = jsonFile['s_curId']
                self.BuildNet()
                self.m_PaintWidget.m_lShape.sort(lambda x,y:cmp(x.m_bLine, y.m_bLine))
                self.m_PaintWidget.update()
                History.Push(self.m_PaintWidget.m_lShape)
        else:
            QMessageBox.information(None, u"路径", u"你没有选中任何文件")
        print u'读取状态图'

if __name__ == "__main__" :
    q = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle(u"状态机编辑器")
    w.resize(1600, 800)
    w.show()
    q.exec_()
