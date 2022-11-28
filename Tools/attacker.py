from scapy.all import *
from scapy.layers.dot15d4 import *
from scapy.layers.zigbee import *
from killerbee import *

import time


devstring = input("Enter device id: ") 
kb = KillerBee(device=devstring)
kb.set_channel(11)

cap = PcapReader('hacker.pcap')

while True:
    try:
        packet = cap.pnext()[1]
        time.sleep(1)
        kb.inject(packet[0:-2])
    except TypeError:
        break