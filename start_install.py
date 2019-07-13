#!/usr/bin/env python3

import subprocess
import sys
import argparse
import interactive
import configfile


def config(ip, type):
    start_type = [interactive, configfile][type]
    start_type.start(ip)


arguments = argparse.ArgumentParser()
arguments.add_argument('type', choices=('ipv4', 'ipv6'), help='Type of subnet, default {ipv6}', default='ipv6')
start_type = arguments.add_mutually_exclusive_group()
start_type.add_argument('-i', action='store_false', help='Interactive')
start_type.add_argument('-c', action='store_true', help='Configfile')

args = arguments.parse_args()

config(args.type, args.c)
command = "ansible-playbook ./startup_point.yml -i ./inventory/env"
subprocess.call(command.split(' '))