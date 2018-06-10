#!/usr/bin/env python3

import json
import sys


def my_print(data, endpoint):
    print(endpoint)
    if 'licenses/' in endpoint:
        print_licenses(json.loads(data))
        sys.exit(1)
    my_data = json.loads(data)
    if isinstance(my_data, list):
        print_list(my_data)
    elif isinstance(my_data, dict):
        print_dict(my_data)

def print_list(my_data):
    for row in my_data:
        print('+' + '='*79 + '+')
        for i,j in sorted(row.items()):
            print('{0:15} || {1:<57}'.format(i, str(j)))
            print('-'*79)

    print('+' + '='*79 + '+')

def print_dict(my_data):
    print('+' + '='*79 + '+')
    for i,j in sorted(my_data.items()):
        print('{0:20} || {1:<58}'.format(i, str(j)))
        print('-'*81)

    print('+' + '='*79 + '+')


def print_licenses(my_data):
    print('+' + '='*79 + '+')
    for i,j in sorted(my_data.items()):
        for k,v in sorted(j.items()):
                print('| {0:15} || {1:<57} |'.format(k, str(v)))
                print('-'*79)

    print('+' + '='*79 + '+')
