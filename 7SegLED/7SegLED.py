#! python3
import sys

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsScene
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsEllipseItem


class Segment(QGraphicsPolygonItem):
    def __init__(self, pos, angle, parent=None):
        super(Segment, self).__init__(parent)
        super(Segment, self).setPolygon(QtGui.QPolygonF([QtCore.QPointF(-60,0),QtCore.QPointF(-50,10),QtCore.QPointF(50,10),QtCore.QPointF(60,0),QtCore.QPointF(50,-10),QtCore.QPointF(-50,-10)]))
        super(Segment, self).setPos(pos)
        super(Segment, self).setRotation(angle)
        super(Segment, self).setPen(QtGui.QPen(Qt.black,3))
        super(Segment, self).setBrush(QtGui.QBrush(Qt.red))
    
    def mousePressEvent(self, event):
        if self.brush().color() == Qt.white:
            super(Segment, self).setBrush(QtGui.QBrush(Qt.red))
        else:
            super(Segment, self).setBrush(QtGui.QBrush(Qt.white))
            
        QGraphicsPolygonItem.mousePressEvent(self, event)
        
class SegmentDP(QGraphicsEllipseItem):
    def __init__(self, pos, parent=None):
        super(SegmentDP, self).__init__(parent)
        super(SegmentDP, self).setRect(0, 0, 20, 20)
        super(SegmentDP, self).setPos(pos)
        super(SegmentDP, self).setPen(QtGui.QPen(Qt.black,3))
        super(SegmentDP, self).setBrush(QtGui.QBrush(Qt.red))    
        
    def mousePressEvent(self, event):
        if self.brush().color() == Qt.white:
            super(SegmentDP, self).setBrush(QtGui.QBrush(Qt.red))
        else:
            super(SegmentDP, self).setBrush(QtGui.QBrush(Qt.white))
            
        QGraphicsEllipseItem.mousePressEvent(self, event)


class Seg7LED(QWidget):
    CharCode = {'0-9':[0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F],     #共阴，引脚A-DP对应为0-7
                'A':0x77, 'b':0x7C, 'C':0x39, 'c':0x58, 'd':0x5E, 'E':0x79, 'F':0x71,
                'H':0x76, 'h':0x74, 'L':0x38, 'N':0x37, 'n':0x54, 'o':0x5C, 'P':0x73,
                'R':0x31, 'r':0x50, 't':0x78, 'U':0x3E, '-':0x40, ' ':0x00}
    
    def __init__(self, parent=None):
        super(Seg7LED, self).__init__(parent)
        
        uic.loadUi('7SegLED.ui', self)
        
        self.graScene = QGraphicsScene()
        self.graShape.setScene(self.graScene)
        
        self.graScene.setSceneRect(-120, -150, 240, 300)
        self.graShape.centerOn(0, 0)
        
        self.makeShape()
        
        for i in range(0, self.grpChar.layout().count()):
            chkWid = self.grpChar.layout().itemAt(i).widget()
            chkWid.toggled.connect(lambda checked,chkX=chkWid: self.showChar(chkX.text()) if checked else self.showChar(' '))
        
        self.chkChar0_9.setChecked(True)
        
    def makeShape(self):
        self.seg = QGraphicsPolygonItem()
        self.graScene.addItem(self.seg)
        
        self.segA = Segment(QtCore.QPointF(-10, -120),  0, self.seg)
        
        self.segB = Segment(QtCore.QPointF( 50,  -60), 90, self.seg)
        
        self.segC = Segment(QtCore.QPointF( 50,   60), 90, self.seg)
        
        self.segD = Segment(QtCore.QPointF(-10,  120),  0, self.seg)
        
        self.segE = Segment(QtCore.QPointF(-70,   60), 90, self.seg)
        
        self.segF = Segment(QtCore.QPointF(-70,  -60), 90, self.seg)
        
        self.segG = Segment(QtCore.QPointF(-10,    0),  0, self.seg)
        
        self.segDP= SegmentDP(QtCore.QPointF(80, 110), self.seg)
    
    def showChar(self, char):
        if char == '0-9':
            code = self.CharCode['0-9'][9]
        else:
            code = self.CharCode[char]
        
        for i in range(0, 8):
            if bin(code+256)[::-1][i] == '1':
                self.seg.childItems()[i].setBrush(QtGui.QBrush(Qt.red))
            else:
                self.seg.childItems()[i].setBrush(QtGui.QBrush(Qt.white))
    
    def CodeTransform(self, code):
        rcode = 0x00
        for i in range(0, 8):
            rcode |= ((code>>i)&1) << int(self.grpPin.layout().itemAtPosition(i, 1).widget().currentText())
        
        if self.cmbPolar.currentText() == u'共阳极':
            rcode = 0xFF - rcode
        
        return rcode
    
    @pyqtSlot()
    def on_btnClear_clicked(self):
        self.txtData.clear()
        for i in range(0, self.grpChar.layout().count()):
            self.grpChar.layout().itemAt(i).widget().setChecked(False)
    
    @pyqtSlot()
    def on_btnMake_clicked(self):
        text = ''
        for i in range(0, self.grpChar.layout().count()):
            chkWid = self.grpChar.layout().itemAt(i).widget()
            if chkWid.isChecked():
                if chkWid.text() == '0-9':
                    for i in range(0, 10):
                        text += "            0x%02X,    // '%d'\n" %(self.CodeTransform(self.CharCode['0-9'][i]), i)
                else:
                    text += "            0x%02X,    // '%s'\n" %(self.CodeTransform(self.CharCode[chkWid.text()]), chkWid.text())
        
        if text == '':
            code = 0x00
            for i in range(0, 8):
                if self.seg.childItems()[i].brush().color() == Qt.red:
                    code |= 1<<i
            text += "            0x%02X,    // ''\n" %code
        
        self.txtData.setText(text)
    
    @pyqtSlot()
    def on_btnCopy_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.txtData.toPlainText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    led = Seg7LED()
    led.show()
    app.exec()
