from scapy.all import *
from scapy.layers.zigbee import *
from scapy.layers.dot15d4 import *
 
conf.dot15d4_protocol = 'zigbee'

framecounter_cache = {}

from lamp import Lamp

pckts = []
cntr = 0

Lamp = Lamp()

while 1:
    cntr+=1
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
        source = pkt[Dot15d4].src_addr
        framecounter =  pkt[ZigbeeSecurityHeader].fc
        if source not in framecounter_cache:
            framecounter_cache[source] = framecounter
        else:
            if(framecounter_cache[source] >= framecounter):
                print("BEWARE !!! Replay Attack")
                continue
            else:
                framecounter_cache[source] = framecounter
        try:
            data = pkt[ZigbeeSecurityHeader].data.decode()
            Lamp.command(data)
        except:
            continue
    pckts = pckts_c