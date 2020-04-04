#!/usr/bin/env python3

import subprocess
import ipaddress
import os
import sys

login, passwd, subnet = sys.argv[1:]

head = '''daemon
maxconn 30000
nscache 65536
timeouts 1 5 30 60 180 1800 15 60
setgid 65534
setuid 65534
flush
auth strong
users {login}:CL:{passwd}
allow {login}
'''

rc_local_head = '''#!/bin/bash

ulimit -n 600000
ulimit -u 600000

'''

rc_local_tail ='''
sleep 5

/root/3proxy/src/3proxy /root/3proxy/3proxy.cfg

exit 0
'''

proxy_string = 'proxy -s0 -n -a -p{port} -i{input} -e{output}\n'
rc_local = '/sbin/ip addr add {ip} dev eth0 \n'



def subnet_single(subnet, start):
    config = open('/root/3proxy/3proxy.cfg', 'w')
    subnet = ipaddress.ip_network(subnet)
    config.write(head.format(login=login, passwd=passwd))
    for e, addr in enumerate(subnet):
        config.write(proxy_string.format(port=int(start)+e, input=addr, output=addr))
        ip_add(addr)
    config.close()
    add_autoload(subnet=subnet)

def ip_add(ip):
    intf_ip = subprocess.getoutput('/sbin/ip addr add {} dev eth0'.format(ip))
    print(intf_ip)

def add_autoload(subnet='', address=''):
    os.rename('/etc/rc.local', '/etc/rc.local.backup')
    open('/etc/rc.local', 'w').close()
    rc_local = open('/etc/rc.local', 'a')
    rc_local.write(rc_local_head)
    if subnet != '':
        for addr in subnet:
            rc_local.write('/sbin/ip addr add {ip} dev eth0 \n'.format(ip=addr))
    elif address != '':
        rc_local.write('/sbin/ip addr add {ip} dev eth0 \n'.format(ip=address))
    rc_local.write(rc_local_tail)
    rc_local.close()
    subprocess.call('chmod +x /etc/rc.local', shell=True)

subnet_single(subnet, 30000)
