from scapy.all import *
from scapy.layers.dot15d4 import *
from scapy.layers.zigbee import *

conf.dot15d4_protocol = 'zigbee'

from lamp import Lamp

class Unsecure:

    def __init__(self):
        self.pckts = []
        self.Lamp = Lamp()
        
    def start(self): 
        while 1:
            pcap_reader = PcapReader('test.pcap')
            pckts_c = pcap_reader.read_all(count=-1)
            pcap_reader.close()
            if(len(pckts_c) == len(self.pckts)):
                continue
            l = 0
            for pkt in pckts_c:
                if(l<len(self.pckts)):
                    l+=1
                    continue
                try:
                    data = pkt[ZigbeeSecurityHeader].data.decode()
                    self.Lamp.command(data)
                except:
                    continue
            self.pckts = pckts_c