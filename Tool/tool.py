from scapy.all import *

conf.dot15d4_protocol = 'sixlowpan'

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
        try:
            data = pkt[Raw].load.hex()
            Lamp.command(data)
        except:
            continue
    pckts = pckts_c