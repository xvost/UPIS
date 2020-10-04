#!/usr/bin/env python3

import subprocess
import argparse
from datetime import datetime
from shutil import copyfile

import interactive
import configfile

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


arguments = argparse.ArgumentParser()
start_type = arguments.add_mutually_exclusive_group()
start_type.add_argument('-i', action='store_false', help='Interactive mode')
start_type.add_argument('-c', action='store_true', help='Use configfile ./data_ipv6.conf or ./data_ipv4.conf')
arguments.add_argument('type',
                       choices=('ipv4', 'ipv6','input'),
                       help='Type of subnet, default {ipv6}',
                       default='ipv6',
                       )


def config(ip, type):
    if not type and ip == 'input':
        ip = input(bcolors.OKGREEN + 'Тип сетей для настройки (ipv4|ipv6):\n'+bcolors.ENDC)
    start_type = [interactive, configfile][type]
    start_type.start(ip)

args = arguments.parse_args()
config(args.type, args.c)
time = datetime.utcnow()
copyfile('inventory/env','envarchive/env_{}'.format(time))
command = "ansible-playbook ./startup_point.yml -i ./inventory/env"
subprocess.call(command.split(' '))
