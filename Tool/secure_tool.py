from scapy.all import *
from scapy.layers.zigbee import *
from scapy.layers.dot15d4 import *
import json
import datetime
 
from lamp import Lamp
from notification import WhatsApp

with open("config.json",'r') as j:
        creds = json.loads(j.read())

Whatsapp_Notification = WhatsApp(
    creds['whatsapp']['whatsapp_sid'],
    creds['whatsapp']['whatsapp_token'],
    creds['whatsapp']['whatsapp_from'],
    creds['whatsapp']['whatsapp_to']
    )

conf.dot15d4_protocol = 'zigbee'

framecounter_cache = {}


class Secure:

    def __init__(self):
        self.pckts = []
        self.Lamp = Lamp()
        
    def start(self):
        while 1:
            pcap_reader = PcapReader('user.pcap')
            pckts_c = pcap_reader.read_all(count=-1)
            pcap_reader.close()
            if(len(pckts_c) == len(self.pckts)):
                continue
            l = 0
            for pkt in pckts_c:
                if(l<len(self.pckts)):
                    l+=1
                    continue
                source = pkt[Dot15d4].src_addr
                framecounter =  pkt[ZigbeeSecurityHeader].fc
                if source not in framecounter_cache:
                    framecounter_cache[source] = framecounter
                else:
                    if(framecounter_cache[source] >= framecounter):
                        message = f"Attention! Replay Attack was detected on your virtual lamp on \
                                    {str(datetime.datetime.now()).strip()[0]} at \
                                    {str(datetime.datetime.now()).strip()[1]}"
                        print(message)
                        Whatsapp_Notification.send_message(message)
                        continue
                    else:
                        framecounter_cache[source] = framecounter
                try:
                    data = pkt[ZigbeeSecurityHeader].data.decode()
                    self.Lamp.command(data)
                except:
                    continue
            self.pckts = pckts_c