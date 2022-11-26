from scapy.all import *
from scapy.utils import *
from scapy.layers.dot15d4 import *
from lamp import Lamp

import os

conf.dot15d4_protocol = 'sixlowpan'

pckts = []
cntr = 0

Lamp = Lamp()

while 1:
    cntr+=1
    time.sleep(1)
    pcap_reader = PcapReader('test.pcap')
    pckts_c = pcap_reader.read_all(count=-1)
    pcap_reader.close()
    
    if(len(pckts_c) == len(pckts)):
        continue
    l = 0
    for pkt in pckts_c:
        if(l<len(pckts)):
            l+=1
            continue
        try:
            if pkt[Raw].load.hex() == 'ffff':
                Lamp.command('ffff')
            elif pkt[Raw].load.hex() == 'aaaa':
                Lamp.command('aaaa')
            else:
                print('No Signal')
        except:
            continue
    time.sleep(1)
    pckts = pckts_c