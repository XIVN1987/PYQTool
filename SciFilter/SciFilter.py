#! python3
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtChart import QChart, QChartView, QLineSeries

import numpy as np
import scipy as sp
from scipy import signal


class SciFilter(QWidget):
    def __init__(self, parent=None):
        super(SciFilter, self).__init__(parent)
        
        uic.loadUi('SciFilter.ui', self)

        self.chkLP.setChecked(True)

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
            self.lblFhlim.setEnabled(False)
            self.linFhlim.setEnabled(False)
            self.lblFstop.setText('截止频率：')

        else:
            self.lblFhlim.setEnabled(True)
            self.linFhlim.setEnabled(True)
            self.lblFstop.setText('下限频率：')

    @pyqtSlot(QtWidgets.QAbstractButton, bool)
    def on_bgrpWin_buttonToggled(self, button, checked):
        if not checked: return

        model = self.bgrpWin.checkedButton().text()

        print(model)

    @pyqtSlot()
    def on_btnCalc_clicked(self):
        fSamp = int(self.linFsamp.text()[:-2])
        fStop = int(self.linFstop.text()[:-2])
        fHlim = int(self.linFhlim.text()[:-2])
        ntaps = int(self.linNtap.text())

        filter = self.bgrpType.checkedButton().text().lower().replace(' ', '')

        cutoff = (fStop, fHlim) if 'band' in filter else fStop

        window = {
            'Hann':        'hann',
            'Bessel':      '',
            'Elliptic':    '',
            'Rectangle':   'boxcar',
            'Chebyshev':   'chebwin',
            'Butterworth': ''
        }[self.bgrpWin.checkedButton().text()]

        if self.bgrpArch.checkedButton() == self.chkFIR:
            try:
                signal.firwin(ntaps, cutoff, fs=fSamp, window=window, pass_zero=filter)

            except Exception as e:
                print(e)

        else:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SciFilter()
    win.show()
    app.exec()
