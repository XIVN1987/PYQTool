import QtQuick 2.9
import QtQuick.Layouts 1.3
import QtQuick.Controls 1.4

ApplicationWindow {
	visible: true
	width: 720
	height: 560
	title: "串口助手"

	ColumnLayout {
		anchors.fill: parent
		anchors.margins: 10
		spacing: 10

		TextArea {
			id: txtMain
			objectName: "txtMain"
			readOnly: true
		 	Layout.fillWidth: true
		 	Layout.fillHeight: true
		}

		RowLayout {
			spacing: 10

			Label {
				id: lblSer
				text: "串口号："
			}

			ComboBox {
				id: cmbPort
				objectName: "cmbPort"
				Layout.minimumWidth: 100 * 2 + 10 * 2 + lblSer.width
				model: ports
			}

			Label {
				text: "波特率："
			}

			ComboBox {
				id: cmbBaud
				objectName: "cmbBaud"
				Layout.minimumWidth: 100
				model: [ "1200", "2400", "4800", "9600", "14400", "19200", "28800", "38400", "57600", "115200" ]
			}

			Label {
				Layout.fillWidth: true
			}

			Button {
				id: btnOpen
				objectName: 'btnOpen'
				Layout.minimumWidth: 100
				text: "打开串口"
				onClicked: ser.on_btnOpen_clicked()
			}

			CheckBox {
				id: chkHexShow
				objectName: "chkHexShow"
				Layout.minimumWidth: 80
				text: "HEX 显示"
			}
		}

		RowLayout {
			spacing: 10

			Label {
				text: "数据位："
			}

			ComboBox {
				id: cmbData
				objectName: "cmbData"
				Layout.minimumWidth: 100
				model: [ "8", "6", "7", "8", "9" ]
			}

			Label {
				text: "校验位："
			}

			ComboBox {
				id: cmbParity
				objectName: "cmbParity"
				Layout.minimumWidth: 100
				model: [ "None", "Odd", "Even", "One", "Zero" ]
			}

			Label {
				text: "停止位："
			}

			ComboBox {
				id: cmbStop
				objectName: "cmbStop"
				Layout.minimumWidth: 100
				model: [ "1", "2" ]
			}

			Label {
				Layout.fillWidth: true
			}

			Button {
				id: btnClear
				Layout.minimumWidth: 100
				text: "清除显示"
				onClicked: ser.on_btnClear_clicked()
			}

			CheckBox {
				id: chkWavShow
				objectName: "chkWavShow"
				Layout.minimumWidth: 80
				text: "波形显示"
			}
		}

		GridLayout {
			rows: 3
			columns: 3
			rowSpacing: 10
			columnSpacing: 10
			Layout.topMargin: 5

			TextArea {
				id: txtSend
				objectName: "txtSend"
				Layout.row: 0
				Layout.column: 0
				Layout.rowSpan: 3
				Layout.fillWidth: true
				Layout.maximumHeight: parent.height
				Layout.rightMargin: 10
			}

			Button {
				id: btnSend
				objectName: 'btnSend'
				Layout.row: 0
				Layout.column: 1
				Layout.rowSpan: 3
				Layout.minimumWidth: 100
				Layout.minimumHeight: parent.height
				text: "发送"
				onClicked: ser.on_btnSend_clicked()
			}

			CheckBox {
				id: chkHexSend
				objectName: "chkHexSend"
				Layout.row: 0
				Layout.column: 2
				Layout.minimumWidth: 80
				text: "HEX 发送"
			}

			CheckBox {
				id: chkTimSend
				objectName: "chkTimSend"
				Layout.row: 1
				Layout.column: 2
				Layout.minimumWidth: 80
				text: "定时发送"
			}

			CheckBox {
				id: chkExtTran
				objectName: "chkExtTran"
				Layout.row: 2
				Layout.column: 2
				Layout.minimumWidth: 80
				text: "扩展收发"
			}
		}
	}

	onClosing: {
        ser.on_closed()
    }
}
