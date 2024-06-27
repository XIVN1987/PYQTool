#! python3
import os
import re
import sys
import stat

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog


class FileModify(QWidget):
    def __init__(self, parent=None):
        super(FileModify, self).__init__(parent)
        
        uic.loadUi('FileModify.ui', self)

    @pyqtSlot()
    def on_btnPath_clicked(self):
        dir = QFileDialog.getExistingDirectory(caption='指定文件所在目录', directory=self.linPath.text())
        if dir != '':
            self.linPath.setText(dir)

    @pyqtSlot(int)
    def on_tabOper_currentChanged(self, index):
        self.cmbType.setEnabled(index != 0)

    @pyqtSlot()
    def on_btnExecN_clicked(self):
        path = self.linPath.text()
        srcN = self.linSrcN.text()
        dstN = self.linDstN.text()
        caseSensitive = self.chkCaseN.isChecked()
        
        self.txtInfo.clear()
        self.renameFileDir(path, srcN, dstN, caseSensitive)
        self.txtInfo.append('Done...')
    
    #将指定路径path及其子目录下的文件名和目录名中的srcN替换成dstN
    def renameFileDir(self, path, srcN, dstN, caseSensitive):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in dirs + files:
                if caseSensitive:
                    newname = re.sub(srcN, dstN, name)
                else:
                    newname = re.sub(srcN, dstN, name, flags=re.I)

                if newname != name:
                    os.rename(os.path.join(root, name), os.path.join(root, newname))

                    self.txtInfo.append(f'{os.path.join(root, name)} => {os.path.join(root, newname)}\n')
    
    @pyqtSlot()
    def on_btnExecT_clicked(self):
        path = self.linPath.text()
        srcT = self.linSrcT.text()
        dstT = self.linDstT.text()
        filter = self.cmbType.currentText()
        caseSensitive = self.chkCaseN.isChecked()
        
        self.txtInfo.clear()
        self.replaceString(path, srcT, dstT, filter, caseSensitive)
        self.txtInfo.append('Done...')

    #将指定路径path及其子目录下的文件的内容中的srcT替换成dstT
    def replaceString(self, path, srcT, dstT, filter, caseSensitive):
        for root, dirs, files in os.walk(path):
            for name in files:
                _, ext = os.path.splitext(name)
                if filter != '*.*' and filter.find(ext) < 1: continue   # str.find('') == 0

                fullpath = os.path.join(root, name)
                try:
                    text = open(fullpath, 'r', encoding='gbk').read()
                    encoding = 'gbk'
                except:
                    try:
                        text = open(fullpath, 'r', encoding='utf-8').read()
                        encoding = 'utf-8'
                    except:
                        self.txtInfo.append(f'{fullpath} read fail\n')
                        continue

                if caseSensitive:
                    newtext = re.sub(srcT, dstT, text)
                else:
                    newtext = re.sub(srcT, dstT, text, flags=re.I)

                if newtext != text:
                    os.chmod(fullpath, stat.S_IWRITE)
                    open(fullpath, 'w', encoding=encoding).write(newtext)

                    self.txtInfo.append(f'{fullpath} content changed\n')

    @pyqtSlot()
    def on_btnExecC_clicked(self):
        path = self.linPath.text()
        srcC = self.cmbSrcC.currentText()
        dstC = self.cmbDstC.currentText()
        filter = self.cmbType.currentText()
        
        self.txtInfo.clear()
        self.CodingConvert(path, srcC, dstC, filter)
        self.txtInfo.append('Done...')

    #将指定路径path及其子目录下的文件的内容编码由srcC转换成dstC
    def CodingConvert(self, path, srcC, dstC, filter):
        for root, dirs, files in os.walk(path):
            for name in files:
                _, ext = os.path.splitext(name)
                if filter != '*.*' and filter.find(ext) < 1: continue
                
                fullpath = os.path.join(root, name)
                try:
                    bstr = open(fullpath, 'rb').read()
                    newbstr = bstr.decode(srcC).encode(dstC)
                except:
                    self.txtInfo.append(f'{fullpath} read fail\n')
                    continue

                if newbstr != bstr:
                    os.chmod(fullpath, stat.S_IWRITE)
                    open(fullpath, 'wb').write(newbstr)

                    self.txtInfo.append(f'{fullpath} encoding changed\n')

    @pyqtSlot()
    def on_btnExecL_clicked(self):
        path = self.linPath.text()
        srcL = self.cmbSrcL.currentText()
        dstL = self.cmbDstL.currentText()
        filter = self.cmbType.currentText()
        
        self.txtInfo.clear()
        self.LineLFConvert(path, srcL, dstL, filter)
        self.txtInfo.append('Done...')

    #将指定路径path及其子目录下的文件中的换行符由srcL转换成dstL
    def LineLFConvert(self, path, srcL, dstL, filter):
        srcLF = srcL.replace(r'\r', '\r').replace(r'\n', '\n').encode()
        dstLF = dstL.replace(r'\r', '\r').replace(r'\n', '\n').encode()
        for root, dirs, files in os.walk(path):
            for name in files:
                _, ext = os.path.splitext(name)
                if filter != '*.*' and filter.find(ext) < 1: continue
                
                fullpath = os.path.join(root, name)

                bstr = open(fullpath, 'rb').read()
                newbstr = bstr.replace(srcLF, dstLF)

                if newbstr != bstr:
                    os.chmod(fullpath, stat.S_IWRITE)
                    open(fullpath, 'wb').write(newbstr)

                    self.txtInfo.append(f'{fullpath} linefeed changed\n')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FileModify()
    win.show()
    app.exec()
