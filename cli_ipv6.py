#!/usr/bin/env python3

import sys

from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError


class Ipv4Validate(Validator):
    def validate(self, document):
        import ipaddress
        try:
            for net in document.text.split(' '):
                ipaddress.IPv4Address(net)
        except ipaddress.AddressValueError:
            message = 'Не корректный адрес'
            raise ValidationError(message=message, cursor_position=len(document.text))


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a number",
                                  cursor_position=len(document.text))


class Nipv6Validate(Validator):
    def validate(self, document):
        import ipaddress
        message = 'Не корректный адрес'
        try:
            for net in document.text.split(' '):
                if len(net) < 5:
                    raise ValidationError(message=message, cursor_position=len(document.text))
                ipaddress.IPv6Network(net + '::')
        except ipaddress.AddressValueError or ipaddress.NetmaskValueError:

            raise ValidationError(message=message, cursor_position=len(document.text))


class CronValidate(Validator):
    def validate(self, document):
        import re
        template = re.compile("([\d\*\/]+) ([\d\*\/]+)")
        match = re.match(template, document.text)
        if match is None:
            raise ValidationError(message='строка не в формате cron', cursor_position=len(document.text))


def ipv6():
    greetings = '''Привет!
    Скрипт умеет настроить ipv6 прокси:
    64, 48, 36, 32, 29 - сети
    Одиночные сервера и группы
    Ограничения:
    - только debian8
    - одинаковые логин/пароль для всех прокси (на всех серверах при массовой настройке)
    - Скрипт инсталяции верит в то что вы укажите все данные в верном порядке и без ошибок

    Возможности:
    - ротация
    - настройка systemd сервиса
    - ndppd для работы сетей /64 и /48 с параметром non local bind
    '''

    agree = [
        {
            'type': 'confirm',
            'name': 'agree',
            'message': 'Начать настройку'
        }
    ]

    base = [
        {
            'type': 'list',
            'name': 'subnet_type',
            'message': 'Укажи сеть в которой будут работать прокси',
            'choices': ['64', '48', '36', '32', '29']
        },
        {
            'type': 'input',
            'name': 'server_ip',
            'message': 'Ip адрес для подключения к серверу, через пробел если несколько\n',
            'validate': Ipv4Validate
        },
        {
            'type': 'password',
            'name': 'server_passwd',
            'message': 'Пароль для root пользователя на сервере, через пробел если несколько\n',
        },
        {
            'type': 'input',
            'name': 'gateway_subnet',
            'message': 'Шлюзовая сеть, /64 или /48 сети,'
                       'без указания размерности: 2aaa:bbb:1:2 2a09:400:1 2aaa:bbb:1:3 - например,'
                       'разделитель пробел\n',
            'validate': Nipv6Validate
        }
    ]

    proxy_subnet = [
        {
            'type': 'input',
            'name': 'subnet',
            'message': 'Основные сети через которые будут ходить прокси,'
                       'без указания размерности,'
                       'если несколько, то разделитель пробел\n',
            'validate': Nipv6Validate
        }
    ]

    proxy_data = [
        {
            'type': 'input',
            'name': 'count',
            'message': 'Количество прокси\n',
            "validate": NumberValidator
        },
        {
            'type': 'input',
            'name': 'startport',
            'message': 'Начальный порт\n',
            "validate": NumberValidator
        },
        {
            'type': 'input',
            'name': 'login',
            'message': 'Логин прокси\n'
        },
        {
            'type': 'password',
            'name': 'passwd',
            'message': 'Пароль прокси\n'
        },
        {
            'type': 'confirm',
            'name': 'rotation',
            'message': 'Ротация\n'
        }
    ]

    cron = [
        {
            'type': 'input',
            'name': 'cron',
            'message': 'Маска времени ротации,'
                       'Только часы и минуты'
                       'Пример: 5 */1 - каждый час в 05 минут\n',
            'validate': CronValidate
        }
    ]

    print(greetings)
    answers = prompt(agree)
    if not answers.get("agree"):
        sys.exit(0)

    base_answers = prompt(base)
    subnet_type = base_answers.get('subnet_type')
    server_ip = base_answers.get('server_ip').split(' ')
    server_passwd = base_answers.get('server_passwd').split(' ')
    gateway_subnet = base_answers.get('gateway_subnet').split(' ')

    if subnet_type not in ['64', '48']:
        subnet = prompt(proxy_subnet)
        subnet = subnet.get('subnet').split(' ')
    else:
        subnet = gateway_subnet

    while True:
        proxy_data_answer = prompt(proxy_data)

        count = proxy_data_answer.get("count")
        startport = proxy_data_answer.get("startport")
        login = proxy_data_answer.get("login")
        passwd = proxy_data_answer.get("passwd")
        rotation = proxy_data_answer.get("rotation")
        if (int(startport) + int(count)) > 65534:
            print(f'Конечный порт {int(startport) + int(count)} больше 65534\n'
                  f'Введите данные повторно')
        else:
            break

    if rotation:
        cron_data = prompt(cron)
        cron = cron_data.get("cron")
        rotation = 'True'
    else:
        rotation = 'False'
        cron = '* *'

    env = open('./inventory/env', 'w')
    env.write('proxyv6:\n  hosts:\n')

    for enum, line in enumerate(server_ip):
        ip = server_ip[enum]
        ipv64 = gateway_subnet[enum]
        ipv6 = subnet[enum]
        root_passwd = server_passwd[enum]
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
                   '    start_port: {startport}\n'
                   '    proxy_login: {login}\n'
                   '    proxy_password: {password}\n'
                   '    rotate_type: {rotate_type}\n'
                   '    rotate: {rotate}\n'
                   '    cron_hour: "{hour}"\n'
                   '    cron_minute: "{minute}"').format(net_type=subnet_type,
                                                         count=count,
                                                         startport=startport,
                                                         login=login,
                                                         password=passwd,
                                                         rotate=rotation,
                                                         rotate_type='simple',
                                                         hour=cron.split(' ')[1],
                                                         minute=cron.split(' ')[0])))

    env.close()

    listfile = open('./proxylists/{}.list'.format(server_ip[0]), 'w')
    end = int(startport) + int(count)
    startport = int(startport)
    enum = 0
    inputadd = server_ip[0]
    for line in range(startport, end, 1):
        port = startport + enum
        inputadd = inputadd
        port = port
        user = login
        password = passwd
        listfile.write(f'{inputadd}:{port}@{user}:{password}\n')
        enum += 1


if __name__ == "__main__":
    ipv6()
