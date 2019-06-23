#!/usr/bin/env python3

import subprocess
import sys
import interactive
import configfile

if sys.argv[1].lower() in ['-i', '--interactuve']:
    interactive.start()
else:
    configfile.start()
command = "ansible-playbook ./startup_point.yml -i ./inventory/env"

subprocess.call(command.split(' '))