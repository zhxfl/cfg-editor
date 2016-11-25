#coding: utf-8
from PyQt4.QtGui import *
import BaseShape

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

class LineEditor(QDialog):
    def __init__(self, ShapeObj, parent = None):
        self.m_ShapeObj = ShapeObj
        QWidget.__init__(self, parent)
        self.setWindowTitle(u'线段编辑框')
        self.m_lCombo = []
        lLabels = []
        for i in range(len(self.m_ShapeObj.m_lCondition) + 2):
            lLabels.append(u'条件' + str(i))

        grid = QGridLayout()
        for i in range(len(lLabels)):
            labelObj = QLabel(lLabels[i])
            grid.addWidget(labelObj, i + 1, 1)
            comboObj = QComboBox()
            for (key, value) in BaseShape.BaseShape.s_dCondition.items():
                comboObj.addItem(value)
                comboObj.setCurrentIndex(self.m_ShapeObj.GetCondiction(i))
                grid.addWidget(comboObj, i + 1, 2)
            self.m_lCombo.append(comboObj)
        self.setLayout(grid)

    def closeEvent(self, event):
        lCondition = []
        for ComboObj in self.m_lCombo:
            nIndex = ComboObj.currentIndex()
            if nIndex != 0:
                lCondition.append(nIndex)
        self.m_ShapeObj.SetCondition(lCondition)
        print 'update condictions',lCondition,self.m_ShapeObj.m_lCondition
        print u'线段状态编辑框关闭'


class LayerEditor(QDialog):
    def __init__(self, layerObj, parent = None):
        self.m_layerObj = layerObj
        QWidget.__init__(self, parent)
        self.setWindowTitle(u'线段编辑框')
        self.m_lCombo = []
        lLabels = []
        for i in range(len(self.m_ShapeObj.m_lCondition) + 2):
            lLabels.append(u'条件' + str(i))

        grid = QGridLayout()
        for i in range(len(lLabels)):
            labelObj = QLabel(lLabels[i])
            grid.addWidget(labelObj, i + 1, 1)
            comboObj = QComboBox()
            for (key, value) in BaseShape.BaseShape.s_dCondition.items():
                comboObj.addItem(value)
                comboObj.setCurrentIndex(self.m_ShapeObj.GetCondiction(i))
                grid.addWidget(comboObj, i + 1, 2)
            self.m_lCombo.append(comboObj)
        self.setLayout(grid)

    def closeEvent(self, event):
        lCondition = []
        for ComboObj in self.m_lCombo:
            nIndex = ComboObj.currentIndex()
            if nIndex != 0:
                lCondition.append(nIndex)
        self.m_ShapeObj.SetCondition(lCondition)
        print 'update condictions',lCondition,self.m_ShapeObj.m_lCondition
        print u'线段状态编辑框关闭'
