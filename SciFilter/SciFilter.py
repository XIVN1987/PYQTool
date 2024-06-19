#! python3
import os
import sys
import numpy as np
import scipy as sp
from scipy import signal

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class SciFilter(QWidget):
    def __init__(self, parent=None):
        super(SciFilter, self).__init__(parent)
        
        uic.loadUi('SciFilter.ui', self)

        self.chkLP.setChecked(True)
        self.chkFIR.setChecked(True)
        self.chkWrect.setChecked(True)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.hLayout.addWidget(self.canvas)
        self.graphic.hide()   # 隐藏占位控件

        self.axesFR = self.figure.add_subplot(221)  # Frequency Response
        self.axesPR = self.figure.add_subplot(222)  # Phase Response
        self.axesIR = self.figure.add_subplot(223)  # Impulse Response
        self.axesSR = self.figure.add_subplot(224)  # Step Response
        self.figure.subplots_adjust(wspace=0.3, hspace=0.3)

        self.savedir = ''

    @pyqtSlot(QtWidgets.QAbstractButton, bool)
    def on_bgrpArch_buttonToggled(self, button, checked):
        if not checked: return

        if self.bgrpArch.checkedButton() == self.chkFIR:
            self.lblNtap.setEnabled(True)
            self.linNtap.setEnabled(True)
            self.lblOrder.setEnabled(False)
            self.linOrder.setEnabled(False)

            self.chkWrect.setEnabled(True)
            self.chkWhann.setEnabled(True)
            self.chkWcheb.setEnabled(False)
            self.chkWbess.setEnabled(False)
            self.chkWbutt.setEnabled(False)
            self.chkWelli.setEnabled(False)

            self.chkWrect.setChecked(True)
        
        else:
            self.lblNtap.setEnabled(False)
            self.linNtap.setEnabled(False)
            self.lblOrder.setEnabled(True)
            self.linOrder.setEnabled(True)

            self.chkWrect.setEnabled(False)
            self.chkWhann.setEnabled(False)
            self.chkWcheb.setEnabled(True)
            self.chkWbess.setEnabled(True)
            self.chkWbutt.setEnabled(True)
            self.chkWelli.setEnabled(True)

            self.chkWcheb.setChecked(True)
    
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

        if self.bgrpWin.checkedButton() in (self.chkWelli, ):
            self.lblApass.setEnabled(True)
            self.linApass.setEnabled(True)

        else:
            self.lblApass.setEnabled(False)
            self.linApass.setEnabled(False)

        if self.bgrpWin.checkedButton() in (self.chkWelli, self.chkWcheb):
            self.lblAstop.setEnabled(True)
            self.linAstop.setEnabled(True)

        else:
            self.lblAstop.setEnabled(False)
            self.linAstop.setEnabled(False)

    @pyqtSlot()
    def on_btnCalc_clicked(self):
        try:
            fSamp = float(self.linFsamp.text()[:-2])
            fStop = float(self.linFstop.text()[:-2])
            fHlim = float(self.linFhlim.text()[:-2])
            nTaps = int(self.linNtap.text())
            nOrder= int(self.linOrder.text())

            Aripple = float(self.linApass.text()[:-2])
            Aattenuation = float(self.linAstop.text()[:-2])

        except Exception as e:
            QMessageBox.critical(self, 'filter parameter error', str(e))
            return

        filter = self.bgrpType.checkedButton().text().lower().replace(' ', '')

        cutoff = (fStop, fHlim) if 'band' in filter else fStop

        window = {
            'Hann':        'hann',
            'Bessel':      'bessel',
            'Elliptic':    'ellip',
            'Rectangle':   'boxcar',
            'Chebyshev':   'cheby2',
            'Butterworth': 'butter'
        }[self.bgrpWin.checkedButton().text()]

        try:
            if self.bgrpArch.checkedButton() == self.chkFIR:
                b = signal.firwin(nTaps, cutoff, fs=fSamp, pass_zero=filter, window=window)

                w, h = signal.freqz(b, worN=1024)

                ir = b

                sr = np.cumsum(b)           # 阶跃响应是冲激响应的积分

            else:
                b, a = signal.iirfilter(nOrder, cutoff, fs=fSamp, btype=filter, ftype=window, rp=Aripple, rs=Aattenuation)
                
                w, h = signal.freqz(b, a, worN=1024)

                iir = signal.dlti(b, a)     # discrete-time linear time invariant system

                t, ir = signal.dimpulse(iir, n=31)
                t, ir = t, np.squeeze(ir)

                t, sr = signal.dstep(iir, n=31)
                t, sr = t, np.squeeze(sr)

        except Exception as e:
            QMessageBox.critical(self, 'filter calculate error', str(e))
            return

        self.axesFR.clear()
        self.axesFR.set_title('Frequency Response')
        self.axesFR.set_xlabel('Frequency [Hz]')
        self.axesFR.set_ylabel('Amplitude [dB]')
        self.axesFR.plot((w/np.pi)*(fSamp/2), 20*np.log10(np.abs(h)))
        self.axesFR.grid(True)

        self.axesPR.clear()
        self.axesPR.set_title('Phase Response')
        self.axesPR.set_xlabel('Frequency [Hz]')
        self.axesPR.set_ylabel('Angle [radian]')
        self.axesPR.plot((w/np.pi)*(fSamp/2), np.angle(h))
        self.axesPR.grid(True)

        self.axesIR.clear()
        self.axesIR.set_title('Impulse Response')
        self.axesIR.plot(ir)
        self.axesIR.grid(True)

        self.axesSR.clear()
        self.axesSR.set_title('Step Response')
        self.axesSR.plot(sr)
        self.axesSR.grid(True)

        self.canvas.draw()

        if self.bgrpArch.checkedButton() == self.chkFIR:
            return b

        else:
            return b, a

    @pyqtSlot()
    def on_btnGen_clicked(self):
        coef = self.on_btnCalc_clicked()
        if coef is None:
            return

        dtype = self.cmbType.currentText()
        if dtype in ('int8_t', 'int16_t'):
            dtype = 'int16'

        arch = self.bgrpArch.checkedButton().text().lower()

        text = open(f'template/{arch}_{dtype}.c', 'r').read()

        if arch == 'fir':
            b, a = coef, np.ndarray(0)

        else:
            b, a = coef

        if dtype == 'int16':
            a = (a * 2**15).astype(int)
            b = (b * 2**15).astype(int)

            stra = self.data2str(a, '{:6d}, ')
            strb = self.data2str(b, '{:6d}, ')

        else:
            stra = self.data2str(a, '{:.9f}, ')
            strb = self.data2str(b, '{:.9f}, ')

        if arch == 'fir':
            text = text.replace('<n_tap>', f'{self.linNtap.text()}')
            text = text.replace('<coef_b>', strb)

        else:
            text = text.replace('<n_coef>', f'{self.linOrder.text()}')
            text = text.replace('<coef_a>', stra)
            text = text.replace('<coef_b>', strb)

        path, filter = QFileDialog.getSaveFileName(self, '将生成的代码保存至', f'{self.savedir}/{arch}.c', 'C file (*.c)')
        if path:
            open(path, 'w').write(text)

            self.savedir = os.path.dirname(path)

    def data2str(self, data, fmt):
        str = ''

        for i, x in enumerate(data):
            str += fmt.format(x)
            if i and i % 8 == 7:
                str += '\n\t\t'

        return str


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SciFilter()
    win.show()
    app.exec()
