def start(subnet_type):
    if subnet_type == 'ipv4':
        ipv4()
    else:
        ipv6()


def ipv6():
    import configobj

    config = configobj.ConfigObj('data_ipv6.conf')

    proxy = config['Proxy']
    servers = config['Servers']

    cron = proxy['cronstring']
    hour = cron[0]
    minute = cron[1]

    env = open('./inventory/env', 'w')
    env.write('proxyv6:\n  hosts:\n')

    for server in servers.keys():
        server = servers[server]
        if isinstance(server['proxynetwork'], list):
            network = ', '.join(server['proxynetwork'])
        else:
            network = server['proxynetwork']
        env.write(str('\n'
                      '    server_{ip}:\n'
                      '      ansible_host: {ip}\n'
                      '      ansible_ssh_user: {user}\n'
                      '      ansible_ssh_pass: {user_passwd}\n'
                      '      ipv4: {ip}\n'
                      '      nipv6: {ipv6}\n'
                      '      nipv664: {ipv64}\n').format(ip=server['ip'],
                                                         user=server['login'],
                                                         user_passwd=server['password'],
                                                         ipv6=network,
                                                         ipv64=server['gatewayipv64']))

    env.write(str(('\n'
                   '  vars:\n'
                   '    net_type: {net_type}\n'
                   '    count: {count}\n'
                   '    start_port: {startport}\n'
                   '    proxy_login: {login}\n'
                   '    proxy_password: {password}\n'
                   '    rotate_type: {rotate_type}\n'
                   '    rotate: {rotate}\n'
                   '    cron_hour: "{hour}"\n'
                   '    cron_minute: "{minute}"').format(net_type=proxy['nettype'],
                                                         count=proxy['quantitypersubnet'],
                                                         startport=proxy['startport'],
                                                         login=proxy['login'],
                                                         password=proxy['password'],
                                                         rotate=proxy['rotation'],
                                                         rotate_type=proxy['randomtype'],
                                                         hour=hour,
                                                         minute=minute)))

    env.close()


def ipv4():
    import configobj

    config = configobj.ConfigObj('data_ipv4.conf')
    proxy = config['Proxy']
    servers = config['Servers']

    env = open('./inventory/env', 'w')
    env.write('proxyv4:\n  hosts:')

    for server in servers:

        server = servers[server]

        if isinstance(server['proxynetwork'], list):
            network = ', '.join(server['proxynetwork'])
        else:
            network = server['proxynetwork']
        env.write(str('\n'
                      '    server_{ip}:\n'
                      '      ansible_host: {ip}\n'
                      '      ansible_ssh_user: {user}\n'
                      '      ansible_ssh_pass: {user_passwd}\n'
                      '      subnet: {subnet}').format(ip=server['ip'],
                                                       user=server['login'],
                                                       user_passwd=server['password'],
                                                       subnet=network))


    env.write(str(('\n'
                   '  vars:\n'
                   '    count: {count}\n'
                   '    start_port: {port}\n'
                   '    proxy_login: {login}\n'
                   '    proxy_password: {password}\n'
                   '    input: {input}').format(count=proxy['quantitypersubnet'],
                                                            port=proxy['startport'],
                                                            login=proxy['login'],
                                                            password=proxy['password'],
                                                            input=proxy['input'])))
    env.close()