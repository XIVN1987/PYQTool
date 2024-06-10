#! python3
import sys

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsScene
from PyQt5.QtWidgets import QGraphicsObject, QGraphicsRectItem, QGraphicsSimpleTextItem


#QGraphicsObject extends QGraphicsItem with QObject's signal/slot and property mechanisms
class ColorRectItem(QGraphicsObject):
    def __init__(self, x, y, w, h, color, parent = None):
        super(ColorRectItem, self).__init__(parent)
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        
        super(ColorRectItem, self).setPos(self.x, self.y)
        
        self.setAcceptHoverEvents(True)
    
    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.w, self.h)
    
    def paint(self, painter, option, widget):
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawRect(QtCore.QRectF(0, 0, self.w, self.h))
    
    mousePress = pyqtSignal()
    hoverEnter = pyqtSignal()
    hoverLeave = pyqtSignal()
    
    def mousePressEvent(self, event):
        self.mousePress.emit()
        QGraphicsObject.mousePressEvent(self, event)
    
    def hoverEnterEvent(self, event):
        self.hoverEnter.emit()
        QGraphicsObject.hoverEnterEvent(self, event)
    
    def hoverLeaveEvent(self, event):
        self.hoverLeave.emit()
        QGraphicsObject.hoverLeaveEvent(self, event)


class ResColor(QWidget):
    Colors = [['棕', QtGui.QColor(156, 101,  49),    1,      10,    1],
              ['红', QtGui.QColor(255,   0,   0),    2,     100,    2],
              ['橙', QtGui.QColor(255, 101,   0),    3,    1000, None],
              ['黄', QtGui.QColor(255, 255,   0),    4,   10000, None],
              ['绿', QtGui.QColor(  0, 255,   0),    5,  100000,  0.5],
              ['蓝', QtGui.QColor(  0,   0, 255),    6, 1000000, None],
              ['紫', QtGui.QColor(206,   0, 206),    7,    None,  0.1],
              ['灰', QtGui.QColor(156, 154, 156),    8,    None, None],
              ['白', QtGui.QColor(255, 255, 255),    9,    None, None],
              ['黑', QtGui.QColor(  0,   0,   0),    0,       1, None],
              ['金', QtGui.QColor(255, 207,  49), None,     0.1,    5],
              ['银', QtGui.QColor(206, 207, 206), None,    0.01,   10]]
            
    def __init__(self, parent=None):
        super(ResColor, self).__init__(parent)
        
        uic.loadUi('ResColor.ui', self)
        
        self.graScene = QGraphicsScene()
        self.graView.setScene(self.graScene)
        
        self.graScene.setSceneRect(-150, -160, 300, 320)
        self.graView.centerOn(0, 0)
        
        self.makeRes()
        self.makeLblBar(self.resX - 40, self.resY+self.resH+10)
        self.makeBtnBar1(self.resX+ 10, self.resY+self.resH+10)
        self.makeBtnBar2(self.resX+ 45, self.resY+self.resH+10)
        self.makeBtnBar3(self.resX+ 80, self.resY+self.resH+10)
        self.makeBtnBar4(self.resX+115, self.resY+self.resH+10)
        self.makeBtnBar5(self.resX+165, self.resY+self.resH+10)
        
        self.ResValue = 0   #色环电阻阻值
        self.ResError = 0   #色环电阻误差
        
        self.chkColor4.setChecked(True)
    
    def makeRes(self):
        self.resX = -100
        self.resY = -145
        self.resW =  200
        self.resH =   45
        self.itemRes = QGraphicsRectItem(self.resX, self.resY, self.resW, self.resH)
        self.itemRes.setBrush(QtGui.QBrush(QtGui.QColor(128, 64, 32, 16)))
        self.graScene.addItem(self.itemRes)

        self.itemRe1 = QGraphicsRectItem(self.resX+ 10, self.resY, 20, self.resH, self.itemRes)
        self.itemRe1.setBrush(QtGui.QBrush(Qt.red))
        
        self.itemRs1 = QGraphicsSimpleTextItem('', self.itemRe1)
        self.itemRs1.setFont(QtGui.QFont('Microsoft YaHei', 15))
        self.itemRs1.setBrush(Qt.black)
        self.itemRs1.setPos(self.resX+ 13,self.resY-23)
        
        
        self.itemRe2 = QGraphicsRectItem(self.resX+ 45, self.resY, 20, self.resH, self.itemRes)
        self.itemRe2.setBrush(QtGui.QBrush(Qt.yellow))
        
        self.itemRs2 = QGraphicsSimpleTextItem('', self.itemRe2)
        self.itemRs2.setFont(QtGui.QFont('Microsoft YaHei', 15))
        self.itemRs2.setBrush(Qt.black)
        self.itemRs2.setPos(self.resX+ 48,self.resY-23)
        
        
        self.itemRe3 = QGraphicsRectItem(self.resX+ 80, self.resY, 20, self.resH, self.itemRes)
        self.itemRe3.setBrush(QtGui.QBrush(Qt.green))
        
        self.itemRs3 = QGraphicsSimpleTextItem('', self.itemRe3)
        self.itemRs3.setFont(QtGui.QFont('Microsoft YaHei', 15))
        self.itemRs3.setBrush(Qt.black)
        self.itemRs3.setPos(self.resX+ 83,self.resY-23)
              
        
        self.itemRe4 = QGraphicsRectItem(self.resX+115, self.resY, 20, self.resH, self.itemRes)
        self.itemRe4.setBrush(QtGui.QBrush(Qt.black))
        
        self.itemRs4 = QGraphicsSimpleTextItem('', self.itemRe4)
        self.itemRs4.setFont(QtGui.QFont('Microsoft YaHei', 15))
        self.itemRs4.setBrush(Qt.black)
        self.itemRs4.setPos(self.resX+118,self.resY-23)


        self.itemRe5 = QGraphicsRectItem(self.resX+165, self.resY, 20, self.resH, self.itemRes)
        self.itemRe5.setBrush(QtGui.QBrush(ResColor.Colors[10][1]))
        
        self.itemRs5 = QGraphicsSimpleTextItem('', self.itemRe5)
        self.itemRs5.setFont(QtGui.QFont('Microsoft YaHei', 15))
        self.itemRs5.setBrush(Qt.black)
        self.itemRs5.setPos(self.resX+168,self.resY-23)

        
        self.itemPin = QGraphicsRectItem(self.resX- 40, self.resY+20, 40, 5, self.itemRes)
        self.itemPin = QGraphicsRectItem(self.resX+self.resW, self.resY+20, 40, 5, self.itemRes)
    
    def makeLblBar(self, x0, y0):
        self.LblBar = QGraphicsRectItem(x0, y0, 20, 20*12)
        self.LblBar.setPen(Qt.white)
        self.graScene.addItem(self.LblBar)
        
        for i in range(0, 12):
            lbl = QGraphicsSimpleTextItem(ResColor.Colors[i][0], self.LblBar)
            lbl.setFont(QtGui.QFont('Microsoft YaHei', 12))
            lbl.setBrush(Qt.black)
            lbl.setPos(x0,y0+i*20)
    
    def makeBtnBar1(self, x0, y0):
        self.BtnBar1 = QGraphicsRectItem(x0, y0, 20, 20*12)
        self.BtnBar1.setPen(Qt.white)
        self.graScene.addItem(self.BtnBar1)
        
        for i in range(0, 9):
            btn = ColorRectItem(x0, y0+i*20, 20, 20, ResColor.Colors[i][1], self.BtnBar1)
            btn.mousePress.connect(lambda b=btn: self.updateResValue(self.itemRe1, b.color))
            btn.hoverEnter.connect(lambda idx=i: self.itemRs1.setText(str(ResColor.Colors[idx][2])))
            btn.hoverLeave.connect(lambda: self.itemRs1.setText(''))
    
    def makeBtnBar2(self, x0, y0):
        self.BtnBar2 = QGraphicsRectItem(x0, y0, 20, 20*12)
        self.BtnBar2.setPen(Qt.white)
        self.graScene.addItem(self.BtnBar2)
        
        for i in range(0, 10):
            btn = ColorRectItem(x0, y0+i*20, 20, 20, ResColor.Colors[i][1], self.BtnBar2)
            btn.mousePress.connect(lambda b=btn: self.updateResValue(self.itemRe2, b.color))
            btn.hoverEnter.connect(lambda idx=i: self.itemRs2.setText(str(ResColor.Colors[idx][2])))
            btn.hoverLeave.connect(lambda: self.itemRs2.setText(''))            
    
    def makeBtnBar3(self, x0, y0):
        self.BtnBar3 = QGraphicsRectItem(x0, y0, 20, 20*12)
        self.BtnBar3.setPen(Qt.white)
        self.graScene.addItem(self.BtnBar3)
        
        for i in range(0, 12):
            btn = ColorRectItem(x0, y0+i*20, 20, 20, ResColor.Colors[i][1], self.BtnBar3)
            btn.mousePress.connect(lambda b=btn: self.updateResValue(self.itemRe3, b.color))
            btn.hoverEnter.connect(lambda idx=i: self.itemRs3.setText('*'+str(ResColor.Colors[idx][3])) if self.chkColor4.isChecked() else self.itemRs3.setText(str(ResColor.Colors[idx][2])))
            btn.hoverLeave.connect(lambda: self.itemRs3.setText(''))            
    
    def makeBtnBar4(self, x0, y0):
        self.BtnBar4 = QGraphicsRectItem(x0, y0, 20, 20*12)
        self.BtnBar4.setPen(Qt.white)
        self.graScene.addItem(self.BtnBar4)
        
        for i in range(0, 12):
            btn = ColorRectItem(x0, y0+i*20, 20, 20, ResColor.Colors[i][1], self.BtnBar4)
            btn.mousePress.connect(lambda b=btn: self.updateResValue(self.itemRe4, b.color))
            btn.hoverEnter.connect(lambda idx=i: self.itemRs4.setText('*'+str(ResColor.Colors[idx][3])))
            btn.hoverLeave.connect(lambda: self.itemRs4.setText(''))            
    
    def makeBtnBar5(self, x0, y0):
        self.BtnBar5 = QGraphicsRectItem(x0, y0, 20, 20*12)
        self.BtnBar5.setPen(Qt.white)
        self.graScene.addItem(self.BtnBar5)
        
        for i in range(0,12):
            btn = ColorRectItem(x0, y0+i*20, 20, 20, ResColor.Colors[i][1], self.BtnBar5)
            btn.mousePress.connect(lambda b=btn: self.updateResValue(self.itemRe5, b.color))
            btn.hoverEnter.connect(lambda idx=i: self.itemRs5.setText('%'+str(ResColor.Colors[idx][4])))
            btn.hoverLeave.connect(lambda: self.itemRs5.setText(''))                   
            
        for i in range( 2, 4): self.BtnBar5.childItems()[i].hide()
        for i in range( 5, 6): self.BtnBar5.childItems()[i].hide()
        for i in range( 7,10): self.BtnBar5.childItems()[i].hide()
    
    def updateResValue(self, res, color):
        if res != None:
            res.setBrush(color)
        else:
            self.itemRe3.setBrush(ResColor.Colors[1][1])
        
        if self.chkColor4.isChecked():
            for lst in ResColor.Colors:
                if self.itemRe1.brush().color() == lst[1]:
                    self.ResValue = lst[2]*10
                    break
            for lst in ResColor.Colors:
                if self.itemRe2.brush().color() == lst[1]:
                    self.ResValue += lst[2]
                    break
            for lst in ResColor.Colors:
                if self.itemRe3.brush().color() == lst[1]:
                    self.ResValue *= lst[3]
                    break
            for lst in ResColor.Colors:
                if self.itemRe5.brush().color() == lst[1]:
                    self.ResError = lst[4]
                    break
        else:
            for lst in ResColor.Colors:
                if self.itemRe1.brush().color() == lst[1]:
                    self.ResValue = lst[2]*100
                    break
            for lst in ResColor.Colors:
                if self.itemRe2.brush().color() == lst[1]:
                    self.ResValue += lst[2]*10
                    break
            for lst in ResColor.Colors:
                if self.itemRe3.brush().color() == lst[1]:
                    self.ResValue += lst[2]
                    break            
            for lst in ResColor.Colors:
                if self.itemRe4.brush().color() == lst[1]:
                    self.ResValue *= lst[3]
                    break
            for lst in ResColor.Colors:
                if self.itemRe5.brush().color() == lst[1]:
                    self.ResError = lst[4]
                    break
        
        dispstr = '电阻值：'
        if self.ResValue < 1000:
            dispstr += '%d' %self.ResValue
        elif self.ResValue < 1000000:
            dispstr += '%0.1fK' %(self.ResValue/1000.0)
        else:
            dispstr += '%0.1fM' %(self.ResValue/1000000.0)
        
        if type(self.ResError) == int:
            dispstr += '    误差：%%%d' %self.ResError
        else:
            dispstr += '    误差：%%%1.1f' %self.ResError
        
        self.lblValue.setText(dispstr)
        
    @pyqtSlot(bool)
    def on_chkColor4_toggled(self, chkd):
        if chkd:
            self.itemRe4.hide()
            for i in range( 0,12): self.BtnBar4.childItems()[i].hide()
            for i in range( 6, 9): self.BtnBar3.childItems()[i].hide()
            for i in range(10,12): self.BtnBar3.childItems()[i].show()
            
            self.updateResValue(None, None)
    
    @pyqtSlot(bool)
    def on_chkColor5_toggled(self,chkd):
        if chkd:
            self.itemRe4.show()
            for i in range( 0, 6): self.BtnBar4.childItems()[i].show()
            for i in range( 9,12): self.BtnBar4.childItems()[i].show()
            for i in range( 6, 9): self.BtnBar3.childItems()[i].show()
            for i in range(10,12): self.BtnBar3.childItems()[i].hide()
            
            self.updateResValue(None, None)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    res = ResColor()
    res.show()
    app.exec()
