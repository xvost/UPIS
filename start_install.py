#!/usr/bin/env python3

import sys
import subprocess
import argparse
from datetime import datetime
from shutil import copyfile

import configfile
import cli

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
ip_type = arguments.add_mutually_exclusive_group()
ip_type.add_argument('-n', choices=['ipv4', 'ipv6'], default='ipv6',
                     action='store', dest="type", help='Type of subnet')
arguments.add_argument('-l', action='store_true', dest="list", help='List tags', required=False)
arguments.add_argument('-t', nargs='+', dest="tags", help='Use tags list: -t=sysctl,dns,config and etc.', required=False)


def config(ip, type):
    start_type = [cli, configfile][type]
    start_type.start(ip)

args = arguments.parse_args()

if args.list:
    command = "ansible-playbook ./startup_point.yml -i ./inventory/env --list-tags"
    subprocess.call(command.split(' '))
    sys.exit(0)

tagsstring = ''
if args.tags:
    tagsstring = ','.join(args.tags)
    tagsstring = f' --tags {tagsstring}'

config(args.type, args.c)
time = datetime.utcnow()
copyfile('inventory/env', f'envarchive/env_{time}')

command = f"ansible-playbook ./startup_point.yml -i ./inventory/env{tagsstring}"
subprocess.call(command.split(' '))
