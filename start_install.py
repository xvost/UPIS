#!/usr/bin/env python3

import subprocess

env = open('./inventory/env', 'w')
env.write('proxy:\n  hosts:\n')

config_data = open('data.conf', 'r')
login, password, count, net_type, rotate_type, rotate = config_data.readline().split(' ')

for line in config_data:
    if line == '': continue
    ip,ipv64,ipv6,root_passwd = line.split(' ')
    env.write(f'''
    server_{ip}:
      ansible_host: {ip}
      ansible_ssh_user: root
      ansible_ssh_pass: {root_passwd}
      ipv4: {ip}
      nipv6: {ipv6}
      nipv664: {ipv64}
''')

env.write(f'''
  vars:
    net_type: {net_type}
    count: {count}
    proxy_password: {password}
    rotate_type: {rotate_type}
    rotate: {rotate}
    ''')

env.close()

command = "ansible-playbook ./startup_point.yml -i ./inventory/env"

subprocess.call(command.split(' '))