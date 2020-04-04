def start(subnet_type):
    if subnet_type == 'ipv4':
        ipv4()
    else:
        ipv6()


def ipv6():
    env = open('./inventory/env', 'w')
    env.write('proxyv6:\n  hosts:\n')

    config_data = open('data_ipv6.conf', 'r')
    login, password, count, net_type, rotate_type, rotate, cron = config_data.readline().split(' ')
    minute = cron.split(',')[1].strip('\n')
    hour = cron.split(',')[0]
    if minute == '*': minute = '"*"'
    if hour == '*': hour = '"*"'

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
                   '    cron_minute: {minute}').format(net_type=net_type,
                                  count=count,
                                  password=password,
                                  rotate=rotate,
                                  rotate_type=rotate_type,
                                  hour=hour,
                                  minute=minute)))

    env.close()


def ipv4():
    env = open('./inventory/env', 'w')
    env.write('proxyv4:\n  hosts:\n')

    config_data = open('data_ipv4.conf', 'r')
    login, password, count = config_data.readline().split(' ')

    for line in config_data:
        if line == '':
            continue
        ip, subnet, root_passwd = line.split(' ')
        env.write(str('\n'
                      '    server_{ip}:\n'
                      '      ansible_host: {ip}\n'
                      '      ansible_ssh_user: root\n'
                      '      ansible_ssh_pass: {root_passwd}\n'
                      '      subnet: {subnet}').format(ip=ip, root_passwd=root_passwd, subnet=subnet))

    env.write(str(('\n'
                   '  vars:\n'
                   '    count: {count}\n'
                   '    proxy_login: {login}\n'     
                   '    proxy_password: {password}').format(count=count, login=login, password=password)))

    env.close()