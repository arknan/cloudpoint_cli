#!/usr/bin/env python3

import os
import json

rows, columns = os.popen('stty size', 'r').read().split()
columns = int(columns)

def chomp(data):
    final = data.replace('\n', '').replace(' ', '')
    return final

def cover():
    print('+', end='')
    print('=' * int(columns -2 ), end='')
    print('+', end='')

def maxlengths(value):

    len_val = 0
    for i in value:
        if len(i) > len_val:
            len_val = len(i)

    return len_val

def print_it(data, col_len=0):

    if isinstance(data, dict):
        col_len = maxlengths(sorted(data))
        for k, v in sorted(data.items()):
            if k.startswith('_'):
                pass
            else:
                print('{1}{0:<{2}}{1}'.format(k, '|', col_len), end='')
                if isinstance(v, dict):
                    print('\n', ' '*col_len, end='')
                    print_it(v, col_len)
                else:
                    clean_value = str(v).replace(' ', '')
                    print('{0}\n'.format(clean_value), end='')

    elif isinstance(data, list):
        for i in data:
            if isinstance(i, dict):
                print_it(i)
            else:
                print(i)
    else:
        print("FAIL")

def print_nested(data):
    clean_data = chomp(data)
    final = json.loads(clean_data)
    cover()
    print_it(final)
    cover()
