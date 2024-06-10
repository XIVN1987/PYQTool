#!python3
import os
import sys
import configparser

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo


class QmlSer(QObject):
    def __init__(self, context, parent=None):
        super().__init__(parent)
        
        self.win = parent
        self.ctx = context

        self.cmbPort = self.win.findChild(QObject, 'cmbPort')
        self.cmbBaud = self.win.findChild(QObject, 'cmbBaud')
        self.cmbData = self.win.findChild(QObject, 'cmbData')
        self.cmbChek = self.win.findChild(QObject, 'cmbParity')
        self.cmbStop = self.win.findChild(QObject, 'cmbStop')

        self.txtMain = self.win.findChild(QObject, 'txtMain')
        self.txtSend = self.win.findChild(QObject, 'txtSend')

        self.btnOpen = self.win.findChild(QObject, 'btnOpen')
        self.btnSend = self.win.findChild(QObject, 'btnSend')

        self.chkHexShow = self.win.findChild(QObject, 'chkHexShow')
        self.chkWavShow = self.win.findChild(QObject, 'chkWavShow')
        self.chkHexSend = self.win.findChild(QObject, 'chkHexSend')
        self.chkTimSend = self.win.findChild(QObject, 'chkTimSend')
        self.chkExtTran = self.win.findChild(QObject, 'chkExtTran')

        self.initSetting()

        self.ser = QSerialPort(self)
        self.ser.readyRead.connect(self.on_ser_dataAvailable)
        
    def initSetting(self):
        if not os.path.exists('setting.ini'):
            open('setting.ini', 'w')
        
        self.conf = configparser.ConfigParser()
        self.conf.read('setting.ini')
        
        if not self.conf.has_section('serial'):
            self.conf.add_section('serial')
            self.conf.set('serial', 'port', 'COM0')
            self.conf.set('serial', 'baud', '9600')

        self.cmbPort.setProperty('currentIndex', self.cmbPort.find(self.conf.get('serial', 'port')))
        self.cmbBaud.setProperty('currentIndex', self.cmbBaud.find(self.conf.get('serial', 'baud')))

    @pyqtSlot()
    def on_btnOpen_clicked(self):
        if not self.ser.isOpen():
            try:
                self.ser.setPortName(self.cmbPort.property('currentText').split()[0])
                self.ser.setBaudRate(int(self.cmbBaud.property('currentText')))
                self.ser.setDataBits(int(self.cmbData.property('currentText')))
                self.ser.setStopBits(int(self.cmbStop.property('currentText')))
                self.ser.setParity({'None': QSerialPort.NoParity, 'Odd': QSerialPort.OddParity, 'Even': QSerialPort.EvenParity, 
                                    'One': QSerialPort.MarkParity, 'Zero': QSerialPort.SpaceParity}[self.cmbChek.property('currentText')])
                self.ser.open(QtCore.QIODevice.ReadWrite)
            except Exception as e:
                print(e)
            else:
                self.btnOpen.setProperty('text', '关闭串口')
                
        else:
            self.ser.close()
            
            self.btnOpen.setProperty('text', '打开串口')

    @pyqtSlot()
    def on_btnSend_clicked(self):
        if self.ser.isOpen():
            text = self.txtSend.property('text')
            if self.chkHexSend.property('checkedState'):
                bytes = ' '.join([chr(int(c, 16)) for c in text.split()]).encode('latin')
            else:
                bytes = text.encode('latin')
            
            self.ser.write(bytes)

    def on_ser_dataAvailable(self):
        bytes = self.ser.read(self.ser.bytesAvailable())
        
        self.txtMain.setProperty('text', self.txtMain.property('text') + bytes.decode('latin'))

    @pyqtSlot()
    def on_btnClear_clicked(self):
        self.txtMain.setProperty('text', '')

    @pyqtSlot()
    def on_closed(self):
        self.ser.close()

        self.conf.set('serial', 'port', self.cmbPort.property('currentText'))
        self.conf.set('serial', 'baud', self.cmbBaud.property('currentText'))

        self.conf.write(open('setting.ini', 'w'))


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    qml = QQmlApplicationEngine(app)

    qml.rootContext().setContextProperty('ports', ['%s (%s)' %(port.portName(), port.description()) for port in QSerialPortInfo.availablePorts()])
    qml.load('QmlSer.qml')

    ser = QmlSer(qml.rootContext() ,qml.rootObjects()[0])
    qml.rootContext().setContextProperty('ser', ser)

    sys.exit(app.exec())
