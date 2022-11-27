#!/bin/bash


while true
do
    if [ -f ./user.pcap ]; then
        sudo zbreplay -c 11 -r user.pcap
        rm -rf user.pcap
    fi
done