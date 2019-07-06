#!/usr/bin/env python3

import subprocess
import sys
import interactive
import configfile
import configfileipv4

if sys.argv[1].lower() in ['-i', '--interactuve']:
    interactive.start()
elif sys.argv[1].lower() in ['-ipv4', '-4']:
    configfileipv4.start()
else:
    configfile.start()
command = "ansible-playbook ./startup_point.yml -i ./inventory/env"

subprocess.call(command.split(' '))
