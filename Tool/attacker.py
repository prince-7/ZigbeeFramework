from scapy.all import *
from scapy.layers.dot15d4 import *
from scapy.layers.zigbee import *
from killerbee import *

import time


devstring = input("Enter device id: ") 
kb = KillerBee(device=devstring)
kb.set_channel(11)

while True:
    try:
        packet = cap.pnext()[1]
        kb.inject(packet[0:-2])
        time.sleep(0.1)
    except TypeError:
        break