#!/bin/bash

/home/3proxy/random.sh > /home/3proxy/ip.list
/home/3proxy/3proxy.sh > /home/3proxy/3proxy.cfg
killall 3proxy
/home/3proxy/3proxy /home/3proxy/3proxy.cfg