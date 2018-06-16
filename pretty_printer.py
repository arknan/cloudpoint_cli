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

def print_it_assets(data, endpoint):
    endpt_len = len(endpoint)
    if endpt_len == 1:
        print_it_general(data["items"])
    elif endpt_len == 2:
        print_it_general(data)

def print_it_general(data, col_len=0, nested=False):

    if (isinstance(data, dict)):
        #row_count = len(data.keys())
        col_len = maxlengths(sorted(data))
        for k, v in sorted(data.items()):
            if k.startswith('_'):
                pass
            else:
                print('{1}{0:<{2}}{1}'.format(k, '|', col_len), end='')
                if (isinstance(v, dict)) and (v):
                    print('\n', ' '*col_len, end='')
                    print_it_general(v, col_len, True)
                else:
                    clean_value = str(v).replace(' ', '')
                    print('{0}\n'.format(clean_value), end='')
        #if (not nested) and (row_count > 1):
        if (not nested):
            print()
            print('=' * columns)
            #row_count -= 1
            
    elif isinstance(data, list):
        for i in data:
            if isinstance(i, dict):
                print_it_general(i)
            else:
                print(i)
    else:
        print("FAIL")

def print_nested(data, endpoint):

    clean_data = chomp(data)
    final = None
    try:
        final = json.loads(clean_data)
        cover()
        if "assets/" in endpoint:
            print_it_assets(final, endpoint)
        else:
            print_it_general(final)
        cover()
    except:
        print(clean_data)
