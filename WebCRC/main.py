from collections import OrderedDict

from bottle import route, template, run, static_file, request

from crcmod import Crc
from crcmod.predefined import _crc_definitions_table, PredefinedCrc

@route('/')
def index():
    predefCrc = OrderedDict()
    for crc in _crc_definitions_table:
        poly = '0x%X' %crc[2]
        poly = poly[:-1] if poly.endswith('L') else poly
        init = '0x%X' %crc[4]
        init = init[:-1] if init.endswith('L') else init
        predefCrc[crc[0]] = {'poly': poly, 'init': init, 'irev': crc[3], 'oxor': crc[5]!=0}
    
    return template('index.html', predefCrc=predefCrc)

@route('/ajax', method='POST')
def calculate():
    if request.forms.type == 'predef':
        crc = PredefinedCrc(request.forms.poly)
    else:
        crc = Crc(long(request.forms.poly, 16),
                  long(request.forms.init, 16),
                  request.forms.irev == 'true',
                  [0xFFFFFFFF, 0][0 if request.forms.oxor == 'true' else 1])

    crc.update(request.forms.data.encode('utf-8'))

    return '0x' + crc.hexdigest()

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/')

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)