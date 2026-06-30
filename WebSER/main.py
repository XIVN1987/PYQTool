#! python3
''' 更改记录
'''
import os
import sys
import json
import time
import threading

from bottle import route, run, request
from bottle import static_file, template

from serial import Serial
from serial.tools.list_ports import comports

from websocket_server import WebsocketServer


@route('/')
def index(info=''):
    return template('index.html', sers=[(desc, port) for port, desc, hwid in comports()],
                                  ws_url=request.url.replace('http', 'ws').replace('8080', '9978'))

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/')


class SerialServer(object):
    ''' 串口硬件  ==>  串口服务器（ws server）  ==>  电脑浏览器（ws client）
        电脑浏览器（ws client） ==>  串口服务器（ws server）  ==>  串口硬件
    '''
    def __init__(self, websocket_server_host, websocket_server_port):
        super(SerialServer, self).__init__()

        self.ser = Serial()

        self.ws_client = None

        self.ws = WebsocketServer(host=websocket_server_host, port=websocket_server_port)
        self.ws.set_fn_new_client(lambda client, server: self.ws_new_client(client))
        self.ws.set_fn_message_received(lambda client, server, message: self.ws_message_received(message))

        threading.Thread(target=self.ws.run_forever).start()

        threading.Thread(target=self.ser_receive).start()

    def ws_new_client(self, client):
        self.ws_client = client

    def ws_message_received(self, message):
        msg = json.loads(message)
        if 'cmd' in msg:
            if msg['cmd'] == 'open serial':
                print(msg['port'])
                print(msg['baud'])

                if not self.ser.is_open:
                    try:
                        self.ser.port     = msg['port']
                        self.ser.baudrate = msg['baud']
                        self.ser.open()
                    except Exception as e:
                        print(e)
                        self.ws.send_message(self.ws_client, json.dumps({'cmd': 'serial closed'}))
                    else:
                        self.ws.send_message(self.ws_client, json.dumps({'cmd': 'serial opened'}))

            elif msg['cmd'] == 'close serial':
                print('close')

                if self.ser.is_open:
                    self.ser.close()

                    self.ws.send_message(self.ws_client, json.dumps({'cmd': 'serial closed'}))

        elif 'data' in msg:
            print(msg['data'])
            if self.ser.is_open:
                self.ser.write(msg['data'].encode())        

    def ser_receive(self):
        while True:
            if self.ser.is_open:
                num = self.ser.in_waiting
                if num > 0:
                    bytes = self.ser.read(num)
                    print(bytes)

                    if self.ws_client:
                        self.ws.send_message(self.ws_client, json.dumps({'data': bytes.decode()}))

            time.sleep(0.1)


if __name__ == '__main__':
    ser = SerialServer(websocket_server_host='localhost', websocket_server_port=9978)
    
    run(host='localhost', port='8080', debug=True, reloader=True)

    ''' 在NanoPi上执行:
    ser = SerialServer(websocket_server_host='0.0.0.0', websocket_server_port=9978)
    run(host='0.0.0.0', port='8080', debug=True)
    去掉reloader=True： 发现不去掉时，在NanoPi执行会执行两次WebSocket初始化，从而报地址已使用错误

    由于pyserial扫描不出nanopi上的串口，所以只能根据板子的情况硬编码串口号，将
    sers=[(desc, port) for port, desc, hwid in comports()]
    改成：
    sers=[('/dev/ttyS1', '/dev/ttyS1'), ('/dev/ttyS2', '/dev/ttyS2')]
    上面列表中的串口号在不同的板子上取值和个数不同，需要根据实际情况修改

    执行时要以“sudo python3 main.py”执行，不加sudo的话会报错串口打不开、没权限
    '''
