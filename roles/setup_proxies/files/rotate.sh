#!/bin/bash

/root/random.sh > /root/ip.list
/root/3proxy.sh > /root/3proxy/3proxy.cfg
killall 3proxy
/root/3proxy/3proxy /root/3proxy/3proxy.cfg

