#coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import BaseShape
import CfgInstance

class RectEditor(QDialog):
    def __init__(self, ShapeObj, parent=None):
        self.m_ShapeObj = ShapeObj
        QWidget.__init__(self, parent)
        self.setWindowTitle(u'矩形状态编辑框')

        grid = QGridLayout()

        labelObj = QLabel(u'状态名')
        grid.addWidget(labelObj, 1, 1)

        self.m_Combo = QComboBox()
        for (key, value) in BaseShape.BaseShape.s_dState.items():
            self.m_Combo.addItem(value)
        self.m_Combo.setCurrentIndex(self.m_ShapeObj.GetStateId())
        grid.addWidget(self.m_Combo, 1, 2)
        self.setLayout(grid)

    def closeEvent(self, event):
        self.m_ShapeObj.SetStateId(self.m_Combo.currentIndex())
        print u'矩形状态编辑框关闭'

class CreateLayerEditor(QDialog):
    """
        @创建新的层
    """
    def __init__(self, func_callback, parent = None):
        QWidget.__init__(self, parent)
        self.setWindowTitle(u'创建新的层')

        grid = QGridLayout()

        self.m_comboObj = QComboBox()
        grid.addWidget(self.m_comboObj, 1, 1)
        self.m_funcCallBack = func_callback

        for sLayerName in CfgInstance.g_lLayerTypeList:
            self.m_comboObj.addItem(sLayerName)
        self.setLayout(grid)

    def closeEvent(self, event):
        nIdx = self.m_comboObj.currentIndex()
        print nIdx
        sName = CfgInstance.g_lLayerTypeList[nIdx]
        self.m_funcCallBack(sName)
        print u'创建新的层', sName

class LayerConfigEditor(QWidget):
    """
        @每个层对应的属性编辑框
    """
    def __init__(self):
        super(LayerConfigEditor, self).__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

    def ShowLayerConfig(self, layer):
        #inputs
        #outputs
        table = QTableWidget();
        table.setColumnCount(2);
        table.setRowCount(len(layer.m_dKeys));
        
        grid = self.layout()
        grid.addWidget(table, 0, 0)
        nIdx = 0
        for (sName, value) in layer.m_dKeys.items() :
            table.setItem(nIdx, 0, QTableWidgetItem(sName))
            table.setItem(nIdx, 1, QTableWidgetItem(str(value)))
            #第一列不支持编辑
            table.item(nIdx, 0).setFlags(table.item(nIdx, 0).flags() & (~ Qt.ItemIsEditable))
            nIdx = nIdx +  1
