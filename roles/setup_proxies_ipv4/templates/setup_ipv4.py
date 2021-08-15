#!/usr/bin/env python3

import subprocess
import ipaddress
import configobj
import os
import sys

configFile = sys.argv[1]
config = configobj.ConfigObj(configFile)

login = config['Proxy']['login']
passwd = config['Proxy']['password']
subnet = config['Proxy']['subnet']
inputIp = config['Proxy']['address']
startPort = config['Proxy']['startport']
inputType = config['Proxy']['input']

head = '''daemon
maxconn 20000
nserver 127.0.0.1
nserver 8.8.8.8
nserver 1.1.1.1
nscache 65536
timeouts 1 5 30 60 180 1800 15 60
setgid 65534
setuid 65534
pidfile /tmp/3proxy.pid
flush
auth strong
users {login}:CL:{passwd}
allow {login}
'''

rc_local_head = '#!/bin/bash \n'
rc_local_tail = '\n exit 0'
proxy_string = 'proxy -s0 -n -a -p{port} -i{input} -e{output} \n'
rc_local = '/sbin/ip addr add {ip} dev eth0 \n'


def subnet_single(subnets, start, ip):
    start = int(start)
    with open('{{ PROXY_DIR }}/3proxy.cfg', 'w') as config3proxy:
        config3proxy.write(head.format(login=login, passwd=passwd))
        for sub in subnets:
            sub = ipaddress.ip_network(sub)
            for addr in sub:
                if inputType == 'self':
                    ip = addr
                config3proxy.write(proxy_string.format(port=start, input=ip, output=addr))
                start += 1
    add_autoload(outputsubnet=subnets)


def add_autoload(outputsubnet='', address=''):
    os.rename('/etc/rc.local', '/etc/rc.local.backup')
    open('/etc/rc.local', 'w').close()
    rcLocal = open('/etc/rc.local', 'a')
    rcLocal.write(rc_local_head)
    if outputsubnet != '':
        for sub in outputsubnet:
            for addr in ipaddress.ip_network(sub):
                rcLocal.write('/sbin/ip addr add {ip} dev eth0 \n'.format(ip=addr))
    elif address != '':
        rcLocal.write('/sbin/ip addr add {ip} dev eth0 \n'.format(ip=address))
    rcLocal.write(rc_local_tail)
    rcLocal.close()
    subprocess.call('chmod +x /etc/rc.local', shell=True)
    subprocess.call('/etc/rc.local', stderr=subprocess.DEVNULL)


subnet = str(subnet).split(',')
subnet_single(subnet, startPort, inputIp)
