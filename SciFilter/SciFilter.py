#! python3
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtChart import QChart, QChartView, QLineSeries

import numpy as np
import scipy as sp


class SciFilter(QWidget):
    def __init__(self, parent=None):
        super(SciFilter, self).__init__(parent)
        
        uic.loadUi('SciFilter.ui', self)

        self.bgrpArch = QtWidgets.QButtonGroup(self)
        self.bgrpArch.addButton(self.chkFIR)
        self.bgrpArch.addButton(self.chkIIR)
        self.bgrpArch.buttonToggled.connect(self.on_bgrpArch_buttonToggled)

        self.bgrpType = QtWidgets.QButtonGroup(self)
        self.bgrpType.addButton(self.chkLP)
        self.bgrpType.addButton(self.chkHP)
        self.bgrpType.addButton(self.chkBP)
        self.bgrpType.addButton(self.chkBS)
        self.bgrpType.buttonToggled.connect(self.on_bgrpType_buttonToggled)
        self.on_bgrpType_buttonToggled(self.chkLP, True)

        self.bgrpModl = QtWidgets.QButtonGroup(self)
        self.bgrpModl.addButton(self.chkCheb)
        self.bgrpModl.addButton(self.chkBess)
        self.bgrpModl.addButton(self.chkButt)
        self.bgrpModl.addButton(self.chkElli)
        self.bgrpModl.buttonToggled.connect(self.on_bgrpModl_buttonToggled)

    def on_bgrpArch_buttonToggled(self, button, checked):
        if not checked: return

        if self.bgrpArch.checkedButton() == self.chkFIR:
            self.lblNtap.setEnabled(True)
            self.linNtap.setEnabled(True)
        
        else:
            self.lblNtap.setEnabled(False)
            self.linNtap.setEnabled(False)
    
    def on_bgrpType_buttonToggled(self, button, checked):
        if not checked: return

        if self.bgrpType.checkedButton() in (self.chkLP, self.chkHP):
            self.lblHlimit.setEnabled(False)
            self.linHlimit.setEnabled(False)
            self.lblFstop.setText('截止频率：')

        else:
            self.lblHlimit.setEnabled(True)
            self.linHlimit.setEnabled(True)
            self.lblFstop.setText('下限频率：')

    def on_bgrpModl_buttonToggled(self, button, checked):
        if not checked: return

        model = self.bgrpModl.checkedButton().text()

        print(model)

    @pyqtSlot()
    def on_btnCalc_clicked(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SciFilter()
    win.show()
    app.exec()
