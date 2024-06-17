import QtQuick 2.9
import QtQuick.Layouts 1.3
import QtQuick.Controls 1.4

ApplicationWindow {
	visible: true
	width: 720
	height: 580
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
				id: lblPort
				text: "串口号："
			}

			ComboBox {
				id: cmbPort
				objectName: "cmbPort"
				Layout.minimumWidth: 100 * 2 + 10 * 2 + lblPort.width
				model: ports
			}

			Label {
				id: lblBaud
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
				id: chkWave
				objectName: "chkWave"
				Layout.minimumWidth: 80
				text: "波形显示"
			}
		}

		RowLayout {
			spacing: 10

			Label {
				id: lblData
				text: "数据位："
			}

			ComboBox {
				id: cmbData
				objectName: "cmbData"
				Layout.minimumWidth: 100
				model: [ "8", "6", "7", "8", "9" ]
			}

			Label {
				id: lblChek
				text: "校验位："
			}

			ComboBox {
				id: cmbChek
				objectName: "cmbChek"
				Layout.minimumWidth: 100
				model: [ "None", "Odd", "Even", "One", "Zero" ]
			}

			Label {
				id: lblStop
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
				id: chkSave
				objectName: "chkSave"
				Layout.minimumWidth: 80
				text: "保存接收"
			}
		}

		GridLayout {
			rows: 4
			columns: 3
			rowSpacing: 6
			columnSpacing: 10

			TextArea {
				id: txtSend
				objectName: "txtSend"
				Layout.row: 0
				Layout.column: 0
				Layout.rowSpan: 4
				Layout.fillWidth: true
				Layout.maximumHeight: parent.height
				Layout.rightMargin: 10
			}

			Button {
				id: btnSend
				Layout.row: 0
				Layout.column: 1
				Layout.rowSpan: 4
				Layout.minimumWidth: 100
				Layout.minimumHeight: parent.height
				text: "发送"
				onClicked: ser.on_btnSend_clicked()
			}

			ComboBox {
				id: cmbICode
				objectName: "cmbICode"
				Layout.row: 0
				Layout.column: 2
				Layout.minimumWidth: 80
				model: ["ASCII", "HEX", "GBK", "UTF-8"]
			}

			ComboBox {
				id: cmbOCode
				objectName: "cmbOCode"
				Layout.row: 1
				Layout.column: 2
				Layout.minimumWidth: 80
				model: ["ASCII", "HEX", "GBK", "UTF-8"]
			}

			ComboBox {
				id: cmbEnter
				objectName: "cmbEnter"
				Layout.row: 2
				Layout.column: 2
				Layout.minimumWidth: 80
				model: ["\\r\\n", "\\n", "\\r"]
			}

			ComboBox {
				id: cmbAuto
				objectName: "cmbAuto"
				Layout.row: 3
				Layout.column: 2
				Layout.minimumWidth: 80
				model: [ "No Auto", "0.1s", "0.2s", "0.5s", "1s", "2s", "5s" ]
			}
		}
	}

	onClosing: {
        ser.on_closed()
    }
}
