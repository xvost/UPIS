#!/usr/bin/env python3

import subprocess
import ipaddress
import os
import sys

login = sys.argv[1]
passwd = sys.argv[2]
subnet = sys.argv[3:][0].split(', ')
inputip = sys.argv[4]
startport = sys.argv[5]

print(subnet)

head = '''daemon
maxconn 20000
nserver 127.0.0.1
nserver 8.8.8.8
nserver 1.1.1.1
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

/root/3proxy/3proxy /root/3proxy/3proxy.cfg

exit 0
'''

proxy_string = 'proxy -s0 -n -a -p{port} -i{input} -e{output}\n'
rc_local = '/sbin/ip addr add {ip} dev eth0 \n'


def subnet_single(subnets, start, ip):
    start=int(start)
    config = open('/root/3proxy/3proxy.cfg', 'w')
    config.write(head.format(login=login, passwd=passwd))
    for subnet in subnets:
        subnet = ipaddress.ip_network(subnet)
        for addr in subnet:
            config.write(proxy_string.format(port=start, input=ip, output=addr))
            start += 1
    config.close()
    add_autoload(subnet=subnets)


def add_autoload(subnet='', address=''):
    os.rename('/etc/rc.local', '/etc/rc.local.backup')
    open('/etc/rc.local', 'w').close()
    rc_local = open('/etc/rc.local', 'a')
    rc_local.write(rc_local_head)
    if subnet != '':
        for sub in subnet:
            for addr in ipaddress.ip_network(sub):
                rc_local.write('/sbin/ip addr add {ip} dev eth0 \n'.format(ip=addr))
    elif address != '':
        rc_local.write('/sbin/ip addr add {ip} dev eth0 \n'.format(ip=address))
    rc_local.write(rc_local_tail)
    rc_local.close()
    subprocess.call('chmod +x /etc/rc.local', shell=True)

subnet_single(subnet, startport, inputip)
