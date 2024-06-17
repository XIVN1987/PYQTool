#! python3
import sys
import numpy as np
import scipy as sp
from scipy import signal

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class SciFilter(QWidget):
    def __init__(self, parent=None):
        super(SciFilter, self).__init__(parent)
        
        uic.loadUi('SciFilter.ui', self)

        self.chkLP.setChecked(True)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.hLayout.addWidget(self.canvas)
        self.graphic.hide()   # 隐藏占位控件

        self.axesFR = self.figure.add_subplot(221)  # Frequency Response
        self.axesPR = self.figure.add_subplot(222)  # Phase Response
        self.axesIR = self.figure.add_subplot(223)  # Impulse Response
        self.axesSR = self.figure.add_subplot(224)  # Step Response

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
                b = signal.firwin(ntaps, cutoff, fs=fSamp, window=window, pass_zero=filter)

                w, h = signal.freqz(b, worN=1000)

                self.axesFR.clear()
                self.axesFR.set_title("频率响应")
                self.axesFR.set_xlabel('Frequency (Hz)')
                self.axesFR.plot((w/np.pi)*(fSamp/2), 20*np.log10(np.abs(h)), linewidth=2)
                self.axesFR.grid(True)

                self.canvas.draw()

            except Exception as e:
                print(e)

        else:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SciFilter()
    win.show()
    app.exec()
