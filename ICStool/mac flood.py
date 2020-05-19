#!/usr/bin/env python3 
# -*- coding:utf-8 -*- 
from scapy.all import RandMAC,RandIP,Ether,IP,sendp 
import sys 
iface = 'eth0' 
if len(sys.argv) >= 2: 
    iface = sys.argv[1] 
packet = Ether(src=RandMAC(),dst=RandMAC())/IP(src=RandIP(),dst=RandIP()) 
sendp(packet,iface=iface,loop=1) 