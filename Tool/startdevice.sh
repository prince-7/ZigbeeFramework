#!/bin/bash

if [ -f user.pcap ] ; then
    rm  -rf user.pcap
fi

if [ -f hacker.pcap ] ; then
    rm  -rf hacker.pcap
fi

sudo whsniff -c 11 > user.pcap & sudo python3 device.py && fg