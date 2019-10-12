from scapy.all import *
for i in range(1,256):
    ip="192.168.2."+str(i)
    arpReq=Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip,hwdst="ff:ff:ff:ff:ff:ff")
    arpRes=srp1(arpReq,timeout=1,verbose=0)
    if arpRes:
        print("IP:" + arpRes.psrc + " MAC:" + arpRes.hwsrc)