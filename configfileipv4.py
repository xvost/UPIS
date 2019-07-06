def start():
    env = open('./inventory/env_ipv4', 'w')
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