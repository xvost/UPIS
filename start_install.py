#!/usr/bin/env python3

import subprocess

env = open('./inventory/env', 'w')
env.write('proxy:\n  hosts:\n')

config_data = open('data.conf', 'r')
login, password, count, net_type, rotate_type, rotate, cron = config_data.readline().split(' ')

for line in config_data:
    if line == '':
        continue
    ip, ipv64, ipv6, root_passwd = line.split(' ')
    env.write(str('\n'
                  '    server_{ip}:\n'
                  '      ansible_host: {ip}\n'
                  '      ansible_ssh_user: root\n'
                  '      ansible_ssh_pass: {root_passwd}\n'
                  '      ipv4: {ip}\n'
                  '      nipv6: {ipv6}\n'
                  '      nipv664: {ipv64}\n').format(ip=ip,
                                                     root_passwd=root_passwd,
                                                     ipv6=ipv6,
                                                     ipv64=ipv64))

env.write(str(('\n'
               '  vars:\n'
               '    net_type: {net_type}\n'
               '    count: {count}\n'
               '    proxy_password: {password}\n'
               '    rotate_type: {rotate_type}\n'
               '    rotate: {rotate}\n'
               '    cron_hour: {hour}\n'
               '    cron_minute: {minute}\n'
               '    ').format(net_type=net_type,
                              count=count,
                              password=password,
                              rotate=rotate,
                              rotate_type=rotate_type,
                              hour=cron.split(',')[1],
                              minute=cron.split(',')[0])))

env.close()

command = "ansible-playbook ./startup_point.yml -i ./inventory/env"

subprocess.call(command.split(' '))