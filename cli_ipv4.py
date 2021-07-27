#!/usr/bin/env python3

import sys
import ipaddress
from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError


class Ipv4AddressValidate(Validator):
    def validate(self, document):
        try:
            for net in document.text.split(' '):
                ipaddress.IPv4Address(net)
        except ipaddress.AddressValueError:
            message = 'Не корректный адрес'
            raise ValidationError(message=message, cursor_position=len(document.text))


class Ipv4SubnetValidate(Validator):
    def validate(self, document):
        try:
            for net in document.text.split(' '):
                ipaddress.IPv4Network(net)
        except ipaddress.AddressValueError:
            message = 'Не корректная сеть'
            raise ValidationError(message=message, cursor_position=len(document.text))


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a number",
                                  cursor_position=len(document.text))


def ipv4():
    greetings = '''Привет!
    Скрипт умеет настроить ipv4 прокси:
    Одиночные сервера и группы
    Ограничения:
    - одинаковые логин/пароль для всех прокси (на всех серверах при массовой настройке)
    - Скрипт инсталяции верит в то, что вы укажите все данные в верном порядке и без ошибок

    Возможности:
    - настройка systemd сервиса
    '''

    agree = [{
            'type': 'confirm',
            'name': 'agree',
            'message': 'Начать настройку'
        }]

    server = [{
            'type': 'input',
            'name': 'server_ip',
            'message': 'Ip адрес для подключения к серверу, через пробел если несколько\n',
            'validate': Ipv4AddressValidate
        },
        {
            'type': 'input',
            'name': 'server_user',
            'message': 'Пользователь для входа, требуются root права\n',
        },
        {
            'type': 'password',
            'name': 'server_passwd',
            'message': 'Пароль для root пользователя на сервере, через пробел если несколько\n',
        }]

    address_type = [{
            'type': 'list',
            'name': 'proxy_type',
            'message': 'Укажи тип настройки прокси',
            'choices': [{'key': '1',
                         'name': 'Прокси на основном адресе',
                         'value': 'one'},
                        {'key': '2',
                         'name': 'Прокси на дополнительном адресе',
                         'value': 'add'},
                        {'key': '3',
                         'name': 'Прокси на адресах из подсети',
                         'value': 'sub'}
                        ]
        }]

    input_output_type = [{
            'type': 'list',
            'name': 'input_type',
            'message': 'Конфигурация входящего/исходящего адреса',
            'choices': [
                        {'key': '1',
                         'name': 'Один входящий адрес для всех прокси',
                         'value': 'one'},
                        {'key': '2',
                         'name': 'Входящий == исходящий',
                         'value': 'self'}
                        ]
        }]

    proxy_data = [{
            'type': 'input',
            'name': 'proxy_login',
            'message': 'Логин для прокси\n'},
        {
            'type': 'input',
            'name': 'proxy_password',
            'message': 'Пароль для прокси\n'
        },
        {
            'type': 'input',
            'name': 'count',
            'message': 'Количество прокси, если испольуется несколько подсетей,то количество на 1 сеть\n',
            'validate': NumberValidator
        },
        {
            'type': 'input',
            'name': 'start',
            'message': 'Начальный порт\n',
            'validate': NumberValidator
        }]

    proxy_address = [{
            'type': 'input',
            'name': 'proxy_addr',
            'message': 'Адрес для прокси\n',
            'validate': Ipv4AddressValidate
        }]

    proxy_network = [{
            'type': 'input',
            'name': 'proxy_net',
            'message': 'Адрес для прокси\n',
            'validate': Ipv4SubnetValidate
        }]

    print(greetings)
    answers = prompt(agree)
    if not answers.get("agree"):
        sys.exit(0)
    server_answers = prompt(server)
    address_type_answers = prompt(address_type)
    proxy_type = address_type_answers.get('proxy_type', 'one')
    if proxy_type == 'one':
        proxy_data = prompt(proxy_data)
    elif proxy_type == 'add':
        proxy_address = prompt(proxy_address)
        proxy_data = prompt(proxy_data)
        proxy_addresses = proxy_address.get('proxy_addr').split(' ')
    else:
        proxy_network = prompt(proxy_network)
        input_output_type = prompt(input_output_type)
        proxy_data = prompt(proxy_data)
        proxy_networks = proxy_network.get('proxy_net').split(' ')
        input_output = input_output_type.get('input_type')

    env = open('./inventory/env', 'w')
    env.write('proxyv4:\n  hosts:')
    servers = server_answers.get('server_ip').split(' ')
    servers_users = server_answers.get('server_user').split(' ')
    servers_passwords = server_answers.get('server_passwd').split(' ')

    for num, server in enumerate(servers):
        ip = servers[num]
        user = servers_users[num]
        user_passwd = servers_passwords[num]
        if proxy_type == 'one':
            network = ip
        elif proxy_type == 'add':
            network = proxy_addresses[num]
        else:
            network = proxy_networks[num]

        env.write(str(f'\n'
                      f'    server_{ip}:\n'
                      f'      ansible_host: {ip}\n'
                      f'      ansible_ssh_user: {user}\n'
                      f'      ansible_ssh_pass: {user_passwd}\n'
                      f'      subnet: {network}'))
        listfile = open('./proxylists/{}.list'.format(ip), 'w')

        end = ipaddress.ip_network(network).num_addresses+int(proxy_data['start'])
        start = int(proxy_data['start'])
        enum = 0
        for line in range(start, end, 1):
            if input_output == 'self':
                inputadd = ipaddress.ip_network(network)[enum]
            else:
                inputadd = network
            port = start + enum
            inputadd = inputadd
            port = port
            user = proxy_data['proxy_login']
            password = proxy_data['proxy_password']
            listfile.write(f'{inputadd}:{port}@{user}:{password}\n')
            enum += 1

    count = proxy_data['count']
    port = proxy_data['start']
    login = proxy_data['proxy_login']
    password = proxy_data['proxy_password']
    input = input_output
    env.write(str(f'\n'
                  f'  vars:\n'
                  f'    count: {count}\n'
                  f'    start_port: {port}\n'
                  f'    proxy_login: {login}\n'
                  f'    proxy_password: {password}\n'
                  f'    input: {input}'))
    env.close()


if __name__ == "__main__":
    ipv4()
