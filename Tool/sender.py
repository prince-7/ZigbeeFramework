from scapy.all import *
from scapy.layers.dot15d4 import *
from scapy.layers.zigbee import *

import secrets

conf.dot15d4_protocol = 'zigbee'

sample_pkt = Dot15d4(b'a\x88h\x9e&\x00\x00XB\t\x12\x00\x00XB\x01aq\x9d1%\x00K\x12\x00(&\x00\x00\x00q\x9d1%\x00K\x12\x00\x00ffff')

framecounter = secrets.randbelow(2 ** 32)

while 1:
    on = input("Enter Command: ")
    if on == "ON":
        sample_pkt[ZigbeeSecurityHeader].data = "ffffff"
    elif on == "OFF":
        sample_pkt[ZigbeeSecurityHeader].data = "aaaaaa"
    sample_pkt[ZigbeeSecurityHeader].fc = framecounter
    wrpcap('user.pcap', sample_pkt)
    wrpcap('hacker.pcap', sample_pkt, append=True)
    framecounter = (framecounter+1) % 2**32
    time.sleep(1)