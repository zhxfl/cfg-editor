#coding: utf-8
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PaintWidget
import BaseShape
import json
import History
import Config
import Editor
import CfgInstance

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

        #菜单栏
        FileMemu = self.menuBar().addMenu(u"菜单")
        saveAction = QAction(u"保存", FileMemu)
        saveAction.triggered.connect(self.save)
        readAction = QAction(u"读取", FileMemu)
        readAction.triggered.connect(self.read)
        FileMemu.addAction(saveAction)
        FileMemu.addAction(readAction)

        #画布
        #TODO 画布大小自动调整
        self.m_PaintWidget.setMinimumSize(2000, 2000)
        Scroll = QScrollArea()
        Scroll.setWidget(self.m_PaintWidget)
        Scroll.setAutoFillBackground(True)
        Scroll.setWidgetResizable(True)
        grid.addWidget(Scroll, 0, 1)

        #layer的属性编辑
        editor = Editor.LayerConfigEditor()
        grid.addWidget(editor, 0, 0)
        self.setCentralWidget(mainQWidget)
        
        #向画板传递editor的句柄，方便回调编辑
        self.m_PaintWidget.m_editor = editor

        #设置布局器比例
        grid.setColumnStretch(0, 3)
        grid.setColumnStretch(1, 10)

        #添加工具栏,提供属性编辑
        editorTooBar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, editorTooBar)

        self.read()

    def save(self):
        """
            @保存配置表
        """
        fileDialog = QFileDialog(self)
        fileDialog.setWindowTitle(u'保存状态图')
        fileDialog.setDirectory('.')
        fileDialog.setFilter("Image Files(*.cfg)")
        path = ''
        if fileDialog.exec_() == QDialog.Accepted:
            path = fileDialog.selectedFiles()[0]
            QMessageBox.information(None, u"路径", u"保存目录为：" + path)
            sConfig = CfgInstance.g_sHead
            for (sName, shapeObj) in self.m_PaintWidget.m_dLayers.items():
                sConfig += "[Layer]\n";
                for(sKey, value) in shapeObj.m_dKeys.items():
                    if sKey == "outputs":
                        continue
                    sConfig += sKey + "="
                    if isinstance(value, list):
                        if len(value) >= 1:
                            sConfig += str(value[0])
                            nIdx = 1
                            while nIdx < len(value):
                                sConfig += "," + str(value[nIdx])
                                nIdx = nIdx + 1
                        sConfig += "\n";
                    else:
                        sConfig += str(value) + "\n"

                sConfig +="[end]\n\n";
            file = open(path, "w")
            file.write(sConfig)
            file.close()
        else:
            QMessageBox.information(None, u"路径", u"你没有选中任何文件")
        print u'保存状态图'

    #读取配置表，抽取配置表信息，建立树形结构
    def read(self):
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
            self.m_PaintWidget.transLayersToShape()
        else:
            QMessageBox.information(None, u"路径", u"你没有选中任何文件")
        print u'读取状态图'

if __name__ == "__main__" :
    q = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle(u"神经网络配置表编辑器")
    w.resize(1600, 800)
    w.show()
    q.exec_()
