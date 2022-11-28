from scapy.all import *
from scapy.layers.dot15d4 import *
from scapy.layers.zigbee import *
from killerbee import *

import secrets
import os

conf.dot15d4_protocol = 'zigbee'

framecounter = secrets.randbelow(2 ** 32)
devstring = input("Enter device id: ") 
kb = KillerBee(device=devstring)
kb.set_channel(11)

while 1:
    cmd = input("Enter Command: ")

    # Build Packet
    sample_pkt = Dot15d4(b'a\x88h\x9e&\x00\x00XB\t\x12\x00\x00XB\x01aq\x9d1%\x00K\x12\x00(&\x00\x00\x00q\x9d1%\x00K\x12\x00\x00ffff')
    if cmd == "ON":
        sample_pkt[ZigbeeSecurityHeader].data = "ffffff"
    elif cmd == "OFF":
        sample_pkt[ZigbeeSecurityHeader].data = "aaaaaa"
    sample_pkt[ZigbeeSecurityHeader].fc = framecounter
    wrpcap('user.pcap', sample_pkt)
    wrpcap('hacker.pcap', sample_pkt, append=True)
    framecounter = (framecounter+1) % 2**32

    #Send Packet
    cap = PcapReader('user.pcap')
    packet = cap.pnext()[1]
    os.remove('user.pcap')

    time.sleep(1)
    kb.inject(packet[0:-2])
