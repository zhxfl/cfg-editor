#coding: utf-8
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PaintWidget
import BaseShape
import json
import History
import Config
class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        title = QLabel('Tile')
        author = QLabel('Author')
        review = QLabel('Review')
        
        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)
        self.setLayout(grid)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, windowTitle=u"配置表编辑器")
        self.m_PaintWidget = PaintWidget.PaintWidget()

        #申请一个新的QWidget修改来添加grid布局器
        mainQWidget = QWidget()
        self.setCentralWidget(mainQWidget)
        #布局器
        grid = QGridLayout()
        grid.setSpacing(2)
        mainQWidget.setLayout(grid)

        #self.m_PaintWidget.Update()
        #菜单栏
        FileMemu = self.menuBar().addMenu(u"菜单")
        SaveAction = QAction(u"保存", FileMemu)
        SaveAction.triggered.connect(self.Save)
        ReadAction = QAction(u"读取", FileMemu)
        ReadAction.triggered.connect(self.Read)
        FileMemu.addAction(SaveAction)
        FileMemu.addAction(ReadAction)

        #画布
        #TODO 画布大小自动调整
        self.m_PaintWidget.setMinimumSize(2000, 2000)
        Scroll = QScrollArea()
        Scroll.setWidget(self.m_PaintWidget)
        Scroll.setAutoFillBackground(True)
        Scroll.setWidgetResizable(True)
        grid.addWidget(Scroll, 0, 1)
        
        example = Example()
        grid.addWidget(example, 0, 0)
        self.setCentralWidget(mainQWidget)

        #设置布局器比例
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 5)

        #添加工具栏,提供属性编辑
        editorTooBar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, editorTooBar)

        #TODO
        self.Read()

    def Save(self):
        """
            @保存配置表
        """
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
            self.m_PaintWidget.m_dLayers = cfgObj.m_dLayers
            self.m_PaintWidget.TransLayersToShape()
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
