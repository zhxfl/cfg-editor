#coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import BaseShape
import CfgInstance
import json

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
        self.m_notEditorCheckbox = QCheckBox(u"不需要编辑")
        self.m_weightCheckbox = QCheckBox(u"权重")
        self.m_inputCheckbox = QCheckBox(u"输入数据规格")
        self.m_allCheckbox = QCheckBox(u"全部")

        self.m_inputCheckbox.setChecked(True)
        self.m_weightCheckbox.setChecked(True)

        #grid.setSpacing()
        #设置布局器比例
        grid.setRowStretch(0, 3)
        grid.setRowStretch(1, 10)

        grid.addWidget(self.m_notEditorCheckbox, 0, 0)
        grid.addWidget(self.m_weightCheckbox, 0, 1)
        grid.addWidget(self.m_inputCheckbox, 0, 2)
        grid.addWidget(self.m_allCheckbox, 0, 3)

        self.setLayout(grid)

    def ShowLayerConfig(self, layer):
        #inputs
        #outputs
        table = QTableWidget();
        self.m_table = table
        self.m_layer = layer
        table.setColumnCount(2);
        table.setRowCount(len(layer.m_dKeys));
        
        grid = self.layout()
        grid.addWidget(table, 1, 0, 1, 4)
        keyItems = layer.m_dKeys.items()
        keyItems.sort()
        nIdx = 0
        for (sName, value) in keyItems:
            if self.checkKey(sName):
                table.setItem(nIdx, 0, QTableWidgetItem(sName))
                table.setItem(nIdx, 1, QTableWidgetItem(json.dumps(value)))
                #第一列不支持编辑
                table.item(nIdx, 0).setFlags(table.item(nIdx, 0).flags() & (~ Qt.ItemIsEditable))
                nIdx = nIdx +  1
        table.itemChanged.connect(self.itemChangeCallBack)

    def checkKey(self, sName):
        if self.m_allCheckbox.isChecked():
            return True
        else:
            if self.m_notEditorCheckbox.isChecked() == True:
                notEditorSet = set([ "inputs", "outputs", "name", "type"])
                if sName in notEditorSet:
                    return True
            if self.m_weightCheckbox.isChecked() == True:
                weightSet= set(["inputMaps","outputMaps", "filterWidth", "filterHeight", "paddingHeight", "paddingWidth", "strideWidth", "strideHeight"]) | \
                set(["winWidth", "winHeight", "strideHeight", "strideWidth", "paddingHeight", "paddingWidth"]) | set(["outDim"]) 
                if sName in weightSet:
                    return True
            if self.m_inputCheckbox.isChecked() == True:
                inputSet = set(["height", "width", "inDim", "inputMaps", "outputMaps"])
                if sName in inputSet:
                    return True
        return False 



    def itemChangeCallBack(self, item):
        sKey = str(self.m_table.item(item.row(),0).text())
        print item.column(), item.row(), sKey, str(item.text())
        #列表的解析TODO
        self.m_layer.m_dKeys[sKey] = json.loads(str(item.text()))
