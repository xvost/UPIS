import sys

def start(test):
    if test == 'ipv4':
        print('Sorry Mario, but you need config file method')
        sys.exit(0)
    else:
        ipv6()

def ipv6():
    import ipaddress

    print('\n\nПривет!\n'
          'Скрипт умеет настроить ipv6 прокси:\n'
          '64, 48, 36, 32 - сети\n'
          'Одиночные сервера и группы\n'
          'Ограничения:\n'
          '- только debian8\n'
          '- одинаковые логин/пароль для всех прокси (на всех серверах при массовой настройке)\n'
          '- Скрипт инсталяции верит в то что вы укажите все данные в верном порядке и без ошибок'
          '\n\n'
          'Возможности:\n'
          '- ротация\n'
          '- настройка systemd сервиса\n'
          '- ndppd для работы сетей /64 и /48 с параметром non local bind\n'
          '- возможность добавления автоматического обновления конфигурации при измении файла 3proxy.cfg\n'
          'Начать настройку? (y/N)\n')

    iagree = input()

    if iagree.lower() not in ['y', 'yes', 'да', 'д']: sys.exit(0)

    subnet_type = input('Укажи сеть в которой будут работать прокси\n'
                        'принимаемые значения:\n'
                        '64\n'
                        '48\n'
                        '36\n'
                        '32\n')

    if subnet_type not in ['64', '48', '36', '32']:
        print('Сеть не распознана\n')
        sys.exit(0)

    server_ip = input('ip адрес серера для подключения к серверу\n'
                      'если несколько, то разделитель пробел\n').split(' ')

    server_passwd = input('root пароль сервера\n'
                          'если несколько, то разделитель пробел\n').split(' ')

    getway_subnet = input('Укажи шлюзовую сеть, это /64 обычно\n'
                          'без указания размерности\n'
                          'если серверов несколько, то разделитель пробел\n'
                          'Пример:\n'
                          '2aaa:bbb:1:2 2a09:400:1 2aaa:bbb:1:3\n').split(' ')
    try:
        for net in getway_subnet:
            ipaddress.IPv6Network(net+'::')
    except ipaddress.NetmaskValueError:
        print('Одна или несколько сетей указаны не верно\n')
        sys.exit(0)
    except ipaddress.AddressValueError:
        print('Одна или несколько сетей указаны не верно\n')
        sys.exit(0)

    if subnet_type != '64':
        subnet = input('Основные сети через которые будут ходить прокси\n'
                   'без указания размерности\n'
                   'если несколько, то разделитель пробел\n').split(' ')

        try:
            for net in subnet:
                ipaddress.IPv6Network(net+'::')
        except ipaddress.NetmaskValueError:
            print('Одна или несколько сетей указаны не верно')
            sys.exit(0)
        except ipaddress.AddressValueError:
            print('Одна или несколько сетей указаны не верно')
            sys.exit(0)
    else:
        subnet = getway_subnet

    count = input('Количество прокси\n')
    login = input('Логин прокси\n')
    passwd = input('Пароль прокси\n')
    rotation = input('Ротация Y|N\n')

    if rotation.lower() == 'y':
        rotation = 'True'
        cron = input('Маска времени ротации \n'
                     'Укажи только часы и минуты\n'
                     'Пример: 5 */1 - каждый час в 05 минут')
    else:
        rotation = 'False'
        cron = '* *'

    env = open('./inventory/env', 'w')
    env.write('proxyv6:\n  hosts:\n')

    for id, line in enumerate(server_ip):
        ip = server_ip[id]
        ipv64 = getway_subnet[id]
        ipv6 = subnet[id]
        root_passwd = server_passwd[id]
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
                   '    cron_hour: "{hour}"\n'
                   '    cron_minute: "{minute}"').format(net_type=subnet_type,
                                  count=count,
                                  password=passwd,
                                  rotate=rotation,
                                  rotate_type='simple',
                                  hour=cron.split(' ')[1],
                                  minute=cron.split(' ')[0])))

    env.close()