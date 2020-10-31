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
        ip = server['ip']
        user = server['login']
        user_passwd = server['password']
        ipv6 = network
        ipv64 = server['gatewayipv64']
        env.write(str(f'\n'
                      f'    server_{ip}:\n'
                      f'      ansible_host: {ip}\n'
                      f'      ansible_ssh_user: {user}\n'
                      f'      ansible_ssh_pass: {user_passwd}\n'
                      f'      ipv4: {ip}\n'
                      f'      nipv6: {ipv6}\n'
                      f'      nipv664: {ipv64}\n'))
        listfile = open('./proxylists/{}.list'.format(server['ip']), 'w')
        end = int(proxy['startport'])+int(proxy['quantityinsubnet'])
        start = int(proxy['startport'])
        enum = 0
        inputadd = server['ip']
        for line in range(start, end, 1):
            port = start + enum
            inputadd = inputadd
            port = port
            user = proxy['login']
            password = proxy['password']
            listfile.write(f'{inputadd}:{port}@{user}:{password}\n')
            enum += 1
    net_type = proxy['nettype']
    count = proxy['quantityinsubnet']
    startport = proxy['startport']
    login = proxy['login']
    password = proxy['password']
    rotate = proxy['rotation']
    rotate_type = proxy['randomtype']
    hour = hour
    minute = minute
    env.write(str(f'\n'
                  f'  vars:\n'
                  f'    net_type: {net_type}\n'
                  f'    count: {count}\n'
                  f'    start_port: {startport}\n'
                  f'    proxy_login: {login}\n'
                  f'    proxy_password: {password}\n'
                  f'    rotate_type: {rotate_type}\n'
                  f'    rotate: {rotate}\n'
                  f'    cron_hour: "{hour}"\n'
                  f'    cron_minute: "{minute}"'))

    env.close()


def ipv4():
    import configobj
    import ipaddress

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
        ip = server['ip']
        user = server['login']
        user_passwd = server['password']
        env.write(str(f'\n'
                      f'    server_{ip}:\n'
                      f'      ansible_host: {ip}\n'
                      f'      ansible_ssh_user: {user}\n'
                      f'      ansible_ssh_pass: {user_passwd}\n'
                      f'      subnet: {network}'))
        listfile = open('./proxylists/{}.list'.format(server['ip']), 'w')

        end = ipaddress.ip_network(network).num_addresses+int(proxy['startport'])
        start = int(proxy['startport'])
        enum = 0
        for line in range(start, end, 1):
            if proxy['input'] == 'self':
                inputadd = ipaddress.ip_network(network)[enum]
            else:
                inputadd = server['ip']
            port = start + enum
            inputadd = inputadd
            port = port
            user = proxy['login']
            password = proxy['password']
            listfile.write(f'{inputadd}:{port}@{user}:{password}\n')
            enum += 1

    count = proxy['quantitypersubnet']
    port = proxy['startport']
    login = proxy['login']
    password = proxy['password']
    input = proxy['input']
    env.write(str(f'\n'
                  f'  vars:\n'
                  f'    count: {count}\n'
                  f'    start_port: {port}\n'
                  f'    proxy_login: {login}\n'
                  f'    proxy_password: {password}\n'
                  f'    input: {input}'))
    env.close()