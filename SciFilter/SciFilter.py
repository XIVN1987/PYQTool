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

        self.on_bgrpType_buttonToggled(self.chkLP, True)

    @pyqtSlot(QtWidgets.QAbstractButton, bool)
    def on_bgrpArch_buttonToggled(self, button, checked):
        if not checked: return

        if self.bgrpArch.checkedButton() == self.chkFIR:
            self.lblNtap.setEnabled(True)
            self.linNtap.setEnabled(True)
        
        else:
            self.lblNtap.setEnabled(False)
            self.linNtap.setEnabled(False)
    
    @pyqtSlot(QtWidgets.QAbstractButton, bool)
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

    @pyqtSlot(QtWidgets.QAbstractButton, bool)
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
