#!/bin/bash

/home/3proxy/random.sh > /home/3proxy/ip.list
/home/3proxy/3proxy.sh > /home/3proxy/3proxy.cfg
service 3proxy restart