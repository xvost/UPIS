#!/usr/bin/env python3

import cli_ipv6
import cli_ipv4


def start(proxy_type):
    if proxy_type == 'ipv4':
        cli_ipv4.ipv4()
    if proxy_type == 'ipv6':
        cli_ipv6.ipv6()
